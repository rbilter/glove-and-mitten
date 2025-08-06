#!/home/rbilter/work/repos/glove-and-mitten/.venv/bin/python
"""
Google Cloud Text-to-Speech Reader for Markdown Files
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
    def __init__(self, config_file="dev/config/tts-config.json", init_client=True):
        self.config = self.load_config(config_file)
        self.cache_dir = Path("dev/cache/audio-cache")
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
                "save_audio": True,
                "auto_open_editor": True
            }
        }
        
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                # Merge with defaults (deep merge for nested dictionaries)
                for key in default_config:
                    if key not in config:
                        config[key] = default_config[key]
                    elif isinstance(default_config[key], dict) and isinstance(config.get(key), dict):
                        # Merge nested dictionaries
                        for subkey in default_config[key]:
                            if subkey not in config[key]:
                                config[key][subkey] = default_config[key][subkey]
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
            f"content/characters/**/{char_name}.md",
            f"content/characters/**/*{char_name}*.md",
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
            
            # Prefer files in content/characters/ directory
            if "content/characters/" in filepath:
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
    
    def split_text_into_chunks(self, text, max_bytes=4500):
        """Split text into chunks that fit within TTS byte limit"""
        chunks = []
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        current_chunk = ""
        for sentence in sentences:
            # Check if adding this sentence would exceed the limit
            test_chunk = current_chunk + (" " if current_chunk else "") + sentence
            if len(test_chunk.encode('utf-8')) > max_bytes and current_chunk:
                # Save current chunk and start new one
                chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:
                current_chunk = test_chunk
        
        # Add the last chunk
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
            
        return chunks
    
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
        
        # Check if text is too long and needs chunking
        text_bytes = len(text.encode('utf-8'))
        if text_bytes > 4500:  # Leave some safety margin
            print(f"📊 Text too long ({text_bytes:,} bytes), splitting into chunks...")
            chunks = self.split_text_into_chunks(text)
            print(f"📊 Split into {len(chunks)} chunks")
            
            # Process each chunk and combine audio
            chunk_files = []
            for i, chunk in enumerate(chunks, 1):
                print(f"🎙️  Processing chunk {i}/{len(chunks)} ({len(chunk.encode('utf-8')):,} bytes)...")
                chunk_file = self.synthesize_single_chunk(chunk, f"{i:03d}")
                if chunk_file:
                    chunk_files.append(chunk_file)
                else:
                    print(f"❌ Failed to process chunk {i}")
                    return None
            
            # Combine chunks into final audio file
            if chunk_files:
                combined_file = self.combine_audio_chunks(chunk_files, cache_file)
                # Clean up temporary chunk files
                for chunk_file in chunk_files:
                    try:
                        chunk_file.unlink()
                    except:
                        pass
                return combined_file
            else:
                return None
        else:
            # Text is short enough, process normally
            return self.synthesize_single_chunk(text)
    
    def synthesize_single_chunk(self, text, chunk_suffix=""):
        """Synthesize a single text chunk"""
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
        
        # Generate cache filename
        if chunk_suffix:
            content_hash = hashlib.md5(f"{text}{self.config['voice']['name']}".encode()).hexdigest()[:8]
            cache_file = self.cache_dir / f"tts-chunk-{chunk_suffix}-{content_hash}.mp3"
        else:
            cache_file = self.get_cache_filename(text, self.config["voice"]["name"])
        
        try:
            response = self.client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            
            # Save audio
            with open(cache_file, "wb") as out:
                out.write(response.audio_content)
            
            if not chunk_suffix:
                print(f"✅ Audio generated: {cache_file.name}")
            return cache_file
            
        except Exception as e:
            print(f"❌ Error generating speech: {e}")
            return None
    
    def combine_audio_chunks(self, chunk_files, output_file):
        """Combine multiple audio chunks into a single file"""
        try:
            # Try to use ffmpeg for combining
            if subprocess.run(['which', 'ffmpeg'], capture_output=True).returncode == 0:
                print("🔗 Combining audio chunks with ffmpeg...")
                
                # Create input list for ffmpeg
                input_list = self.cache_dir / "input_list.txt"
                with open(input_list, "w") as f:
                    for chunk_file in chunk_files:
                        f.write(f"file '{chunk_file.absolute()}'\n")
                
                # Combine with ffmpeg
                result = subprocess.run([
                    'ffmpeg', '-f', 'concat', '-safe', '0', '-i', str(input_list),
                    '-c', 'copy', str(output_file), '-y'
                ], capture_output=True, text=True)
                
                input_list.unlink()  # Clean up
                
                if result.returncode == 0:
                    print(f"✅ Combined audio saved: {output_file.name}")
                    return output_file
                else:
                    print(f"❌ ffmpeg error: {result.stderr}")
                    return None
            else:
                # Fallback: just use the first chunk
                print("⚠️  ffmpeg not found, using first chunk only")
                first_chunk = chunk_files[0]
                import shutil
                shutil.copy2(first_chunk, output_file)
                return output_file
                
        except Exception as e:
            print(f"❌ Error combining audio: {e}")
            return None
    
    def play_audio(self, audio_file):
        """Play audio file using MPV with interactive controls"""
        if not audio_file or not audio_file.exists():
            print("❌ No audio file to play")
            return False
        
        try:
            # Check if mpv is available (preferred for interactive controls)
            if subprocess.run(['which', 'mpv'], capture_output=True).returncode == 0:
                return self._play_with_mpv(audio_file)
            else:
                # Fallback to blocking players
                return self._play_with_fallback(audio_file)
                
        except Exception as e:
            print(f"❌ Error playing audio: {e}")
            return False
    
    def _play_with_mpv(self, audio_file):
        """Play audio with MPV in interactive mode"""
        try:
            print("🎵 Launching MPV audio player in new terminal...")
            print("📱 Controls: SPACE=pause/play, LEFT/RIGHT=seek, Q=quit, +/-=volume")
            
            # Try to launch MPV in a new terminal window for better visibility
            terminal_commands = [
                # GNOME Terminal
                ['gnome-terminal', '--', 'mpv', '--no-video', '--keep-open', '--term-osd-bar', '--osd-level=1', '--title=Audio Player', str(audio_file)],
                # KDE Konsole
                ['konsole', '-e', 'mpv', '--no-video', '--keep-open', '--term-osd-bar', '--osd-level=1', '--title=Audio Player', str(audio_file)],
                # XFCE Terminal
                ['xfce4-terminal', '-e', f'mpv --no-video --keep-open --term-osd-bar --osd-level=1 --title="Audio Player" "{audio_file}"'],
                # X Terminal
                ['xterm', '-e', f'mpv --no-video --keep-open --term-osd-bar --osd-level=1 --title="Audio Player" "{audio_file}"'],
            ]
            
            # Try each terminal in order
            for cmd in terminal_commands:
                try:
                    if subprocess.run(['which', cmd[0]], capture_output=True).returncode == 0:
                        print(f"🖥️  Opening MPV in {cmd[0]}...")
                        process = subprocess.Popen(cmd)
                        print(f"🔊 Audio player launched in new terminal window (PID: {process.pid})")
                        print("🎛️  Look for the new terminal window to control playback")
                        print("💡 If you don't see it, check your taskbar or alt-tab")
                        return True
                except:
                    continue
            
            # Fallback: try running MPV directly (background mode)
            print("⚠️  No terminal emulator found, falling back to background mode")
            cmd = [
                'mpv',
                '--no-video',           # Audio only
                '--keep-open',          # Don't exit after playing
                '--term-osd-bar',       # Show progress bar
                '--osd-level=1',        # Show basic OSD
                '--title=' + f"Audio: {audio_file.name}",  # Set window title
                str(audio_file)
            ]
            
            # Start MPV in the background (non-blocking)
            process = subprocess.Popen(cmd)
            
            print(f"🔊 Audio playing in background (PID: {process.pid})")
            print(f"🎛️  To stop this audio: kill {process.pid}")
            print("💡 Try: pkill mpv (to stop all audio)")
            
            return True
            
        except Exception as e:
            print(f"❌ MPV failed: {e}")
            return self._play_with_fallback(audio_file)
    
    def _play_with_fallback(self, audio_file):
        """Fallback to blocking audio players"""
        try:
            # Try different audio players (blocking mode)
            players = ['mpg123', 'ffplay', 'mplayer', 'paplay', 'aplay']
            
            for player in players:
                if subprocess.run(['which', player], capture_output=True).returncode == 0:
                    print(f"🔊 Playing audio with {player} (blocking mode)...")
                    
                    # Special handling for different players
                    if player == 'ffplay':
                        # ffplay needs -nodisp to run without video window
                        cmd = [player, '-nodisp', '-autoexit', str(audio_file)]
                    else:
                        cmd = [player, str(audio_file)]
                    
                    result = subprocess.run(cmd, capture_output=True, text=True)
                    if result.returncode == 0:
                        return True
                    else:
                        print(f"⚠️  {player} failed: {result.stderr.strip()}")
                    
            print("❌ No suitable audio player found")
            print("Install MPV for interactive controls or one of: mpg123, ffplay, mplayer, paplay, aplay")
            return False
            
        except Exception as e:
            print(f"❌ Error in fallback audio: {e}")
            return False
    
    def open_in_editor(self, file_path):
        """Open file in VS Code editor"""
        try:
            file_path = Path(file_path).absolute()
            
            # Check if VS Code is available
            vscode_commands = ['code', 'code-insiders']
            
            for cmd in vscode_commands:
                if subprocess.run(['which', cmd], capture_output=True).returncode == 0:
                    print(f"📝 Opening file in VS Code: {file_path.name}")
                    
                    # Open file in VS Code (non-blocking)
                    process = subprocess.Popen([cmd, str(file_path)])
                    
                    print("💡 File opened in editor - you can follow along with the audio")
                    return True
            
            # Fallback: try xdg-open (Linux default file handler)
            if subprocess.run(['which', 'xdg-open'], capture_output=True).returncode == 0:
                print(f"📝 Opening file with default editor: {file_path.name}")
                subprocess.Popen(['xdg-open', str(file_path)])
                return True
                
            print("⚠️  No editor found (VS Code recommended)")
            print("   Install VS Code: https://code.visualstudio.com/")
            return False
            
        except Exception as e:
            print(f"❌ Error opening file in editor: {e}")
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
        char_files = glob.glob("content/characters/**/*.md", recursive=True)
        
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
        
        # Open file in editor if configured
        if self.config["playback"].get("auto_open_editor", True):
            self.open_in_editor(file_path)
        
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
    parser.add_argument("--no-editor", action="store_true", help="Don't auto-open file in editor")
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
    
    # Override auto-editor if requested
    if args.no_editor:
        tts.config["playback"]["auto_open_editor"] = False
    
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
