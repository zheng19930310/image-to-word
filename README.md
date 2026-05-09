# Image to Word Converter

将拍摄的A4纸张图片转换为可编辑的Word文档，支持文字识别、版面还原和红色图片提取。

## 功能特性

- ✅ A4纸张自动检测与透视矫正
- ✅ 高精度OCR文字识别（百度AI）
- ✅ 字体大小和类型智能估计
- ✅ 红色图片自动提取（HSV颜色分割）
- ✅ Word文档自动生成（保留版面布局）
- ✅ 红色图片设置为浮动可移动对象
- ✅ 完全免费（个人学习使用）

## 技术栈

- **Python 3.8+**
- **OpenCV**: 图像处理和A4检测
- **百度AI OCR API**: 文字识别和版面分析
- **python-docx**: Word文档生成
- **NumPy**: 数值计算
- **Pillow**: 图像处理

## 项目结构

```
image-to-word/
├── config.py              # 配置文件
├── a4_detector.py         # A4纸张检测与矫正
├── baidu_ocr.py           # 百度OCR API调用
├── red_image_extractor.py # 红色图片提取
├── word_generator.py      # Word文档生成
├── main.py                # 主程序入口
├── requirements.txt       # Python依赖
├── README.md              # 项目说明
├── API_SETUP_GUIDE.md     # API申请指南
├── input/                 # 输入图片目录
│   └── .gitkeep
├── output/                # 输出Word文档目录
│   └── .gitkeep
└── temp/                  # 临时文件目录
    └── .gitkeep
```

## 快速开始

### 1. 安装Python环境

如果你的电脑还没有Python环境，请先安装：
- 下载 Python 3.8+：https://www.python.org/downloads/
- 安装时勾选 "Add Python to PATH"

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置百度API

请参考 [API申请指南](API_SETUP_GUIDE.md) 获取API密钥，然后在 `config.py` 中配置。

### 4. 运行程序

```bash
python main.py --input input/test.jpg --output output/result.docx
```

## 使用说明

1. 将需要转换的图片放入 `input/` 目录
2. 运行程序
3. 在 `output/` 目录查看生成的Word文档
4. 在Word中手动微调个别元素位置

## 注意事项

- 确保拍摄时光线充足，A4纸张完整在画面内
- 红色图片会被自动提取并设置为浮动对象
- 首次使用需要先申请百度AI API密钥（免费）
- 个人用户每天有50,000次免费调用额度

## 许可证

本项目仅供个人学习使用。
