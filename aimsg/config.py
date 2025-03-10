import os
import json
from typing import Dict, Optional
from dotenv import load_dotenv

CONFIG_DIR = os.path.expanduser("~/.config/aimsg")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

DEFAULT_CONFIG = {
    "api_key": "",
    "api_base": "https://api.openai.com/v1",
    "model": "gpt-3.5-turbo",
    "prompt": """Based on the following git diff, generate a concise and descriptive commit message that follows conventional commits format.
Focus on the "what" and "why" of the changes.
Start with a type (feat, fix, docs, style, refactor, perf, test, build, ci, chore).
Do not include scope.
Limit the first line to 72 characters.
Add a blank line followed by a more detailed description if necessary.
"""
}

def ensure_config_dir():
    """确保配置目录存在"""
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)

def load_config() -> Dict:
    """加载配置文件"""
    ensure_config_dir()
    if not os.path.exists(CONFIG_FILE):
        return DEFAULT_CONFIG.copy()
    
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            return {**DEFAULT_CONFIG, **config}
    except Exception:
        return DEFAULT_CONFIG.copy()

def save_config(config: Dict):
    """保存配置文件"""
    ensure_config_dir()
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def get_config_value(key: str, default=None) -> Optional[str]:
    """获取配置值，按优先级顺序：.env文件 > 环境变量 > 配置文件"""
    env_key = f"AIMSG_{key.upper()}"
    # 1. 首先尝试.env文件
    load_dotenv()
    env_value = os.getenv(env_key)
    if env_value:
        # 检查这个值是否来自.env文件
        try:
            with open(os.path.join(os.getcwd(), '.env'), 'r') as f:
                if any(line.strip().startswith(env_key) for line in f):
                    return env_value
        except FileNotFoundError:
            pass
    
    # 2. 然后尝试环境变量
    if env_key in os.environ:
        return os.environ[env_key]
    
    # 3. 最后尝试配置文件
    config = load_config()
    return config.get(key, default)

def add_custom_model(name: str, model_id: str, api_base: str):
    """添加自定义模型"""
    config = load_config()
    if "custom_models" not in config:
        config["custom_models"] = {}
    
    config["custom_models"][name] = {
        "model_id": model_id,
        "api_base": api_base
    }
    save_config(config)

def remove_custom_model(name: str):
    """删除自定义模型"""
    config = load_config()
    if "custom_models" not in config or name not in config["custom_models"]:
        raise ValueError(f"Custom model '{name}' not found")
    
    del config["custom_models"][name]
    
    # 如果删除的是当前默认模型，重置为默认的 GPT-3.5
    if config.get("model") == name:
        config["model"] = DEFAULT_CONFIG["model"]
    
    save_config(config)

def get_custom_model(name: str) -> Optional[Dict]:
    """获取自定义模型配置"""
    config = load_config()
    return config.get("custom_models", {}).get(name)

def list_custom_models() -> Dict:
    """列出所有自定义模型"""
    config = load_config()
    return config.get("custom_models", {})
