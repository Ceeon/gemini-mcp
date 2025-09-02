#!/usr/bin/env python3
"""
Gemini MCP Server (核心版)
基于原始API文档功能设计，只实现核心功能
"""

import os
import sys
from pathlib import Path
from typing import Union, List
from fastmcp import FastMCP
from dotenv import load_dotenv

# 添加src目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

# 导入Gemini API模块
from gemini_api import process_image_async

# 加载环境变量
load_dotenv()

# 创建MCP实例
mcp = FastMCP("Gemini Image Processor")

# 配置
API_KEY = os.getenv("GEMINI_API_KEY")
BASE_URL = os.getenv("API_BASE_URL", "https://api.tu-zi.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.5-flash-image")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./outputs")


@mcp.tool()
async def send_images_to_gemini(
    images: Union[str, List[str]],
    prompt: str
) -> str:
    """
    向Gemini AI发送图片进行处理（核心功能）
    
    这是原始API的核心功能：发送图片+提示词，获取AI响应
    
    Args:
        images: 图片输入，支持：
               - 单张图片路径: "/path/to/image.jpg"
               - 多张图片列表: ["/path/to/img1.jpg", "/path/to/img2.png"]
               - 支持本地文件、URL、base64格式
        prompt: 提示词，告诉AI你想做什么
               例如："描述这张图片" 或 "生成卡通风格版本"
    
    Returns:
        AI响应内容，包含：
        - 文字描述或分析
        - 生成的图片（自动保存到本地）
        - 保存的文件路径
    
    功能特性（自动处理）：
        ✅ 自动将本地文件转换为base64
        ✅ 自动下载URL图片
        ✅ 自动保存生成的图片到本地
        ✅ 自动重试（配额超限最多10次）
        ✅ 使用流式响应获取完整数据
        ✅ 保存调试信息到输出目录
    
    使用示例：
        # 分析单张图片
        images = "/Users/me/photo.jpg"
        prompt = "描述这张图片的内容"
        
        # 生成图片（多张参考图）
        images = ["photo1.jpg", "photo2.jpg"]
        prompt = "基于这两张图片生成一个融合版本"
        
        # 使用URL
        images = "https://example.com/image.png"
        prompt = "将这张图片转换为油画风格"
    """
    try:
        # 调用原始API功能
        result = await process_image_async(
            image_input=images,
            prompt=prompt,
            api_key=API_KEY,
            base_url=BASE_URL,
            model_name=MODEL_NAME,
            output_dir=OUTPUT_DIR,
            save_output=True  # 始终保存输出
        )
        
        if result["success"]:
            # 构建响应
            response = []
            
            # 添加文本响应
            response.append(result["text"])
            
            # 如果有生成的图片
            if result.get("images"):
                response.append("\n" + "="*50)
                response.append("📸 生成/提取的图片已保存：")
                for img_path in result["images"]:
                    response.append(f"  ✅ {img_path}")
            
            # 输出目录信息
            if result.get("output_dir"):
                response.append(f"\n📂 所有文件保存在: {result['output_dir']}")
                response.append("  - content.txt: 处理后的文本")
                response.append("  - original_content.txt: 原始响应")
                response.append("  - raw_api_response.json: API响应调试信息")
            
            return "\n".join(response)
        else:
            return f"❌ 处理失败: {result.get('error', '未知错误')}"
            
    except Exception as e:
        return f"❌ 错误: {str(e)}"


# 主程序入口
if __name__ == "__main__":
    if not API_KEY:
        print("⚠️ 警告: GEMINI_API_KEY 环境变量未设置")
        print("请在 .env 文件中设置 API 密钥")
        print("\n示例 .env 文件内容：")
        print("GEMINI_API_KEY=sk-your-api-key")
        print("API_BASE_URL=https://api.tu-zi.com/v1")
        print("MODEL_NAME=gemini-2.5-flash-image")
        print("OUTPUT_DIR=./outputs")
    else:
        print("✅ Gemini MCP Server 已启动")
        print(f"📡 API: {BASE_URL}")
        print(f"🤖 模型: {MODEL_NAME}")
        print(f"📁 输出: {OUTPUT_DIR}")
    
    # 运行MCP服务器（stdio模式）
    mcp.run(transport="stdio")