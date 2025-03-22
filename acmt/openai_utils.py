from enum import Enum
from typing import Optional, Union, Dict, List
import openai
from .utils import Spinner

class Model(str, Enum):
    # OpenAI Models
    GPT35 = "gpt-3.5-turbo"
    GPT35_16K = "gpt-3.5-turbo-16k"
    GPT4 = "gpt-4"
    GPT4_32K = "gpt-4-32k"
    GPT4_TURBO = "gpt-4-1106-preview"
    
    # Anthropic Models
    CLAUDE2 = "claude-2"
    CLAUDE_INSTANT = "claude-instant-1"
    
    # Google Models
    PALM2 = "palm-2"
    GEMINI_PRO = "gemini-pro"
    
    # Chinese Models
    QIANWEN = "qwen-turbo"           # 通义千问
    QIANWEN_PLUS = "qwen-plus"       # 通义千问增强版
    SPARK = "spark-v3"               # 讯飞星火
    SPARK_V2 = "spark-v2"           # 讯飞星火V2
    BAICHUAN = "baichuan-53b"       # 百川大模型
    GLM4 = "chatglm-4"              # 智谱 GLM-4
    GLM3_TURBO = "chatglm-turbo"    # 智谱 GLM-3-Turbo
    ERNIE = "ernie-4.0"             # 文心一言
    ERNIE_TURBO = "ernie-turbo"     # 文心一言 Turbo
    KIMI = "kimi-v1"                # Moonshot AI 的 KIMI
    HUNYUAN = "hunyuan"             # 腾讯混元
    HUNYUAN_LITE = "hunyuan-lite"   # 腾讯混元 Lite
    DOUBAO = "doubao-v1"            # 字节豆包
    DOUBAO_TURBO = "doubao-turbo"   # 字节豆包 Turbo
    
    # Hosted Open Source Models
    DEEPSEEK = "deepseek-chat"
    LLAMA2 = "meta-llama/llama-2-70b-chat"        # Replicate hosted
    MISTRAL = "mistralai/mistral-7b-instruct"     # Together AI hosted
    MIXTRAL = "mistralai/mixtral-8x7b-instruct"   # Together AI hosted
    CODELLAMA = "meta-llama/codellama-34b-instruct" # Replicate hosted

    @property
    def api_base(self) -> str:
        """获取模型的默认 API base"""
        api_bases = {
            # OpenAI Models - 使用默认 API base
            "gpt-3.5-turbo": "https://api.openai.com/v1",
            "gpt-3.5-turbo-16k": "https://api.openai.com/v1",
            "gpt-4": "https://api.openai.com/v1",
            "gpt-4-32k": "https://api.openai.com/v1",
            "gpt-4-1106-preview": "https://api.openai.com/v1",
            
            # Other models...
            "claude-2": "https://api.anthropic.com/v1",
            "claude-instant-1": "https://api.anthropic.com/v1",
            "palm-2": "https://generativelanguage.googleapis.com/v1beta",
            "gemini-pro": "https://generativelanguage.googleapis.com/v1",
            "qwen-turbo": "https://dashscope.aliyuncs.com/api/v1",
            "qwen-plus": "https://dashscope.aliyuncs.com/api/v1",
            "spark-v3": "https://spark-api.xf-yun.com/v3.1",
            "spark-v2": "https://spark-api.xf-yun.com/v2.1",
            "baichuan-53b": "https://api.baichuan-ai.com/v1",
            "chatglm-4": "https://open.bigmodel.cn/api/v1",
            "chatglm-turbo": "https://open.bigmodel.cn/api/v1",
            "ernie-4.0": "https://aip.baidubce.com/rpc/2.0/ai_custom/v1",
            "ernie-turbo": "https://aip.baidubce.com/rpc/2.0/ai_custom/v1",
            "kimi-v1": "https://api.moonshot.cn/v1",
            "hunyuan": "https://hunyuan.cloud.tencent.com/hyllm/v1",
            "hunyuan-lite": "https://hunyuan.cloud.tencent.com/hyllm/v1",
            "doubao-v1": "https://api.doubao.com/v1",
            "doubao-turbo": "https://api.doubao.com/v1",
            "deepseek-chat": "https://api.deepseek.com/v1",
            "meta-llama/llama-2-70b-chat": "https://api.replicate.com/v1",
            "mistralai/mistral-7b-instruct": "https://api.together.xyz/v1",
            "mistralai/mixtral-8x7b-instruct": "https://api.together.xyz/v1",
            "meta-llama/codellama-34b-instruct": "https://api.replicate.com/v1",
        }
        return api_bases.get(self.value)

DEFAULT_PROMPT = """Based on the following git diff, generate a concise and descriptive commit message that follows conventional commits format.
Focus on the "what" and "why" of the changes.
Start with a type (feat, fix, docs, style, refactor, perf, test, build, ci, chore).
Do not include scope.
Limit the first line to 72 characters.
Add a blank line followed by a more detailed description if necessary.
"""

