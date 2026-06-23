# dlt pipeline helpers
# Usage: make <target> [PIPELINE=name]
# Override pipeline: make show PIPELINE=rest_api_pokemon

PIPELINE ?= rest_api_github
PY       ?= python

.PHONY: help list show info trace run-github run-pokemon drop drop-all clean nuke

help:               ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN{FS=":.*?## "}{printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

list:               ## List all dlt pipelines
	dlt pipeline --list-pipelines

show:               ## Open Streamlit dashboard for PIPELINE (needs streamlit)
	dlt pipeline $(PIPELINE) show

info:               ## Print PIPELINE state + last load info
	dlt pipeline $(PIPELINE) info

trace:              ## Print last run trace for PIPELINE
	dlt pipeline $(PIPELINE) trace

run-github:         ## Run GitHub pipeline
	$(PY) rest_api_pipeline.py

run-pokemon:        ## Run Pokemon pipeline (same script)
	$(PY) rest_api_pipeline.py

drop:               ## Drop pending packages for PIPELINE
	dlt pipeline $(PIPELINE) drop-pending-packages

drop-all:           ## Drop ALL data + schema for PIPELINE (keeps working dir)
	dlt pipeline $(PIPELINE) drop --drop-all

clean:              ## Remove PIPELINE working dir (~/.dlt/pipelines/PIPELINE)
	rm -rf ~/.dlt/pipelines/$(PIPELINE)

nuke:               ## Wipe ALL pipeline working dirs + local duckdb files
	rm -rf ~/.dlt/pipelines/
	rm -f *.duckdb
