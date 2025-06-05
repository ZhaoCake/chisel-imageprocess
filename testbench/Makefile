# Makefile for ProcessMain testbench using iverilog

# Variables
TOPLEVEL = ProcessMain_tb
BUILD_DIR = ../build
SV_SOURCES = $(shell cat $(BUILD_DIR)/filelist.f | sed "s|^|$(BUILD_DIR)/|")
CONVERTED_DIR = $(OUTPUT_DIR)/converted
VERILOG_SOURCES = $(CONVERTED_DIR)/$(TOPLEVEL).v $(patsubst $(BUILD_DIR)/%.sv,$(CONVERTED_DIR)/%.v,$(filter %.sv,$(SV_SOURCES)))
OUTPUT_DIR = sim_output
SV2V = sv2v

# Check if sv2v is installed
CHECK_SV2V := $(shell which sv2v 2>/dev/null)

# Compile and run simulation
all: check_sv2v convert compile run

check_sv2v:
	@if [ -z "$(CHECK_SV2V)" ]; then \
		echo "Error: sv2v not found. Please install sv2v first."; \
		echo "You can download it from: https://github.com/zachjs/sv2v/releases"; \
		echo "Installation steps:"; \
		echo "  wget https://github.com/zachjs/sv2v/releases/download/v0.0.13/sv2v-Linux.zip"; \
		echo "  unzip sv2v-Linux.zip"; \
		echo "  sudo cp sv2v-Linux/sv2v /usr/bin/sv2v"; \
		echo "  sudo chmod +x /usr/bin/sv2v"; \
		exit 1; \
	fi

install_sv2v:
	@echo "Installing sv2v..."
	wget https://github.com/zachjs/sv2v/releases/download/v0.0.13/sv2v-Linux.zip
	unzip sv2v-Linux.zip
	sudo cp sv2v-Linux/sv2v /usr/bin/sv2v
	sudo chmod +x /usr/bin/sv2v
	rm -rf sv2v-Linux sv2v-Linux.zip

convert: check_sv2v
	@echo "Converting SystemVerilog to Verilog..."
	mkdir -p $(CONVERTED_DIR)
	$(SV2V) $(TOPLEVEL).v -w $(CONVERTED_DIR)/$(TOPLEVEL).v
	@for file in $(filter %.sv,$(SV_SOURCES)); do \
		target_dir=$(CONVERTED_DIR)/`dirname $${file#$(BUILD_DIR)/}`; \
		mkdir -p $$target_dir; \
		target_file=$$target_dir/`basename $$file .sv`.v; \
		echo "Converting $$file to $$target_file"; \
		$(SV2V) $$file -w $$target_file; \
	done

compile: convert
	@echo "Compiling with iverilog..."
	mkdir -p $(OUTPUT_DIR)
	iverilog -o $(OUTPUT_DIR)/sim -g2012 $(VERILOG_SOURCES)

run:
	@echo "Running simulation..."
	vvp $(OUTPUT_DIR)/sim

view:
	@echo "Opening waveform viewer..."
	gtkwave waveform.vcd &

clean:
	rm -rf $(OUTPUT_DIR)
	rm -f *.vcd output_gray.hex

.PHONY: all compile run view clean install_sv2v check_sv2v convert
