"""
Word文档生成模块
使用python-docx库生成Word文档，保留版面布局和样式
"""

from docx import Document
from docx.shared import Pt, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from config import WORD_GENERATION


class WordGenerator:
    """Word文档生成器"""
    
    def __init__(self):
        self.doc = Document()
        
        # 设置页面边距
        sections = self.doc.sections
        for section in sections:
            section.top_margin = Cm(WORD_GENERATION['margin_top'] / 28.35)  # 磅转厘米
            section.bottom_margin = Cm(WORD_GENERATION['margin_bottom'] / 28.35)
            section.left_margin = Cm(WORD_GENERATION['margin_left'] / 28.35)
            section.right_margin = Cm(WORD_GENERATION['margin_right'] / 28.35)
    
    def add_text_with_position(self, text_data):
        """
        添加带位置信息的文本
        
        Args:
            text_data: 文本数据列表，每个元素包含text, left, top, width, height, font_size
        """
        # 按top坐标排序，从上到下添加
        sorted_data = sorted(text_data, key=lambda x: x.get('top', 0))
        
        current_y = 0
        
        for item in sorted_data:
            text = item.get('text', '')
            if not text:
                continue
            
            # 获取字体大小
            font_size = item.get('font_size', WORD_GENERATION['default_font_size'])
            
            # 创建段落
            paragraph = self.doc.add_paragraph()
            
            # 设置段落格式
            paragraph_format = paragraph.paragraph_format
            
            # 根据left位置设置对齐方式
            left = item.get('left', 0)
            if left < 100:
                paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
            elif left > 400:
                paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            else:
                paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
            
            # 添加文本并设置格式
            run = paragraph.add_run(text)
            font = run.font
            font.name = WORD_GENERATION['default_font']
            font.size = Pt(font_size)
            
            # 设置中文字体
            run._element.rPr.rFonts.set(qn('w:eastAsia'), WORD_GENERATION['default_font'])
            
            # 添加适当的段后间距
            paragraph_format.space_after = Pt(font_size * 0.3)
        
        print(f"已添加 {len(sorted_data)} 个文本块")
    
    def add_image(self, image_path, width_cm=None, height_cm=None, position=None):
        """
        添加图片到文档
        
        Args:
            image_path: 图片路径
            width_cm: 宽度（厘米）
            height_cm: 高度（厘米）
            position: 位置信息字典 {'x', 'y', 'width', 'height'}
        """
        try:
            # 如果没有指定尺寸，使用默认值
            if width_cm is None and height_cm is None:
                if position:
                    # 根据位置信息估算尺寸
                    width_cm = position['width'] / 100  # 像素转厘米（粗略估算）
                    height_cm = position['height'] / 100
                else:
                    width_cm = 5
                    height_cm = 5
            
            # 添加图片
            if width_cm and height_cm:
                self.doc.add_picture(
                    image_path, 
                    width=Cm(width_cm), 
                    height=Cm(height_cm)
                )
            else:
                self.doc.add_picture(image_path)
            
            print(f"已添加图片：{image_path}")
            return True
        except Exception as e:
            print(f"添加图片失败 {image_path}：{str(e)}")
            return False
    
    def add_floating_image(self, image_path, position=None):
        """
        添加浮动图片（可移动）
        注意：python-docx对浮动图片支持有限，这里使用嵌入式图片
        用户可以在Word中手动设置为浮动
        
        Args:
            image_path: 图片路径
            position: 位置信息
        """
        # 添加段落作为占位
        paragraph = self.doc.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # 添加说明文字
        run = paragraph.add_run("[红色图片 - 请在Word中设置为浮动对象]")
        run.font.size = Pt(9)
        run.font.color.rgb = None  # 灰色
        
        # 添加图片
        self.add_image(image_path, width_cm=4, height_cm=4, position=position)
        
        # 添加空行
        self.doc.add_paragraph()
    
    def generate_document(self, text_data, red_images, output_path):
        """
        生成完整的Word文档
        
        Args:
            text_data: 文本数据列表
            red_images: 红色图片列表 [(image_data, position), ...]
            output_path: 输出文件路径
        """
        print("开始生成Word文档...")
        
        # 添加标题
        title = self.doc.add_heading('文档转换结果', 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # 添加说明
        intro = self.doc.add_paragraph()
        intro_run = intro.add_run(
            "本文档由图片自动生成，文字和图片位置已尽量还原。\n"
            "红色图片已提取为独立对象，可在Word中拖动调整位置。"
        )
        intro_run.font.size = Pt(10)
        intro_run.font.color.rgb = None  # 灰色
        
        self.doc.add_paragraph()  # 空行
        
        # 添加文本内容
        if text_data:
            self.add_text_with_position(text_data)
        
        # 添加红色图片
        if red_images:
            self.doc.add_heading('提取的红色图片', level=1)
            
            for i, (img_data, position) in enumerate(red_images, 1):
                self.doc.add_paragraph(f'红色图片 {i}:')
                self.add_floating_image(position['output_path'], position)
        
        # 保存文档
        try:
            self.doc.save(output_path)
            print(f"Word文档已保存到：{output_path}")
            return True
        except Exception as e:
            print(f"保存文档失败：{str(e)}")
            return False
    
    def generate_simple_document(self, text_data, output_path):
        """
        生成简化版Word文档（仅文本）
        
        Args:
            text_data: 文本数据列表
            output_path: 输出文件路径
        """
        print("开始生成简化版Word文档...")
        
        # 按位置排序
        sorted_data = sorted(text_data, key=lambda x: x.get('top', 0))
        
        # 添加每个文本块
        for item in sorted_data:
            text = item.get('text', '')
            if not text:
                continue
            
            paragraph = self.doc.add_paragraph(text)
            
            # 设置字体
            for run in paragraph.runs:
                font = run.font
                font.name = WORD_GENERATION['default_font']
                font.size = Pt(item.get('font_size', WORD_GENERATION['default_font_size']))
                run._element.rPr.rFonts.set(qn('w:eastAsia'), WORD_GENERATION['default_font'])
        
        # 保存文档
        try:
            self.doc.save(output_path)
            print(f"简化版Word文档已保存到：{output_path}")
            return True
        except Exception as e:
            print(f"保存文档失败：{str(e)}")
            return False


if __name__ == "__main__":
    # 测试代码
    print("Word生成器模块测试")
    print("请通过main.py运行完整流程")
