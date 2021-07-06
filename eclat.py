"""
Eclat CLI
"""
import grpc
import argparse

# import the generated classes
import eclat_pb2
import eclat_pb2_grpc


def run(scriptfile):
    # open a gRPC channel
    channel = grpc.insecure_channel('localhost:50051')

    # create a stub (client)
    stub = eclat_pb2_grpc.EclatStub(channel)

    # create a valid request message
    with open(scriptfile, 'r') as f:
        script = f.read()
        req = eclat_pb2.EclatRunRequest(script=script)

    # make the call
    response = stub.Run(req)

    # et voila
    print(response.status)
    print(response.message)
    return response


def main():
    # parse argument
    parser = argparse.ArgumentParser(
        description='Eclat CLI.')
    parser.add_argument('-r', '--run',
                        action="store", help="Eclat script to run", required=True)

    args = vars(parser.parse_args())

    print(args)

    ret = run(args['run'])
    print(ret)
    return ret


if __name__ == "__main__":
    main()
