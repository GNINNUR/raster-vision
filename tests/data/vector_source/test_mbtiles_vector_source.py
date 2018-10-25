import unittest

from rastervision.data.vector_source import (MBTilesVectorSourceConfigBuilder,
                                             MBTilesVectorSourceConfig)
from rastervision.core.box import Box
from rastervision.core.class_map import ClassMap
from rastervision.data.crs_transformer import IdentityCRSTransformer
from tests import data_file_path


class TestMBTilesVectorSource(unittest.TestCase):
    def setUp(self):
        # This test file was copied from https://github.com/developmentseed/label-maker
        self.uri = data_file_path('portugal-z17.mbtiles')
        self.class_id_to_filter = {'1': ['has', 'building']}
        self.class_map = ClassMap.construct_from(['building'])
        self.crs_transformer = IdentityCRSTransformer()

        b = MBTilesVectorSourceConfigBuilder() \
            .with_class_filters(self.class_id_to_filter) \
            .with_uri(self.uri) \
            .build()

        self.config = MBTilesVectorSourceConfig.from_proto(b.to_proto())

    def test_get_geojson(self):
        # Extent covers subset of shapes.
        extent = Box.make_square(38.85, -10.0, 1.0)
        source = self.config.create_source(self.crs_transformer, extent,
                                           self.class_map)
        geojson = source.get_geojson()
        self.assertEqual(len(geojson['features']), 352)

        # Extent covers whole set of shapes.
        extent = Box.make_square(38.0, -10.0, 1.0)
        source = self.config.create_source(self.crs_transformer, extent,
                                           self.class_map)
        geojson = source.get_geojson()
        self.assertEqual(len(geojson['features']), 554)


if __name__ == '__main__':
    unittest.main()
