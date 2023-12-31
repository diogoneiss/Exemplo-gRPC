# Feito por Diogo Oliveira Neiss 2021421915

.PHONY: clean stubs

stubs:
	@python3 generate_stubs.py

clean:
	rm -f *.o
	rm -f svc_par
	rm -f cln_par
	rm -f svc_cen
	rm -f cln_cen
	rm -f *pb2*.py


run_serv_pares_1: stubs
	@python3 ./svc_par.py $(arg)

run_serv_pares_2: stubs
	@python3 ./svc_par.py $(arg) qqcoisa

run_cli_pares: stubs
	@python3 ./cln_par.py $(arg)

run_serv_central: stubs
	@python3 ./svc_cen.py $(arg)

run_cli_central: stubs
	@python3 ./cln_cen.py $(arg)


