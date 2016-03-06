.PHONY: test
test:
	PYTHONPATH=`pwd` python -m pytest -s

.PHONY: clean
clean:
	rm examples/*.png
