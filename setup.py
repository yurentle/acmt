from setuptools import setup, find_packages

setup(
    name="aimsg",
    version="0.2.3",
    packages=find_packages(),
    install_requires=[
        "openai>=1.0.0",
        "gitpython>=3.1.40",
        "python-dotenv>=1.0.0",
        "click>=8.1.7",
    ],
    entry_points={
        "console_scripts": [
            "aimsg=aimsg.cli:cli",
        ],
    },
    author="yurentle",
    author_email="yurentle@gmail.com",
    description="A CLI tool to generate commit messages using OpenAI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yurentle/aimsg",
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Version Control :: Git",
    ],
    keywords="git commit message openai gpt cli",
)
