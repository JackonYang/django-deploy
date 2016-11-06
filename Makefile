PY?=python
PIP?=pip

build:
	$(PIP) install -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com -r requirements.txt


.PHONY: build
