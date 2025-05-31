BUILD_DIR := ./build

all: verilog

verilog:
	-mkdir -p $(BUILD_DIR);
	-rm $(BUILD_DIR)/* -r;
	mill -i imageprocess.runMain imageprocess.Elaborate --target-dir $(BUILD_DIR)

.PHONY: verilog