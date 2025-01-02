from openai import OpenAI
from enum import Enum
import os
from typing import Optional

class Model(str, Enum):
    GPT35 = "gpt-3.5-turbo"
    GPT4 = "gpt-4"
    DEEPSEEK = "deepseek-chat"

DEFAULT_MODEL = Model.GPT35

# Model-specific API base URLs
MODEL_API_BASES = {
    Model.GPT35: "https://api.openai.com/v1",
    Model.GPT4: "https://api.openai.com/v1",
    Model.DEEPSEEK: "https://api.deepseek.com",
}

DEFAULT_PROMPT = """Based on the following git diff, generate a concise and descriptive commit message that follows conventional commits format.
Focus on the "what" and "why" of the changes.
Start with a type (feat, fix, docs, style, refactor, perf, test, build, ci, chore).
Do not include scope.
Limit the first line to 72 characters.
Add a blank line followed by a more detailed description if necessary.
"""

def get_model_settings(model: Model):
    """Get the appropriate settings for each model."""
    if model == Model.GPT35:
        return {
            "temperature": 0.7,
            "max_tokens": 100,
            "system_message": "You are a helpful assistant that generates clear and concise git commit messages."
        }
    elif model == Model.DEEPSEEK:
        return {
            "temperature": 0.7,
            "max_tokens": 100,
            "system_message": "You are an expert programmer. Generate a clear and concise git commit message."
        }
    elif model == Model.GPT4:
        return {
            "temperature": 0.7,
            "max_tokens": 100,
            "system_message": "You are a helpful assistant that generates clear and concise git commit messages."
        }
    raise ValueError(f"Unknown model: {model}")

def generate_commit_message(diff, api_key, api_base=None, model=None, prompt_template=None):
    """Generate commit message using OpenAI API."""
    model_name = model or DEFAULT_MODEL
    
    if not api_key:
        raise ValueError("API key is required")
    
    if not diff:
        raise ValueError("No changes to commit")
    
    # 检查是否包含依赖更新标记
    dependency_update = None
    if diff.startswith("DEPENDENCY_UPDATE:"):
        lines = diff.split('\n', 1)
        dependency_update = lines[0].split(':')[1].strip()
        diff = lines[1] if len(lines) > 1 else ""
    
    # 如果只有依赖更新，没有其他变更
    if dependency_update and not diff:
        return f"chore: update dependencies ({dependency_update})"
    
    # 使用 AI 生成提交信息
    client = OpenAI(
        api_key=api_key,
        base_url=api_base or MODEL_API_BASES.get(model_name),
    )

    with Spinner("Generating commit message..."):
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": prompt_template or DEFAULT_PROMPT},
                    {"role": "user", "content": diff},
                ],
                temperature=0.7,
                max_tokens=100,
                n=1,
            )
            commit_msg = response.choices[0].message.content.strip()
            
            # 如果有依赖更新，在生成的提交信息后面添加依赖信息
            if dependency_update:
                return f"{commit_msg} and update dependencies ({dependency_update})"
            
            return commit_msg
            
        except Exception as e:
            raise Exception(f"Error: {str(e)}")
