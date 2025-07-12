# AI Hub 🚀

> Universal AI CLI - One terminal interface for all major AI providers

AI Hub is a powerful command-line interface that provides unified access to multiple AI providers including Grok, Claude, OpenAI, and Gemini. Inspired by Claude Code, it offers a seamless chat experience with intelligent model switching and beautiful terminal UI.

## ✨ Features

- 🤖 **Multi-Provider Support**: Grok (XAI), Claude (Anthropic), OpenAI (GPT-4/3.5), Gemini (Google)
- 💬 **Interactive Chat Mode**: Claude Code-like interface with streaming responses
- 🎯 **Smart Defaults**: Automatic model selection based on your preferences
- ⚙️ **Easy Setup**: Guided first-time configuration wizard
- 🔧 **Slash Commands**: Full set of `/help`, `/config`, `/export`, `/clear`, etc.
- 🎨 **Beautiful UI**: Colored output, progress indicators, and clean formatting
- 📱 **Cross-Platform**: Works on Linux, macOS, and Windows
- 🔒 **Secure**: API keys stored locally in encrypted format

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-hub.git
cd ai-hub

# Install dependencies
pip install -r requirements.txt

# Install AI Hub
pip install -e .
```

### First Run

Simply run `hub` and follow the guided setup:

```bash
hub
```

This will walk you through:
1. 🔥 **Provider Selection** - Choose which AI services to configure
2. 🔑 **API Key Setup** - Securely enter your API keys
3. 🎯 **Model Selection** - Pick your default AI model
4. 🚀 **Ready to Chat** - Start conversing immediately!

## 💻 Usage

### Interactive Mode (Default)

```bash
hub                    # Start chat with default model
hub -m claude         # Use Claude specifically
hub -m gpt-4          # Use GPT-4
hub -m gemini         # Use Gemini
```

### Quick Queries

```bash
hub "Explain quantum computing"
hub -m claude "Write a Python function to sort a list"
hub -m gpt-4 "What's the weather like?"
```

### Configuration

```bash
hub --setup           # Reconfigure settings
hub --help            # Show all options
```

## 🎮 Interactive Commands

While in chat mode, use these commands:

| Command | Description |
|---------|-------------|
| `/help` | Show all available commands |
| `/clear` | Clear conversation history |
| `/config` | View current configuration |
| `/setup` | Reconfigure API keys |
| `/model` | Show current model info |
| `/export` | Export conversation to file |
| `/history` | Show conversation history |
| `/system [prompt]` | Set system prompt |
| `/compact` | Compress conversation with AI summary |
| `/cost` | Show session usage stats |
| `/doctor` | Check AI Hub health |
| `/exit` | Exit the chat |

## 🔧 Configuration

AI Hub stores configuration in `~/.ai-hub/config.yaml`:

```yaml
# API Keys
grok_api_key: "your-grok-key"
claude_api_key: "your-claude-key" 
openai_api_key: "your-openai-key"
gemini_api_key: "your-gemini-key"

# Settings
default_model: "grok"
max_tokens: 8192
temperature: 0.7
system_prompt: "You are a helpful AI assistant."
```

### Environment Variables

You can also set API keys via environment variables:

```bash
export GROK_API_KEY="your-grok-key"
export ANTHROPIC_API_KEY="your-claude-key"
export OPENAI_API_KEY="your-openai-key"
export GEMINI_API_KEY="your-gemini-key"
```

## 🤖 Supported Models

| Provider | Models | Description |
|----------|--------|-------------|
| **Grok (XAI)** | `grok-beta` | Latest and fastest model from X.AI |
| **Claude (Anthropic)** | `claude-3-5-sonnet` | Best for reasoning and analysis |
| **OpenAI** | `gpt-4`, `gpt-4o`, `gpt-3.5-turbo` | Most popular and versatile |
| **Gemini (Google)** | `gemini-pro` | Great for multimodal tasks |

## 📋 Requirements

- Python 3.8+
- API keys for desired providers:
  - [Grok (XAI)](https://x.ai/) - `GROK_API_KEY`
  - [Claude (Anthropic)](https://anthropic.com/) - `ANTHROPIC_API_KEY`
  - [OpenAI](https://openai.com/) - `OPENAI_API_KEY`
  - [Gemini (Google)](https://ai.google.dev/) - `GEMINI_API_KEY`

## 🛠️ Development

### Project Structure

```
ai-hub/
├── hub/                    # Main package
│   ├── cli.py             # CLI interface and argument parsing
│   ├── config.py          # Configuration management
│   ├── interactive.py     # Interactive chat session
│   ├── clients/           # AI provider clients
│   │   ├── base.py        # Base client interface
│   │   ├── grok.py        # Grok/XAI client
│   │   ├── claude.py      # Claude/Anthropic client
│   │   ├── openai_client.py # OpenAI client
│   │   └── gemini.py      # Gemini/Google client
│   └── utils/             # Utilities
│       ├── formatting.py  # Text formatting and colors
│       └── terminal.py    # Terminal utilities
├── setup.py               # Package setup
├── requirements.txt       # Dependencies
└── README.md             # This file
```

### Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🎯 Roadmap

- [ ] **Plugin System** - Custom AI provider plugins
- [ ] **Conversation Management** - Save/load chat sessions
- [ ] **Template System** - Reusable prompt templates
- [ ] **Voice Interface** - Speech-to-text and text-to-speech
- [ ] **Multi-Modal Support** - Image and file uploads
- [ ] **Team Features** - Shared configurations and sessions
- [ ] **Web Interface** - Optional browser-based UI
- [ ] **Model Comparison** - Side-by-side responses

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by [Claude Code](https://claude.ai/code) - Anthropic's excellent CLI interface
- Built with love for the AI community
- Thanks to all AI providers for their amazing APIs

---

<div align="center">

**Made with ❤️ by the AI Hub Team**

[⭐ Star us on GitHub](https://github.com/yourusername/ai-hub) • [🐦 Follow on Twitter](https://twitter.com/aihub) • [📝 Read the Docs](https://docs.ai-hub.dev)

</div>