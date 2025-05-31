#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
图像处理脚本: 将图像转换为十六进制形式，以便BSV处理
支持BGR三通道和灰度图转换
"""

import cv2
import numpy as np
import argparse
import os
import sys

def image_to_hex_bgr(image_path, output_path):
    """
    读取图像并将BGR三通道分别转换为十六进制格式
    
    Args:
        image_path: 输入图像路径
        output_path: 输出十六进制文件路径
    """
    # 读取图像
    image = cv2.imread(image_path)
    if image is None:
        print(f"错误: 无法读取图像 {image_path}")
        return False
    
    height, width, channels = image.shape
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    # 打开输出文件
    with open(output_path, 'w') as f:
        # 写入文件头: 图像尺寸信息
        f.write(f"// Image: {os.path.basename(image_path)}\n")
        f.write(f"// Size: {width}x{height}\n")
        f.write(f"// Format: BGR (3 channels)\n\n")
        
        # 逐像素写入十六进制值
        for y in range(height):
            for x in range(width):
                b, g, r = image[y, x]
                # 将BGR值转为十六进制，格式: RRGGBB
                hex_value = f"{r:02X}{g:02X}{b:02X}"
                f.write(f"{hex_value}\n")
    
    print(f"已将BGR图像转换为十六进制格式并保存至 {output_path}")
    print(f"图像尺寸: {width}x{height}, 总像素: {width*height}")
    return True

def image_to_hex_gray(image_path, output_path):
    """
    读取图像并将灰度值转换为十六进制格式
    
    Args:
        image_path: 输入图像路径
        output_path: 输出十六进制文件路径
    """
    # 读取图像为灰度图
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        print(f"错误: 无法读取图像 {image_path}")
        return False
    
    height, width = image.shape
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    # 打开输出文件
    with open(output_path, 'w') as f:
        # 写入文件头: 图像尺寸信息
        f.write(f"// Image: {os.path.basename(image_path)}\n")
        f.write(f"// Size: {width}x{height}\n")
        f.write(f"// Format: Grayscale (1 channel)\n\n")
        
        # 逐像素写入十六进制值
        for y in range(height):
            for x in range(width):
                # 将灰度值转为十六进制
                hex_value = f"{image[y, x]:02X}"
                f.write(f"{hex_value}\n")
    
    print(f"已将灰度图像转换为十六进制格式并保存至 {output_path}")
    print(f"图像尺寸: {width}x{height}, 总像素: {width*height}")
    return True

def hex_to_image(hex_file_path, output_path, mode="bgr"):
    """
    从十六进制文件中读取数据并转换回图像
    
    Args:
        hex_file_path: 输入十六进制文件路径
        output_path: 输出图像路径
        mode: 'bgr'或'gray'，指定输入数据格式
    """
    # 读取十六进制文件
    with open(hex_file_path, 'r') as f:
        lines = f.readlines()
    
    # 解析文件头信息
    width = 0
    height = 0
    format_type = ""
    
    data_start = 0
    for i, line in enumerate(lines):
        line = line.strip()
        if line.startswith("// Size:"):
            try:
                size_info = line.split(":")[1].strip().split("x")
                width = int(size_info[0])
                height = int(size_info[1])
            except:
                print("错误: 无法解析文件头中的尺寸信息")
                return False
        elif line.startswith("// Format:"):
            format_type = line.split(":")[1].strip()
        
        if line == "":
            data_start = i + 1
            break
    
    if width == 0 or height == 0:
        # 如果文件头中没有尺寸信息，尝试推断
        pixel_count = len([l for l in lines if not l.startswith("//") and l.strip()])
        if mode == "bgr":
            # 假设是正方形图像
            width = height = int(np.sqrt(pixel_count))
        elif mode == "gray":
            width = height = int(np.sqrt(pixel_count))
        
        print(f"警告: 未找到尺寸信息，假设为 {width}x{height}")
    
    # 根据模式创建图像
    if mode == "bgr":
        image = np.zeros((height, width, 3), dtype=np.uint8)
        
        pixel_index = 0
        for line in lines[data_start:]:
            line = line.strip()
            if not line or line.startswith("//"):
                continue
                
            try:
                # 假设格式是RRGGBB
                r = int(line[0:2], 16)
                g = int(line[2:4], 16)
                b = int(line[4:6], 16)
                
                y = pixel_index // width
                x = pixel_index % width
                
                if y < height and x < width:
                    image[y, x] = [b, g, r]  # OpenCV使用BGR顺序
                
                pixel_index += 1
            except:
                print(f"警告: 跳过无效的十六进制值 '{line}'")
                continue
                
    elif mode == "gray":
        image = np.zeros((height, width), dtype=np.uint8)
        
        pixel_index = 0
        for line in lines[data_start:]:
            line = line.strip()
            if not line or line.startswith("//"):
                continue
                
            try:
                # 灰度值
                gray = int(line, 16)
                
                y = pixel_index // width
                x = pixel_index % width
                
                if y < height and x < width:
                    image[y, x] = gray
                
                pixel_index += 1
            except:
                print(f"警告: 跳过无效的十六进制值 '{line}'")
                continue
    
    # 保存图像
    cv2.imwrite(output_path, image)
    print(f"已将十六进制数据转换为图像并保存至 {output_path}")
    print(f"图像尺寸: {width}x{height}")
    
    return True

def main():
    parser = argparse.ArgumentParser(description="图像与十六进制格式转换工具")
    
    # 命令类型
    parser.add_argument("command", choices=["to-hex", "from-hex"], 
                        help="选择命令: to-hex (图像转十六进制) 或 from-hex (十六进制转图像)")
    
    # 输入和输出文件
    parser.add_argument("input", help="输入文件路径")
    parser.add_argument("output", help="输出文件路径")
    
    # 模式选择
    parser.add_argument("--mode", choices=["bgr", "gray"], default="bgr",
                        help="处理模式: bgr (彩色三通道) 或 gray (灰度)")
    
    args = parser.parse_args()
    
    if args.command == "to-hex":
        if args.mode == "bgr":
            image_to_hex_bgr(args.input, args.output)
        else:
            image_to_hex_gray(args.input, args.output)
    elif args.command == "from-hex":
        hex_to_image(args.input, args.output, args.mode)

if __name__ == "__main__":
    main()