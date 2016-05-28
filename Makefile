.PHONEY: help
.PHONEY: install
.PHONEY: publish
.PHONEY: test
.PHONEY: test-slack
.PHONEY: scrape
.PHONEY: clear-cache
.PHONEY: scrape-old
.PHONEY: wayback-extract
.PHONEY: wayback-download
.PHONEY: format-file-names

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

wayback-extract:
	touch ./wayback-scraper/examined.lst
	touch ./wayback-scraper/urls.lst
	cd ./wayback-scraper && find ./data -type f | node ./extractor.js
	less ./wayback-scraper/urls.lst > ./wayback-scraper/tmp.lst
	less ./wayback-scraper/tmp.lst | sort | uniq -u > ./wayback-scraper/urls.lst

wayback-download:
	# get downloaded files into tmp
	find ./wayback-scraper/data -type f | sed s/\\.\\/wayback\\-scraper\\/data/https:\\/\\/web\\.archive\\.org/g | sed s/http:\\/www/http:\\/\\/www/g | grep "[0-9]/" > ./wayback-scraper/tmp.lst

	# append urls into tmp
	less ./wayback-scraper/urls.lst >> ./wayback-scraper/tmp.lst

	# sort tmp, and get a list of the first 10 unique files (these are known, but not downloaded)
	less ./wayback-scraper/tmp.lst | sort | uniq -u | head -100 > ./wayback-scraper/toGet-chunk.lst

	#get those files
	wget -i ./wayback-scraper/toGet-chunk.lst --wait=1 --force-directories --no-host-directories --directory-prefix=./wayback-scraper/data

format-file-names:
	./format-file-names.sh
