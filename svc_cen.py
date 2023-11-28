# Feito por Diogo Oliveira Neiss 2021421915

import grpc
from concurrent import futures
import central_key_value_store_pb2
import central_key_value_store_pb2_grpc
import sys
from common import show_debug_messages, fix_address


class CentralKeyValueStoreServicer(central_key_value_store_pb2_grpc.CentralKeyValueStoreServicer):
    def __init__(self):
        self.key_directory = {}

    def Register(self, request, context):
        identifier = request.identifier
        count = 0
        for key in request.keys:
            self.key_directory[key] = identifier
            count += 1
        if show_debug_messages:
            print("Todas as chaves armazenadas e identificadores: ")
            print(self.key_directory)
        return central_key_value_store_pb2.Response(result=count)

    def MapKey(self, request, context):
        key = request.key
        identifier = self.key_directory.get(key, "")
        return central_key_value_store_pb2.ServiceIdentifier(identifier=identifier)

    def Terminate(self, request, context):
        # Lógica para terminar o servidor
        return central_key_value_store_pb2.Response(result=0)


def serve(port):
    if show_debug_messages:
        print("Starting central server at address ", fix_address(port))
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servicer = CentralKeyValueStoreServicer()
    central_key_value_store_pb2_grpc.add_CentralKeyValueStoreServicer_to_server(servicer, server)
    server.add_insecure_port(f'0.0.0.0:{port}')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python svc_cen.py <porto>")
        sys.exit(1)

    port = sys.argv[1]
    serve(port)
