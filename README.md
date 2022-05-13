[![Inline docs](https://img.shields.io/readthedocs/hike-eclat)](https://hike-eclat.readthedocs.io/en/latest/index.html)

## Prerequisites

Python 3.5 or higher
pip version 9.0.1 or higher
If necessary, upgrade your version of pip:

```shell
$ python -m pip install --upgrade pip
```

If you cannot upgrade pip due to a system-owned installation, you can run the example in a virtualenv:

```shell
$ python -m pip install virtualenv
$ virtualenv venv
$ source venv/bin/activate
$ python -m pip install --upgrade pip
```

## Install

```shell
git clone https://github.com/netgroup/eclat-daemon.git
git submodule update --init --recursive
cd eclat-daemon
pip install -r requirements.txt
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. eclat.proto
```

## Run

```shell
python eclatd.py #start the daemon
python eclat.py --load test/eclat_scripts/ddos.eclat --package test #load a test script
python eclat.py --load test/eclat_scripts/ddos2.eclat --define DEVNAME enp6s0f0 --package test

python eclat.py --dumpmap /sys/fs/bpf/maps/system/hvm_chain_map
python eclat.py --lookup /sys/fs/bpf/maps/system/hvm_chain_map 64
```

## Unit tests

```shell
python -m unittest test.test_grpc
python -m unittest test.test_parser
python -m unittest test.test_controller
```

## dokerized eCLAT 

A docker container which provides the eCLAT development and testing environment is available [here](https://github.com/netgroup/eclat-docker)


