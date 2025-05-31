## 图像转换为十六进制文件

```bash
# 将图像转为BGR三通道十六进制文件
python scripts/image_to_hex.py to-hex resources/lena.png output/lena_bgr.hex --mode bgr

# 将图像转为灰度图十六进制文件
python scripts/image_to_hex.py to-hex resources/lena.png output/lena_gray.hex --mode gray
```

## 十六进制文件转回图像

```bash
# 将BGR三通道十六进制文件转回图像
python scripts/image_to_hex.py from-hex output/lena_bgr.hex output/lena_restored.png --mode bgr

# 将灰度图十六进制文件转回图像
python scripts/image_to_hex.py from-hex output/lena_gray.hex output/lena_restored_gray.png --mode gray
```

## 实时可视化十六进制图像数据

```bash
# 可视化BGR三通道十六进制文件
python scripts/hex_visualizer.py output/lena_bgr.hex --mode bgr

# 可视化灰度图十六进制文件
python scripts/hex_visualizer.py output/lena_gray.hex --mode gray

# 启用自动刷新，每秒刷新2次
python scripts/hex_visualizer.py output/lena_bgr.hex --auto-refresh --refresh-rate 2.0
```

## TODO

- [ ] rgb565等更常用的格式