# Makefile para o exercício de armazenamento chave-valor distribuído

.PHONY: clean stubs run_serv_pares_50051

stubs:
	python3 generate_stubs.py

clean:
	rm -f *.o
	rm -f svc_par
	rm -f cln_par
	rm -f svc_cen
	rm -f cln_cen
	rm -f *pb2*.py

run_cli_pares: stubs
	python3 ./cln_par.py $(arg)

run_cli_pares_padrao: stubs
	python3 ./cln_par.py 50051

run_serv_pares_1: stubs
	python3 ./svc_par.py $(arg)

run_serv_pares_1_padrao: stubs
	python3 ./svc_par.py 50051

run_serv_pares_2_padrao: stubs
	python3 ./svc_par.py 50051 1

run_serv_pares_2: stubs
	python3 ./svc_par.py $(arg) 1

run_serv_central: stubs
	python3 ./svc_cen.py $(arg)

run_serv_central_padrao: stubs
	python3 ./svc_cen.py 3001

run_cli_central: stubs
	python3 ./cln_cen.py $(arg)

run_cli_central_padrao: stubs
	python3 ./cln_cen.py 3001

