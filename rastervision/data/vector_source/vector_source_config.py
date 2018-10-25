from copy import deepcopy

import rastervision as rv
from rastervision.core.config import Config, ConfigBuilder
from rastervision.protos.vector_source_pb2 import (VectorSourceConfig as
                                                   VectorSourceConfigMsg)


class VectorSourceConfig(Config):
    def __init__(self, source_type, class_id_to_filter=None):
        self.source_type = source_type
        self.class_id_to_filter = class_id_to_filter

    def to_proto(self):
        msg = VectorSourceConfigMsg(source_type=self.source_type)

        # TODO get this working
        '''
        if self.class_id_to_filter:
            d = {'class_id_to_filter': self.class_id_to_filter}
            msg.MergeFrom(json_format.ParseDict(d, VectorSourceConfigMsg()))
        '''

        return msg

    @staticmethod
    def builder(source_type):
        return rv._registry.get_config_builder(rv.VECTOR_SOURCE, source_type)()

    def to_builder(self):
        return rv._registry.get_config_builder(rv.VECTOR_SOURCE,
                                               self.source_type)(self)

    @staticmethod
    def from_proto(msg):
        """Creates a from the specificed protobuf message.
        """
        return rv._registry.get_config_builder(rv.VECTOR_SOURCE, msg.source_type)() \
                           .from_proto(msg) \
                           .build()


class VectorSourceConfigBuilder(ConfigBuilder):
    def validate(self):
        # TODO validate class_id_to_filter
        pass

    def from_proto(self, msg):
        b = self
        if msg.HasField('class_id_to_filter'):
            b = b.with_class_filters(msg.class_id_to_filter)

        return b

    def with_class_filters(self, class_id_to_filter):
        b = deepcopy(self)
        b.config['class_id_to_filter'] = class_id_to_filter
        return b
