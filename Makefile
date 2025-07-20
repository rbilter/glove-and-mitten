# Glove and Mitten Project Makefile
# Provides simple interface to workflow automation

.PHONY: help process-episode sync commit-local clean status

# Default target
help:
	@echo "Glove and Mitten Project Workflows"
	@echo "=================================="
	@echo ""
	@echo "Available commands:"
	@echo "  make process-episode EPISODE=<path>  - Generate metadata from PowerPoint episode"
	@echo "  make commit-local                    - Commit local changes and sync to Google Drive"
	@echo "  make sync                            - Alias for commit-local"
	@echo "  make clean                           - Clean generated files"
	@echo "  make status                          - Show project status"
	@echo "  make help                            - Show this help message"
	@echo ""
	@echo "Examples:"
	@echo "  make process-episode EPISODE=stories/sagas/school-daze/stories/lights/tuff-daze/01-lights-tuff-daze-episode.pptx"
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
	@echo "Working directory status:"
	@git status --short
	@echo ""
	@echo "File counts:"
	@find . -type f -not -path "./.git/*" | wc -l | xargs echo "Files:"
	@find . -type d -not -path "./.git/*" | wc -l | xargs echo "Directories:"
