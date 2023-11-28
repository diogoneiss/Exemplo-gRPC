import socket

from grpc_tools import protoc

# o protoc as vezes deu problema nos ambientes que testei (mesmo com o grpcio-tools instalado) entao para garantir
# que funcione independente de PATH, vamos chamar o protoc diretamente do python

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

#print("Nome completo da maquina: ", socket.getfqdn())
