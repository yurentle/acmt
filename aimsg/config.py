import os
import json
from pathlib import Path
from typing import Dict, Optional

CONFIG_DIR = os.path.expanduser("~/.config/aimsg")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

DEFAULT_CONFIG = {
    "custom_models": {},  # 用户自定义模型
    "default_model": "gpt-3.5-turbo",  # 默认模型
}

def ensure_config_dir():
    """确保配置目录存在"""
    os.makedirs(CONFIG_DIR, exist_ok=True)

def load_config() -> dict:
    """加载配置文件"""
    ensure_config_dir()
    if not os.path.exists(CONFIG_FILE):
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
    
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return DEFAULT_CONFIG

def save_config(config: dict):
    """保存配置文件"""
    ensure_config_dir()
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def add_custom_model(name: str, model_id: str, api_base: str):
    """添加自定义模型"""
    config = load_config()
    config.setdefault('custom_models', {})
    config['custom_models'][name] = {
        'model_id': model_id,
        'api_base': api_base
    }
    save_config(config)

def remove_custom_model(name: str):
    """删除自定义模型"""
    config = load_config()
    
    if name not in config.get("custom_models", {}):
        raise ValueError(f"Custom model '{name}' not found")
    
    # 如果是默认模型，重置为默认的 GPT-3.5
    if config.get("default_model") == name:
        config["default_model"] = "gpt-3.5-turbo"
    
    del config["custom_models"][name]
    save_config(config)

def get_custom_model(name: str) -> Optional[Dict]:
    """获取自定义模型配置"""
    config = load_config()
    return config.get('custom_models', {}).get(name)

def list_custom_models() -> Dict:
    """列出所有自定义模型"""
    config = load_config()
    return config.get('custom_models', {})

def set_default_model(model: str):
    """设置默认模型"""
    config = load_config()
    config["default_model"] = model
    save_config(config)

def get_default_model() -> str:
    """获取默认模型"""
    config = load_config()
    return config.get("default_model", "gpt-3.5-turbo")
