@echo off
chcp 65001 >nul
echo ========================================
echo   图片转Word转换器 - 环境检查
echo ========================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到Python，请先安装Python 3.8+
    echo 下载地址：https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [✓] Python已安装
python --version
echo.

REM 检查依赖是否安装
echo 检查依赖包...
python -c "import cv2" >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] 依赖包未安装，开始安装...
    echo.
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo [错误] 依赖安装失败
        pause
        exit /b 1
    )
    echo [✓] 依赖安装完成
) else (
    echo [✓] 依赖包已安装
)

echo.
echo ========================================
echo   环境检查完成！
echo ========================================
echo.
echo 下一步：
echo 1. 按照 API_SETUP_GUIDE.md 申请百度API密钥
echo 2. 在 config.py 中配置API密钥
echo 3. 将图片放入 input/ 目录
echo 4. 运行: python main.py --input input/你的图片.jpg
echo.
pause
