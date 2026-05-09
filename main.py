"""
主程序入口
整合所有模块，完成图片到Word文档的转换流程
"""

import os
import sys
import argparse
from a4_detector import detect_a4_paper, save_corrected_image
from baidu_ocr import BaiduOCR
from red_image_extractor import extract_red_images, create_red_mask, visualize_red_regions
from red_image_extractor_precise import extract_red_images_precise, create_enhanced_mask, visualize_precise_regions
from word_generator import WordGenerator
from config import DIRECTORIES


def ensure_directories():
    """确保所需目录存在"""
    for dir_name in DIRECTORIES.values():
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
            print(f"创建目录：{dir_name}")


def convert_image_to_word(input_path, output_path=None, skip_a4_detection=False, use_precise_extraction=True):
    """
    将图片转换为Word文档的主流程
    
    Args:
        input_path: 输入图片路径
        output_path: 输出Word文档路径（可选）
        skip_a4_detection: 是否跳过A4检测
        use_precise_extraction: 是否使用精准抠图
        
    Returns:
        success: 是否成功
    """
    print("=" * 60)
    print("图片转Word文档转换器")
    print("=" * 60)
    
    # 确保目录存在
    ensure_directories()
    
    # 检查输入文件
    if not os.path.exists(input_path):
        print(f"错误：输入文件不存在 {input_path}")
        return False
    
    # 设置输出路径
    if output_path is None:
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        output_path = os.path.join(DIRECTORIES['output'], f"{base_name}.docx")
    
    # 步骤1：A4纸张检测与矫正
    print("\n【步骤1】A4纸张检测与矫正...")
    corrected_image_path = os.path.join(DIRECTORIES['temp'], "corrected.jpg")
    
    if skip_a4_detection:
        print("跳过A4检测，使用原图")
        corrected_image_path = input_path
        success = True
    else:
        corrected_image, success = detect_a4_paper(input_path)
        
        if success and corrected_image is not None:
            save_corrected_image(corrected_image, corrected_image_path)
        else:
            print("警告：A4检测失败，使用原图继续处理")
            corrected_image_path = input_path
    
    # 步骤2：提取红色图片（使用精准抠图）
    if use_precise_extraction:
        print("\n【步骤2】提取红色图片（精准模式）...")
        red_images = extract_red_images_precise(corrected_image_path, DIRECTORIES['temp'], use_edge_refinement=True)
        create_enhanced_mask(corrected_image_path)
        if red_images:
            visualize_precise_regions(corrected_image_path, red_images)
    else:
        print("\n【步骤2】提取红色图片（普通模式）...")
        red_images = extract_red_images(corrected_image_path, DIRECTORIES['temp'])
        create_red_mask(corrected_image_path)
        if red_images:
            visualize_red_regions(corrected_image_path, red_images)
    
    # 步骤3：OCR文字识别
    print("\n【步骤3】OCR文字识别...")
    ocr_client = BaiduOCR()
    text_data = ocr_client.recognize_and_parse(corrected_image_path)
    
    if not text_data:
        print("错误：OCR识别失败，请检查API配置和网络连接")
        return False
    
    print(f"成功识别 {len(text_data)} 个文字区域")
    
    # 步骤4：生成Word文档
    print("\n【步骤4】生成Word文档...")
    generator = WordGenerator()
    
    if red_images:
        # 包含红色图片的完整版本
        success = generator.generate_document(text_data, red_images, output_path)
    else:
        # 仅文本的简化版本
        print("未检测到红色图片，生成简化版文档")
        success = generator.generate_simple_document(text_data, output_path)
    
    if success:
        print("\n" + "=" * 60)
        print("✅ 转换完成！")
        print(f"📄 Word文档：{output_path}")
        print(f"📊 识别文字：{len(text_data)} 个区域")
        print(f"🖼️  提取图片：{len(red_images)} 个红色区域")
        print("=" * 60)
        print("\n提示：请在Word中手动微调个别元素位置以获得最佳效果")
        return True
    else:
        print("\n❌ 转换失败")
        return False


def batch_convert(input_dir, output_dir=None):
    """
    批量转换目录下的所有图片
    
    Args:
        input_dir: 输入目录
        output_dir: 输出目录（可选）
    """
    if output_dir is None:
        output_dir = DIRECTORIES['output']
    
    # 获取所有图片文件
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
    image_files = [
        f for f in os.listdir(input_dir)
        if os.path.splitext(f)[1].lower() in image_extensions
    ]
    
    if not image_files:
        print(f"目录 {input_dir} 中没有找到图片文件")
        return
    
    print(f"找到 {len(image_files)} 个图片文件")
    print("=" * 60)
    
    success_count = 0
    fail_count = 0
    
    for i, image_file in enumerate(image_files, 1):
        print(f"\n[{i}/{len(image_files)}] 处理：{image_file}")
        
        input_path = os.path.join(input_dir, image_file)
        base_name = os.path.splitext(image_file)[0]
        output_path = os.path.join(output_dir, f"{base_name}.docx")
        
        if convert_image_to_word(input_path, output_path):
            success_count += 1
        else:
            fail_count += 1
    
    print("\n" + "=" * 60)
    print(f"批量转换完成！")
    print(f"✅ 成功：{success_count} 个")
    print(f"❌ 失败：{fail_count} 个")
    print("=" * 60)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='图片转Word文档转换器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法：
  # 转换单个图片
  python main.py --input input/test.jpg
  
  # 指定输出路径
  python main.py --input input/test.jpg --output output/result.docx
  
  # 跳过A4检测
  python main.py --input input/test.jpg --skip-a4
  
  # 批量转换
  python main.py --batch input/
        """
    )
    
    parser.add_argument(
        '--input', '-i',
        type=str,
        help='输入图片路径'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        default=None,
        help='输出Word文档路径（可选）'
    )
    
    parser.add_argument(
        '--skip-a4',
        action='store_true',
        help='跳过A4纸张检测'
    )
    
    parser.add_argument(
        '--batch', '-b',
        type=str,
        default=None,
        help='批量转换目录'
    )
    
    parser.add_argument(
        '--precise', '-p',
        action='store_true',
        help='使用精准抠图模式（带透明背景）'
    )
    
    args = parser.parse_args()
    
    # 批量转换模式
    if args.batch:
        batch_convert(args.batch)
        return
    
    # 单文件转换模式
    if not args.input:
        parser.print_help()
        return
    
    convert_image_to_word(args.input, args.output, args.skip_a4, args.precise)


if __name__ == "__main__":
    main()
