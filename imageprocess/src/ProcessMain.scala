package imageprocess

import chisel3._
import chisel3.util._

// 顶层模块，连接各子模块
class ProcessMain extends Module {
  val io = IO(new Bundle {
    val convert_enable = Input(Bool())
    val convert_done = Output(Bool())

    // ram 读出接口，用于在测试时读取结果
    val readram_addr = Input(UInt(18.W))
    val readram_data = Output(UInt(8.W))
    
    // Add input ROM write interface
    val inputrom_write_addr = Input(UInt(18.W))
    val inputrom_write_data = Input(UInt(24.W))
    val inputrom_write_enable = Input(Bool())
  })
  
  // 实例化子模块
  val inputROM = Module(new InputROM())
  val outputRAM = Module(new OutputRAM())
  val imageProcessor = Module(new ImageProcessor())
  
  // 连接各模块
  imageProcessor.io.convert_enable := io.convert_enable
  io.convert_done := imageProcessor.io.convert_done
  
  // 连接输入ROM
  inputROM.io.addr := imageProcessor.io.input_rom_addr
  imageProcessor.io.input_rom_data := inputROM.io.data
  
  // Connect input ROM write interface
  inputROM.io.write_addr := io.inputrom_write_addr
  inputROM.io.write_data := io.inputrom_write_data
  inputROM.io.write_enable := io.inputrom_write_enable
  
  // 连接输出RAM
  outputRAM.io.write_addr := imageProcessor.io.output_ram_addr
  outputRAM.io.write_data := imageProcessor.io.output_ram_data
  outputRAM.io.write_enable := imageProcessor.io.output_ram_write_enable
  
  // 读取接口不使用
  io.readram_data := outputRAM.io.read_data
  outputRAM.io.read_addr := io.readram_addr
}
