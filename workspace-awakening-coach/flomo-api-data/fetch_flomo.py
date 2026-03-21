#!/usr/bin/env python3
"""
Flomo to OpenClaw Data Importer
Fetches notes from Flomo API and saves them as Markdown files
for OpenClaw indexing.
"""

import requests
import json
import os
from datetime import datetime
import time

def load_config():
    """Load configuration from config.json"""
    with open('config.json', 'r') as f:
        return json.load(f)

def fetch_flomo_notes(api_key, base_url, batch_size=50):
    """Fetch all notes from Flomo API"""
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }
    
    all_notes = []
    offset = 0
    
    while True:
        url = f"{base_url}/memos?limit={batch_size}&offset={offset}"
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            break
            
        data = response.json()
        notes = data.get('data', [])
        
        if not notes:
            break
            
        all_notes.extend(notes)
        print(f"Fetched {len(notes)} notes (total: {len(all_notes)})")
        
        if len(notes) < batch_size:
            break
            
        offset += batch_size
        time.sleep(0.1)  # Rate limiting
        
    return all_notes

def save_notes_as_markdown(notes, output_dir):
    """Save notes as individual Markdown files"""
    os.makedirs(output_dir, exist_ok=True)
    
    for note in notes:
        # Create filename from title or first few words
        title = note.get('content', '')[:50].strip()
        if not title:
            title = f"note_{note.get('id', 'unknown')}"
        
        # Clean filename
        filename = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        filename = filename.replace(' ', '_')[:30]
        filename = f"{filename}_{note.get('id', 'unknown')}.md"
        
        filepath = os.path.join(output_dir, filename)
        
        # Create Markdown content
        content = f"""---
id: {note.get('id', '')}
created_at: {note.get('created_at', '')}
updated_at: {note.get('updated_at', '')}
---

{note.get('content', '')}
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    print(f"Saved {len(notes)} notes to {output_dir}")

def main():
    config = load_config()
    api_key = config['api_key']
    
    if api_key == "YOUR_FLOMO_API_KEY_HERE":
        print("Please update config.json with your actual Flomo API key")
        return
        
    print("Fetching notes from Flomo...")
    notes = fetch_flomo_notes(
        api_key=api_key,
        base_url=config['base_url'],
        batch_size=config['batch_size']
    )
    
    print(f"Total notes fetched: {len(notes)}")
    
    # Save metadata
    metadata_path = os.path.join(config['metadata_dir'], 'flomo_metadata.json')
    os.makedirs(config['metadata_dir'], exist_ok=True)
    with open(metadata_path, 'w') as f:
        json.dump({
            'fetch_time': datetime.now().isoformat(),
            'total_notes': len(notes),
            'notes': notes
        }, f, indent=2, ensure_ascii=False)
    
    # Save as Markdown files
    save_notes_as_markdown(notes, config['output_dir'])
    
    print("Done! Notes are ready for OpenClaw indexing.")

if __name__ == "__main__":
    main()