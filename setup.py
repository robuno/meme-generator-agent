#!/usr/bin/env python3
"""
Setup script for Meme Generator Agent
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="meme-generator-agent",
    version="1.0.0",
    author="AI Meme Generator",
    author_email="your.email@example.com",
    description="A powerful AI agent that generates hilarious memes using Hugging Face models and Imgflip API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/robuno/meme-generator-ai-agent",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Artistic Software",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "meme-generator=main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="meme, ai, artificial-intelligence, humor, image-generation, huggingface, imgflip",
    project_urls={
        "Bug Reports": "https://github.com/robuno/meme-generator-ai-agent/issues",
        "Source": "https://github.com/robuno/meme-generator-ai-agent",
        "Documentation": "https://github.com/robuno/meme-generator-ai-agent#readme",
    },
) 