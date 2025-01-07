import os
import sys
import click
import json
from dotenv import load_dotenv
from pathlib import Path
from aimsg.git_utils import get_staged_diff
from aimsg.openai_utils import (
    generate_commit_message,
    DEFAULT_PROMPT,
    Model,
    DEFAULT_MODEL,
    MODEL_API_BASES
)
from aimsg.utils import Spinner
from aimsg.config import (
    add_custom_model, remove_custom_model, list_custom_models,
    set_default_model, get_default_model, get_custom_model
)

def get_config_dir():
    """Get the user's configuration directory."""
    # On macOS, use ~/Library/Application Support/aimsg
    if sys.platform == "darwin":
        config_dir = Path.home() / "Library" / "Application Support" / "aimsg"
    # On Linux, use ~/.config/aimsg
    else:
        config_dir = Path.home() / ".config" / "aimsg"
    
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir

def get_config_file():
    """Get the path to the configuration file."""
    return get_config_dir() / "config.json"

def load_config():
    """Load configuration from file."""
    config_file = get_config_file()
    default_config = {
        "openai_api_key": None,
        "openai_api_base": "https://api.openai.com/v1",
        "model": DEFAULT_MODEL.value,
        "prompt": DEFAULT_PROMPT
    }
    
    if config_file.exists():
        try:
            config = json.loads(config_file.read_text())
            # Convert model string to enum if present
            if "model" in config:
                config["model"] = Model(config["model"])
            return {**default_config, **config}
        except (json.JSONDecodeError, ValueError):
            return default_config
    return default_config

def save_config(config):
    """Save configuration to file."""
    config_file = get_config_file()
    try:
        # Convert enum to string for JSON serialization
        if "model" in config and isinstance(config["model"], Model):
            config = {**config, "model": config["model"].value}
        config_file.write_text(json.dumps(config, indent=2))
        click.echo(f"Configuration saved to {config_file}")
    except PermissionError:
        click.echo("Error: Unable to save configuration. Please check file permissions.", err=True)
        sys.exit(1)

def update_config(**kwargs):
    """Update specific configuration values."""
    config = load_config()
    config.update(kwargs)
    save_config(config)

def get_default_api_base(model: Model) -> str:
    """Get the default API base URL for a model."""
    return MODEL_API_BASES.get(model, "https://api.openai.com/v1")

@click.group()
def cli():
    """AI-powered commit message generator."""
    pass

@cli.command()
def init():
    """Initialize configuration for the tool."""
    # First, let user select the model
    click.echo("\nAvailable models:")
    models = [(i + 1, m) for i, m in enumerate(Model)]
    default_index = next(i for i, (_, m) in enumerate(models) if m == DEFAULT_MODEL)
    
    for i, model in models:
        is_default = model == DEFAULT_MODEL
        api_base = get_default_api_base(model)
        click.echo(f"{i}. {model.value} (API: {api_base})" + (" (default)" if is_default else ""))
    
    while True:
        try:
            choice = click.prompt(
                "\nSelect model by number",
                type=int,
                default=default_index + 1
            )
            if 1 <= choice <= len(models):
                selected_model = models[choice - 1][1]
                break
            click.echo(f"Please enter a number between 1 and {len(models)}")
        except ValueError:
            click.echo("Please enter a valid number")
    
    click.echo(f"\nSelected model: {selected_model.value}")
    
    # Get the default API base for the selected model
    default_api_base = get_default_api_base(selected_model)
    click.echo(f"Default API base URL for this model: {default_api_base}")
    
    # Then configure API key and base URL
    api_key = click.prompt("\nPlease enter your API key", type=str)
    
    use_custom_url = click.confirm("\nDo you want to use a custom API base URL?", default=False)
    if use_custom_url:
        api_base = click.prompt("Enter custom API base URL", type=str)
    else:
        api_base = default_api_base
    
    update_config(
        openai_api_key=api_key,
        openai_api_base=api_base,
        model=selected_model
    )
    click.echo("\nConfiguration completed successfully!")

