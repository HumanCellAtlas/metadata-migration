.PHONY: install
install:
	virtualenv -p python3 venv
	venv/bin/pip install -r requirements.txt --upgrade

.PHONY: test
test:
	. venv/bin/activate && python -m unittest discover -s test -p 'test_*.py'

.PHONY: docs
docs:
	ruby -e "require 'erb'; require 'json'; File.open('README.md.erb','r') { |fh| puts ERB.new(fh.read, 0, '>').result() }" > README.md
