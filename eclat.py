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

    # print the outcome
    print(f"{response.status}: {response.message}")

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

    # print the outcome
    print(f"{response.status}: {response.message}")
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
    response = stub.FetchPackage(req)

    # print the outcome
    print(f"{response.status}: {response.message}")
    return response


def quit():
    channel = grpc.insecure_channel('localhost:50051')
    stub = eclat_pb2_grpc.EclatStub(channel)
    req = eclat_pb2.EclatQuitRequest()
    response = stub.Quit(req)
    
    # print the outcome
    print(f"{response.status}: {response.message}")

    return response


def get_map_value(mapname, key):
    channel = grpc.insecure_channel('localhost:50051')
    stub = eclat_pb2_grpc.EclatStub(channel)
    req = eclat_pb2.EclatGetMapValueRequest(mapname=mapname, key=key)
    response = stub.GetMapValue(req)
    
    # print the outcome
    print(f"{response.status}: {response.message}")

    return response


def dump_map(mapname):
    print(f"Dumping {mapname}")
    channel = grpc.insecure_channel('localhost:50051')
    stub = eclat_pb2_grpc.EclatStub(channel)
    req = eclat_pb2.EclatDumpMapRequest(mapname=mapname)
    response = stub.DumpMap(req)
    
    # print the outcome
    print(f"{response.status}: {response.message}")

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
    ######

    # implementing the commands
    args = parser.parse_args()

    if args.cmd == 'load':
        defines = args.define if hasattr(args, 'define') else []
        ret = load(scriptfile=args.name,
                   package=args.package, defines=defines)
    elif args.cmd == 'fetch':
        ret = fetch(scriptfile=args.name, package=args.package)
    elif args.cmd == 'fetch-pkg':
        ret = fetch_pkg(package=args.name)
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

    if ret.status == 'OK':
        print("status: OK")
        sys.exit(0)
    else:
        print("status: ERROR")
        sys.exit(1)


if __name__ == "__main__":
    main()
