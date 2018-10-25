import json

from rastervision.data.vector_source.vector_source import VectorSource
from rastervision.utils.files import file_to_str


class GeoJSONVectorSource(VectorSource):
    def __init__(self, uri, class_map, class_id_to_filter=None):
        self.uri = uri
        super().__init__(class_map, class_id_to_filter=class_id_to_filter)

    def _get_geojson(self):
        return json.loads(file_to_str(self.uri))
