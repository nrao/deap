.PHONY: all check clean install

all:
	$(MAKE) -C lib
	$(MAKE) -C api

install:
	$(MAKE) -C lib install
	$(MAKE) -C api install

clean:
	$(MAKE) -C lib clean
	$(MAKE) -C api clean
