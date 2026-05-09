"""
增强版红色图片提取模块
使用多种技术实现精准抠图：
1. HSV颜色分割
2. 边缘检测优化
3. 形态学精细处理
4. 轮廓平滑
"""

import cv2
import numpy as np
import os
from config import RED_EXTRACTION


def extract_red_images_precise(image_path, output_dir='temp', use_edge_refinement=True):
    """
    精准提取红色区域（增强版）
    
    Args:
        image_path: 输入图片路径
        output_dir: 输出目录
        use_edge_refinement: 是否使用边缘优化
        
    Returns:
        red_images: 提取的红色图片列表，每个元素为(图片数据, 位置信息)
    """
    # 读取图片
    img = cv2.imread(image_path)
    if img is None:
        print(f"错误：无法读取图片 {image_path}")
        return []
    
    original_height, original_width = img.shape[:2]
    
    # 步骤1：HSV颜色空间分割
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    lower_red_1 = np.array(RED_EXTRACTION['lower_red_1'])
    upper_red_1 = np.array(RED_EXTRACTION['upper_red_1'])
    lower_red_2 = np.array(RED_EXTRACTION['lower_red_2'])
    upper_red_2 = np.array(RED_EXTRACTION['upper_red_2'])
    
    mask1 = cv2.inRange(hsv, lower_red_1, upper_red_1)
    mask2 = cv2.inRange(hsv, lower_red_2, upper_red_2)
    mask = cv2.add(mask1, mask2)
    
    # 步骤2：形态学优化
    kernel_size = RED_EXTRACTION['morph_kernel']
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    
    # 开运算去除小噪点
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    # 闭运算填充空洞
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    # 步骤3：边缘优化（可选）
    if use_edge_refinement:
        mask = refine_edges(mask, img)
    
    # 步骤4：查找轮廓
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
        
        # 轮廓近似和平滑
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        
        # 获取边界框
        x, y, w, h = cv2.boundingRect(approx)
        
        # 添加自适应边距（根据区域大小）
        padding = max(3, min(10, int(min(w, h) * 0.05)))
        x1 = max(0, x - padding)
        y1 = max(0, y - padding)
        x2 = min(original_width, x + w + padding)
        y2 = min(original_height, y + h + padding)
        
        # 裁剪图片
        red_region = img[y1:y2, x1:x2]
        
        # 如果区域太小，跳过
        if red_region.shape[0] < 10 or red_region.shape[1] < 10:
            continue
        
        # 创建透明背景的PNG（精准抠图）
        png_output_path = os.path.join(output_dir, f"red_image_precise_{i}.png")
        save_with_transparency(red_region, mask[y1:y2, x1:x2], png_output_path)
        
        # 也保存普通版本
        jpg_output_path = os.path.join(output_dir, f"red_image_{i}.png")
        cv2.imwrite(jpg_output_path, red_region)
        
        # 记录位置信息
        position = {
            'x': x,
            'y': y,
            'width': w,
            'height': h,
            'output_path': png_output_path,  # 使用PNG版本（带透明背景）
            'area': area
        }
        
        red_images.append((red_region, position))
        print(f"精准提取红色图片 {i+1}：位置({x}, {y})，尺寸{w}x{h}，面积{int(area)}")
    
    print(f"共精准提取 {len(red_images)} 个红色区域")
    
    return red_images


def refine_edges(mask, original_img):
    """
    优化边缘，使抠图更精准
    
    Args:
        mask: 二值掩码图
        original_img: 原始图片
        
    Returns:
        refined_mask: 优化后的掩码图
    """
    # 使用Canny边缘检测找到真实边缘
    gray = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    
    # 将边缘信息与颜色掩码结合
    refined_mask = cv2.bitwise_and(mask, mask, mask=edges)
    
    # 膨胀边缘以覆盖完整区域
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    refined_mask = cv2.dilate(refined_mask, kernel, iterations=2)
    
    # 再次与原始掩码合并
    refined_mask = cv2.bitwise_or(mask, refined_mask)
    
    # 最后的形态学清理
    refined_mask = cv2.morphologyEx(refined_mask, cv2.MORPH_CLOSE, kernel)
    
    return refined_mask


def save_with_transparency(bgr_image, mask, output_path):
    """
    保存带透明背景的PNG图片（精准抠图）
    
    Args:
        bgr_image: BGR格式图片
        mask: 二值掩码图
        output_path: 输出路径
    """
    # 确保mask是单通道
    if len(mask.shape) == 3:
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    
    # 创建4通道图片（BGRA）
    bgra = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2BGRA)
    
    # 将mask作为alpha通道
    bgra[:, :, 3] = mask
    
    # 保存PNG（支持透明）
    cv2.imwrite(output_path, bgra)


def create_enhanced_mask(image_path, output_path='temp/red_mask_enhanced.png'):
    """
    创建增强的红色区域掩码图（用于调试）
    
    Args:
        image_path: 输入图片路径
        output_path: 输出掩码图路径
    """
    img = cv2.imread(image_path)
    if img is None:
        return False
    
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    lower_red_1 = np.array(RED_EXTRACTION['lower_red_1'])
    upper_red_1 = np.array(RED_EXTRACTION['upper_red_1'])
    lower_red_2 = np.array(RED_EXTRACTION['lower_red_2'])
    upper_red_2 = np.array(RED_EXTRACTION['upper_red_2'])
    
    mask1 = cv2.inRange(hsv, lower_red_1, upper_red_1)
    mask2 = cv2.inRange(hsv, lower_red_2, upper_red_2)
    mask = cv2.add(mask1, mask2)
    
    # 应用边缘优化
    refined_mask = refine_edges(mask, img)
    
    # 保存
    cv2.imwrite(output_path, refined_mask)
    print(f"增强版红色掩码图已保存到：{output_path}")
    
    return True


def visualize_precise_regions(image_path, red_images, output_path='temp/red_visualization_precise.png'):
    """
    可视化精准提取的红色区域
    
    Args:
        image_path: 输入图片路径
        red_images: 提取的红色图片列表
        output_path: 输出可视化图片路径
    """
    img = cv2.imread(image_path)
    if img is None:
        return False
    
    for _, position in red_images:
        x = position['x']
        y = position['y']
        w = position['width']
        h = position['height']
        area = position.get('area', 0)
        
        # 绘制矩形框（绿色）
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # 添加标签（包含面积信息）
        label = f'Red ({int(area)}px)'
        cv2.putText(img, label, (x, y - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    cv2.imwrite(output_path, img)
    print(f"精准红色区域可视化图已保存到：{output_path}")
    
    return True


if __name__ == "__main__":
    # 测试代码
    import sys
    
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        
        print("开始精准提取红色区域...")
        red_images = extract_red_images_precise(image_path, use_edge_refinement=True)
        
        # 创建增强掩码图
        create_enhanced_mask(image_path)
        
        # 可视化
        if red_images:
            visualize_precise_regions(image_path, red_images)
        
        print(f"\n精准提取完成！共找到 {len(red_images)} 个红色区域")
        print("提示：PNG文件带有透明背景，可实现精准抠图")
    else:
        print("用法：python red_image_extractor_precise.py <image_path>")
