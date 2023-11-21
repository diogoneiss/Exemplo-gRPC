import sys

import grpc
import key_value_store_pb2
import key_value_store_pb2_grpc


def main():
    if len(sys.argv) < 2:
        print("Uso: python cln_par.py <endereço_do_servidor>")
        sys.exit(1)

    server_address = sys.argv[1]

    try:
        with grpc.insecure_channel(server_address) as channel:
            # Testa a conexão
            try:
                grpc.channel_ready_future(channel).result(timeout=3)
            except grpc.FutureTimeoutError:
                print(f"Erro: Não foi possível conectar ao servidor no endereço {server_address}. Verifique se ele está rodando ou se o endereço está correto.")
                sys.exit(1)

            stub = key_value_store_pb2_grpc.KeyValueStoreStub(channel)

            # Loop para ler comandos da entrada padrão
            while True:
                try:
                    command = input("Digite um comando (I, C, A, T) ou 'sair' para encerrar: ")
                    if command.lower() == 'sair':
                        break

                    process_command(command, stub)
                except KeyboardInterrupt:
                    break
    except grpc.RpcError as e:
        print(f"Erro de RPC ao tentar conectar: {e}")
        sys.exit(1)


def process_command(command: str, stub):
    parts = command.split(',')
    # Evitar erros de acesso ao array
    if len(parts) == 0:
        return

    # aceitar minusculo ou maiusculo ignorando espacos extras
    cmd_type = parts[0].upper().replace(' ', '')

    if cmd_type == 'I':
        # Inserção
        if len(parts) != 3:
            print("Formato inválido para inserção. Use: I,chave,valor")
            return
        chave = int(parts[1].strip())
        valor = parts[2].strip()
        insert(chave, valor, stub)
    elif cmd_type == 'C':
        # Consulta
        if len(parts) != 2:
            print("Formato inválido para consulta. Use: C,chave")
            return
        chave = int(parts[1].strip())
        query(chave, stub)
    elif cmd_type == 'A':
        # Ativação
        if len(parts) != 2:
            print("Formato inválido para ativação. Use: A,identificador_do_serviço")
            return
        service_identifier = parts[1].strip()
        activate(service_identifier, stub)
    elif cmd_type == 'T':
        # Término
        terminate(stub)


def insert(key, value, stub):
    response = stub.Insert(key_value_store_pb2.KeyValue(key=key, value=value))
    print("Resposta do servidor:", response.result)


def query(key, stub):
    response = stub.Query(key_value_store_pb2.Key(key=key))
    print("Valor:", response.value)


def activate(service_identifier, stub):
    response = stub.Activate(key_value_store_pb2.ServiceIdentifier(identifier=service_identifier))
    print("Resposta do servidor:", response.result)


def terminate(stub):
    response = stub.Terminate(key_value_store_pb2.Empty())
    print("Resposta do servidor:", response.result)


if __name__ == '__main__':
    main()