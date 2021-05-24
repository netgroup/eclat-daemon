import grpc
from concurrent import futures
import time

# import the generated classes
import eclat_pb2
import eclat_pb2_grpc


from engine import EclatEngine

engine = EclatEngine()


class EclatServicer(eclat_pb2_grpc.EclatServicer):
    def __init__(self, eclatd):
        self.engine = engine

    def Run(self, request, context):
        print(request.script)
        response = eclat_pb2.EclatRunResponse()
        ret = self.engine.run(request.script)
        if ret:
            response.status = "OK"
            response.message = "test ret message for message " + request.script
        else:
            response.status = "FAIL"
        return response


# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))


eclat_pb2_grpc.add_EclatServicer_to_server(
    EclatServicer(engine), server)

# listen on port 50051
print('Starting server. Listening on port 50051.')
server.add_insecure_port('[::]:50051')
server.start()

# since server.start() will not block,
# a sleep-loop is added to keep alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