@cli.command()
def model():
    """Configure the model and API base URL."""
    config = load_config()
    current_model = config["model"]
    current_api_base = config["openai_api_base"]
    
    click.echo("\nCurrent configuration:")
    click.echo(f"Model: {current_model.value}")
    click.echo(f"API Base URL: {current_api_base}")
    
    click.echo("\nAvailable models:")
    models = [(i + 1, m) for i, m in enumerate(Model)]
    current_index = next(i for i, (_, m) in enumerate(models) if m == current_model)
    
    for i, model in models:
        is_current = model == current_model
        api_base = get_default_api_base(model)
        click.echo(f"{i}. {model.value} (API: {api_base})" + (" (current)" if is_current else ""))
    
    while True:
        try:
            choice = click.prompt(
                "\nSelect model by number",
                type=int,
                default=current_index + 1
            )
            if 1 <= choice <= len(models):
                selected_model = models[choice - 1][1]
                break
            click.echo(f"Please enter a number between 1 and {len(models)}")
        except ValueError:
            click.echo("Please enter a valid number")
    
    # Get the default API base for the selected model
    default_api_base = get_default_api_base(selected_model)
    
    # If the model changed and it has a specific API base
    if selected_model != current_model and selected_model in MODEL_API_BASES:
        click.echo(f"\nNote: {selected_model.value} requires using its API: {default_api_base}")
        api_base = default_api_base
    # Otherwise, ask if user wants to modify API base URL
    else:
        if click.confirm("\nDo you want to modify the API base URL?", default=False):
            use_default = click.confirm(
                f"Use default API URL for this model ({default_api_base})?",
                default=True
            )
            if use_default:
                api_base = default_api_base
            else:
                api_base = click.prompt("Enter custom API base URL", type=str, default=current_api_base)
        else:
            api_base = current_api_base
    
    # Only update if something changed
    if selected_model != current_model or api_base != current_api_base:
        update_config(
            model=selected_model,
            openai_api_base=api_base
        )
        click.echo("\nConfiguration updated:")
        if selected_model != current_model:
            click.echo(f"- Model: {selected_model.value}")
        if api_base != current_api_base:
            click.echo(f"- API Base URL: {api_base}")
    else:
        click.echo("\nConfiguration unchanged")

@cli.command()
def prompt():
    """Configure custom prompt template."""
    config = load_config()
    current_prompt = config["prompt"]
    
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
                update_config(prompt=new_prompt)
                click.echo("Prompt template updated successfully!")
            else:
                click.echo("Prompt template unchanged (empty input)")

@cli.command()
def reset_prompt():
    """Reset prompt template to default."""
    update_config(prompt=DEFAULT_PROMPT)
    click.echo("Prompt template reset to default successfully!")

@cli.command()
@click.option(
    "--api-base",
    help="Custom OpenAI API base URL",
    default=None,
)
def commit(api_base):
    """Generate commit message using OpenAI based on staged changes."""
    config = load_config()
    
    # Check for OpenAI API key
    if not config["openai_api_key"]:
        click.echo("Error: OpenAI API key not found. Please run 'aimsg init' first.", err=True)
        return

    try:
        # Get git diff
        diff = get_staged_diff()
        if not diff:
            click.echo("No staged changes found. Please stage your changes first using 'git add'", err=True)
            return

        # Use command line api_base if provided, otherwise use from config
        api_base = api_base or config["openai_api_base"]
        
        # Generate commit message with loading spinner
        with Spinner(f"Generating commit message using {config['model'].value}..."):
            commit_message = generate_commit_message(
                diff, 
                config["openai_api_key"], 
                api_base,
                model=config["model"],
                prompt_template=config["prompt"]
            )
        
        # Output the generated message
        click.echo("\nGenerated commit message:")
        click.echo("-" * 40)
        click.echo(commit_message)
        click.echo("-" * 40)
        
        # Ask if user wants to use this message
        if click.confirm("\nDo you want to commit with this message?"):
            os.system(f'git commit -m "{commit_message}"')
            click.echo("Changes committed successfully!")
        else:
            click.echo("Commit cancelled.")

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

@cli.group()
def model():
    """Manage custom models"""
    pass

@model.command(name='add')
@click.argument('name')
@click.argument('model_id')
@click.argument('api_base')
def add_model(name, model_id, api_base):
    """Add a custom model"""
    try:
        add_custom_model(name, model_id, api_base)
        click.echo(f"Successfully added custom model: {name}")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

@model.command(name='remove')
@click.argument('name')
def remove_model(name):
    """Remove a custom model"""
    try:
        remove_custom_model(name)
        click.echo(f"Successfully removed custom model: {name}")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

@model.command(name='use')
@click.argument('name')
def use_model(name):
    """Set the default model to use"""
    try:
        # 检查是否是内置模型
        try:
            Model(name)
            set_default_model(name)
            click.echo(f"Successfully set default model to: {name}")
            return
        except ValueError:
            pass
        
        # 检查是否是自定义模型
        custom_model = get_custom_model(name)
        if custom_model:
            set_default_model(name)
            click.echo(f"Successfully set default model to: {name}")
        else:
            click.echo(f"Error: Model '{name}' not found. Use 'aimsg model list' to see available models.")
            
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

