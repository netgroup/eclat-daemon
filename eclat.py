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
    if not defines:
        return script
    for var, value in defines:
        script = script.replace(var, value)
    print(script)
    return script


def run(scriptfile, package, defines):
    # open a gRPC channel
    #channel = grpc.insecure_channel('[::1]:50051')
    channel = grpc.insecure_channel('localhost:50051')

    # create a stub (client)
    stub = eclat_pb2_grpc.EclatStub(channel)

    # create a valid request message
    with open(scriptfile, 'r') as f:
        script = f.read()
        script = preprocess(script, defines)
        print(f"sending {script} of package {package} to grpc")
        req = eclat_pb2.EclatLoadRequest(script=script, package=package)

    # make the call
    response = stub.LoadConfiguration(req)

    print(response.status)
    print(response.message)
    return response


def get_map_value(mapname, key):
    channel = grpc.insecure_channel('localhost:50051')
    stub = eclat_pb2_grpc.EclatStub(channel)
    req = eclat_pb2.EclatGetMapValueRequest(mapname=mapname, key=key)
    response = stub.GetMapValue(req)
    print(response.status)
    print(response.message)
    return response


def dump_map(mapname):
    channel = grpc.insecure_channel('localhost:50051')
    stub = eclat_pb2_grpc.EclatStub(channel)
    req = eclat_pb2.EclatDumpMapRequest(mapname=mapname)
    response = stub.DumpMap(req)
    print(response.status)
    print(response.message)
    return response


def main():
    # parse argument
    parser = argparse.ArgumentParser(
        description='Eclat CLI.')
    parser.add_argument(
        '-l', '--load', help="Load an eclat script", required=False)
    parser.add_argument('-p', '--package',
                        help="Package name of the eclat script", required=False)
    parser.add_argument('-D', '--define', nargs=2, action="append",
                        help="Define constant for eCLAT preprocessor", required=False)
    parser.add_argument('-m', '--getmapvalue', nargs=2, action="append",
                        help="Get the map value corresponding to a given key", required=False)
    parser.add_argument('-M', '--dumpmap', action="append",
                        help="Dump the content of a given map", required=False)

    args = vars(parser.parse_args())

    if args['load'] is not None:
        # load a script
        if not "package" in args:
            parser.error('Missing package name. Use --package argument')
        ret = run(scriptfile=args['load'],
                  package=args['package'], defines=args['define'])
    elif args['getmapvalue'] is not None:
        ret = get_map_value(*args['getmapvalue'][0])
    elif args['dumpmap'] is not None:
        ret = dump_map(*args['dumpmap'])
    else:
        parser.error('No command specified.')
    print(ret)
    return ret


if __name__ == "__main__":
    main()
