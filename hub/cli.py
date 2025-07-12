# hub/cli.py
import argparse
import sys
import os
from typing import Optional

from .config import Config
from .interactive import InteractiveSession
from .clients.grok import GrokClient
from .clients.claude import ClaudeClient
from .clients.gemini import GeminiClient
from .clients.openai_client import OpenAIClient
from .utils.formatting import print_response, print_error, print_info, print_bold
from .utils.terminal import setup_terminal
import getpass


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="hub",
        description="AI Hub - Universal terminal interface for multiple AI providers",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--model", "-m",
        choices=["grok", "claude", "gemini", "gpt-4", "gpt-3.5-turbo", "gpt-4o"],
        default="grok",
        help="Choose the AI model to use (default: grok)"
    )
    
    parser.add_argument(
        "--config", "-c",
        type=str,
        help="Path to config file"
    )
    
    parser.add_argument(
        "--interactive", "-i",
        action="store_true",
        help="Start interactive mode"
    )
    
    parser.add_argument(
        "--setup",
        action="store_true",
        help="Setup API keys and configuration"
    )
    
    parser.add_argument(
        "--version", "-v",
        action="version",
        version="Grok4 CLI 1.0.0"
    )
    
    parser.add_argument(
        "prompt",
        nargs="*",
        help="The prompt to send to the AI model"
    )
    
    return parser


def show_welcome_message():
    print("╭───────────────────────────────────────────────────╮")
    print("│ ✻ Welcome to AI Hub!                             │")
    print("│                                                   │")
    print("│   --setup to configure API keys                  │")
    print("│   -i for interactive mode                         │")
    print("│                                                   │")
    print("│   Universal AI interface (Grok, Claude, GPT...)  │")
    print("╰───────────────────────────────────────────────────╯")
    print()
    print(" Tips for getting started:")
    print()
    print(" 1. Run hub --setup to configure your API keys")
    print(" 2. Use hub -i for interactive chat mode")
    print(" 3. Use hub -m claude to switch models")
    print(" 4. Use hub -m gpt-4 for OpenAI GPT-4")
    print(" 5. Use hub -m gemini for Google Gemini")
    print()


def setup_configuration(config: Config) -> int:
    print_bold("🔧 AI Hub Setup")
    print_info("Configure your API keys for multiple AI providers")
    print()
    
    # Grok API Key
    current_grok = "✓ Set" if config.grok_api_key else "✗ Not set"
    print(f"Grok API Key: {current_grok}")
    
    if input("Configure Grok API key? (y/N): ").lower().startswith('y'):
        grok_key = getpass.getpass("Enter your Grok API key: ").strip()
        if grok_key:
            config.set_grok_api_key(grok_key)
            print_info("✓ Grok API key saved")
        else:
            print_error("No key entered")
    
    print()
    
    # Claude API Key
    current_claude = "✓ Set" if config.claude_api_key else "✗ Not set"
    print(f"Claude API Key: {current_claude}")
    
    if input("Configure Claude API key? (y/N): ").lower().startswith('y'):
        claude_key = getpass.getpass("Enter your Claude API key: ").strip()
        if claude_key:
            config.set_claude_api_key(claude_key)
            print_info("✓ Claude API key saved")
        else:
            print_error("No key entered")
    
    print()
    
    # OpenAI API Key
    current_openai = "✓ Set" if config.openai_api_key else "✗ Not set"
    print(f"OpenAI API Key: {current_openai}")
    
    if input("Configure OpenAI API key? (y/N): ").lower().startswith('y'):
        openai_key = getpass.getpass("Enter your OpenAI API key: ").strip()
        if openai_key:
            config.set_openai_api_key(openai_key)
            print_info("✓ OpenAI API key saved")
        else:
            print_error("No key entered")
    
    print()
    
    # Gemini API Key
    current_gemini = "✓ Set" if config.gemini_api_key else "✗ Not set"
    print(f"Gemini API Key: {current_gemini}")
    
    if input("Configure Gemini API key? (y/N): ").lower().startswith('y'):
        gemini_key = getpass.getpass("Enter your Gemini API key: ").strip()
        if gemini_key:
            config.set_gemini_api_key(gemini_key)
            print_info("✓ Gemini API key saved")
        else:
            print_error("No key entered")
    
    print()
    
    # Default model
    print(f"Current default model: {config.default_model}")
    if input("Change default model? (y/N): ").lower().startswith('y'):
        print("1. grok")
        print("2. claude")
        print("3. gpt-4")
        print("4. gpt-3.5-turbo")
        print("5. gemini")
        choice = input("Choose (1-5): ").strip()
        models = {"1": "grok", "2": "claude", "3": "gpt-4", "4": "gpt-3.5-turbo", "5": "gemini"}
        if choice in models:
            config.set_default_model(models[choice])
            print_info(f"✓ Default model set to {models[choice]}")
    
    print()
    print_info(f"Configuration saved to: {config.config_path}")
    print_info("You can now use: hub -i")
    
    return 0


def has_any_api_key(config: Config) -> bool:
    """Check if user has configured any API key"""
    return bool(config.grok_api_key or config.claude_api_key or config.openai_api_key or config.gemini_api_key)


