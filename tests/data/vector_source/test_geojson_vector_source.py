import unittest
import json

from rastervision.data.vector_source import (GeoJSONVectorSourceConfigBuilder,
                                             GeoJSONVectorSourceConfig)
from rastervision.core.class_map import ClassMap
from rastervision.utils.files import file_to_str
from tests import data_file_path


class TestMBTilesVectorSource(unittest.TestCase):
    def setUp(self):
        self.uri = data_file_path('polygon-labels.geojson')
        self.class_id_to_filter = {'1': ['has', 'building']}
        self.class_map = ClassMap.construct_from(['building'])
        self.geojson = json.loads(file_to_str(self.uri))

        b = GeoJSONVectorSourceConfigBuilder() \
            .with_class_filters(self.class_id_to_filter) \
            .with_uri(self.uri) \
            .build()

        self.config = GeoJSONVectorSourceConfig.from_proto(b.to_proto())

    def test_get_geojson(self):
        source = self.config.create_source(self.class_map)
        geojson = source.get_geojson()
        self.assertDictEqual(geojson, self.geojson)


if __name__ == '__main__':
    unittest.main()
