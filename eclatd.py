import grpc
from concurrent import futures
import time

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
        response = eclat_pb2.EclatLoadResponse()
        ret = self.controller.load_configuration(
            request.script, request.package)
        if ret:
            response.status = "OK"
            response.message = "test ret message for message " + request.script
        else:
            response.status = "FAIL"
        return response


# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))


eclat_pb2_grpc.add_EclatServicer_to_server(
    EclatServicer(controller), server)

# listen on port 50051
print('Starting server. Listening on port 50051.')
server.add_insecure_port('[::]:50051')
server.start()
server.wait_for_termination()
