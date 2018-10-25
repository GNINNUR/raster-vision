from copy import deepcopy

import rastervision as rv
from rastervision.data.vector_source.vector_source_config import (
    VectorSourceConfig, VectorSourceConfigBuilder)
from rastervision.data.vector_source.mbtiles_vector_source import MBTilesVectorSource


class MBTilesVectorSourceConfig(VectorSourceConfig):
    def __init__(self, uri, class_id_to_filter=None):
        self.uri = uri
        super().__init__(
            rv.MBTILES_SOURCE, class_id_to_filter=class_id_to_filter)

    def to_proto(self):
        msg = super().to_proto()
        msg.mbtiles.uri = self.uri
        return msg

    def create_source(self, crs_transformer, extent, class_map):
        return MBTilesVectorSource(
            self.uri,
            crs_transformer,
            extent,
            class_map,
            class_id_to_filter=self.class_id_to_filter)

    def update_for_command(self, command_type, experiment_config, context=[]):
        conf = self
        io_def = rv.core.CommandIODefinition()
        io_def.add_input(self.uri)

        return (conf, io_def)


class MBTilesVectorSourceConfigBuilder(VectorSourceConfigBuilder):
    def __init__(self, prev=None):
        config = {}
        if prev:
            config = {
                'class_id_to_filter': prev.class_id_to_filter,
                'uri': prev.uri
            }

        super().__init__(MBTilesVectorSourceConfig, config)

    def validate(self):
        # TODO
        if self.config.get('uri') is None:
            raise rv.ConfigError('Must set uri.')

        super().validate()

    def from_proto(self, msg):
        b = super().from_proto(msg)
        b = b.with_uri(msg.mbtiles.uri)
        return b

    def with_uri(self, uri):
        b = deepcopy(self)
        b.config['uri'] = uri
        return b
