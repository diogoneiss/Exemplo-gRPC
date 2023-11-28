import socket
import sys
import grpc
import central_key_value_store_pb2
import central_key_value_store_pb2_grpc
import key_value_store_pb2
import key_value_store_pb2_grpc
from common import fix_address, show_debug_messages


def main():
    if len(sys.argv) < 2:
        print("Uso: python cln_cen.py <endereço_do_servidor_central>")
        sys.exit(1)

    server_address = sys.argv[1]
    server_address = fix_address(server_address)

    try:
        with grpc.insecure_channel(server_address) as channel:
            # Testar a conexão com o servidor
            try:
                grpc.channel_ready_future(channel).result(timeout=10)
            except grpc.FutureTimeoutError:
                print(f"Erro: Não foi possível conectar ao servidor no endereço {server_address}.")
                sys.exit(1)

            stub = central_key_value_store_pb2_grpc.CentralKeyValueStoreStub(channel)

            while True:
                try:
                    input_prompt = "Digite um comando (C,ch ou T) ou 'sair' para encerrar: " if show_debug_messages else ""
                    command = input(input_prompt)

                    if command.lower() == 'sair' or command == '':
                        break

                    process_command(command, stub)
                # Interrupção do teclado ou fim do arquivo redirecionado do stdin encerram o cliente
                except (KeyboardInterrupt, EOFError):
                    break

    except grpc.RpcError as e:
        print(f"Erro de RPC ao tentar conectar: {e}")
        sys.exit(1)

def process_command(command, stub):
    parts = command.split(',', maxsplit=2)

    if len(parts) == 0:
        return

    cmd_type = parts[0].upper()

    if cmd_type == 'C':
        # Mapeamento
        if len(parts) != 2:
            print("Formato inválido para mapeamento. Use: C,chave")
            return
        chave = int(parts[1].strip())
        map_key(chave, stub)
    elif cmd_type == 'T':
        # Término
        terminate(stub)
        sys.exit(0)


def map_key(key, central_stub):
    try:
        response = central_stub.MapKey(central_key_value_store_pb2.Key(key=key))
        if response.identifier:
            if show_debug_messages:
                print(f"Servidor responsável pela chave {key}: {response.identifier}")
            mensagem = response.identifier
            # Estabelecer conexão com o servidor responsável
            with grpc.insecure_channel(response.identifier) as server_channel:
                server_stub = key_value_store_pb2_grpc.KeyValueStoreStub(server_channel)

                try:
                    # Consultar a chave no servidor responsável
                    value_response = server_stub.Query(key_value_store_pb2.Key(key=key))
                    if value_response.value:
                        if show_debug_messages:
                            print(f"Valor associado à chave {key}: {value_response.value}")
                        mensagem = mensagem + ":" + value_response.value
                        print(mensagem)
                    else:
                        print("<NADA> Chave não encontrada no servidor responsável.")
                except grpc.RpcError as e:
                    print(f"Erro de RPC ao consultar chave no servidor: {e}")
        else:
            # chave nao encontrada no servidor central
            print("")
    except grpc.RpcError as e:
        print(f"Erro de RPC ao mapear chave no servidor centralizador: {e}")


def terminate(stub):
    response = stub.Terminate(central_key_value_store_pb2.Empty())
    if show_debug_messages:
        print("Resposta do servidor central:", response.result)
    else:
        print(response.result)
    sys.exit(0)  # Encerra o programa após o término do servidor


if __name__ == '__main__':
    main()
