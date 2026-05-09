"""
百度OCR API调用模块
使用百度AI开放平台的OCR服务进行文字识别和版面分析
"""

import base64
import requests
import json
from config import BAIDU_OCR


class BaiduOCR:
    """百度OCR客户端"""
    
    def __init__(self):
        self.app_id = BAIDU_OCR['APP_ID']
        self.api_key = BAIDU_OCR['API_KEY']
        self.secret_key = BAIDU_OCR['SECRET_KEY']
        self.access_token = None
    
    def get_access_token(self):
        """
        获取百度API访问令牌
        
        Returns:
            access_token: 访问令牌
        """
        if self.access_token:
            return self.access_token
        
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {
            'grant_type': 'client_credentials',
            'client_id': self.api_key,
            'client_secret': self.secret_key
        }
        
        try:
            response = requests.post(url, params=params)
            result = response.json()
            
            if 'access_token' in result:
                self.access_token = result['access_token']
                print("成功获取百度API访问令牌")
                return self.access_token
            else:
                print(f"获取访问令牌失败：{result}")
                return None
        except Exception as e:
            print(f"获取访问令牌异常：{str(e)}")
            return None
    
    def recognize_text(self, image_path):
        """
        通用文字识别（高精度版）
        
        Args:
            image_path: 图片路径
            
        Returns:
            result: 识别结果字典
        """
        access_token = self.get_access_token()
        if not access_token:
            return None
        
        # 读取图片并转为base64
        with open(image_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')
        
        url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        params = {
            'access_token': access_token,
            'image': image_data,
            'detect_direction': 'true',  # 检测图像方向
            'probability': 'true'        # 返回置信度
        }
        
        try:
            response = requests.post(url, headers=headers, data=params)
            result = response.json()
            
            if 'words_result' in result:
                print(f"成功识别 {len(result['words_result'])} 个文字区域")
                return result
            else:
                print(f"识别失败：{result}")
                return None
        except Exception as e:
            print(f"文字识别异常：{str(e)}")
            return None
    
    def recognize_with_location(self, image_path):
        """
        通用文字识别（含位置信息）
        
        Args:
            image_path: 图片路径
            
        Returns:
            result: 识别结果字典，包含文字位置信息
        """
        access_token = self.get_access_token()
        if not access_token:
            return None
        
        # 读取图片并转为base64
        with open(image_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')
        
        url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate"
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        params = {
            'access_token': access_token,
            'image': image_data,
            'detect_direction': 'true',
            'probability': 'true',
            'vertexes_location': 'true'  # 返回顶点位置
        }
        
        try:
            response = requests.post(url, headers=headers, data=params)
            result = response.json()
            
            if 'words_result' in result:
                print(f"成功识别 {len(result['words_result'])} 个文字区域（含位置）")
                return result
            else:
                print(f"识别失败：{result}")
                return None
        except Exception as e:
            print(f"文字识别异常：{str(e)}")
            return None
    
    def parse_ocr_result(self, ocr_result):
        """
        解析OCR结果，提取文字、位置和字体大小信息
        
        Args:
            ocr_result: OCR识别结果
            
        Returns:
            parsed_data: 解析后的数据列表
        """
        if not ocr_result or 'words_result' not in ocr_result:
            return []
        
        parsed_data = []
        
        for item in ocr_result['words_result']:
            word_info = {
                'text': item.get('words', ''),
                'confidence': item.get('probability', {}).get('average', 0),
            }
            
            # 提取位置信息（如果有）
            if 'location' in item:
                loc = item['location']
                word_info['left'] = loc.get('left', 0)
                word_info['top'] = loc.get('top', 0)
                word_info['width'] = loc.get('width', 0)
                word_info['height'] = loc.get('height', 0)
                
                # 估算字体大小（基于高度）
                word_info['font_size'] = max(8, min(int(loc.get('height', 20) * 0.6), 72))
            
            # 提取顶点位置（如果有）
            if 'vertexes_location' in item:
                word_info['vertexes'] = item['vertexes_location']
            
            parsed_data.append(word_info)
        
        return parsed_data
    
    def recognize_and_parse(self, image_path):
        """
        识别文字并解析结果
        
        Args:
            image_path: 图片路径
            
        Returns:
            parsed_data: 解析后的文字数据列表
        """
        # 先尝试获取带位置信息的识别结果
        result = self.recognize_with_location(image_path)
        
        if result:
            return self.parse_ocr_result(result)
        
        # 如果失败，尝试基础识别
        result = self.recognize_text(image_path)
        if result:
            return self.parse_ocr_result(result)
        
        return []


if __name__ == "__main__":
    # 测试代码
    import sys
    
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        
        ocr = BaiduOCR()
        result = ocr.recognize_and_parse(image_path)
        
        if result:
            print(f"\n识别结果（共{len(result)}个文字区域）：")
            print("-" * 60)
            for i, item in enumerate(result, 1):
                print(f"{i}. 文字：{item['text']}")
                print(f"   置信度：{item['confidence']:.2f}")
                if 'font_size' in item:
                    print(f"   估计字号：{item['font_size']}pt")
                if 'left' in item:
                    print(f"   位置：({item['left']}, {item['top']})")
                print()
        else:
            print("识别失败")
    else:
        print("用法：python baidu_ocr.py <image_path>")
