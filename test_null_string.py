#!/usr/bin/env python3
"""测试字符串"null"的处理"""

import asyncio
from gemini_mcp.gemini_api import process_image_async

async def test_null_string():
    print("测试字符串'null'...")
    result = await process_image_async(
        image_input="null",  # 字符串"null"
        prompt="生成一张科技风格的工作空间图片",
        api_key="sk-MsWgWObFOM204xHdzmNM0vjdiDSeaLDcWhPccGwJ9XEF9KUv",
        base_url="https://api.tu-zi.com/v1",
        model_name="gemini-2.5-flash-image",
        output_dir="./test_null_output",
        save_output=True
    )
    
    print(f"Success: {result.get('success')}")
    print(f"Error: {result.get('error')}")
    if result.get('success'):
        print(f"Images: {result.get('images')}")
    return result.get('success')

async def test_none_string():
    print("\n测试字符串'None'...")
    result = await process_image_async(
        image_input="None",  # 字符串"None"
        prompt="生成一张图片",
        api_key="sk-MsWgWObFOM204xHdzmNM0vjdiDSeaLDcWhPccGwJ9XEF9KUv",
        base_url="https://api.tu-zi.com/v1",
        model_name="gemini-2.5-flash-image",
        output_dir="./test_null_output",
        save_output=True
    )
    
    print(f"Success: {result.get('success')}")
    return result.get('success')

async def test_undefined_string():
    print("\n测试字符串'undefined'...")
    result = await process_image_async(
        image_input="undefined",  # 字符串"undefined"
        prompt="生成一张图片",
        api_key="sk-MsWgWObFOM204xHdzmNM0vjdiDSeaLDcWhPccGwJ9XEF9KUv",
        base_url="https://api.tu-zi.com/v1",
        model_name="gemini-2.5-flash-image",
        output_dir="./test_null_output",
        save_output=True
    )
    
    print(f"Success: {result.get('success')}")
    return result.get('success')

async def main():
    print("测试字符串null/None/undefined处理")
    print("="*50)
    
    r1 = await test_null_string()
    r2 = await test_none_string()
    r3 = await test_undefined_string()
    
    print("\n" + "="*50)
    print("测试结果:")
    print(f"字符串'null': {'✅ 通过' if r1 else '❌ 失败'}")
    print(f"字符串'None': {'✅ 通过' if r2 else '❌ 失败'}")
    print(f"字符串'undefined': {'✅ 通过' if r3 else '❌ 失败'}")

if __name__ == "__main__":
    asyncio.run(main())