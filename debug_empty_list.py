#!/usr/bin/env python3
"""调试空列表问题"""

import asyncio
from gemini_mcp.gemini_api import process_image_async

async def test():
    print("测试空列表直接传递给API...")
    
    # 直接调用API函数，模拟MCP传递空列表
    result = await process_image_async(
        image_input=[],  # 空列表
        prompt="生成一张小猫图片",
        api_key="sk-MsWgWObFOM204xHdzmNM0vjdiDSeaLDcWhPccGwJ9XEF9KUv",
        base_url="https://api.tu-zi.com/v1",
        model_name="gemini-2.5-flash-image",
        output_dir="./debug_output",
        save_output=True
    )
    
    print(f"成功: {result.get('success')}")
    print(f"错误: {result.get('error')}")
    print(f"文本: {result.get('text', '')[:100]}...")
    
    # 调试信息
    if not result.get('success'):
        print("\n调试信息:")
        print(f"完整结果: {result}")

asyncio.run(test())