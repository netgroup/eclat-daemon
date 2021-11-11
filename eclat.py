"""
Eclat CLI
"""
import grpc
import argparse

# import the generated classes
import eclat_pb2
import eclat_pb2_grpc


def run(scriptfile, package):
    # open a gRPC channel
    channel = grpc.insecure_channel('localhost:50051')

    # create a stub (client)
    stub = eclat_pb2_grpc.EclatStub(channel)

    # create a valid request message
    with open(scriptfile, 'r') as f:
        script = f.read()
        print(f"sending {script} of package {package} to grpc")
        req = eclat_pb2.EclatLoadRequest(script=script, package=package)

    # make the call
    response = stub.LoadConfiguration(req)

    # et voila
    print(response.status)
    print(response.message)
    return response


def main():
    # parse argument
    parser = argparse.ArgumentParser(
        description='Eclat CLI.')
    parser.add_argument(
        '-l', '--load', help="Load an eclat script", required=True)
    parser.add_argument('-p', '--package',
                        help="Package name of the eclat script", required=True)

    args = vars(parser.parse_args())

    print(args)

    ret = run(scriptfile=args['load'], package=args['package'])
    print(ret)
    return ret


if __name__ == "__main__":
    main()
