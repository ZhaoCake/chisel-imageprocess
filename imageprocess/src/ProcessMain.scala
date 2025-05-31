package imageprocess

import chisel3._
import chisel3.util._

// 顶层模块，连接各子模块
class ProcessMain extends Module {
  val io = IO(new Bundle {
    val convert_enable = Input(Bool())
    val convert_done = Output(Bool())
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
  
  // 连接输出RAM
  outputRAM.io.write_addr := imageProcessor.io.output_ram_addr
  outputRAM.io.write_data := imageProcessor.io.output_ram_data
  outputRAM.io.write_enable := imageProcessor.io.output_ram_write_enable
  
  // 读取接口不使用
  outputRAM.io.read_addr := 0.U
}
