from abc import ABC, abstractmethod

from rastervision.data.vector_source.class_transformer import ClassTransformer


class VectorSource(ABC):
    def __init__(self, class_map, class_id_to_filter=None):
        self.class_transformer = ClassTransformer(
            class_map, class_id_to_filter=class_id_to_filter)
        self.geojson = None

    def get_geojson(self):
        if self.geojson is None:
            self.geojson = self.class_transformer.transform_geojson(
                self._get_geojson())
        return self.geojson

    @abstractmethod
    def _get_geojson(self):
        pass
