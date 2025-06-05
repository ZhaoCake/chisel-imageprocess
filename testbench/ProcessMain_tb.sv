`timescale 1ns/1ps

module ProcessMain_tb;
  // Clock and reset
  reg clock = 0;
  reg reset = 1;
  
  // DUT I/O
  reg io_convert_enable = 0;
  wire io_convert_done;
  
  // Read RAM interface for dumping
  reg [17:0] io_readram_addr = 0;
  wire [7:0] io_readram_data;
  
  // Add InputROM write interface
  reg [17:0] io_inputrom_write_addr = 0;
  reg [23:0] io_inputrom_write_data = 0;
  reg io_inputrom_write_enable = 0;
  
  // Instantiate the DUT
  ProcessMain dut (
    .clock(clock),
    .reset(reset),
    .io_convert_enable(io_convert_enable),
    .io_convert_done(io_convert_done),
    .io_readram_addr(io_readram_addr),
    .io_readram_data(io_readram_data),
    .io_inputrom_write_addr(io_inputrom_write_addr),
    .io_inputrom_write_data(io_inputrom_write_data),
    .io_inputrom_write_enable(io_inputrom_write_enable)
  );
  
  // Clock generation - 10ns period (100MHz)
  always #5 clock = ~clock;
  
  // File handles
  integer input_file;
  integer dump_file;
  integer file_status;
  
  // Simulation parameters
  integer i;
  localparam IMAGE_SIZE = 512 * 512;
  reg [23:0] pixel_data;
  
  // Test sequence
  initial begin
    // Setup waveform dumping
    $dumpfile("waveform.vcd");
    $dumpvars(0, ProcessMain_tb);
    
    // Initialize
    $display("Starting simulation setup...");
    reset = 1;
    io_convert_enable = 0;
    io_readram_addr = 0;
    io_inputrom_write_enable = 0;
    #50;
    
    // Release reset
    reset = 0;
    #50;
    
    // Load the input image from hex file - using relative path
    // Try multiple possible locations for the file
    if ($fopen("../output/lena_bgr.hex", "r") != 0)
      load_input_image_from_file("../output/lena_bgr.hex");
    else if ($fopen("lena_bgr.hex", "r") != 0)
      load_input_image_from_file("lena_bgr.hex");
    else begin
      $display("ERROR: Could not find lena_bgr.hex in any location");
      $finish;
    end
    
    // Ensure all data is loaded - longer wait time
    #1000;
    
    // Now start the actual simulation
    $display("Image loaded successfully, now starting processing at %t ns", $time);
    
    // Start image conversion
    $display("Starting image conversion at %t ns", $time);
    io_convert_enable = 1;
    
    // Wait for conversion to complete
    wait(io_convert_done);
    $display("Conversion completed at %t ns", $time);
    
    // Keep convert_enable high for a bit
    #100;
    io_convert_enable = 0;
    
    // Wait for the system to stabilize
    #200;
    
    // Dump the output RAM contents to a file
    dump_output_ram_to_file();
    
    // End simulation
    $display("Simulation finished at %t ns", $time);
    #100;
    $finish;
  end
  
  // Task to load the input image from a hex file
  task load_input_image_from_file(input string filename);
    begin
      $display("Loading input image from %s...", filename);
      
      input_file = $fopen(filename, "r");
      if (input_file == 0) begin
        $display("ERROR: Could not open %s for reading", filename);
        return;
      end
      
      // Read each pixel from the file and write to InputROM
      i = 0;
      while (i < IMAGE_SIZE) begin
        if ($fscanf(input_file, "%h", pixel_data) != 1) begin
          $display("WARNING: End of file reached after reading %0d pixels", i);
          i = IMAGE_SIZE; // Exit the loop instead of using break
        end
        else begin
          // Write the pixel to InputROM
          io_inputrom_write_addr = i;
          io_inputrom_write_data = pixel_data;
          io_inputrom_write_enable = 1;
          #10; // Wait one clock cycle
          
          // Display progress every 10000 pixels
          if (i % 10000 == 0)
            $display("Loaded %0d pixels...", i);
            
          i = i + 1;
        end
      end
      
      // Make sure the last write completes
      #10;
      
      // Disable write after loading
      io_inputrom_write_enable = 0;
      
      $fclose(input_file);
      $display("Input image loaded successfully (%0d pixels)", i);
    end
  endtask
  
  // Task to dump the OutputRAM memory contents to a file
  // Uses the exposed read interface
  task dump_output_ram_to_file;
    begin
      dump_file = $fopen("output_gray.hex", "w");
      if (dump_file == 0) begin
        $display("ERROR: Could not open output_gray.hex for writing");
        return;
      end
      
      $display("Dumping OutputRAM contents to output_gray.hex...");
      
      // Read each memory location through the RAM read interface
      for (i = 0; i < IMAGE_SIZE; i = i + 1) begin
        io_readram_addr = i;
        #10; // Allow one clock cycle for data to be read
        $fdisplay(dump_file, "%02h", io_readram_data);
      end
      
      $fclose(dump_file);
      $display("Memory dump completed successfully");
    end
  endtask

endmodule
