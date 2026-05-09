# 快速开始指南

欢迎使用图片转Word转换器！按照以下步骤快速上手。

## 📋 三步快速开始

### 第一步：检查环境（1分钟）

双击运行 `check_environment.bat` 文件，它会自动：
- ✓ 检查Python是否安装
- ✓ 安装所需的依赖包

如果提示需要安装Python，请访问：https://www.python.org/downloads/

### 第二步：配置API密钥（5分钟）

1. **申请百度API密钥**
   - 访问：https://ai.baidu.com/
   - 注册/登录账号
   - 进入控制台创建应用
   - 获取 App ID、API Key、Secret Key
   
   📖 详细步骤请查看：[API_SETUP_GUIDE.md](API_SETUP_GUIDE.md)

2. **配置到项目**
   - 打开 `config.py` 文件
   - 填入你的三个密钥值
   - 保存文件

```python
BAIDU_OCR = {
    'APP_ID': '你的App ID',
    'API_KEY': '你的API Key',
    'SECRET_KEY': '你的Secret Key',
}
```

### 第三步：转换图片（1分钟）

1. **准备图片**
   - 将A4纸张照片放入 `input/` 目录
   - 确保拍摄清晰、光线充足

2. **运行转换**
   ```bash
   python main.py --input input/你的图片.jpg
   ```

3. **查看结果**
   - 生成的Word文档在 `output/` 目录
   - 用Microsoft Word打开
   - 根据需要微调个别元素位置

---

## 💡 使用技巧

### 拍摄技巧
- ✅ 确保A4纸张完整在画面内
- ✅ 光线充足且均匀
- ✅ 保持相机稳定
- ❌ 避免阴影和反光
- ❌ 避免过度倾斜

### 命令行用法

```bash
# 基本用法
python main.py --input input/photo.jpg

# 指定输出路径
python main.py --input input/photo.jpg --output output/result.docx

# 跳过A4检测（如果图片已经是正面）
python main.py --input input/photo.jpg --skip-a4

# 批量转换整个目录
python main.py --batch input/
```

### 常见问题

**Q: 提示"未检测到Python"？**
A: 请先安装Python 3.8+，下载地址：https://www.python.org/downloads/

**Q: 提示"OCR识别失败"？**
A: 检查config.py中的API密钥是否正确填写

**Q: 文字识别不准确？**
A: 
- 确保图片清晰
- 光线充足
- 文字不要太模糊

**Q: 红色图片没有提取出来？**
A: 
- 检查红色是否足够鲜艳
- 可以在temp/目录查看red_mask.png调试图
- 调整config.py中的HSV颜色范围

---

## 📁 项目文件说明

```
image-to-word/
├── main.py                    # 主程序入口
├── config.py                  # 配置文件（需要填入API密钥）
├── config_template.py         # 配置模板
├── a4_detector.py             # A4检测模块
├── baidu_ocr.py               # OCR识别模块
├── red_image_extractor.py     # 红色图片提取模块
├── word_generator.py          # Word生成模块
├── requirements.txt           # Python依赖
├── check_environment.bat      # 环境检查脚本
├── README.md                  # 项目说明
├── API_SETUP_GUIDE.md         # API申请指南
├── PROJECT_PLAN.md            # 项目计划
├── QUICK_START.md             # 本文件
├── input/                     # 输入图片目录
├── output/                    # 输出Word目录
└── temp/                      # 临时文件目录
```

---

## 🎯 预期效果

### 能做到的
- ✅ 识别90-95%的文字内容
- ✅ 还原文字大小和位置
- ✅ 提取红色图片
- ✅ 生成可编辑的Word文档

### 需要手动调整的
- ⚠️ 个别文字位置可能有几像素偏差
- ⚠️ 复杂排版的细节优化
- ⚠️ 特殊字体的精确匹配
- ⚠️ 红色图片的最终位置调整

**总体自动化程度：约90%**

---

## 🔧 技术支持

遇到问题？

1. 查看 [README.md](README.md) 了解项目详情
2. 查看 [API_SETUP_GUIDE.md](API_SETUP_GUIDE.md) 了解API配置
3. 查看 [PROJECT_PLAN.md](PROJECT_PLAN.md) 了解项目架构
4. 检查 `temp/` 目录的调试图片

---

## 🚀 开始使用吧！

现在就按照上面的三步开始使用，祝你转换顺利！

如有问题或建议，欢迎反馈！
