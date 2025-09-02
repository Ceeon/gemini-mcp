#!/usr/bin/env python3
"""测试空图片参数的处理"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "gemini_mcp"))

from gemini_api import process_image_async

async def test_empty_list():
    """测试空列表"""
    print("测试1: 空列表 []")
    result = await process_image_async(
        image_input=[],  # 空列表
        prompt="生成一张可爱的猫咪图片",
        api_key="sk-MsWgWObFOM204xHdzmNM0vjdiDSeaLDcWhPccGwJ9XEF9KUv",
        base_url="https://api.tu-zi.com/v1",
        model_name="gemini-2.5-flash-image",
        output_dir="./test_outputs",
        save_output=True
    )
    
    print(f"Success: {result.get('success')}")
    if result.get('error'):
        print(f"Error: {result.get('error')}")
    if result.get('images'):
        print(f"Images: {result.get('images')}")
    return result

async def test_empty_string_list():
    """测试包含空字符串的列表"""
    print("\n测试2: 包含空字符串的列表 ['']")
    result = await process_image_async(
        image_input=[""],  # 包含空字符串
        prompt="生成一只狗狗的图片",
        api_key="sk-MsWgWObFOM204xHdzmNM0vjdiDSeaLDcWhPccGwJ9XEF9KUv",
        base_url="https://api.tu-zi.com/v1",
        model_name="gemini-2.5-flash-image",
        output_dir="./test_outputs",
        save_output=True
    )
    
    print(f"Success: {result.get('success')}")
    if result.get('error'):
        print(f"Error: {result.get('error')}")
    if result.get('images'):
        print(f"Images: {result.get('images')}")
    return result

async def test_none():
    """测试None"""
    print("\n测试3: None")
    result = await process_image_async(
        image_input=None,  # None
        prompt="生成一朵花的图片",
        api_key="sk-MsWgWObFOM204xHdzmNM0vjdiDSeaLDcWhPccGwJ9XEF9KUv",
        base_url="https://api.tu-zi.com/v1",
        model_name="gemini-2.5-flash-image",
        output_dir="./test_outputs",
        save_output=True
    )
    
    print(f"Success: {result.get('success')}")
    if result.get('error'):
        print(f"Error: {result.get('error')}")
    if result.get('images'):
        print(f"Images: {result.get('images')}")
    return result

async def main():
    print("测试空图片参数处理")
    print("="*50)
    
    # 测试所有情况
    r1 = await test_empty_list()
    r2 = await test_empty_string_list()
    r3 = await test_none()
    
    print("\n" + "="*50)
    print("测试总结:")
    print(f"空列表 []: {'✅ 通过' if r1.get('success') else '❌ 失败'}")
    print(f"空字符串列表 ['']: {'✅ 通过' if r2.get('success') else '❌ 失败'}")
    print(f"None: {'✅ 通过' if r3.get('success') else '❌ 失败'}")

if __name__ == "__main__":
    asyncio.run(main())