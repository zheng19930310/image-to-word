"""
红色图片提取模块
使用HSV颜色空间分割提取红色区域
"""

import cv2
import numpy as np
import os
from config import RED_EXTRACTION


def extract_red_images(image_path, output_dir='temp'):
    """
    从图片中提取红色区域
    
    Args:
        image_path: 输入图片路径
        output_dir: 输出目录
        
    Returns:
        red_images: 提取的红色图片列表，每个元素为(图片数据, 位置信息)
    """
    # 读取图片
    img = cv2.imread(image_path)
    if img is None:
        print(f"错误：无法读取图片 {image_path}")
        return []
    
    # 转换为HSV颜色空间
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # 定义红色的HSV范围（红色在HSV中有两个区间）
    lower_red_1 = np.array(RED_EXTRACTION['lower_red_1'])
    upper_red_1 = np.array(RED_EXTRACTION['upper_red_1'])
    lower_red_2 = np.array(RED_EXTRACTION['lower_red_2'])
    upper_red_2 = np.array(RED_EXTRACTION['upper_red_2'])
    
    # 创建红色掩码
    mask1 = cv2.inRange(hsv, lower_red_1, upper_red_1)
    mask2 = cv2.inRange(hsv, lower_red_2, upper_red_2)
    mask = cv2.add(mask1, mask2)
    
    # 形态学操作，去除噪点
    kernel_size = RED_EXTRACTION['morph_kernel']
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    
    # 开运算：先腐蚀后膨胀，去除小噪点
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    # 闭运算：先膨胀后腐蚀，填充小空洞
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    # 查找轮廓
    contours, hierarchy = cv2.findContours(
        mask, 
        cv2.RETR_EXTERNAL, 
        cv2.CHAIN_APPROX_SIMPLE
    )
    
    red_images = []
    min_area = RED_EXTRACTION['min_area']
    
    for i, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        
        # 过滤太小的区域
        if area < min_area:
            continue
        
        # 获取边界框
        x, y, w, h = cv2.boundingRect(contour)
        
        # 提取红色区域（带一些边距）
        padding = 5
        x1 = max(0, x - padding)
        y1 = max(0, y - padding)
        x2 = min(img.shape[1], x + w + padding)
        y2 = min(img.shape[0], y + h + padding)
        
        # 裁剪图片
        red_region = img[y1:y2, x1:x2]
        
        # 如果区域太小，跳过
        if red_region.shape[0] < 10 or red_region.shape[1] < 10:
            continue
        
        # 保存提取的图片
        output_path = os.path.join(output_dir, f"red_image_{i}.png")
        cv2.imwrite(output_path, red_region)
        
        # 记录位置信息
        position = {
            'x': x,
            'y': y,
            'width': w,
            'height': h,
            'output_path': output_path
        }
        
        red_images.append((red_region, position))
        print(f"提取红色图片 {i+1}：位置({x}, {y})，尺寸{w}x{h}")
    
    print(f"共提取 {len(red_images)} 个红色区域")
    
    return red_images


def create_red_mask(image_path, output_path='temp/red_mask.png'):
    """
    创建红色区域的掩码图（用于调试）
    
    Args:
        image_path: 输入图片路径
        output_path: 输出掩码图路径
    """
    # 读取图片
    img = cv2.imread(image_path)
    if img is None:
        return False
    
    # 转换为HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # 创建红色掩码
    lower_red_1 = np.array(RED_EXTRACTION['lower_red_1'])
    upper_red_1 = np.array(RED_EXTRACTION['upper_red_1'])
    lower_red_2 = np.array(RED_EXTRACTION['lower_red_2'])
    upper_red_2 = np.array(RED_EXTRACTION['upper_red_2'])
    
    mask1 = cv2.inRange(hsv, lower_red_1, upper_red_1)
    mask2 = cv2.inRange(hsv, lower_red_2, upper_red_2)
    mask = cv2.add(mask1, mask2)
    
    # 保存掩码图
    cv2.imwrite(output_path, mask)
    print(f"红色掩码图已保存到：{output_path}")
    
    return True


def visualize_red_regions(image_path, red_images, output_path='temp/red_visualization.png'):
    """
    可视化红色区域（在原图上绘制框）
    
    Args:
        image_path: 输入图片路径
        red_images: 提取的红色图片列表
        output_path: 输出可视化图片路径
    """
    # 读取原图
    img = cv2.imread(image_path)
    if img is None:
        return False
    
    # 在原图上绘制红色框
    for _, position in red_images:
        x = position['x']
        y = position['y']
        w = position['width']
        h = position['height']
        
        # 绘制矩形框
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # 添加标签
        cv2.putText(img, 'Red', (x, y - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    # 保存可视化图片
    cv2.imwrite(output_path, img)
    print(f"红色区域可视化图已保存到：{output_path}")
    
    return True


if __name__ == "__main__":
    # 测试代码
    import sys
    
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        
        # 提取红色图片
        red_images = extract_red_images(image_path)
        
        # 创建掩码图
        create_red_mask(image_path)
        
        # 可视化
        if red_images:
            visualize_red_regions(image_path, red_images)
        
        print(f"\n提取完成！共找到 {len(red_images)} 个红色区域")
    else:
        print("用法：python red_image_extractor.py <image_path>")
