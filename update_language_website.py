#!/usr/bin/env python3
"""
Multi-language website updater - avoids conflicts with development
Only updates language-specific pages, not the root redirect page
"""

import os
import re
import json
import argparse
from datetime import date
from pathlib import Path

def update_language_page(language='en_GB'):
    """Update the language-specific page with new content"""
    
    # Language configuration
    config = {
        'en_GB': {
            'page_path': 'docs/en_GB/index.html',
            'audio_dir': 'docs/en_GB/audio',
            'text_dir': 'docs/en_GB'
        },
        'fr_FR': {
            'page_path': 'docs/fr_FR/index.html', 
            'audio_dir': 'docs/fr_FR/audio',
            'text_dir': 'docs/fr_FR'
        }
    }
    
    if language not in config:
        print(f"❌ Unsupported language: {language}")
        return False
    
    lang_config = config[language]
    page_path = lang_config['page_path']
    
    # Check if the page exists
    if not os.path.exists(page_path):
        print(f"⚠️ Language page not found: {page_path}")
        return False
    
    # Get today's files
    today_str = date.today().strftime("%Y_%m_%d")
    audio_file = f"{lang_config['audio_dir']}/news_digest_ai_{today_str}.mp3"
    text_file = f"{lang_config['text_dir']}/news_digest_ai_{today_str}.txt"
    
    # Check if today's content exists
    if not (os.path.exists(audio_file) and os.path.exists(text_file)):
        print(f"⚠️ Today's content not found for {language}")
        print(f"   Expected: {audio_file}")
        print(f"   Expected: {text_file}")
        return False
    
    # Read the current page
    with open(page_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Read the digest text
    with open(text_file, 'r', encoding='utf-8') as f:
        digest_text = f.read()
    
    # Get audio file stats
    audio_size = os.path.getsize(audio_file)
    audio_size_mb = audio_size / (1024 * 1024)
    
    # Calculate duration (rough estimate: 1MB ≈ 1 minute for speech)
    duration_minutes = int(audio_size_mb)
    duration_seconds = int((audio_size_mb - duration_minutes) * 60)
    duration_formatted = f"{duration_minutes}min {duration_seconds}sec"
    
    # Update title with today's date
    today_formatted = date.today().strftime("%B %d, %Y")
    if language == 'en_GB':
        new_title = f"AudioNews.uk - Daily Voice News Digest - {today_formatted}"
        new_description = f"Daily AI-generated audio news digest for {today_formatted} brought to you by Dynamic Devices. Professional Irish voice, screen reader optimized."
    else:  # fr_FR
        new_title = f"AudioNews France - Digest Audio Quotidien - {today_formatted}"
        new_description = f"Résumé quotidien d'actualités audio généré par IA pour {today_formatted} présenté par Dynamic Devices. Voix française professionnelle, optimisé pour lecteurs d'écran."
    
    # Update HTML content (only for actual content pages, not coming soon pages)
    if 'Bientôt Disponible' not in html and 'Coming Soon' not in html:
        # Update title
        html = re.sub(r'<title>.*?</title>', f'<title>{new_title}</title>', html)
        
        # Update meta description
        html = re.sub(r'<meta name="description" content=".*?"', f'<meta name="description" content="{new_description}"', html)
        
        # Update audio source (relative path from language directory)
        audio_filename = f"audio/news_digest_ai_{today_str}.mp3"
        html = re.sub(r'<source src="audio/[^"]*"', f'<source src="{audio_filename}"', html)
        
        # Update download link
        html = re.sub(r'<a[^>]*download[^>]*href="audio/[^"]*"', f'<a download="{audio_filename}" href="{audio_filename}"', html)
        
        # Update digest content in the page
        digest_pattern = r'(<div class="digest-content"[^>]*>)(.*?)(</div>)'
        if re.search(digest_pattern, html, re.DOTALL):
            # Convert text to HTML paragraphs
            digest_paragraphs = []
            for paragraph in digest_text.split('\n\n'):
                if paragraph.strip():
                    digest_paragraphs.append(f'<p>{paragraph.strip()}</p>')
            
            digest_html = '\n            '.join(digest_paragraphs)
            html = re.sub(digest_pattern, f'\\1\n            {digest_html}\n        \\3', html, flags=re.DOTALL)
    
    # Write the updated HTML
    with open(page_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ Updated {language} page: {page_path}")
    print(f"   📄 Content: {len(digest_text)} characters")
    print(f"   🎧 Audio: {audio_size_mb:.1f}MB ({duration_formatted})")
    
    return True

def main():
    """Main function with command line argument parsing"""
    parser = argparse.ArgumentParser(description='Update language-specific website pages')
    parser.add_argument('--language', '-l', 
                       choices=['en_GB', 'fr_FR'], 
                       default='en_GB',
                       help='Language to update (default: en_GB)')
    
    args = parser.parse_args()
    
    print(f"🌐 Updating {args.language} website page...")
    success = update_language_page(args.language)
    
    if success:
        print(f"🎉 Website update completed for {args.language}")
    else:
        print(f"❌ Website update failed for {args.language}")
        exit(1)

if __name__ == "__main__":
    main()
