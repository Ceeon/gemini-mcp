#!/bin/bash

# 发布到 PyPI 的脚本

echo "🚀 准备发布 Gemini MCP 到 PyPI..."

# 清理旧的构建文件
echo "🧹 清理旧的构建文件..."
rm -rf dist/ build/ *.egg-info

# 构建包
echo "📦 构建包..."
python -m pip install --upgrade build
python -m build

# 显示构建的文件
echo "📋 构建的文件："
ls -la dist/

# 提示上传
echo ""
echo "✅ 构建完成！"
echo ""
echo "要上传到 TestPyPI（测试）："
echo "  python -m twine upload -r testpypi dist/*"
echo ""
echo "要上传到 PyPI（正式）："
echo "  python -m twine upload dist/*"
echo ""
echo "注意：需要先安装 twine："
echo "  pip install twine"