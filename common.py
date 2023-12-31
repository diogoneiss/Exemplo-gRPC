import socket

show_debug_messages = False


def fix_address(address, use_localhost=False):
    # Infere o endereço completo se apenas a porta for fornecida no endereco
    base = "localhost" if use_localhost else socket.getfqdn()
    if ":" not in address:
        address = base + ":" + address
        if show_debug_messages:
            print("Endereco gerado: ", address)
    return address
