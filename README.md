```shell
git clone https://github.com/netgroup/eclat-daemon.git
cd eclat-daemon
pip install -r requirements.txt
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. eclat.proto

python eclatd.py
python eclat.py --run nomescript.eclat
```

# TEST

python -m unittest test_run.py
