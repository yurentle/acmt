from openai import OpenAI

def generate_commit_message(diff, api_key, api_base):
    """Generate commit message using OpenAI API."""
    client = OpenAI(api_key=api_key, base_url=api_base)
    
    prompt = f"""Based on the following git diff, generate a concise and descriptive commit message that follows conventional commits format.
The message should be clear and explain what changes were made and why.

Git diff:
{diff}

Generate a commit message in the format: <type>(<scope>): <description>
Where type can be: feat, fix, docs, style, refactor, test, chore
Keep the message under 72 characters if possible.
"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates clear and concise git commit messages."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=100
    )

    return response.choices[0].message.content.strip()
