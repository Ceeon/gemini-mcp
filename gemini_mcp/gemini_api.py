"""
Gemini API 图像处理模块
重构自原始脚本，用于MCP集成
"""

import os
import base64
import re
import requests
import time
import json
import asyncio
from datetime import datetime
from typing import Union, Dict, List, Optional
from openai import OpenAI


class GeminiImageProcessor:
    """Gemini图片处理器"""
    
    def __init__(
        self,
        api_key: str = None,
        base_url: str = None,
        model_name: str = None,
        max_retries: int = 10,
        retry_delay: float = 0,
        api_timeout: int = 120,
        use_stream: bool = True,
        output_dir: str = "./outputs"
    ):
        """初始化处理器"""
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "sk-**")
        self.base_url = base_url or os.getenv("API_BASE_URL", "https://api.tu-zi.com/v1")
        self.model_name = model_name or os.getenv("MODEL_NAME", "gemini-2.5-flash-image")
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.api_timeout = api_timeout
        self.use_stream = use_stream
        self.output_dir = output_dir
        
        # 初始化OpenAI客户端
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
    
    def prepare_image_data(self, image_input: Union[str, bytes]) -> str:
        """准备图片数据，转换为base64格式"""
        # 如果已经是base64格式
        if isinstance(image_input, str) and image_input.startswith("data:image"):
            return image_input
        
        # 如果是URL
        if isinstance(image_input, str) and (image_input.startswith("http://") or image_input.startswith("https://")):
            # 下载图片
            response = requests.get(image_input)
            response.raise_for_status()
            image_bytes = response.content
        # 如果是文件路径
        elif isinstance(image_input, str):
            # 打印调试信息
            print(f"尝试读取文件: {image_input}")
            if not os.path.exists(image_input):
                raise FileNotFoundError(f"文件不存在: {image_input}")
            with open(image_input, "rb") as img_file:
                image_bytes = img_file.read()
        # 如果是字节数据
        elif isinstance(image_input, bytes):
            image_bytes = image_input
        else:
            raise ValueError(f"不支持的图片输入类型: {type(image_input)}")
        
        # 转换为base64
        encoded_data = base64.b64encode(image_bytes).decode("utf-8")
        return "data:image/png;base64," + encoded_data
    
    def create_output_directory(self) -> str:
        """创建输出目录"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = os.path.join(self.output_dir, f"output_{timestamp}")
        os.makedirs(output_dir, exist_ok=True)
        return output_dir
    
    def save_base64_image(self, base64_data: str, output_dir: str, image_index: int) -> Optional[str]:
        """保存base64图片到本地"""
        try:
            # 移除data:image/png;base64,前缀（如果存在）
            if base64_data.startswith('data:image/'):
                base64_data = base64_data.split(',', 1)[1]
            
            # 解码base64数据
            image_data = base64.b64decode(base64_data)
            
            # 保存图片
            image_filename = f"image_{image_index}.png"
            image_path = os.path.join(output_dir, image_filename)
            
            with open(image_path, "wb") as img_file:
                img_file.write(image_data)
            
            return image_path
        except Exception as e:
            print(f"保存base64图片时出错: {e}")
            return None
    
    def download_image_from_url(self, url: str, output_dir: str, image_index: int) -> Optional[str]:
        """从URL下载图片到本地"""
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            # 获取文件扩展名
            content_type = response.headers.get('content-type', '')
            if 'png' in content_type.lower():
                ext = 'png'
            elif 'jpg' in content_type.lower() or 'jpeg' in content_type.lower():
                ext = 'jpg'
            elif 'gif' in content_type.lower():
                ext = 'gif'
            else:
                ext = 'png'  # 默认扩展名
            
            # 保存图片
            image_filename = f"image_url_{image_index}.{ext}"
            image_path = os.path.join(output_dir, image_filename)
            
            with open(image_path, "wb") as img_file:
                for chunk in response.iter_content(chunk_size=8192):
                    img_file.write(chunk)
            
            return image_path
        except Exception as e:
            print(f"下载URL图片时出错: {e}")
            return None
    
    def save_mixed_content(self, content: str, output_dir: str) -> Dict[str, any]:
        """保存混合内容（文字、base64图片、URL图片）"""
        result = {
            "text": content,
            "images": [],
            "text_file": None
        }
        
        try:
            # 查找base64图片
            base64_pattern = r'data:image/[^;]+;base64,([A-Za-z0-9+/=]+)'
            base64_matches = re.finditer(base64_pattern, content)
            
            # 查找URL链接（包括API返回的生成图片URL）
            # 匹配常见的图片URL格式，包括google.datas.systems的URL
            url_patterns = [
                r'https?://[^\s<>"]+\.(png|jpg|jpeg|gif)',  # 标准图片URL
                r'https?://google\.datas\.systems/[^\s<>"]+',  # API生成的图片URL
                r'!\[image\]\((https?://[^\)]+)\)'  # Markdown格式的图片
            ]
            
            url_matches = []
            for pattern in url_patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    # 提取URL（处理Markdown格式）
                    if '![image]' in match.group(0):
                        url = match.group(1)
                    else:
                        url = match.group(0)
                    url_matches.append(url)
            
            # 保存文字内容到文件
            text_content = content
            image_index = 1
            
            # 处理base64图片
            for match in base64_matches:
                full_match = match.group(0)
                base64_data = match.group(1)
                
                # 保存base64图片
                saved_path = self.save_base64_image(base64_data, output_dir, image_index)
                if saved_path:
                    result["images"].append(saved_path)
                    # 在文本中替换base64数据为文件路径
                    text_content = text_content.replace(full_match, f"[保存的图片: {saved_path}]")
                    image_index += 1
            
            # 处理URL图片（去重）
            processed_urls = set()
            for url in url_matches:
                if url not in processed_urls:
                    processed_urls.add(url)
                    
                    # 下载URL图片
                    saved_path = self.download_image_from_url(url, output_dir, image_index)
                    if saved_path:
                        result["images"].append(saved_path)
                        # 在文本中替换URL为文件路径
                        text_content = text_content.replace(url, f"[下载的图片: {saved_path}]")
                        image_index += 1
            
            # 保存处理后的文字内容
            text_filename = os.path.join(output_dir, "content.txt")
            with open(text_filename, "w", encoding="utf-8") as text_file:
                text_file.write(text_content)
            result["text_file"] = text_filename
            
            # 更新处理后的文本
            result["text"] = text_content
            
        except Exception as e:
            print(f"保存混合内容时出错: {e}")
        
        return result
    
    def is_quota_exceeded_error(self, error_message: str) -> bool:
        """检查是否为配额超出错误"""
        quota_keywords = [
            "exceeded your current quota",
            "quota exceeded",
            "billing details",
            "plan and billing"
        ]
        error_str = str(error_message).lower()
        return any(keyword in error_str for keyword in quota_keywords)
    
    def call_api_with_retry(self, messages: List[Dict]) -> Dict:
        """带重试功能的API调用"""
        for attempt in range(self.max_retries):
            try:
                if self.use_stream:
                    # 使用流式响应
                    completion = self.client.chat.completions.create(
                        model=self.model_name,
                        messages=messages,
                        timeout=self.api_timeout,
                        stream=True
                    )
                    
                    # 收集流式响应
                    full_content = ""
                    for chunk in completion:
                        # 安全检查：确保choices存在且不为空
                        if hasattr(chunk, 'choices') and chunk.choices and len(chunk.choices) > 0:
                            if hasattr(chunk.choices[0], 'delta'):
                                delta = chunk.choices[0].delta
                                if hasattr(delta, 'content') and delta.content:
                                    full_content += delta.content
                    
                    return {
                        "content": full_content,
                        "success": True
                    }
                else:
                    # 非流式响应
                    completion = self.client.chat.completions.create(
                        model=self.model_name,
                        messages=messages,
                        timeout=self.api_timeout
                    )
                    
                    return {
                        "content": completion.choices[0].message.content,
                        "success": True
                    }
                    
            except Exception as e:
                error_message = str(e)
                print(f"API调用失败 (尝试 {attempt + 1}/{self.max_retries}): {error_message}")
                
                # 检查是否为配额超出错误或超时错误
                if self.is_quota_exceeded_error(error_message) or "timeout" in error_message.lower():
                    if attempt < self.max_retries - 1:
                        if self.retry_delay > 0:
                            time.sleep(self.retry_delay)
                        continue
                    else:
                        raise
                else:
                    # 非可重试错误，直接抛出
                    raise
        
        # 如果所有重试都失败了
        raise Exception(f"经过 {self.max_retries} 次重试后仍然失败")
    
    def process_images(
        self,
        images: Union[str, List[str], None],
        prompt: str,
        save_output: bool = True
    ) -> Dict:
        """
        处理图片的主函数
        
        Args:
            images: 单个或多个图片（路径、URL或base64），或None（纯文字生图）
            prompt: 提示词
            save_output: 是否保存输出
        
        Returns:
            包含处理结果的字典
        """
        try:
            # 添加调试日志
            print(f"[DEBUG] process_images 接收到的参数:")
            print(f"  - images: {images}")
            print(f"  - images type: {type(images)}")
            print(f"  - images == []: {images == []}")
            print(f"  - images is None: {images is None}")
            
            # 构建消息内容
            content_list = []
            
            # 处理图片输入
            # 检查是否为字符串形式的null/none/undefined
            if isinstance(images, str) and images.lower() in ["null", "none", "undefined"]:
                print(f"[DEBUG] 检测到字符串'{images}'，视为纯文字模式")
                images = None
            
            if images is not None and images != [] and images != "":
                print(f"[DEBUG] 进入图片处理分支")
                # 确保images是列表
                if isinstance(images, str):
                    images = [images]
                
                # 过滤掉空字符串
                valid_images = [img for img in images if img and img != ""]
                print(f"[DEBUG] 过滤后的valid_images: {valid_images}")
                
                # 如果没有有效的图片，视为纯文字生图
                if not valid_images:
                    print(f"[DEBUG] 没有有效图片，切换到纯文字模式")
                    content_list = prompt  # 纯文字模式
                else:
                    print(f"[DEBUG] 有 {len(valid_images)} 张有效图片")
                    # 准备所有图片数据
                    image_contents = []
                    for i, image in enumerate(valid_images):
                        try:
                            image_data = self.prepare_image_data(image)
                            image_contents.append({
                                "type": "image_url",
                                "image_url": {
                                    "url": image_data,
                                },
                            })
                        except Exception as e:
                            print(f"处理第 {i+1} 张图片时出错: {e}")
                            continue
                    
                    if not image_contents:
                        # 如果所有图片都处理失败，回退到纯文字模式
                        print("所有图片处理失败，切换到纯文字生图模式")
                        content_list = prompt
                    else:
                        # 添加文本和图片到内容列表
                        content_list.append({"type": "text", "text": prompt})
                        content_list.extend(image_contents)
            else:
                # 纯文字模式 - 只有提示词
                print(f"[DEBUG] 直接进入纯文字模式 (images为None或空)")
                content_list = prompt  # 直接使用字符串作为content
            
            messages = [
                {
                    "role": "user",
                    "content": content_list,
                }
            ]
            
            # 调用API
            api_result = self.call_api_with_retry(messages)
            
            if not api_result["success"]:
                return {
                    "success": False,
                    "error": "API调用失败",
                    "text": None,
                    "images": []
                }
            
            # 处理响应
            response_content = api_result["content"]
            
            # 保存输出（如果需要）
            if save_output:
                output_dir = self.create_output_directory()
                save_result = self.save_mixed_content(response_content, output_dir)
                
                return {
                    "success": True,
                    "error": None,
                    "text": save_result["text"],
                    "images": save_result["images"],
                    "output_dir": output_dir
                }
            else:
                return {
                    "success": True,
                    "error": None,
                    "text": response_content,
                    "images": [],
                    "output_dir": None
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "text": None,
                "images": []
            }


# 异步包装器，用于MCP集成
async def process_image_async(
    image_input: Union[str, List[str], None],
    prompt: str,
    api_key: str = None,
    save_output: bool = True,
    **kwargs
) -> Dict:
    """异步处理图片或纯文字生图"""
    processor = GeminiImageProcessor(api_key=api_key, **kwargs)
    
    # 在线程池中运行同步函数
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None,
        processor.process_images,
        image_input,
        prompt,
        save_output
    )
    
    return result


# 保留向后兼容的同步函数
def process_image(
    image_input: Union[str, List[str]],
    prompt: str,
    api_key: str = None,
    save_output: bool = True,
    **kwargs
) -> Dict:
    """同步处理图片（向后兼容）"""
    processor = GeminiImageProcessor(api_key=api_key, **kwargs)
    return processor.process_images(image_input, prompt, save_output)