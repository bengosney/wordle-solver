.PHONY: help clean test install all init dev
.DEFAULT_GOAL := dev

HOOKS=$(.git/hooks/pre-commit)
INS=$(wildcard requirements.*.in)
REQS=$(subst in,txt,$(INS))

WORDLIST=words.txt

help: ## Display this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.gitignore:
	curl -q "https://www.toptal.com/developers/gitignore/api/visualstudiocode,python,direnv" > $@
	echo "\n# generated by makefile" >> $@
	echo $(WORDLIST) >> $@


.git: .gitignore
	git init

$(WORDLIST):
	curl https://www.wordgamedictionary.com/sowpods/download/sowpods.txt > $@
	curl https://www.wordgamedictionary.com/twl06/download/twl06.txt >> $@

requirements.dev.in:
	@echo "pre-commit" >> $@
	@echo "pip-tools" >> $@
	@echo "pytest" >> $@
	@echo "icecream" >> $@

.pre-commit-config.yaml:
	curl https://gist.githubusercontent.com/bengosney/4b1f1ab7012380f7e9b9d1d668626143/raw/060fd68f4c7dec75e8481e5f5a4232296282779d/.pre-commit-config.yaml > $@

requirements.in:
	@touch $@

requirements.%.txt: requirements.%.in
	@echo "Builing $@"
	@pip-compile -q -o $@ $^

requirements.txt: requirements.in
	@echo "Builing $@"
	@pip-compile -q $^

.direnv: .envrc
	pip install --upgrade pip
	pip install wheel pip-tools
	@touch $@ $^

.git/hooks/pre-commit: .pre-commit-config.yaml
	pre-commit install

.envrc:
	@echo "Setting up .envrc then stopping"
	@echo "layout python python3.10" > $@
	@touch -d '+1 minute' $@
	@false

init: .direnv .git .git/hooks/pre-commit requirements.dev.in $(WORDLIST) ## Initalise a enviroment

clean: ## Remove all build files
	find . -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete
	rm -rf .pytest_cache
	rm -f .testmondata

install: requirements.txt $(REQS) ## Install development requirements (default)
	@echo "Installing $^"
	@pip-sync $^

dev: init install ## Start work
	code .
