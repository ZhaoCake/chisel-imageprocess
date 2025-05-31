# Makefile for ProcessMain testbench using iverilog

# Variables
TOPLEVEL = ProcessMain_tb
BUILD_DIR = ../build
VERILOG_SOURCES = $(shell find $(BUILD_DIR) -name "*.sv") $(TOPLEVEL).sv
OUTPUT_DIR = sim_output

# Compile and run simulation
all: compile run

compile:
	@echo "Compiling with iverilog..."
	mkdir -p $(OUTPUT_DIR)
	iverilog -o $(OUTPUT_DIR)/sim -g2012 -DDUMP_ENABLE $(VERILOG_SOURCES)

run:
	@echo "Running simulation..."
	vvp $(OUTPUT_DIR)/sim

view:
	@echo "Opening waveform viewer..."
	gtkwave dump.vcd &

clean:
	rm -rf $(OUTPUT_DIR)
	rm -f *.vcd output_gray.hex

.PHONY: all compile run view clean
