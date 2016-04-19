.PHONY: test
test:
	PYTHONPATH=`pwd` python -m pytest -s

.PHONY: cat-error1
cat-error1:
	cat examples/error1.prog

.PHONY: run-error1
run-error1:
	python bin/proglan examples/error1.prog || true

.PHONY: cat-error2
cat-error2:
	cat examples/error2.prog

.PHONY: run-error2
run-error2:
	python bin/proglan examples/error2.prog || true

.PHONY: cat-error3
cat-error3:
	cat examples/error3.prog

.PHONY: run-error3
run-error3:
	python bin/proglan examples/error3.prog || true

.PHONY: cat-arrays
cat-arrays:
	cat examples/arrays.prog

.PHONY: run-arrays
run-arrays:
	python bin/proglan examples/arrays.prog

.PHONY: cat-conditionals
cat-conditionals:
	cat examples/conditionals.prog

.PHONY: run-conditionals
run-conditionals:
	python bin/proglan examples/conditionals.prog

.PHONY: cat-recursion
cat-recursion:
	cat examples/recursion.prog

.PHONY: run-recursion
run-recursion:
	python bin/proglan examples/recursion.prog

.PHONY: cat-iteration
cat-iteration:
	cat examples/iteration.prog

.PHONY: run-iteration
run-iteration:
	python bin/proglan examples/iteration.prog

.PHONY: cat-functions
cat-functions:
	cat examples/functions.prog

.PHONY: run-functions
run-functions:
	python bin/proglan examples/functions.prog

.PHONY: cat-dictionary
cat-dictionary:
	cat examples/dictionary.prog
	cat examples/dictionary-test.prog

.PHONY: run-dictionary
run-dictionary:
	python bin/proglan examples/dictionary-test.prog

.PHONY: cat-problem
cat-problem:
	cat examples/priority-queue.prog
	cat examples/wire.prog
	cat examples/wire-test.prog

.PHONY: run-problem
run-problem:
	python bin/proglan examples/wire-test.prog

.PHONY: clean
clean:
	rm examples/*.png
	find . -name "*.pyc" | xargs -n 1 rm
