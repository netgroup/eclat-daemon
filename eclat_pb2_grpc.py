# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import eclat_pb2 as eclat__pb2


class EclatStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.LoadConfiguration = channel.unary_unary(
                '/Eclat/LoadConfiguration',
                request_serializer=eclat__pb2.EclatLoadRequest.SerializeToString,
                response_deserializer=eclat__pb2.EclatLoadResponse.FromString,
                )
        self.FetchConfiguration = channel.unary_unary(
                '/Eclat/FetchConfiguration',
                request_serializer=eclat__pb2.EclatFetchRequest.SerializeToString,
                response_deserializer=eclat__pb2.EclatFetchResponse.FromString,
                )
        self.DumpMap = channel.unary_unary(
                '/Eclat/DumpMap',
                request_serializer=eclat__pb2.EclatDumpMapRequest.SerializeToString,
                response_deserializer=eclat__pb2.EclatDumpMapResponse.FromString,
                )
        self.GetMapValue = channel.unary_unary(
                '/Eclat/GetMapValue',
                request_serializer=eclat__pb2.EclatGetMapValueRequest.SerializeToString,
                response_deserializer=eclat__pb2.EclatGetMapValueResponse.FromString,
                )
        self.Quit = channel.unary_unary(
                '/Eclat/Quit',
                request_serializer=eclat__pb2.EclatQuitRequest.SerializeToString,
                response_deserializer=eclat__pb2.EclatQuitResponse.FromString,
                )


class EclatServicer(object):
    """Missing associated documentation comment in .proto file."""

    def LoadConfiguration(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def FetchConfiguration(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DumpMap(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetMapValue(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Quit(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_EclatServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'LoadConfiguration': grpc.unary_unary_rpc_method_handler(
                    servicer.LoadConfiguration,
                    request_deserializer=eclat__pb2.EclatLoadRequest.FromString,
                    response_serializer=eclat__pb2.EclatLoadResponse.SerializeToString,
            ),
            'FetchConfiguration': grpc.unary_unary_rpc_method_handler(
                    servicer.FetchConfiguration,
                    request_deserializer=eclat__pb2.EclatFetchRequest.FromString,
                    response_serializer=eclat__pb2.EclatFetchResponse.SerializeToString,
            ),
            'DumpMap': grpc.unary_unary_rpc_method_handler(
                    servicer.DumpMap,
                    request_deserializer=eclat__pb2.EclatDumpMapRequest.FromString,
                    response_serializer=eclat__pb2.EclatDumpMapResponse.SerializeToString,
            ),
            'GetMapValue': grpc.unary_unary_rpc_method_handler(
                    servicer.GetMapValue,
                    request_deserializer=eclat__pb2.EclatGetMapValueRequest.FromString,
                    response_serializer=eclat__pb2.EclatGetMapValueResponse.SerializeToString,
            ),
            'Quit': grpc.unary_unary_rpc_method_handler(
                    servicer.Quit,
                    request_deserializer=eclat__pb2.EclatQuitRequest.FromString,
                    response_serializer=eclat__pb2.EclatQuitResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Eclat', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Eclat(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def LoadConfiguration(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Eclat/LoadConfiguration',
            eclat__pb2.EclatLoadRequest.SerializeToString,
            eclat__pb2.EclatLoadResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def FetchConfiguration(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Eclat/FetchConfiguration',
            eclat__pb2.EclatFetchRequest.SerializeToString,
            eclat__pb2.EclatFetchResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DumpMap(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Eclat/DumpMap',
            eclat__pb2.EclatDumpMapRequest.SerializeToString,
            eclat__pb2.EclatDumpMapResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetMapValue(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Eclat/GetMapValue',
            eclat__pb2.EclatGetMapValueRequest.SerializeToString,
            eclat__pb2.EclatGetMapValueResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Quit(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Eclat/Quit',
            eclat__pb2.EclatQuitRequest.SerializeToString,
            eclat__pb2.EclatQuitResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
