import grpc
from concurrent import futures
import time
import traceback

# import the generated classes
import eclat_pb2
import eclat_pb2_grpc

from controller import EclatController

controller = EclatController()


class EclatServicer(eclat_pb2_grpc.EclatServicer):
    def __init__(self, eclatd):
        self.controller = controller

    def LoadConfiguration(self, request, context):
        print(request.script)
        print("PACKAGE:",request.package)
        response = eclat_pb2.EclatLoadResponse()
        try:
            ret = self.controller.load_configuration(
                request.script, request.package)
        except Exception as e:
            print(traceback.format_exc())
            ret = False
            raise e

        if ret:
            response.status = "OK"
            response.message = "test ret message for message " + request.script
        else:
            response.status = "FAIL"
        return response

    def DumpMap(self, request, context):
        response = eclat_pb2.EclatDumpMapResponse()
        try:
            ret = self.controller.dump_map(
                request.mapname)
            response.message = ret
        except Exception as e:
            print(traceback.format_exc())
            ret = False
            raise e
        response.status = "OK" if ret else "FAIL"
        return response

    def GetMapValue(self, request, context):
        response = eclat_pb2.EclatGetMapValueResponse()
        try:
            ret = self.controller.get_map_value(
                request.mapname, request.key)
            response.message = ret
        except Exception as e:
            print(traceback.format_exc())
            ret = False
            raise e
        response.status = "OK" if ret else "FAIL"
        return response


# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))


eclat_pb2_grpc.add_EclatServicer_to_server(
    EclatServicer(controller), server)

# listen on port 50051
server.add_insecure_port('[::]:50051')
server.start()
print('Server started. Listening on port 50051.')
server.wait_for_termination()
