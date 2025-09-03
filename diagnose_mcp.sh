#!/bin/bash

echo "==================================="
echo "MCP 服务诊断脚本"
echo "==================================="
echo ""

# 1. 检查虚拟环境
echo "1. 检查虚拟环境..."
if [ -f "venv/bin/python3" ]; then
    echo "✅ 虚拟环境存在"
    echo "   Python 版本: $(venv/bin/python3 --version)"
else
    echo "❌ 虚拟环境不存在"
    exit 1
fi
echo ""

# 2. 检查依赖
echo "2. 检查依赖安装..."
venv/bin/pip list | grep -E "fastmcp|openai|requests|python-dotenv" | while read line; do
    echo "   ✅ $line"
done
echo ""

# 3. 检查代码语法
echo "3. 检查代码语法..."
venv/bin/python3 -c "from gemini_mcp import mcp" 2>&1
if [ $? -eq 0 ]; then
    echo "✅ MCP 模块可以导入"
else
    echo "❌ MCP 模块导入失败"
    exit 1
fi
echo ""

# 4. 测试 MCP 服务器启动
echo "4. 测试 MCP 服务器启动（5秒超时）..."
timeout 5 venv/bin/python3 -m gemini_mcp.mcp_server 2>&1 | head -20
echo ""

# 5. 检查配置文件
echo "5. 检查配置文件..."
if [ -f "$HOME/.cursor/mcp.json" ]; then
    echo "✅ Cursor 配置文件存在"
    echo "   路径: $HOME/.cursor/mcp.json"
    echo "   内容预览:"
    cat "$HOME/.cursor/mcp.json" | python3 -m json.tool | head -20
else
    echo "❌ Cursor 配置文件不存在"
fi
echo ""

# 6. 检查工具注册
echo "6. 检查工具注册..."
venv/bin/python3 -c "
from gemini_mcp.mcp_server import send_images_to_gemini
print(f'✅ 工具已注册: send_images_to_gemini')
print(f'   类型: {type(send_images_to_gemini)}')
"
echo ""

echo "==================================="
echo "诊断完成"
echo "==================================="
echo ""
echo "如果所有检查都通过但仍无法使用："
echo "1. 重启 Cursor"
echo "2. 检查 Cursor 是否支持 MCP（需要最新版本）"
echo "3. 查看 Cursor 的开发者控制台是否有错误信息"