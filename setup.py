# setup.py
from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="hub",
    version="1.0.0",
    description="AI Hub - Universal terminal interface for multiple AI providers (Grok, Claude, OpenAI, Gemini)",
    author="AI Hub Team",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "hub=hub.main:entry_point",
            "ai=hub.main:entry_point",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)