def first_time_setup(config: Config) -> int:
    """Interactive first-time setup wizard"""
    print("╭───────────────────────────────────────────────────╮")
    print("│ ✻ Welcome to AI Hub!                             │")
    print("│                                                   │")
    print("│   First time setup - Let's get you started!      │")
    print("╰───────────────────────────────────────────────────╯")
    print()
    print_info("AI Hub supports multiple AI providers. Let's configure at least one:")
    print()
    print("Available providers:")
    print("1. 🔥 Grok (XAI) - Latest and fastest")
    print("2. 🧠 Claude (Anthropic) - Best for reasoning")
    print("3. 🚀 OpenAI (GPT-4, GPT-3.5) - Most popular")
    print("4. 🌟 Gemini (Google) - Great multimodal")
    print()
    
    configured_any = False
    
    # Ask about each provider
    if input("Configure Grok? (Y/n): ").lower() != 'n':
        grok_key = getpass.getpass("Enter your Grok API key: ").strip()
        if grok_key:
            config.set_grok_api_key(grok_key)
            print_info("✓ Grok configured!")
            configured_any = True
        print()
    
    if input("Configure Claude? (Y/n): ").lower() != 'n':
        claude_key = getpass.getpass("Enter your Claude API key: ").strip()
        if claude_key:
            config.set_claude_api_key(claude_key)
            print_info("✓ Claude configured!")
            configured_any = True
        print()
    
    if input("Configure OpenAI? (Y/n): ").lower() != 'n':
        openai_key = getpass.getpass("Enter your OpenAI API key: ").strip()
        if openai_key:
            config.set_openai_api_key(openai_key)
            print_info("✓ OpenAI configured!")
            configured_any = True
        print()
    
    if input("Configure Gemini? (Y/n): ").lower() != 'n':
        gemini_key = getpass.getpass("Enter your Gemini API key: ").strip()
        if gemini_key:
            config.set_gemini_api_key(gemini_key)
            print_info("✓ Gemini configured!")
            configured_any = True
        print()
    
    if not configured_any:
        print_error("No API keys configured. You need at least one to use AI Hub.")
        print_info("You can run 'hub --setup' later to configure API keys.")
        return 1
    
    # Choose default model
    print_info("Choose your default model:")
    available_models = []
    if config.grok_api_key:
        available_models.append(("1", "grok", "Grok"))
    if config.claude_api_key:
        available_models.append((str(len(available_models)+1), "claude", "Claude"))
    if config.openai_api_key:
        available_models.append((str(len(available_models)+1), "gpt-4", "GPT-4"))
    if config.gemini_api_key:
        available_models.append((str(len(available_models)+1), "gemini", "Gemini"))
    
    for num, model_id, name in available_models:
        print(f"{num}. {name}")
    
    choice = input(f"Choose default model (1-{len(available_models)}): ").strip()
    
    for num, model_id, name in available_models:
        if choice == num:
            config.set_default_model(model_id)
            print_info(f"✓ Default model set to {name}")
            break
    
    print()
    print_info("🎉 Setup complete! Starting AI Hub...")
    print_info("You can always run 'hub --setup' to change settings.")
    print()
    
    return 0


def main():
    parser = create_parser()
    args = parser.parse_args()
    
    # Load configuration
    config = Config(args.config)
    
    # Setup terminal
    setup_terminal()
    
    # Handle setup command
    if args.setup:
        return setup_configuration(config)
    
    # Check if this is first time (no API keys configured)
    if not has_any_api_key(config):
        result = first_time_setup(config)
        if result != 0:
            return result
        # Reload config after setup
        config = Config(args.config)
    
    # If no arguments, start interactive mode by default
    if not args.prompt and not args.interactive and not args.setup:
        args.interactive = True
    
    # Use default model if not specified
    model = args.model if args.model != "grok" or config.grok_api_key else config.default_model
    
    # Create client based on model choice
    if model == "grok":
        if not config.grok_api_key:
            print_error("Grok API key not found. Please run 'hub --setup' to configure.")
            return 1
        client = GrokClient(config.grok_api_key)
    elif model == "claude":
        if not config.claude_api_key:
            print_error("Claude API key not found. Please run 'hub --setup' to configure.")
            return 1
        client = ClaudeClient(config.claude_api_key)
    elif model == "gemini":
        if not config.gemini_api_key:
            print_error("Gemini API key not found. Please run 'hub --setup' to configure.")
            return 1
        client = GeminiClient(config.gemini_api_key)
    elif model in ["gpt-4", "gpt-3.5-turbo", "gpt-4o"]:
        if not config.openai_api_key:
            print_error("OpenAI API key not found. Please run 'hub --setup' to configure.")
            return 1
        client = OpenAIClient(config.openai_api_key, model)
    else:
        print_error(f"Unsupported model: {model}")
        return 1
    
    # Handle interactive mode
    if args.interactive or not args.prompt:
        session = InteractiveSession(client, config)
        try:
            session.run()
        except KeyboardInterrupt:
            print("\nGoodbye!")
        return 0
    
    # Handle single prompt
    prompt = " ".join(args.prompt)
    if not prompt.strip():
        print_error("Please provide a prompt or use --interactive mode")
        return 1
    
    try:
        response = client.chat(prompt)
        print_response(response)
    except Exception as e:
        print_error(f"Error: {e}")
        return 1
    
    return 0