import click
from dotenv import load_dotenv
from pathlib import Path
from .git_utils import get_staged_diff, commit_with_message
from .openai_utils import generate_commit_message, Model
from .config import load_config, save_config, get_config_value, Config
from . import __version__
import sys

# 加载环境变量
load_dotenv()

@click.group()
@click.version_option(__version__, prog_name='aimsg', message='%(prog)s version %(version)s')
def cli():
    """AI-powered Git commit message generator."""
    pass

@cli.command()
def commit():
    """Generate commit message for staged changes."""
    try:
        # 获取 diff 和依赖文件列表
        diff, dependency_files = get_staged_diff()
        if not diff and not dependency_files:
            click.echo("No staged changes found. Please stage your changes first using 'git add'.", err=True)
            return
             
        # 获取配置
        api_key = get_config_value("api_key")
        api_base = get_config_value("api_base")
        model = get_config_value("model")
        prompt = get_config_value("prompt")

        # 生成提交消息
        commit_message = generate_commit_message(
            diff=diff,
            api_key=api_key,
            api_base=api_base,
            model=model,
            prompt_template=prompt,
            dependency_files=dependency_files
        )
        
        # 显示生成的消息
        click.echo("Generated commit message:")
        click.echo("-" * 40)
        click.echo(commit_message)
        click.echo("-" * 40)
        
        # 询问是否提交
        if click.confirm("Do you want to commit with this message?"):
            if commit_with_message(commit_message):
                click.echo("Changes committed successfully!")
            else:
                click.echo("Failed to commit changes", err=True)
        else:
            click.echo("Commit cancelled.") 

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

@cli.command()
def init():
    """Initialize or update configuration."""
    try:
        # 获取现有配置
        config = load_config()
        current_model = config.get("model")
        
        # 显示内置模型
        click.echo("\nAvailable models:")
        models = list(Model)
        for i, model in enumerate(models, 1):
            prefix = "* " if model.value == current_model else "  "
            click.echo(f"{i}. {prefix}{model.value}")
        
        # 显示自定义模型
        custom_models = config.get("custom_models", {})
        custom_start = len(models) + 1
        if custom_models:
            click.echo("\nCustom models:")
            for i, (name, api_base) in enumerate(custom_models.items(), custom_start):
                prefix = "* " if name == current_model else "  "
                click.echo(f"{i}. {prefix}{name} ({api_base})")
        
        while True:
            choice = click.prompt('\nSelect a model (enter number)', type=int)
            if 1 <= choice <= len(models):
                # 选择内置模型
                selected_model = models[choice-1]
                model_name = selected_model.value
                api_base = selected_model.api_base
                break
            elif custom_start <= choice < custom_start + len(custom_models):
                # 选择自定义模型
                name = list(custom_models.keys())[choice-custom_start]
                model_name = name
                api_base = custom_models[name]
                break
            click.echo("Invalid choice. Please try again.")
        
        # 如果选择了内置模型，询问是否要自定义 API base
        if 1 <= choice <= len(models):
            click.echo(f"\nDefault API base for {model_name}: {api_base}")
            customize = click.confirm("Do you want to use a custom API base?", default=False)
            if customize:
                api_base = click.prompt(
                    'Enter your custom API base URL',
                    type=str,
                    default=api_base
                )
        
        # 设置 API key
        api_key = click.prompt('\nEnter your API key', type=str)
        if not api_key:
            raise ValueError("API key is required")
        
        # 更新配置
        config.update({
            "api_key": api_key,
            "api_base": api_base,
            "model": model_name
        })
        
        # 保存配置
        save_config(config)
        
        # 显示配置信息
        click.echo("\nConfiguration saved:")
        click.echo(f"Model: {model_name}")
        click.echo(f"API Base: {api_base}")
        click.echo("API Key: ********" + api_key[-4:])
        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

@cli.command()
def current():
    """Show current configuration."""
    click.echo(f"Model: {get_config_value('model')}")
    click.echo(f"API Base: {get_config_value('api_base')}")
    click.echo(f"API Key: {get_config_value('api_key')}")
    click.echo(f"Prompt: {get_config_value('prompt')}")

@cli.command()
def prompt():
    """Configure custom prompt template."""
    config = load_config()
    
    current_prompt = config.get("prompt")
    
    click.echo("\nCurrent prompt template:")
    click.echo("-" * 40)
    click.echo(current_prompt)
    click.echo("-" * 40)
    
    if click.confirm("\nDo you want to modify the prompt template?"):
        click.echo("\nAvailable variables:")
        click.echo("- {diff}: The git diff content")
        click.echo("\nEnter your custom prompt template (press Ctrl+D or Ctrl+Z when finished):")
        lines = []
        try:
            while True:
                line = input()
                lines.append(line)
        except EOFError:
            new_prompt = "\n".join(lines)
            if new_prompt.strip():
                config["prompt"] = new_prompt
                save_config(config)
                click.echo("Prompt template updated successfully!")
            else:
                click.echo("Prompt template unchanged (empty input)")

