#!/home/rbilter/work/repos/glove-and-mitten/.venv/bin/python
"""
Google Cloud Text-to-Speech Reader for Character Profiles
Converts markdown files to high-quality speech using Google Cloud TTS
"""

import os
import sys
import json
import hashlib
import argparse
import re
import glob
from pathlib import Path
from google.cloud import texttospeech
import subprocess

class TTSReader:
    def __init__(self, config_file="scripts/tts-config.json", init_client=True):
        self.config = self.load_config(config_file)
        self.cache_dir = Path("scripts/audio-cache")
        self.cache_dir.mkdir(exist_ok=True)
        
        # Initialize Google Cloud TTS client only if needed
        self.client = None
        if init_client:
            try:
                self.client = texttospeech.TextToSpeechClient()
                print("✅ Google Cloud TTS client initialized")
            except Exception as e:
                print(f"❌ Error initializing TTS client: {e}")
                print("Make sure GOOGLE_APPLICATION_CREDENTIALS is set and valid")
                sys.exit(1)
    
    def load_config(self, config_file):
        """Load TTS configuration from JSON file"""
        default_config = {
            "voice": {
                "language_code": "en-US",
                "name": "en-US-Neural2-D",
                "ssml_gender": "MALE"
            },
            "audio_config": {
                "audio_encoding": "MP3",
                "speaking_rate": 1.0,
                "pitch": 0.0
            },
            "playback": {
                "auto_play": True,
                "save_audio": True
            }
        }
        
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                # Merge with defaults
                for key in default_config:
                    if key not in config:
                        config[key] = default_config[key]
                return config
        except FileNotFoundError:
            print(f"📁 Creating default config: {config_file}")
            Path(config_file).parent.mkdir(exist_ok=True)
            with open(config_file, 'w') as f:
                json.dump(default_config, f, indent=2)
            return default_config
    
    def find_character_file(self, character_name):
        """Find character file by name, searching common locations"""
        # Convert to lowercase for case-insensitive matching
        char_name = character_name.lower()
        
        # Search patterns for character files
        search_patterns = [
            f"characters/**/{char_name}.md",
            f"characters/**/*{char_name}*.md",
            f"**/{char_name}.md",
            f"**/*{char_name}*.md"
        ]
        
        found_files = []
        for pattern in search_patterns:
            matches = glob.glob(pattern, recursive=True)
            found_files.extend(matches)
        
        # Remove duplicates and sort by relevance
        found_files = list(set(found_files))
        
        if not found_files:
            return None
        
        # Prioritize exact matches and shorter paths
        def file_score(filepath):
            filename = Path(filepath).stem.lower()
            score = 0
            
            # Exact filename match gets highest priority
            if filename == char_name:
                score += 100
            
            # Partial match in filename
            elif char_name in filename:
                score += 50
            
            # Prefer files in characters/ directory
            if "characters/" in filepath:
                score += 20
            
            # Prefer shorter paths (closer to root)
            score -= filepath.count('/')
            
            return score
        
        # Sort by score (highest first)
        found_files.sort(key=file_score, reverse=True)
        
        return found_files[0]  # Return best match
    
    def clean_markdown(self, text):
        """Convert markdown to clean text suitable for TTS"""
        # Remove image references
        text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
        
        # Convert links to just the text
        text = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', text)
        
        # Remove headers but keep the text
        text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
        
        # Remove bold/italic markup
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
        text = re.sub(r'\*(.*?)\*', r'\1', text)
        
        # Remove code blocks and inline code
        text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
        text = re.sub(r'`([^`]*)`', r'\1', text)
        
        # Remove horizontal rules
        text = re.sub(r'^---+$', '', text, flags=re.MULTILINE)
        
        # Clean up extra whitespace
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r'[ \t]+', ' ', text)
        
        # Remove table formatting
        text = re.sub(r'\|[^|\n]*\|', '', text)
        
        return text.strip()
    
    def get_cache_filename(self, text, voice_name):
        """Generate cache filename based on content and voice"""
        content_hash = hashlib.md5(f"{text}{voice_name}".encode()).hexdigest()[:12]
        return self.cache_dir / f"tts-{content_hash}.mp3"
    
    def synthesize_speech(self, text, voice_name=None):
        """Convert text to speech using Google Cloud TTS"""
        if not self.client:
            print("❌ TTS client not initialized - call TTSReader(init_client=True)")
            return None
            
        if voice_name:
            self.config["voice"]["name"] = voice_name
        
        # Check cache first
        cache_file = self.get_cache_filename(text, self.config["voice"]["name"])
        if cache_file.exists():
            print(f"🎵 Using cached audio: {cache_file.name}")
            return cache_file
        
        # Prepare the request
        synthesis_input = texttospeech.SynthesisInput(text=text)
        
        voice = texttospeech.VoiceSelectionParams(
            language_code=self.config["voice"]["language_code"],
            name=self.config["voice"]["name"],
            ssml_gender=getattr(texttospeech.SsmlVoiceGender, self.config["voice"]["ssml_gender"])
        )
        
        audio_config = texttospeech.AudioConfig(
            audio_encoding=getattr(texttospeech.AudioEncoding, self.config["audio_config"]["audio_encoding"]),
            speaking_rate=self.config["audio_config"]["speaking_rate"],
            pitch=self.config["audio_config"]["pitch"]
        )
        
        # Make the request
        print(f"🎙️  Synthesizing speech with {self.config['voice']['name']}...")
        print(f"📊 Character count: {len(text):,}")
        
        try:
            response = self.client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            
            # Save to cache
            with open(cache_file, "wb") as out:
                out.write(response.audio_content)
            
            print(f"✅ Audio generated: {cache_file.name}")
            return cache_file
            
        except Exception as e:
            print(f"❌ Error generating speech: {e}")
            return None
    
    def play_audio(self, audio_file):
        """Play audio file using system audio player"""
        if not audio_file or not audio_file.exists():
            print("❌ No audio file to play")
            return False
        
        try:
            # Try different audio players
            players = ['paplay', 'aplay', 'mpg123', 'ffplay', 'mplayer']
            
            for player in players:
                if subprocess.run(['which', player], capture_output=True).returncode == 0:
                    print(f"🔊 Playing audio with {player}...")
                    result = subprocess.run([player, str(audio_file)], 
                                          capture_output=True, text=True)
                    if result.returncode == 0:
                        return True
                    
            print("❌ No suitable audio player found")
            print("Install one of: paplay, aplay, mpg123, ffplay, or mplayer")
            return False
            
        except Exception as e:
            print(f"❌ Error playing audio: {e}")
            return False
    
    def read_character(self, character_name, voice_name=None):
        """Read a character by name (auto-discovers file)"""
        file_path = self.find_character_file(character_name)
        
        if not file_path:
            print(f"❌ Character '{character_name}' not found")
            print("Available characters:")
            self.list_available_characters()
            return False
        
        print(f"📖 Found: {file_path}")
        return self.read_file(file_path, voice_name)
    
    def list_available_characters(self):
        """List all available character files"""
        char_files = glob.glob("characters/**/*.md", recursive=True)
        
        if not char_files:
            print("  No character files found")
            return
        
        for file_path in sorted(char_files):
            char_name = Path(file_path).stem
            print(f"  {char_name} ({file_path})")
    
    def read_file(self, file_path, voice_name=None):
        """Read a markdown file aloud"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            print(f"❌ File not found: {file_path}")
            return False
        
        print(f"📖 Reading: {file_path}")
        
        # Read and clean the file
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                raw_text = f.read()
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            return False
        
        # Clean markdown
        clean_text = self.clean_markdown(raw_text)
        
        if not clean_text.strip():
            print("❌ No readable text found in file")
            return False
        
        print(f"📊 Processed text length: {len(clean_text):,} characters")
        
        # If no TTS client (test mode), just show the processed text
        if not self.client:
            print("🧪 Test mode - showing first 200 characters of processed text:")
            print("-" * 50)
            print(clean_text[:200] + "..." if len(clean_text) > 200 else clean_text)
            print("-" * 50)
            return True
        
        # Generate speech
        audio_file = self.synthesize_speech(clean_text, voice_name)
        
        if not audio_file:
            return False
        
        # Play audio if configured
        if self.config["playback"]["auto_play"]:
            return self.play_audio(audio_file)
        else:
            print(f"🎵 Audio saved: {audio_file}")
            return True

def main():
    parser = argparse.ArgumentParser(description="Read markdown files using Google Cloud TTS")
    parser.add_argument("input", nargs='?', help="Character name or markdown file path to read")
    parser.add_argument("--voice", help="Voice name (e.g., en-US-Neural2-D)")
    parser.add_argument("--no-play", action="store_true", help="Don't auto-play audio")
    parser.add_argument("--list-voices", action="store_true", help="List available voices")
    parser.add_argument("--test-mode", action="store_true", help="Test mode - process text but don't use TTS")
    parser.add_argument("--list-characters", action="store_true", help="List available characters")
    
    args = parser.parse_args()
    
    if args.list_voices:
        # List available voices
        try:
            client = texttospeech.TextToSpeechClient()
            voices = client.list_voices()
            
            print("\n🎙️  Available Voices (English):")
            print("=" * 50)
            
            for voice in voices.voices:
                if voice.language_codes[0].startswith('en-'):
                    print(f"Name: {voice.name}")
                    print(f"Language: {voice.language_codes[0]}")
                    print(f"Gender: {voice.ssml_gender.name}")
                    print("-" * 30)
        except Exception as e:
            print(f"❌ Error listing voices: {e}")
        return

    if args.list_characters:
        print("\n📚 Available Characters:")
        print("=" * 30)
        tts = TTSReader(init_client=False)  # Don't need TTS client for listing
        tts.list_available_characters()
        return
    
    # Check if input is provided when not using list commands
    if not args.input:
        parser.error("input is required when not using --list-voices or --list-characters")

    # Initialize TTS reader (with client for actual TTS operations)
    init_client = not args.test_mode  # Skip TTS client in test mode
    tts = TTSReader(init_client=init_client)
    
    # Override auto-play if requested
    if args.no_play:
        tts.config["playback"]["auto_play"] = False
    
    # Determine if input is a file path or character name
    input_path = Path(args.input)
    
    if input_path.exists() and input_path.suffix == '.md':
        # Direct file path
        success = tts.read_file(args.input, args.voice)
    else:
        # Character name - try to find the file
        success = tts.read_character(args.input, args.voice)
    
    if success:
        print("✅ Reading completed successfully")
    else:
        print("❌ Reading failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
