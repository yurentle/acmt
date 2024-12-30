import os
import sys
import click
import json
from dotenv import load_dotenv
from pathlib import Path
from git_utils import get_staged_diff
from openai_utils import generate_commit_message, DEFAULT_PROMPT

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
    return get_config_dir() / "config.env"

def get_prompt_file():
    """Get the path to the prompt configuration file."""
    return get_config_dir() / "prompt.json"

# Try to load environment variables from config file
config_file = get_config_file()
if config_file.exists():
    load_dotenv(config_file)

def load_prompt():
    """Load custom prompt from configuration."""
    prompt_file = get_prompt_file()
    if prompt_file.exists():
        try:
            return json.loads(prompt_file.read_text())
        except json.JSONDecodeError:
            return {"prompt": DEFAULT_PROMPT}
    return {"prompt": DEFAULT_PROMPT}

def save_config(api_key, api_base=None):
    """Save configuration to config file in user's config directory."""
    config_file = get_config_file()
    content = [f"OPENAI_API_KEY={api_key}"]
    if api_base:
        content.append(f"OPENAI_API_BASE={api_base}")
    
    try:
        config_file.write_text("\n".join(content))
        click.echo(f"Configuration saved to {config_file}")
    except PermissionError:
        click.echo("Error: Unable to save configuration. Please check file permissions.", err=True)
        sys.exit(1)

def save_prompt(prompt):
    """Save custom prompt to configuration file."""
    prompt_file = get_prompt_file()
    try:
        prompt_file.write_text(json.dumps({"prompt": prompt}, indent=2))
        click.echo(f"Prompt configuration saved to {prompt_file}")
    except PermissionError:
        click.echo("Error: Unable to save prompt configuration. Please check file permissions.", err=True)
        sys.exit(1)

@click.group()
def cli():
    """AI-powered commit message generator."""
    pass

@cli.command()
def init():
    """Initialize configuration for the tool."""
    api_key = click.prompt("Please enter your OpenAI API key", type=str)
    
    use_proxy = click.confirm("Do you want to use a custom API base URL (proxy)?", default=False)
    api_base = None
    if use_proxy:
        api_base = click.prompt("Please enter the API base URL", type=str)
    
    save_config(api_key, api_base)
    click.echo("Configuration completed successfully!")

@cli.command()
def prompt():
    """Configure custom prompt template."""
    current_prompt = load_prompt()["prompt"]
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
                save_prompt(new_prompt)
                click.echo("Prompt template updated successfully!")
            else:
                click.echo("Prompt template unchanged (empty input)")

@cli.command()
def reset_prompt():
    """Reset prompt template to default."""
    save_prompt(DEFAULT_PROMPT)
    click.echo("Prompt template reset to default successfully!")

@cli.command()
@click.option(
    "--api-base",
    help="Custom OpenAI API base URL",
    default=lambda: os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1"),
)
def commit(api_base):
    """Generate commit message using OpenAI based on staged changes."""
    # Check for OpenAI API key
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        click.echo("Error: OpenAI API key not found. Please run 'aimsg init' first.", err=True)
        return

    try:
        # Get git diff
        diff = get_staged_diff()
        if not diff:
            click.echo("No staged changes found. Please stage your changes first using 'git add'", err=True)
            return

        # Load custom prompt
        prompt_template = load_prompt()["prompt"]
        
        # Generate commit message
        commit_message = generate_commit_message(diff, api_key, api_base, prompt_template)
        
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

if __name__ == "__main__":
    cli()
