.SUFFIXES: # ignore builtin rules
.PHONY: all

TARGET ?= clean_build
TYPE ?= Debug #Release

all: build

build:
	@echo 'Building $@...!'
	${MAKE} -C project_dir ${TARGET} TYPE=${TYPE}
