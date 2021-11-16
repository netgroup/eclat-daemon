"""
Eclat CLI
"""
import grpc
import argparse

# import the generated classes
import eclat_pb2
import eclat_pb2_grpc


def preprocess(script, defines):
    """
    Preprocess an eCLAT script, substituting some defines in the script
    """
    for var, value in defines:
        script = script.replace(var, value)
    print(script)
    return script


def run(scriptfile, package, defines):
    # open a gRPC channel
    channel = grpc.insecure_channel('localhost:50051')

    # create a stub (client)
    stub = eclat_pb2_grpc.EclatStub(channel)

    # create a valid request message
    with open(scriptfile, 'r') as f:
        script = f.read()
        script = preprocess(script, defines)
        print(f"sending {script} of package {package} to grpc")
        return
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
    parser.add_argument('-D', '--define', nargs=2, action="append",
                        help="Define constant for eCLAT preprocessor", required=False)

    args = vars(parser.parse_args())

    print(args)

    ret = run(scriptfile=args['load'],
              package=args['package'], defines=args['define'])
    print(ret)
    return ret


if __name__ == "__main__":
    main()
