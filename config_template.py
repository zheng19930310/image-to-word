# 配置文件模板
# 复制此文件为 config.py 并填入你的API密钥

# 百度AI API配置
BAIDU_OCR = {
    # 请在 https://console.bce.baidu.com/ai/ 申请API密钥
    'APP_ID': '',          # 填入你的App ID
    'API_KEY': '',         # 填入你的API Key
    'SECRET_KEY': '',      # 填入你的Secret Key
}

# A4纸张检测配置
A4_DETECTION = {
    'min_area': 100000,      # 最小面积（像素）
    'max_area': 5000000,     # 最大面积（像素）
    'approx_epsilon': 0.02,  # 轮廓近似精度
}

# 红色图片提取配置
RED_EXTRACTION = {
    # HSV颜色范围（红色）
    'lower_red_1': [0, 43, 46],      # 红色范围1下限
    'upper_red_1': [10, 255, 255],   # 红色范围1上限
    'lower_red_2': [156, 43, 46],    # 红色范围2下限
    'upper_red_2': [180, 255, 255],  # 红色范围2上限
    'min_area': 500,                 # 最小面积（像素）
    'morph_kernel': 5,               # 形态学操作核大小
}

# Word文档生成配置
WORD_GENERATION = {
    'default_font': '宋体',           # 默认字体
    'default_font_size': 12,         # 默认字号（磅）
    'margin_top': 72,                # 上边距（磅）
    'margin_bottom': 72,             # 下边距（磅）
    'margin_left': 90,               # 左边距（磅）
    'margin_right': 90,              # 右边距（磅）
}

# 目录配置
DIRECTORIES = {
    'input': 'input',
    'output': 'output',
    'temp': 'temp',
}
