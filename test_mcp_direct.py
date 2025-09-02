#!/usr/bin/env python3
"""直接测试MCP服务器函数"""

import asyncio
import sys
import os
from pathlib import Path

# 设置环境变量
os.environ["GEMINI_API_KEY"] = "sk-MsWgWObFOM204xHdzmNM0vjdiDSeaLDcWhPccGwJ9XEF9KUv"
os.environ["API_BASE_URL"] = "https://api.tu-zi.com/v1"
os.environ["MODEL_NAME"] = "gemini-2.5-flash-image"
os.environ["OUTPUT_DIR"] = "./test_outputs"

sys.path.insert(0, str(Path(__file__).parent / "gemini_mcp"))

# 导入MCP服务器模块
from mcp_server import send_images_to_gemini

async def test_mcp_with_empty_list():
    """测试MCP函数 - 空列表"""
    print("测试MCP函数 - images=[]")
    print("-"*50)
    
    # 模拟MCP调用 - 空列表
    result = await send_images_to_gemini(
        prompt="生成一张可爱的小猫图片",
        images=[]  # 空列表，应该被识别为纯文字生图
    )
    
    print("结果:")
    print(result)
    print()
    
    # 检查是否包含错误信息
    if "处理失败" in result:
        print("❌ 仍然有错误")
        return False
    else:
        print("✅ 成功处理")
        return True

async def test_mcp_with_empty_string_list():
    """测试MCP函数 - 包含空字符串的列表"""
    print("测试MCP函数 - images=['']")
    print("-"*50)
    
    result = await send_images_to_gemini(
        prompt="生成一只狗狗的图片",
        images=[""]  # 包含空字符串
    )
    
    print("结果:")
    print(result)
    print()
    
    if "处理失败" in result:
        print("❌ 仍然有错误")
        return False
    else:
        print("✅ 成功处理")
        return True

async def test_mcp_with_none():
    """测试MCP函数 - None"""
    print("测试MCP函数 - images=None")
    print("-"*50)
    
    result = await send_images_to_gemini(
        prompt="生成一朵花的图片",
        images=None  # None
    )
    
    print("结果:")
    print(result)
    print()
    
    if "处理失败" in result:
        print("❌ 仍然有错误")
        return False
    else:
        print("✅ 成功处理")
        return True

async def main():
    print("直接测试MCP服务器函数")
    print("="*50)
    
    # 测试所有情况
    r1 = await test_mcp_with_empty_list()
    r2 = await test_mcp_with_empty_string_list()
    r3 = await test_mcp_with_none()
    
    print("="*50)
    print("测试总结:")
    print(f"空列表 []: {'✅ 通过' if r1 else '❌ 失败'}")
    print(f"空字符串列表 ['']: {'✅ 通过' if r2 else '❌ 失败'}")
    print(f"None: {'✅ 通过' if r3 else '❌ 失败'}")
    
    if not (r1 and r2 and r3):
        print("\n⚠️ 需要进一步调试")

if __name__ == "__main__":
    asyncio.run(main())