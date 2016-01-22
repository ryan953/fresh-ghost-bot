.PHONEY: help
.PHONEY: install
.PHONEY: publish
.PHONEY: test
.PHONEY: test-slack
.PHONEY: scrape
.PHONEY: clear-cache

help:
	@echo "Commands:"
	@echo ""
	@echo "help"
	@echo "    This help"
	@echo ""
	@echo "install"
	@echo "    Install dependencies in a virtualenv"
	@echo "publish"
	@echo "    Push the code to ryan953.com"
	@echo "clear-cache"
	@echo "    Clear any existing data"
	@echo ""
	@echo "test"
	@echo "    Run the script without saving new data or posting to slack"
	@echo "test-slack"
	@echo "    Run the script without saving new data and DO post to slack"
	@echo "test-save"
	@echo "    Run the script and save new data; no posting to slack"
	@echo "scrape"
	@echo "    Run the script, save new data, post results"
	@echo ""


install:
	mkdir -p ./data
	mkdir -p ./env
	touch ./data/last-run.lst
	pip install virtualenv
	virtualenv ./env
	source ./env/bin/activate && pip install BeautifulSoup && deactivate

publish:
	rsync -zhrv -e '/usr/bin/ssh' \
		--bwlimit=2000 \
		--exclude='.git' \
		--exclude='./data' \
		--exclude='./env' \
		. ryan953@ryan953.com:/home/ryan953/freshbooks-faces

test:
	source ./env/bin/activate && python getFaces.py --verbose && deactivate

test-slack:
	source ./env/bin/activate && python getFaces.py --verbose --slack && deactivate

test-save:
	source ./env/bin/activate && python getFaces.py --verbose --save && deactivate

scrape:
	source ./env/bin/activate && python getFaces.py --save --slack && deactivate

clear-cache:
	rm -f ./data/*.html
