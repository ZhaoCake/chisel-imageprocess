# Imageprocess in Chisel

玩具性质的chisel图像处理库。

## 6/5

草，bind语法烦死了，sv2v也不支持bind语法，最后还是只能用verilator吗，还真是有够烦人的呢。

错误的。烦人的不是verilator，而是iverilog这个老土的解释型仿真器。

下次换成Verilator吧，iverilog烦死了，尤其是还要dump memory来看。