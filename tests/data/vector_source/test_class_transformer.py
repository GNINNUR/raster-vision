import unittest

from rastervision.data.vector_source.class_transformer import ClassTransformer
from rastervision.core.class_map import ClassMap


class TestClassTransformer(unittest.TestCase):
    def setUp(self):
        self.class_map = ClassMap.construct_from(['building', 'car'])
        self.class_id_to_filter = {
            1: ['==', 'type', 'building'],
            2: ['any', ['==', 'type', 'car'], ['==', 'type', 'auto']]
        }
        self.class_transformer = ClassTransformer(self.class_map,
                                                  self.class_id_to_filter)

    def test_transform_geojson(self):
        # This should hit the 4 ways of inferring a class_id.
        geojson = {
            'type':
            'FeatureCollection',
            'features': [{
                'properties': {
                    'class_id': 3
                }
            }, {
                'properties': {
                    'label': 'car'
                }
            }, {
                'properties': {
                    'type': 'auto'
                }
            }, {}]
        }

        transformed_geojson = self.class_transformer.transform_geojson(geojson)
        expected_transformed_geojson = {
            'type':
            'FeatureCollection',
            'features': [{
                'properties': {
                    'class_id': 3
                }
            }, {
                'properties': {
                    'label': 'car',
                    'class_id': 2
                }
            }, {
                'properties': {
                    'type': 'auto',
                    'class_id': 2
                }
            }, {
                'properties': {
                    'class_id': 1
                }
            }]
        }

        self.assertDictEqual(transformed_geojson, expected_transformed_geojson)


if __name__ == '__main__':
    unittest.main()
