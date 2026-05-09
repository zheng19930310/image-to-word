"""
A4纸张检测与透视矫正模块
使用OpenCV检测图片中的A4纸张并进行透视变换矫正
"""

import cv2
import numpy as np
from config import A4_DETECTION


def detect_a4_paper(image_path):
    """
    检测图片中的A4纸张并返回矫正后的图像
    
    Args:
        image_path: 输入图片路径
        
    Returns:
        corrected_image: 矫正后的A4图像
        success: 是否成功检测
    """
    # 读取图片
    img = cv2.imread(image_path)
    if img is None:
        print(f"错误：无法读取图片 {image_path}")
        return None, False
    
    original_height, original_width = img.shape[:2]
    
    # 转换为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 高斯模糊去噪
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Canny边缘检测
    edged = cv2.Canny(blurred, 75, 200)
    
    # 形态学操作，闭合小的间隙
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
    
    # 查找轮廓
    contours, hierarchy = cv2.findContours(
        closed.copy(), 
        cv2.RETR_LIST, 
        cv2.CHAIN_APPROX_SIMPLE
    )
    
    # 按面积排序，取最大的几个轮廓
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
    
    a4_contour = None
    
    for contour in contours:
        # 计算轮廓周长
        peri = cv2.arcLength(contour, True)
        
        # 轮廓近似
        approx = cv2.approxPolyDP(
            contour, 
            A4_DETECTION['approx_epsilon'] * peri, 
            True
        )
        
        # 检查是否是四边形
        if len(approx) == 4:
            area = cv2.contourArea(contour)
            
            # 检查面积是否在合理范围内
            if A4_DETECTION['min_area'] < area < A4_DETECTION['max_area']:
                a4_contour = approx
                break
    
    if a4_contour is None:
        print("警告：未检测到A4纸张，使用原图")
        return img, False
    
    # 对四个角点进行排序：左上、右上、右下、左下
    pts = order_points(a4_contour.reshape(4, 2))
    
    # 计算新的宽度和高度（A4比例约为1:1.414）
    width_a = np.linalg.norm(pts[0] - pts[1])
    width_b = np.linalg.norm(pts[2] - pts[3])
    max_width = max(int(width_a), int(width_b))
    
    height_a = np.linalg.norm(pts[0] - pts[3])
    height_b = np.linalg.norm(pts[1] - pts[2])
    max_height = max(int(height_a), int(height_b))
    
    # 保持A4比例
    if max_width > max_height:
        max_height = int(max_width * 1.414)
    else:
        max_width = int(max_height / 1.414)
    
    # 目标点
    dst_pts = np.array([
        [0, 0],
        [max_width - 1, 0],
        [max_width - 1, max_height - 1],
        [0, max_height - 1]
    ], dtype="float32")
    
    # 计算透视变换矩阵
    M = cv2.getPerspectiveTransform(pts, dst_pts)
    
    # 应用透视变换
    corrected = cv2.warpPerspective(img, M, (max_width, max_height))
    
    print(f"A4纸张检测成功！矫正后尺寸：{max_width}x{max_height}")
    
    return corrected, True


def order_points(pts):
    """
    对四个角点进行排序：左上、右上、右下、左下
    
    Args:
        pts: 四个点的坐标数组
        
    Returns:
        ordered: 排序后的四个点
    """
    # 初始化排序后的点数组
    ordered = np.zeros((4, 2), dtype="float32")
    
    # 按y坐标排序，最小的为顶部点，最大的为底部点
    s = pts.sum(axis=1)
    ordered[0] = pts[np.argmin(s)]  # 左上
    ordered[2] = pts[np.argmax(s)]  # 右下
    
    # 计算差值，最小的为右上，最大的为左下
    diff = np.diff(pts, axis=1)
    ordered[1] = pts[np.argmin(diff)]  # 右上
    ordered[3] = pts[np.argmax(diff)]  # 左下
    
    return ordered


def save_corrected_image(image, output_path):
    """
    保存矫正后的图像
    
    Args:
        image: 矫正后的图像
        output_path: 输出路径
    """
    cv2.imwrite(output_path, image)
    print(f"矫正后的图像已保存到：{output_path}")


if __name__ == "__main__":
    # 测试代码
    import sys
    
    if len(sys.argv) > 1:
        input_path = sys.argv[1]
        output_path = sys.argv[2] if len(sys.argv) > 2 else "temp/corrected.jpg"
        
        corrected, success = detect_a4_paper(input_path)
        
        if success and corrected is not None:
            save_corrected_image(corrected, output_path)
        else:
            print("A4纸张检测失败")
    else:
        print("用法：python a4_detector.py <input_image> [output_image]")
