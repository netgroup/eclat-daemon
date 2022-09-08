import grpc
from concurrent import futures
import logging
from logging import config
import traceback
import settings

# import the generated classes
import eclat_pb2
import eclat_pb2_grpc

from controller import EclatController

# configure the logger
config.dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger(__name__)

controller = EclatController()


class EclatServicer(eclat_pb2_grpc.EclatServicer):
    def __init__(self, eclatd):
        self.controller = controller

    def LoadConfiguration(self, request, context):
        logger.info(f"LoadConfiguration for package {request.package}")
        logger.info(request.script)
        response = eclat_pb2.EclatLoadResponse()
        try:
            ret = self.controller.load_configuration(
                request.script, request.package)
            response.status = "OK"
            response.message = "test ret message for message " + request.script
        except Exception as e:
            logging.exception("Exception occurred in LoadConfiguration")
            response.status = "FAIL"
            response.message = str(e)
        return response

    def FetchConfiguration(self, request, context):
        logger.info("FetchConfiguration")
        response = eclat_pb2.EclatFetchResponse()
        try:
            ret = self.controller.fetch_configuration(
                request.script)
            response.status = "OK"
            response.message = "test ret message for message " + request.script
        except Exception as e:
            logging.exception("Exception occurred in FetchConfiguration")
            response.status = "FAIL"
            response.message = str(e)
        return response

    def FetchPackage(self, request, context):
        response = eclat_pb2.EclatFetchPackageResponse()
        try:
            ret = self.controller.fetch_package(
                request.package)
            response.status = "OK"
            response.message = f"Package {request.package} downloaded succesfully"
        except Exception as e:
            logging.exception("Exception occurred in FetchPackageConfiguration")
            response.status = "FAIL"
            response.message = str(e)
        return response

    def Quit(self, request, context):
        response = eclat_pb2.EclatQuitResponse()
        try:
            ret = server.stop(5)
            response.status = "OK"
            response.message = ret
        except Exception as e:
            logging.exception("Exception occurred in Quit")
            response.status = "FAIL"
            response.message = str(e)
        return response

    def DumpMap(self, request, context):
        response = eclat_pb2.EclatDumpMapResponse()
        try:
            ret = self.controller.dump_map(
                request.mapname)
            response.status = "OK"
            response.message = ret
        except Exception as e:
            logging.exception("Exception occurred in DumpMap")
            response.status = "FAIL"
            response.message = str(e)
        return response



    def GetMapValue(self, request, context):
        response = eclat_pb2.EclatGetMapValueResponse()
        try:
            ret = self.controller.get_map_value(
                request.mapname, request.key)
            response.status = "OK"
            response.message = ret
        except Exception as e:
            logging.exception("Exception occurred in GetMapValue")
            response.status = "FAIL"
            response.message = str(e)
        return response


# configure logging

# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))


eclat_pb2_grpc.add_EclatServicer_to_server(
    EclatServicer(controller), server)

# listen on port 50051
server.add_insecure_port('[::]:50051')
server.start()
logger.info('Server started. Listening on port 50051')
server.wait_for_termination()
