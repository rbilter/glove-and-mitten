# Glove and Mitten Project Makefile
# Provides simple interface to workflow automation

.PHONY: help process-episode sync commit-local clean status read-profile list-voices list-characters

# Default target
help:
	@echo "Glove and Mitten Project Workflows"
	@echo "=================================="
	@echo ""
	@echo "Available commands:"
	@echo "  make process-episode EPISODE=<path>  - Generate metadata from PowerPoint episode"
	@echo "  make commit-local                    - Commit local changes and sync to Google Drive"
	@echo "  make sync                            - Alias for commit-local"
	@echo "  make read-profile CHAR=<name>        - Read character profile by name (e.g. glove, mitten, beaker)"
	@echo "  make read-profile FILE=<path>        - Read any markdown file by path"
	@echo "  make read-profile CHAR=<name> TEST=1 - Test mode (no TTS, just show processed text)"
	@echo "  make list-voices                     - List available TTS voices"
	@echo "  make list-characters                 - List available character profiles"
	@echo "  make clean                           - Clean generated files"
	@echo "  make status                          - Show project status"
	@echo "  make help                            - Show this help message"
	@echo ""
	@echo "Examples:"
	@echo "  make process-episode EPISODE=content/stories/sagas/school-daze/stories/lights/tuff-daze/01-lights-tuff-daze-episode.pptx"
	@echo "  make read-profile CHAR=glove         - Read Glove's profile"
	@echo "  make read-profile CHAR=beaker        - Read Instructor Beaker's profile"
	@echo "  make read-profile FILE=content/characters/main/glove.md"
	@echo "  make commit-local"
	@echo ""
	@echo "For detailed documentation, see workflows/ directory"

# Process episode workflow
process-episode:
	@echo "🚀 Running process-episode workflow..."
	@echo "📖 See workflows/process-episode.md for details"
	@echo ""
	@echo "To execute this workflow, tell the assistant:"
	@echo "  'Process episode: $(EPISODE)'"
	@echo ""
	@echo "The assistant will:"
	@echo "  1. Generate PDF from PowerPoint"
	@echo "  2. Extract episode content"
	@echo "  3. Create YouTube metadata"
	@echo "  4. Generate description and tags"

# Sync project workflow (alias for commit-local)
sync: commit-local

# Commit local changes workflow
commit-local:
	@echo "� Running commit-local workflow..."
	@echo "📖 See workflows/commit-local.md for details"
	@echo ""
	@echo "To execute this workflow, tell the assistant:"
	@echo "  'Run commit-local workflow'"
	@echo ""
	@echo "The assistant will:"
	@echo "  1. Check local changes"
	@echo "  2. Stage and commit to Git"
	@echo "  3. Push to GitHub remote"
	@echo "  4. Sync to Google Drive"
	@echo "  5. Verify sync status"

# Clean generated files
clean:
	@echo "🧹 Cleaning generated files..."
	@echo "This would remove:"
	@echo "  - Generated PDFs"
	@echo "  - Temporary files"
	@echo "  - Cache files"
	@echo ""
	@echo "Run with caution - tell assistant: 'Clean generated files'"

# Status check
status:
	@echo "📊 Project Status"
	@echo "================"
	@git log --oneline -5
	@echo ""

# Text-to-Speech Commands
read-profile:
	@if [ -n "$(CHAR)" ]; then \
		echo "🎙️  Reading $(CHAR)'s profile..."; \
		if [ -n "$(TEST)" ]; then \
			./dev/scripts/read-profile.py "$(CHAR)" --test-mode; \
		else \
			./dev/scripts/read-profile.py "$(CHAR)"; \
		fi; \
	elif [ -n "$(FILE)" ]; then \
		echo "🎙️  Reading file: $(FILE)"; \
		if [ -n "$(TEST)" ]; then \
			./dev/scripts/read-profile.py "$(FILE)" --test-mode; \
		else \
			./dev/scripts/read-profile.py "$(FILE)"; \
		fi; \
	else \
		echo "❌ Please specify either CHAR=<name> or FILE=<path>"; \
		echo "Examples:"; \
		echo "  make read-profile CHAR=glove"; \
		echo "  make read-profile CHAR=glove TEST=1  (test mode)"; \
		echo "  make read-profile FILE=content/characters/main/glove.md"; \
		echo ""; \
		echo "Available characters:"; \
		./dev/scripts/read-profile.py --list-characters; \
		exit 1; \
	fi

list-voices:
	@echo "🎙️  Listing available TTS voices..."
	@./dev/scripts/read-profile.py --list-voices

list-characters:
	@echo "📚 Available character profiles:"
	@./dev/scripts/read-profile.py --list-characters
	@echo "Working directory status:"
	@git status --short
	@echo ""
	@echo "File counts:"
	@find . -type f -not -path "./.git/*" | wc -l | xargs echo "Files:"
	@find . -type d -not -path "./.git/*" | wc -l | xargs echo "Directories:"
