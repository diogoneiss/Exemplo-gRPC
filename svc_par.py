import sys
import time
import socket

import grpc
from concurrent import futures
import key_value_store_pb2
import key_value_store_pb2_grpc
import central_key_value_store_pb2
import central_key_value_store_pb2_grpc
import threading


class KeyValueStoreServicer(key_value_store_pb2_grpc.KeyValueStoreServicer):
    def __init__(self, flag_ativacao=None):
        self.data_store = {}
        self.server_stop_event = threading.Event()
        self.flag_ativacao = flag_ativacao

    def Activate(self, request, context):
        if self.flag_ativacao:
            central_server_address = request.identifier
            try:
                # Conectar ao servidor central
                with grpc.insecure_channel(central_server_address) as channel:
                    central_stub = central_key_value_store_pb2_grpc.CentralKeyValueStoreStub(channel)

                    # Registrar as chaves no servidor central
                    keys = list(self.data_store.keys())
                    response = central_stub.Register(central_key_value_store_pb2.ServerKeys(
                        identifier=socket.getfqdn() + ":" + str(port),
                        keys=keys
                    ))
                    return key_value_store_pb2.Response(result=response.result)
            except grpc.RpcError as e:
                print(f"Erro de RPC ao tentar registrar no servidor central: {e}")
                return key_value_store_pb2.Response(result=-1)
        else:
            return key_value_store_pb2.Response(result=0)

    def Insert(self, request, context):
        chave = request.key
        valor = request.value
        if chave in self.data_store:
            return key_value_store_pb2.Response(result=-1)
        else:
            self.data_store[chave] = valor
            return key_value_store_pb2.Response(result=0)

    def Query(self, request, context):
        chave = request.key
        valor = self.data_store.get(chave, "")
        print("Todos os valores: ")
        print(self.data_store)
        return key_value_store_pb2.ValueResponse(value=valor)

    def Terminate(self, request, context):
        self.server_stop_event.set()
        return key_value_store_pb2.Response(result=0)


def serve(port, flag_ativacao=None):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servicer = KeyValueStoreServicer(flag_ativacao)
    key_value_store_pb2_grpc.add_KeyValueStoreServicer_to_server(servicer, server)

    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f"Servidor iniciado na porta {port}")

    try:
        while not servicer.server_stop_event.is_set():
            time.sleep(1)
    except KeyboardInterrupt:
        server.stop(0)
        print("Servidor interrompido")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Argumentos faltantes! \nUso: python svc_par.py <porto> [flag_ativacao]")
        sys.exit(1)

    port = sys.argv[1]
    flag_ativacao = sys.argv[2] if len(sys.argv) > 2 else None

    serve(port, flag_ativacao)
