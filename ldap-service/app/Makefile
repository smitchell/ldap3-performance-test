# The binary to build (just the basename).
BASE_DIR := src
MODULE := ldap-service

# This version-strategy uses git tags to set the version string
TAG := $(shell git describe --tags --always --dirty)

BLUE='\033[0;34m'
NC='\033[0m' # No Color
IMAGE := $(MODULE)

run:
	@python -m $(BASE_DIR)

test:
	@pytest

lint:
	@echo "\n${BLUE}Running Pylint against source and test files...${NC}\n"
	@pylint --rcfile=setup.cfg **/*.py
	@echo "\n${BLUE}Running Flake8 against source and test files...${NC}\n"
	@flake8
	@echo "\n${BLUE}Running Bandit against source files...${NC}\n"
	@bandit -r --ini setup.cfg

build:
	@echo "\n${BLUE}Building Development image with labels:\n"
	@echo "name: $(MODULE)"
	@echo "version: $(TAG)${NC}"
	@docker build -t $(IMAGE):$(TAG) -t $(IMAGE):latest ../
	@echo "\n${BLUE}Run: docker run -v ~/.config/ldap_service/config.yaml:/etc/ldap_service/config.yaml -p 5002:5002 --name $(MODULE) $(IMAGE):$(TAG)${NC}\n"

clean:
	rm -rf .pytest_cache .coverage .pytest_cache coverage.xml

docker-clean:
	@docker system prune -f --filter "label=name=$(MODULE)"
