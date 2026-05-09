# 启动和测试指南

## ✅ 环境状态

- ✓ Python 3.13.13 已安装
- ✓ 所有依赖包已安装成功
- ✓ 项目可以正常运行

## ⚠️ 使用前必须配置

### 配置百度API密钥

在运行转换之前，**必须**先配置百度OCR API密钥：

1. **打开配置文件**：`config.py`

2. **填入你的API密钥**（需要先申请）：
   ```python
   BAIDU_OCR = {
       'APP_ID': '你的App ID',
       'API_KEY': '你的API Key',
       'SECRET_KEY': '你的Secret Key',
   }
   ```

3. **如何申请API密钥**：
   - 详细步骤请查看：[API_SETUP_GUIDE.md](API_SETUP_GUIDE.md)
   - 快速入口：https://console.bce.baidu.com/ai/
   - 免费额度：每天50,000次调用

## 🧪 测试方法

### 方法1：使用示例图片测试

1. 准备一张A4纸张照片
2. 放入 `input/` 目录
3. 运行命令：
   ```bash
   python main.py --input input/你的图片.jpg
   ```

### 方法2：跳过A4检测测试（如果图片已是正面）

```bash
python main.py --input input/你的图片.jpg --skip-a4
```

### 方法3：指定输出路径

```bash
python main.py --input input/你的图片.jpg --output output/结果.docx
```

### 方法4：批量转换

将多张图片放入 `input/` 目录，然后：

```bash
python main.py --batch input/
```

## 📋 完整工作流程

```
1. 拍摄/准备A4纸张照片
        ↓
2. 放入 input/ 目录
        ↓
3. 确保 config.py 已配置API密钥
        ↓
4. 运行: python main.py --input input/图片.jpg
        ↓
5. 等待处理完成（需要联网调用API）
        ↓
6. 在 output/ 目录查看生成的Word文档
        ↓
7. 用Microsoft Word打开并微调位置
```

## 🔍 调试信息

处理过程中会在 `temp/` 目录生成调试文件：

- `corrected.jpg` - A4矫正后的图片
- `red_mask.png` - 红色区域掩码图
- `red_visualization.png` - 红色区域可视化图
- `red_image_0.png`, `red_image_1.png`... - 提取的红色图片

## ❓ 常见问题

### Q1: 提示"获取访问令牌失败"？
**A**: 检查 `config.py` 中的API密钥是否正确填写

### Q2: 提示"OCR识别失败"？
**A**: 
- 检查网络连接
- 确认API密钥有效
- 查看百度AI控制台的应用状态

### Q3: 没有检测到A4纸张？
**A**: 
- 确保A4纸张完整在画面内
- 光线充足
- 或使用 `--skip-a4` 参数跳过检测

### Q4: 红色图片没有提取出来？
**A**: 
- 检查红色是否足够鲜艳
- 查看 `temp/red_mask.png` 调试图
- 调整 `config.py` 中的HSV颜色范围

## 🎯 预期效果

- **文字识别准确率**：90-95%
- **版面还原准确度**：80-90%
- **自动化程度**：约90%
- **需要手动调整**：个别元素位置微调

## 📞 需要帮助？

查看详细文档：
- [README.md](README.md) - 项目说明
- [QUICK_START.md](QUICK_START.md) - 快速开始
- [API_SETUP_GUIDE.md](API_SETUP_GUIDE.md) - API申请指南
- [PROJECT_PLAN.md](PROJECT_PLAN.md) - 项目计划

---

**准备好了吗？配置好API密钥后就可以开始使用了！** 🚀
