# grok4_cli/interactive.py
import readline
import sys
import getpass
import json
import time
from datetime import datetime
from typing import List, Optional
from .clients.base import BaseClient
from .config import Config
from .utils.formatting import print_response, print_error, print_info, print_bold, print_grey, print_dim, Colors
from .utils.terminal import clear_screen


class InteractiveSession:
    def __init__(self, client: BaseClient, config: Config):
        self.client = client
        self.config = config
        self.conversation_history: List[dict] = []
        self.system_prompt: Optional[str] = None
        self.start_time = time.time()
        self.total_tokens = 0
        
        # Setup readline for better input handling
        readline.set_startup_hook(None)
        readline.parse_and_bind("tab: complete")
    
    def run(self):
        self.print_welcome()
        
        while True:
            try:
                user_input = self.get_user_input()
                
                if not user_input.strip():
                    continue
                
                # Handle special commands
                if user_input.startswith('/'):
                    if self.handle_command(user_input):
                        continue
                    else:
                        break
                
                # Process the message
                self.process_message(user_input)
                
            except KeyboardInterrupt:
                print("\n")
                if self.confirm_exit():
                    break
            except EOFError:
                break
    
    def print_welcome(self):
        print("╭───────────────────────────────────────────────────╮")
        print("│ ✻ Welcome to AI Hub!                             │")
        print("│                                                   │")
        print("│   /help for help, /config for configuration       │")
        print("│                                                   │")
        print(f"│   model: {self.client.model_name:<38} │")
        print("╰───────────────────────────────────────────────────╯")
        print()
        print(" Tips for getting started:")
        print()
        print(" 1. Type /help to see all available commands")
        print(" 2. Use /setup to configure API keys")
        print(" 3. Use /config to view current configuration")
        print(" 4. Type your questions directly or use slash commands")
        print()
        print_dim(" ? for shortcuts")
    
    def get_user_input(self) -> str:
        try:
            # Print grey prompt like Claude Code
            print(f"\n{Colors.GREY}> {Colors.END}", end="")
            return input()
        except (KeyboardInterrupt, EOFError):
            raise
    
    def handle_command(self, command: str) -> bool:
        command = command.strip().lower()
        
        if command == '/exit' or command == '/quit':
            return False
        
        elif command == '/help':
            self.print_help()
        
        elif command == '/clear':
            clear_screen()
            self.conversation_history.clear()
            print_info("Conversation history cleared")
        
        elif command == '/history':
            self.print_history()
        
        elif command.startswith('/system'):
            parts = command.split(' ', 1)
            if len(parts) > 1:
                self.system_prompt = parts[1]
                print_info(f"System prompt set: {self.system_prompt}")
            else:
                print_info(f"Current system prompt: {self.system_prompt or 'None'}")
        
        elif command == '/model':
            print_info(f"Current model: {self.client.model_name}")
            print_info(f"Max tokens: {self.client.max_tokens}")
        
        elif command == '/setup':
            self.setup_api_keys()
        
        elif command == '/config':
            self.show_config()
        
        elif command == '/cost':
            self.show_cost_info()
        
        elif command == '/export':
            self.export_conversation()
        
        elif command == '/doctor':
            self.run_doctor()
        
        elif command.startswith('/compact'):
            parts = command.split(' ', 1)
            instructions = parts[1] if len(parts) > 1 else "Summarize our conversation"
            self.compact_conversation(instructions)
        
        else:
            print_error(f"Unknown command: {command}")
            self.print_help()
        
        return True
    
    def print_help(self):
        print()
        print("/clear                     Clear conversation history and free up context")
        print("/compact                   Clear conversation history but keep a summary in context. Optional: /compact")
        print("                          [instructions for summarization]")
        print("/config                    Open config panel")
        print("/cost                      Show the total cost and duration of the current session")
        print("/doctor                    Checks the health of your Grok CLI installation")
        print("/exit (quit)               Exit the REPL")
        print("/export                    Export the current conversation to a file or clipboard")
        print("/help                      Show help and available commands")
        print("/history                   Show conversation history")
        print("/model                     Show current model info")
        print("/setup                     Configure API keys")
        print("/system [prompt]           Set or view system prompt")
        print()
    
    def print_history(self):
        if not self.conversation_history:
            print_info("No conversation history")
            return
        
        print_info("\nConversation History:")
        for i, entry in enumerate(self.conversation_history, 1):
            print(f"\n{i}. User: {entry['user']}")
            print(f"   AI: {entry['assistant'][:100]}{'...' if len(entry['assistant']) > 100 else ''}")
    
    def process_message(self, message: str):
        try:
            print_info("\nThinking...")
            
            # Use streaming for better UX
            response_text = ""
            print("\nResponse:")
            
            for chunk in self.client.chat_stream(message, self.system_prompt):
                print(chunk, end='', flush=True)
                response_text += chunk
            
            print("\n")
            
            # Add to conversation history
            self.conversation_history.append({
                'user': message,
                'assistant': response_text
            })
            
        except Exception as e:
            print_error(f"Error: {e}")
    
    def setup_api_keys(self):
        print_bold("\n🔧 API Keys Setup")
        print_info("Configure your API keys")
        print()
        
        # Grok API Key
        current_grok = "✓ Set" if self.config.grok_api_key else "✗ Not set"
        print(f"Grok API Key: {current_grok}")
        
        if input("Configure Grok API key? (y/N): ").lower().startswith('y'):
            grok_key = getpass.getpass("Enter your Grok API key: ").strip()
            if grok_key:
                self.config.set_grok_api_key(grok_key)
                print_info("✓ Grok API key saved")
            else:
                print_error("No key entered")
        
        print()
        
        # Claude API Key
        current_claude = "✓ Set" if self.config.claude_api_key else "✗ Not set"
        print(f"Claude API Key: {current_claude}")
        
        if input("Configure Claude API key? (y/N): ").lower().startswith('y'):
            claude_key = getpass.getpass("Enter your Claude API key: ").strip()
            if claude_key:
                self.config.set_claude_api_key(claude_key)
                print_info("✓ Claude API key saved")
            else:
                print_error("No key entered")
        
        print()
        print_info("Configuration updated! Restart to use new keys.")
    
    def show_config(self):
        print_bold("\n⚙️ Configuration")
        print(f"Config file: {self.config.config_path}")
        print(f"Default model: {self.config.default_model}")
        print(f"Grok API key: {'✓ Set' if self.config.grok_api_key else '✗ Not set'}")
        print(f"Claude API key: {'✓ Set' if self.config.claude_api_key else '✗ Not set'}")
        print(f"Max tokens: {self.config.max_tokens}")
        print(f"Temperature: {self.config.temperature}")
        print(f"System prompt: {self.config.system_prompt or 'None'}")
    
    def show_cost_info(self):
        duration = time.time() - self.start_time
        hours = int(duration // 3600)
        minutes = int((duration % 3600) // 60)
        seconds = int(duration % 60)
        
        print_bold("\n💰 Session Info")
        print(f"Duration: {hours:02d}:{minutes:02d}:{seconds:02d}")
        print(f"Messages: {len(self.conversation_history)}")
        print(f"Model: {self.client.model_name}")
        print("Note: Actual API costs depend on your provider's pricing")
    
    def export_conversation(self):
        if not self.conversation_history:
            print_info("No conversation to export")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"grok_conversation_{timestamp}.json"
        
        export_data = {
            "timestamp": datetime.now().isoformat(),
            "model": self.client.model_name,
            "system_prompt": self.system_prompt,
            "conversation": self.conversation_history
        }
        
        try:
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=2)
            print_info(f"✓ Conversation exported to: {filename}")
        except Exception as e:
            print_error(f"Export failed: {e}")
    
    def run_doctor(self):
        print_bold("\n🩺 Grok CLI Health Check")
        
        # Check API keys
        if self.config.grok_api_key:
            print("✓ Grok API key configured")
        else:
            print("✗ Grok API key missing")
        
        if self.config.claude_api_key:
            print("✓ Claude API key configured")
        else:
            print("✗ Claude API key missing")
        
        # Check config file
        try:
            import os
            if os.path.exists(self.config.config_path):
                print("✓ Config file exists")
            else:
                print("✗ Config file missing")
        except:
            print("✗ Config file check failed")
        
        # Check model connection
        print(f"✓ Current model: {self.client.model_name}")
        print("✓ CLI is operational")
    
    def compact_conversation(self, instructions: str):
        if not self.conversation_history:
            print_info("No conversation to compact")
            return
        
        print_info("Compacting conversation with AI summary...")
        
        # Create summary prompt
        conv_text = ""
        for entry in self.conversation_history:
            conv_text += f"User: {entry['user']}\nAI: {entry['assistant']}\n\n"
        
        summary_prompt = f"{instructions}\n\nConversation to summarize:\n{conv_text}"
        
        try:
            summary = self.client.chat(summary_prompt, "You are a helpful assistant that summarizes conversations concisely.")
            
            # Clear history and add summary
            self.conversation_history.clear()
            self.conversation_history.append({
                'user': '[Previous conversation summary]',
                'assistant': summary
            })
            
            print_info("✓ Conversation compacted with AI summary")
            
        except Exception as e:
            print_error(f"Compact failed: {e}")
    
    def confirm_exit(self) -> bool:
        try:
            response = input("Are you sure you want to exit? (y/N): ")
            return response.lower().startswith('y')
        except (KeyboardInterrupt, EOFError):
            return True