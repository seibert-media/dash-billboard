
.PHONY: test
.PHONY: clean

test:
	$(MAKE) -C rocket test

clean:
	$(MAKE) -C rocket clean

