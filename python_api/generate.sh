python3 -m grpc_tools.protoc -I../protos --python_out=. --grpc_python_out=. ../protos/Database.proto
python3 -m grpc_tools.protoc -I../protos --python_out=. --grpc_python_out=. ../protos/Ingester.proto
