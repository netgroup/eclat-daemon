#!/usr/bin/env python3
"""
Eclat CLI
"""
import grpc
import argparse
import json
import sys

# import the generated classes
import eclat_pb2
import eclat_pb2_grpc


def preprocess(script, defines):
    """
    Preprocess an eCLAT script, replacing placeholders with defines
    """
    if not defines:
        return script
    for placeholder, value in defines:
        script = script.replace(placeholder, value)
    # print(script)
    return script


def load(scriptfile, package, defines=[]):
    # open a gRPC channel
    print(f"{defines}")
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


def fetch(scriptfile, package):
    # open a gRPC channel
    # channel = grpc.insecure_channel('[::1]:50051')
    channel = grpc.insecure_channel('localhost:50051')

    # create a stub (client)
    stub = eclat_pb2_grpc.EclatStub(channel)

    # create a valid request message
    with open(scriptfile, 'r') as f:
        script = f.read()
        print(f"sending {script} to grpc")
        req = eclat_pb2.EclatFetchRequest(script=script, package=package)

    # make the call
    response = stub.FetchConfiguration(req)

    print(response.status)
    print(response.message)
    return response


def fetch_pkg(package):
    """
    Download a specific package
    """
    channel = grpc.insecure_channel('localhost:50051')

    # create a stub (client)
    stub = eclat_pb2_grpc.EclatStub(channel)

    req = eclat_pb2.EclatFetchPackageRequest(package=package)

    # make the call
    response = stub.FetchPackageConfiguration(req)

    print(response.status)
    print(response.message)
    return response


def quit():
    channel = grpc.insecure_channel('localhost:50051')
    stub = eclat_pb2_grpc.EclatStub(channel)
    req = eclat_pb2.EclatQuitRequest()
    response = stub.Quit(req)
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
    print(f"Dumping {mapname}")
    channel = grpc.insecure_channel('localhost:50051')
    stub = eclat_pb2_grpc.EclatStub(channel)
    req = eclat_pb2.EclatDumpMapRequest(mapname=mapname)
    response = stub.DumpMap(req)
    print(response.status)
    print(response.message)
    return json.loads(response.message)


def main():
    # https://stackoverflow.com/questions/11760578/argparse-arguments-nesting
    # parse argument
    parser = argparse.ArgumentParser(
        description='Eclat CLI')
    subparsers = parser.add_subparsers(dest='cmd')

    # eclat --load example.eclat [-p testpkg] [-D FOO 2]
    load_p = subparsers.add_parser('load', help="Load an eclat script")
    load_p.add_argument("name", help="eCLAT script file path")
    load_p.add_argument(
        '-p', '--package', default="defaultpkg", help="The name of the package of the eCLAT script", required=False)
    load_p.add_argument('-D', '--define', nargs=2, action="append",
                        help="Define constant for eCLAT preprocessor", required=False)

    # eclat quit
    quit_p = subparsers.add_parser('quit', help="Close eCLATd")

    # eclat fetch example.eclat
    fetch_p = subparsers.add_parser(
        'fetch', help="Download all the packages required by an eCLAT script")
    fetch_p.add_argument("name", help="eCLAT script file path")
    fetch_p.add_argument(
        '-p', '--package', default="defaultpkg", help="The name of the package of the eCLAT script", required=False)

    fetch_pkg_p = subparsers.add_parser(
        'fetch-pkg', help="Make eCLATd download a specific package")
    fetch_pkg_p.add_argument("name", help="name of the package to download")

    # eclat.py read-map /sys/fs/bpf/maps/system/hvm_chain_map [--lookup 64]
    readmap_p = subparsers.add_parser(
        'read-map', help="Make eCLATd download a specific package")
    readmap_p.add_argument("name", help="map name (path)")
    readmap_p.add_argument("-l", "--lookup", nargs=1,
                           help="Get the map value corresponding to a given key", required=False)
    #########
    args = parser.parse_args()
    print(args)

    if args.cmd == 'load':
        defines = args.define if hasattr(args, 'define') else []
        ret = load(scriptfile=args.name,
                   package=args.package, defines=defines)
    elif args.cmd == 'fetch':
        ret = fetch(scriptfile=args.name, package=args.package)
    elif args.cmd == 'fetch_pkg':
        ret = fetch_pkg(scriptfile=args.name)
        pass  # TODO
    elif args.cmd == 'read-map':
        if args.lookup:
            ret = get_map_value(args.name, *args.lookup)
        else:
            ret = dump_map(args.name)
    elif args.cmd == 'quit':
        ret = quit()
    else:
        parser.error('No command specified.')

    print(f"status: {ret.status}")
    if ret.status == 'OK':
        sys.exit(0)
    else:
        sys.exit(1)

    # if args.load:
    #    ret = run(scriptfile=args['load'], package=args['package'], defines=args['define'])

    args = vars(parser.parse_args())
    print(args)
    ret = False
    sys.exit(0)

    # eclat --load example.eclat
    parser.add_argument(
        '-l', '--load', help="Load an eclat script", required=False)
    # eclat --fetch example.eclat
    parser.add_argument(
        '-f', '--fetch', help="Download all the packages required by an eCLAT script", required=False)
    # eclat --fetch-pkg mypackage
    parser.add_argument(
        '-k', '--fetch-pkg', help="Download a specific package", nargs=1, action="append", required=False)
    # eclat --quit
    parser.add_argument(
        '-q', '--quit', action="store_true", help="Close eCLATd", required=False)
    # specify package name (only for load)
    parser.add_argument(
        '-p', '--package', help="Package name of the eclat script", required=False)
    # preprocessor
    parser.add_argument(
        '-D', '--define', nargs=2, action="append", help="Define constant for eCLAT preprocessor", required=False)
    # eclat.py --lookup /sys/fs/bpf/maps/system/hvm_chain_map 64
    parser.add_argument(
        '-m', '--lookup', nargs=2, action="append", help="Get the map value corresponding to a given key", required=False)
    # eclat.py --dumpmap /sys/fs/bpf/maps/system/hvm_chain_map
    parser.add_argument(
        '-M', '--dumpmap', action="append", help="Dump the content of a given map", required=False)

    if args['load'] is not None:
        # load a script
        if not "package" in args:
            parser.error('Missing package name. Use --package argument')
        ret = run(scriptfile=args['load'],
                  package=args['package'], defines=args['define'])
    elif args['fetch'] is not None:
        # fetch the packages related to a script
        if not "package" in args:
            parser.error('Missing package name. Use --package argument')
        ret = fetch(scriptfile=args['fetch'],
                    package=args['package'], defines=args['define'])
    elif args['fetch_pkg'] is not None:
        print(args)
    elif args['lookup'] is not None:
        ret = get_map_value(*args['lookup'][0])
    elif args['dumpmap'] is not None:
        ret = dump_map(*args['dumpmap'])
    elif args['quit'] is not None:
        ret = quit()
    else:
        parser.error('No command specified.')

    print(f"status: {ret.status}")
    if ret.status == 'OK':
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
