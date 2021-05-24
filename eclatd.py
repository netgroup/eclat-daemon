import grpc
from concurrent import futures
import time

# import the generated classes
from protos import eclat_pb2
from protos import eclat_pb2_grpc


import engine


class EclatServicer(eclat_pb2_grpc.EclatServicer):

    def Run(self, request, context):
        print(request.script)
        response = eclat_pb2.EclatRunResponse()
        response.status = "OK" if engine.run(request.script) else "FAIL"
        response.message = "test ret message for message " + request.script
        return response


# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))

# use the generated function `add_CalculatorServicer_to_server`
# to add the defined class to the created server
eclat_pb2_grpc.add_EclatServicer_to_server(
    EclatServicer(), server)

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
