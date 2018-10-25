import json
from subprocess import Popen, PIPE, check_output
import logging

from rastervision.data.vector_source.vector_source import VectorSource
from rastervision.utils.files import download_if_needed
from rastervision.rv_config import RVConfig

log = logging.getLogger(__name__)


def mbtiles_to_geojson(uri, crs_transformer, extent):
    map_extent = extent.reproject(
        lambda point: crs_transformer.pixel_to_map(point))

    with RVConfig.get_tmp_dir() as tmp_dir:
        log.info('Converting MBTiles to GeoJSON...')

        path = download_if_needed(uri, tmp_dir)
        ps = Popen(['tippecanoe-decode', '-c', '-f', path], stdout=PIPE)
        filtered_geojson = check_output(
            [
                'python', '-m', 'label_maker.stream_filter',
                json.dumps(map_extent.shapely_format())
            ],
            stdin=ps.stdout).decode('utf-8')

    # Each line has a feature. The last line is empty so discard.
    features = [
        json.loads(feature) for feature in filtered_geojson.split('\n')[:-1]
    ]
    geojson = {'type': 'FeatureCollection', 'features': features}

    return geojson


class MBTilesVectorSource(VectorSource):
    def __init__(self,
                 uri,
                 crs_transformer,
                 extent,
                 class_map,
                 class_id_to_filter=None):
        self.uri = uri
        self.crs_transformer = crs_transformer
        self.extent = extent
        super().__init__(class_map, class_id_to_filter=class_id_to_filter)

    def _get_geojson(self):
        return mbtiles_to_geojson(self.uri, self.crs_transformer, self.extent)
