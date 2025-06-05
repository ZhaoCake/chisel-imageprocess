package imageprocess

import chisel3._
import chisel3.util._

// 初始化内存以及存放结果的部分，作为试验输入输出方式

class InputROM extends Module {
  val io = IO(new Bundle {
    val addr = Input(UInt(18.W))
    val data = Output(UInt(24.W))
    
    // Add write interface
    val write_addr = Input(UInt(18.W))
    val write_data = Input(UInt(24.W))
    val write_enable = Input(Bool())
  })
  
  val rom = Mem(512 * 512, UInt(24.W))
  
  when(io.write_enable) {
    rom(io.write_addr) := io.write_data
  }
  
  io.data := rom(io.addr)
}

class OutputRAM extends Module {
  val io = IO(new Bundle {
    val write_addr = Input(UInt(18.W))
    val write_data = Input(UInt(8.W))
    val write_enable = Input(Bool())
    val read_addr = Input(UInt(18.W))
    val read_data = Output(UInt(8.W))
  })
  
  val ram = Mem(512 * 512, UInt(8.W))
  
  when(io.write_enable) {
    ram(io.write_addr) := io.write_data
  }
  
  io.read_data := ram(io.read_addr)
}