from grpc_tools import protoc

protoc.main((
    '',
    '-I.',
    '--python_out=.',
    '--grpc_python_out=.',
    './key_value_store.proto',
))

protoc.main((
    '',
    '-I.',
    '--python_out=.',
    '--grpc_python_out=.',
    './central_key_value_store.proto',
))
