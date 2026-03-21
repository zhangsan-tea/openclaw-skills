# Flomo to OpenClaw Importer

## Setup Instructions

1. **Get your Flomo API Key**:
   - Go to https://flomoapp.com/iwh/
   - Copy your API key (Bearer token)

2. **Update Configuration**:
   - Edit `config.json`
   - Replace `"YOUR_FLOMO_API_KEY_HERE"` with your actual API key

3. **Run the Importer**:
   ```bash
   cd /Users/lee/.openclaw/workspace-awakening-coach/flomo-api-data
   python3 fetch_flomo.py
   ```

4. **Verify Import**:
   - Check the `notes/` directory for Markdown files
   - OpenClaw will automatically index these files via memory search

## Directory Structure

- `config.json`: Configuration file
- `fetch_flomo.py`: Main import script
- `notes/`: Individual Markdown files (one per note)
- `metadata/`: Raw JSON data from Flomo API
- `logs/`: Log files (if needed)

## Notes

- Files are saved in Markdown format with YAML frontmatter
- OpenClaw's memory system will automatically index the content
- You can search imported notes using `openclaw memory search "your query"`