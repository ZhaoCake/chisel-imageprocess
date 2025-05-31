#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
十六进制图像数据可视化脚本
用于实时查看通过BSV处理后的图像数据
"""

import cv2
import numpy as np
import argparse
import os
import sys
import time

def visualize_hex_data(hex_file_path, width=None, height=None, mode="bgr", auto_refresh=False, refresh_rate=1.0):
    """
    实时可视化十六进制图像数据
    
    Args:
        hex_file_path: 十六进制图像数据文件路径
        width: 图像宽度，如果为None则尝试从文件头读取
        height: 图像高度，如果为None则尝试从文件头读取
        mode: 'bgr'或'gray'，数据格式
        auto_refresh: 是否自动刷新显示
        refresh_rate: 刷新率(Hz)
    """
    window_name = f"Hex Viewer: {os.path.basename(hex_file_path)}"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    
    last_modified = 0
    
    while True:
        # 检查文件是否更新
        try:
            current_modified = os.path.getmtime(hex_file_path)
        except FileNotFoundError:
            print(f"错误: 文件 {hex_file_path} 不存在")
            return False
        
        # 如果文件更新或者首次读取
        if current_modified != last_modified or last_modified == 0:
            last_modified = current_modified
            
            # 读取十六进制文件
            with open(hex_file_path, 'r') as f:
                lines = f.readlines()
            
            # 解析文件头信息
            file_width = width
            file_height = height
            format_type = ""
            
            data_start = 0
            for i, line in enumerate(lines):
                line = line.strip()
                if line.startswith("// Size:"):
                    try:
                        size_info = line.split(":")[1].strip().split("x")
                        file_width = int(size_info[0])
                        file_height = int(size_info[1])
                    except:
                        print("警告: 无法解析文件头中的尺寸信息")
                elif line.startswith("// Format:"):
                    format_type = line.split(":")[1].strip()
                
                if line == "":
                    data_start = i + 1
                    break
            
            # 如果没有指定尺寸，使用文件头中的尺寸
            if width is None:
                width = file_width
            if height is None:
                height = file_height
            
            # 如果仍然没有尺寸信息，尝试推断
            if width is None or height is None:
                pixel_count = len([l for l in lines if not l.startswith("//") and l.strip()])
                if mode == "bgr":
                    # 假设是正方形图像
                    w = h = int(np.sqrt(pixel_count))
                elif mode == "gray":
                    w = h = int(np.sqrt(pixel_count))
                
                width = width or w
                height = height or h
                print(f"警告: 未找到尺寸信息，假设为 {width}x{height}")
            
            # 创建图像
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
                        # print(f"警告: 跳过无效的十六进制值 '{line}'")
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
                        # print(f"警告: 跳过无效的十六进制值 '{line}'")
                        continue
            
            # 显示图像
            cv2.imshow(window_name, image)
            print(f"已更新显示 {os.path.basename(hex_file_path)}, 尺寸: {width}x{height}")
        
        key = cv2.waitKey(1)
        if key == 27 or key == ord('q'):  # ESC 或 q 退出
            break
        
        # 如果不自动刷新，则等待空格键刷新
        if not auto_refresh:
            print("按空格键刷新图像，按ESC或q退出")
            while True:
                key = cv2.waitKey(0)
                if key == 32:  # 空格键
                    break
                if key == 27 or key == ord('q'):  # ESC 或 q 退出
                    cv2.destroyAllWindows()
                    return
        else:
            time.sleep(1.0 / refresh_rate)
    
    cv2.destroyAllWindows()
    return True

def main():
    parser = argparse.ArgumentParser(description="十六进制图像数据可视化工具")
    
    # 输入文件
    parser.add_argument("input", help="输入十六进制文件路径")
    
    # 图像尺寸
    parser.add_argument("--width", type=int, help="图像宽度 (默认从文件头读取)")
    parser.add_argument("--height", type=int, help="图像高度 (默认从文件头读取)")
    
    # 模式选择
    parser.add_argument("--mode", choices=["bgr", "gray"], default="bgr",
                        help="数据格式: bgr (彩色三通道) 或 gray (灰度)")
    
    # 自动刷新
    parser.add_argument("--auto-refresh", action="store_true", help="自动刷新显示")
    parser.add_argument("--refresh-rate", type=float, default=1.0, help="自动刷新率 (Hz)")
    
    args = parser.parse_args()
    
    visualize_hex_data(args.input, args.width, args.height, 
                    args.mode, args.auto_refresh, args.refresh_rate)

if __name__ == "__main__":
    main()