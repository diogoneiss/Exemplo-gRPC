import socket

from grpc_tools import protoc

# invés de chamar tudo no makefile, optei por abstrair as regras para um arquivo separado, se desejado tratar erros essa abordagem
# funciona melhor

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
