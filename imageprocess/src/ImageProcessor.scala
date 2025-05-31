package imageprocess

import chisel3._
import chisel3.util._

// 针对单个像素的RGB到灰度转换模块
class RGBToGrayConverter extends Module {
  val io = IO(new Bundle {
    val bgr_data = Input(UInt(24.W))
    val gray_data = Output(UInt(8.W))
  })
  
  val b = io.bgr_data(7, 0)
  val g = io.bgr_data(15, 8)
  val r = io.bgr_data(23, 16)
  
  // Grayscale formula: 0.299*R + 0.587*G + 0.114*B
  // Using fixed-point arithmetic (multiply by 256 for precision)
  io.gray_data := ((r * 77.U) + (g * 150.U) + (b * 29.U)) >> 8.U
}

// 图像处理主要模块
class ImageProcessor extends Module {
  val io = IO(new Bundle {
    val convert_enable = Input(Bool())
    val convert_done = Output(Bool())
    
    // 输入ROM接口
    val input_rom_addr = Output(UInt(18.W))
    val input_rom_data = Input(UInt(24.W))
    
    // 输出RAM接口
    val output_ram_addr = Output(UInt(18.W))
    val output_ram_data = Output(UInt(8.W))
    val output_ram_write_enable = Output(Bool())
  })
  
  // 实例化RGB转灰度转换器
  val converter = Module(new RGBToGrayConverter)
  
  // 地址遍历控制状态机
  val s_idle :: s_convert :: s_done :: Nil = Enum(3)
  val state = RegInit(s_idle)
  
  // 地址遍历逻辑
  val addressTraversal = new AddressTraversalFSM()
  val current_addr = addressTraversal.generateAddress(
    enable = state === s_convert,
    reset = state === s_idle
  )
  
  // 输入数据寄存
  val input_data_reg = RegNext(io.input_rom_data)
  
  // 状态转换逻辑
  switch(state) {
    is(s_idle) {
      when(io.convert_enable) {
        state := s_convert
      }
    }
    
    is(s_convert) {
      when(addressTraversal.isComplete) {
        state := s_done
      }
    }
    
    is(s_done) {
      when(!io.convert_enable) {
        state := s_idle
      }
    }
  }
  
  // 连接转换器
  converter.io.bgr_data := input_data_reg
  
  // 控制输出
  io.input_rom_addr := current_addr
  io.output_ram_addr := current_addr
  io.output_ram_data := converter.io.gray_data
  io.output_ram_write_enable := state === s_convert
  io.convert_done := state === s_done
}

// 地址遍历功能模块
class AddressTraversalFSM {
  private val addr = RegInit(0.U(18.W))
  val isComplete = RegInit(false.B)
  
  def generateAddress(enable: Bool, reset: Bool): UInt = {
    when(reset) {
      addr := 0.U
      isComplete := false.B
    }.elsewhen(enable) {
      when(addr === (512*512-1).U) {
        isComplete := true.B
      }.otherwise {
        addr := addr + 1.U
      }
    }
    
    addr
  }
}