def get_model_settings(model: Model):
    """Get model specific settings."""
    # OpenAI GPT-4 Models - 更高温度以增加创造性
    if model in [Model.GPT4, Model.GPT4_32K, Model.GPT4_TURBO]:
        return {
            "temperature": 0.8,
            "max_tokens": 150,
            "system_message": "You are an expert programmer with deep understanding of code changes. Generate clear, concise, and insightful git commit messages."
        }
    
    # Anthropic Claude Models - 更注重准确性
    elif model in [Model.CLAUDE2, Model.CLAUDE_INSTANT]:
        return {
            "temperature": 0.6,
            "max_tokens": 100,
            "system_message": "You are Claude, an AI assistant focused on generating precise and accurate git commit messages. Focus on technical accuracy and clarity."
        }
    
    # Google Models - 平衡的设置
    elif model in [Model.PALM2, Model.GEMINI_PRO]:
        return {
            "temperature": 0.7,
            "max_tokens": 120,
            "system_message": "You are an AI assistant specialized in understanding code changes and generating appropriate git commit messages."
        }
    
    # Chinese Models - 根据各自特点调整
    elif model in [Model.QIANWEN, Model.QIANWEN_PLUS]:
        return {
            "temperature": 0.7,
            "max_tokens": 100,
            "system_message": "你是通义千问助手，专注于生成清晰准确的代码提交信息。"
        }
    elif model in [Model.SPARK, Model.SPARK_V2]:
        return {
            "temperature": 0.7,
            "max_tokens": 100,
            "system_message": "你是讯飞星火助手，擅长理解代码变更并生成恰当的提交信息。"
        }
    elif model in [Model.GLM4, Model.GLM3_TURBO]:
        return {
            "temperature": 0.7,
            "max_tokens": 100,
            "system_message": "你是 ChatGLM 助手，专注于代码理解和提交信息生成。"
        }
    elif model in [Model.ERNIE, Model.ERNIE_TURBO]:
        return {
            "temperature": 0.7,
            "max_tokens": 100,
            "system_message": "你是文心一言助手，擅长分析代码变更并生成清晰的提交信息。"
        }
    elif model == Model.BAICHUAN:
        return {
            "temperature": 0.7,
            "max_tokens": 100,
            "system_message": "你是百川助手，专注于代码分析和提交信息生成。"
        }
    elif model == Model.KIMI:
        return {
            "temperature": 0.7,
            "max_tokens": 100,
            "system_message": "你是 KIMI 助手，专注于代码分析和生成高质量的提交信息。"
        }
    elif model in [Model.HUNYUAN, Model.HUNYUAN_LITE]:
        return {
            "temperature": 0.7,
            "max_tokens": 100,
            "system_message": "你是腾讯混元助手，擅长分析代码变更并生成准确的提交信息。"
        }
    elif model in [Model.DOUBAO, Model.DOUBAO_TURBO]:
        return {
            "temperature": 0.7,
            "max_tokens": 100,
            "system_message": "你是豆包助手，专注于代码理解和提交信息生成。"
        }
    
    # Open Source Models - 使用托管服务
    elif model == Model.DEEPSEEK:
        return {
            "temperature": 0.7,
            "max_tokens": 100,
            "system_message": "You are an expert programmer. Generate clear and concise git commit messages."
        }
    elif model == Model.CODELLAMA:
        return {
            "temperature": 0.7,
            "max_tokens": 100,
            "system_message": "You are CodeLlama, an AI specialized in code understanding. Generate accurate and technical git commit messages."
        }
    elif model in [Model.LLAMA2, Model.MISTRAL, Model.MIXTRAL]:
        return {
            "temperature": 0.7,
            "max_tokens": 100,
            "system_message": "You are an AI assistant. Generate clear and helpful git commit messages."
        }
    
    # Default settings for GPT-3.5 and any new models
    return {
        "temperature": 0.7,
        "max_tokens": 100,
        "system_message": "You are a helpful assistant that generates clear and concise git commit messages."
    }

def generate_commit_message(
    diff: Optional[str],
    api_key: str,
    api_base: Optional[str] = None,
    model: Optional[Union[Model, str]] = None,
    prompt_template: Optional[str] = None,
    dependency_files: Optional[List[str]] = None
) -> str:
    """Generate commit message using OpenAI API.
    
    Args:
        diff: The diff content of non-dependency files
        api_key: API key for the AI service
        api_base: Optional API base URL
        model: Optional model to use
        prompt_template: Optional custom prompt template
        dependency_files: Optional list of dependency files that were changed
    
    Returns:
        Generated commit message
    """

    # 如果只有依赖更新，没有其他变更
    if dependency_files and not diff:
        files_str = ', '.join(dependency_files)
        return f"chore: update dependencies in {files_str}"

    # 使用 AI 生成提交信息
    client = openai.OpenAI(
        api_key=api_key,
        base_url=api_base,
    )

    with Spinner("Generating commit message..."):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": prompt_template or DEFAULT_PROMPT},
                    {"role": "user", "content": diff},
                ],
                temperature=get_model_settings(model)["temperature"] if isinstance(model, Model) else 0.7,
                max_tokens=get_model_settings(model)["max_tokens"] if isinstance(model, Model) else 100,
                n=1,
            )
            commit_msg = response.choices[0].message.content.strip()
            
            # 如果有依赖更新，在生成的提交信息后面添加依赖信息
            if dependency_files:
                files_str = ', '.join(dependency_files)
                return f"{commit_msg} and update dependencies in {files_str}"
            
            return commit_msg
            
        except Exception as e:
            raise Exception(f"Error: {str(e)}")
