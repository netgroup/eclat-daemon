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
cd eclat-daemon
pip install -r requirements.txt
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. eclat.proto
```

## Run

```shell
python eclatd.py
python eclat.py --run nomescript.eclat
```

## Unit test

python -m unittest test_run.py

virtualenv venv
cd venv
source activate bin/activate
