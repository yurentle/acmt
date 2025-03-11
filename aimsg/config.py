import os
import json
from typing import Dict, Optional
from dotenv import load_dotenv

CONFIG_DIR = os.path.expanduser("~/.config/aimsg")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

DEFAULT_CONFIG = {
    "api_key": "",
    "api_base": "",
    "model": "",
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

def get_custom_model(name: str) -> Optional[dict]:
    """获取指定名称的自定义模型配置"""
    config = Config()
    return config.get_model_config(name)

class Config:
    def __init__(self):
        self.config_file = CONFIG_FILE
    
    def load_config(self) -> Dict:
        """加载配置文件"""
        ensure_config_dir()
        if not os.path.exists(self.config_file):
            return DEFAULT_CONFIG.copy()
        
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                return {**DEFAULT_CONFIG, **config}
        except Exception:
            return DEFAULT_CONFIG.copy()
    
    def save_config(self, config: Dict):
        """保存配置文件"""
        ensure_config_dir()
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def add_custom_model(self, name: str, api_base: str):
        """Add a custom model configuration"""
        if not name or not api_base:
            raise ValueError("Model name and API base URL are required")
            
        config = self.load_config()
        if 'custom_models' not in config:
            config['custom_models'] = {}
            
        config['custom_models'][name] = api_base
        self.save_config(config)
    
    def remove_custom_model(self, name: str):
        """删除自定义模型"""
        config = self.load_config()
        custom_models = config.get('custom_models', {})
        
        if name not in custom_models:
            raise ValueError(f"Custom model '{name}' not found")
        
        del custom_models[name]
        self.save_config(config)
    
    def get_custom_models(self) -> dict:
        """Get all custom model configurations"""
        config = self.load_config()
        return config.get('custom_models', {})
    
    def get_model_config(self, model_name: str) -> Optional[dict]:
        """Get configuration for a specific model"""
        config = self.load_config()
        custom_models = config.get('custom_models', {})
        
        if model_name in custom_models:
            return {
                'api_base': custom_models[model_name]
            }
        return None
