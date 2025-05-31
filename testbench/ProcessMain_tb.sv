`timescale 1ns/1ps
`define DUMP_ENABLE

module ProcessMain_tb;
  // Clock and reset signals
  reg clock = 0;
  reg reset = 1;
  
  // DUT I/O
  reg io_convert_enable = 0;
  wire io_convert_done;
  
  // Simulation parameters
  integer i;
  localparam IMAGE_SIZE = 512 * 512;
  
  // Instantiate the DUT
  ProcessMain dut (
    .clock(clock),
    .reset(reset),
    .io_convert_enable(io_convert_enable),
    .io_convert_done(io_convert_done)
  );
  
  // Clock generation - 10ns period (100MHz)
  always #5 clock = ~clock;
  
  // File for memory dump
  integer dump_file;
  
  // Test sequence
  initial begin
    // Setup waveform dumping
    $dumpfile("dump.vcd");
    $dumpvars(0, ProcessMain_tb);
    
    // Initialize signals
    $display("Starting simulation...");
    reset = 1;
    io_convert_enable = 0;
    #100;
    
    // Release reset
    reset = 0;
    #50;
    
    // Start image conversion
    $display("Starting image conversion at %t ns", $time);
    io_convert_enable = 1;
    
    // Wait for conversion to complete
    wait(io_convert_done);
    $display("Conversion completed at %t ns", $time);
    
    // Deactivate conversion
    #100;
    io_convert_enable = 0;
    
    // Wait for the system to stabilize
    #1000;
    
    // Memory dump happens automatically in the ram_262144x8 module
    // due to the final block with DUMP_ENABLE defined
    
    // End simulation
    $display("Simulation finished at %t ns", $time);
    #100;
    $finish;
  end
  
endmodule
