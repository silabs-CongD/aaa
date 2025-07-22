.SUFFIXES: # ignore builtin rules
.PHONY: all

TARGET ?= clean_build
TYPE ?= Debug #Release

all: build

build:
	@echo 'Building $@...!'