@cli.command()
def reset_prompt():
    """Reset prompt template to default."""
    config = load_config()
    
    config["prompt"] = ""
    save_config(config)
    click.echo("Prompt template reset to default successfully!")

@cli.group()
def model():
    """Manage AI models."""
    pass

@model.command(name="list")
def list_models():
    """List all available models."""
    try:
        # 获取当前配置的模型
        config = load_config()
        current_model = config.get("model")
        
        click.echo("Available Models:\n")
        
        # 按服务商分组
        providers = {
            "OpenAI": {
                "models": [Model.GPT35, Model.GPT35_16K, Model.GPT4, Model.GPT4_32K, Model.GPT4_TURBO],
                "description": "OpenAI's GPT models, known for their general-purpose capabilities"
            },
            "Anthropic": {
                "models": [Model.CLAUDE2, Model.CLAUDE_INSTANT],
                "description": "Anthropic's Claude models, focused on safety and reliability"
            },
            "Google": {
                "models": [Model.PALM2, Model.GEMINI_PRO],
                "description": "Google's language models with strong reasoning capabilities"
            },
            "Aliyun": {
                "models": [Model.QIANWEN, Model.QIANWEN_PLUS],
                "description": "Aliyun's Qwen models with broad knowledge base"
            },
            "Xunfei": {
                "models": [Model.SPARK, Model.SPARK_V2],
                "description": "iFlytek's Spark models with Chinese language expertise"
            },
            "Zhipu": {
                "models": [Model.GLM4, Model.GLM3_TURBO],
                "description": "Zhipu's ChatGLM models optimized for Chinese"
            },
            "Baidu": {
                "models": [Model.ERNIE, Model.ERNIE_TURBO],
                "description": "Baidu's ERNIE models with Chinese language capabilities"
            },
            "Moonshot": {
                "models": [Model.KIMI],
                "description": "Moonshot AI's KIMI model"
            },
            "Tencent": {
                "models": [Model.HUNYUAN, Model.HUNYUAN_LITE],
                "description": "Tencent's Hunyuan models"
            },
            "ByteDance": {
                "models": [Model.DOUBAO, Model.DOUBAO_TURBO],
                "description": "ByteDance's Doubao models"
            },
            "DeepSeek": {
                "models": [Model.DEEPSEEK],
                "description": "DeepSeek's models with strong coding capabilities"
            },
            "Replicate": {
                "models": [Model.LLAMA2, Model.CODELLAMA],
                "description": "Open source models hosted by Replicate"
            },
            "Together": {
                "models": [Model.MISTRAL, Model.MIXTRAL],
                "description": "Open source models hosted by Together AI"
            }
        }
        
        # 显示内置模型
        for provider, info in providers.items():
            if info["models"]:  # 只显示有模型的提供商
                click.echo(f"{provider}:")
                click.echo(f"  Description: {info['description']}")
                click.echo("  Models:")
                for model in info["models"]:
                    prefix = "  * " if model.value == current_model else "    "
                    click.echo(f"{prefix}{model.value}")
                click.echo()
        
        # 显示自定义模型
        custom_models = config.get("custom_models", {})
        if custom_models:
            click.echo("Custom Models:")
            for name, api_base in custom_models.items():
                prefix = "* " if name == current_model else "  "
                click.echo(f"{prefix}{name}: {api_base}")
            click.echo()
        
        # 显示说明
        click.echo("Note:")
        click.echo("  * indicates the currently selected model")
        click.echo("  Use 'aimsg init' to change the current model")
        click.echo("  Use 'aimsg model add' to add a custom model")
        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

@model.command()
@click.argument('name')
@click.argument('api_base')
def add(name: str, api_base: str):
    """Add a custom model configuration"""
    try:
        config = Config()
        config.add_custom_model(name, api_base)
        click.echo(f"Successfully added custom model '{name}'")
    except Exception as e:
        click.echo(f"Failed to add custom model: {str(e)}", err=True)
        sys.exit(1)

@model.command(name='remove')
@click.argument('name')
def remove_model(name):
    """Remove a custom model"""
    try:
        config = Config()
        config.remove_custom_model(name)
        click.echo(f"Successfully removed custom model: {name}")
    except ValueError as e:
        click.echo(f"Error: {str(e)}", err=True)
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

if __name__ == "__main__":
    cli()
