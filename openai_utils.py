from openai import OpenAI
from enum import Enum

class Model(str, Enum):
    GPT35 = "gpt-3.5-turbo"
    DEEPSEEK = "deepseek-chat"

DEFAULT_MODEL = Model.GPT35

# Model-specific API base URLs
MODEL_API_BASES = {
    Model.DEEPSEEK: "https://api.deepseek.com"
}

DEFAULT_PROMPT = """Based on the following git diff, generate a concise and descriptive commit message that follows conventional commits format.
The message should be clear and explain what changes were made and why.

Git diff:
{diff}

Generate a commit message in the format: <type>(<scope>): <description>
Where type can be: feat, fix, docs, style, refactor, test, chore
Keep the message under 72 characters if possible."""

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
    raise ValueError(f"Unknown model: {model}")

def generate_commit_message(diff, api_key, api_base, model=None, prompt_template=None):
    """Generate commit message using OpenAI API."""
    model_name = model or DEFAULT_MODEL
    
    # If model has a specific API base and none is provided, use the model's default
    if not api_base and model_name in MODEL_API_BASES:
        api_base = MODEL_API_BASES[model_name]
    
    client = OpenAI(api_key=api_key, base_url=api_base)
    
    # Use custom prompt template if provided, otherwise use default
    prompt = (prompt_template or DEFAULT_PROMPT).format(diff=diff)
    
    # Get model settings
    settings = get_model_settings(model_name)

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": settings["system_message"]},
            {"role": "user", "content": prompt}
        ],
        temperature=settings["temperature"],
        max_tokens=settings["max_tokens"]
    )

    return response.choices[0].message.content.strip()