@model.command(name='list')
def list_models():
    """List all available models, including built-in and custom models"""
    try:
        # 获取当前默认模型
        default_model = get_default_model()
        
        # 显示内置模型
        click.echo("Built-in models:")
        
        # 按类别组织模型
        categories = {
            "OpenAI Models": [],
            "Anthropic Models": [],
            "Google Models": [],
            "Chinese Models": [],
            "Open Source Models": []
        }
        
        # 将模型分类
        for model in Model:
            if "gpt" in model.value:
                categories["OpenAI Models"].append(model)
            elif "claude" in model.value:
                categories["Anthropic Models"].append(model)
            elif "palm" in model.value or "gemini" in model.value:
                categories["Google Models"].append(model)
            elif any(name in model.value for name in ["qwen", "spark", "baichuan", "glm", "ernie", "kimi", "hunyuan", "doubao"]):
                categories["Chinese Models"].append(model)
            elif any(name in model.value for name in ["deepseek", "llama", "mistral", "mixtral", "codellama"]):
                categories["Open Source Models"].append(model)
        
        # 显示每个类别的模型
        for category, models in categories.items():
            if models:
                click.echo(f"\n{category}:")
                for model in models:
                    api_base = MODEL_API_BASES.get(model, "Default OpenAI endpoint")
                    # 标记默认模型
                    default_mark = " (default)" if model.value == default_model else ""
                    click.echo(f"  {model.value}{default_mark}")
                    click.echo(f"    API Base: {api_base}")
        
        # 显示自定义模型
        custom_models = list_custom_models()
        if custom_models:
            click.echo("\nCustom models:")
            for name, config in custom_models.items():
                # 标记默认模型
                default_mark = " (default)" if name == default_model else ""
                click.echo(f"  {name}{default_mark}:")
                click.echo(f"    Model ID: {config['model_id']}")
                click.echo(f"    API Base: {config['api_base']}")
        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

@model.command(name='select')
def select_model():
    """Select a model interactively"""
    try:
        # 获取当前默认模型
        default_model = get_default_model()
        
        # 收集所有模型
        all_models = []
        
        # 收集内置模型
        categories = {
            "OpenAI Models": [],
            "Anthropic Models": [],
            "Google Models": [],
            "Chinese Models": [],
            "Open Source Models": []
        }
        
        for model in Model:
            if "gpt" in model.value:
                categories["OpenAI Models"].append(model)
            elif "claude" in model.value:
                categories["Anthropic Models"].append(model)
            elif "palm" in model.value or "gemini" in model.value:
                categories["Google Models"].append(model)
            elif any(name in model.value for name in ["qwen", "spark", "baichuan", "glm", "ernie", "kimi", "hunyuan", "doubao"]):
                categories["Chinese Models"].append(model)
            elif any(name in model.value for name in ["deepseek", "llama", "mistral", "mixtral", "codellama"]):
                categories["Open Source Models"].append(model)
        
        # 显示所有模型
        click.echo("Available models:")
        click.echo("---------------")
        
        index = 1
        model_map = {}
        
        # 显示内置模型
        for category, models in categories.items():
            if models:
                click.echo(f"\n{category}:")
                for model in models:
                    default_mark = " (current)" if model.value == default_model else ""
                    click.echo(f"{index}. {model.value}{default_mark}")
                    model_map[index] = model.value
                    index += 1
        
        # 显示自定义模型
        custom_models = list_custom_models()
        if custom_models:
            click.echo("\nCustom Models:")
            for name in custom_models:
                default_mark = " (current)" if name == default_model else ""
                click.echo(f"{index}. {name}{default_mark}")
                model_map[index] = name
                index += 1
        
        # 获取用户选择
        while True:
            try:
                choice = click.prompt("\nEnter the number of the model to use (0 to cancel)", type=int)
                if choice == 0:
                    click.echo("Operation cancelled")
                    return
                
                if choice in model_map:
                    selected_model = model_map[choice]
                    set_default_model(selected_model)
                    click.echo(f"\nSuccessfully set default model to: {selected_model}")
                    return
                else:
                    click.echo("Invalid choice. Please try again.")
            except click.exceptions.Abort:
                click.echo("\nOperation cancelled")
                return
            except ValueError:
                click.echo("Please enter a valid number")
        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

if __name__ == "__main__":
    cli()
