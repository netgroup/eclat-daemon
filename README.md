[![Inline docs](https://img.shields.io/readthedocs/hike-eclat)](https://hike-eclat.readthedocs.io/en/latest/index.html)

## Install

A [docker container](https://github.com/netgroup/eclat-docker) provides the development and testing environment for eCLAT.
Please download, build and execute the container following the instructions [here](https://github.com/netgroup/eclat-docker) and then execute the test experiments discussed [here](https://hike-eclat.readthedocs.io/en/latest/experiments.html).

In the following subsections you find some instructions for manually downloading and installing eCLAT, all these steps are automatically performed in the docker container.

### Prerequisites

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

### Install

```shell
git clone https://github.com/netgroup/eclat-daemon.git
git submodule update --init --recursive
cd eclat-daemon
pip install -r requirements.txt
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. eclat.proto
```

### Unit tests

```shell
python -m unittest test.test_grpc #needs eclatd running
python -m unittest test.test_parser
python -m unittest test.test_controller
```

## Run

### start the eCLAT daemon in a terminal

```shell
python eclatd.py #start the daemon
```

### run the eCLAT client in a different terminal

```shell
python eclat.py --load test/eclat_scripts/basic_example.eclat --define DEVNAME eth0 --package test

python eclat.py --dumpmap /sys/fs/bpf/maps/system/hvm_chain_map
python eclat.py --lookup /sys/fs/bpf/maps/system/hvm_chain_map 64
```

