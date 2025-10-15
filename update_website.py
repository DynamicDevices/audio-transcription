import os
import re
import json
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import glob

def load_latest_digest_data() -> Dict:
    """Load the latest digest data from generated files"""
    today_str = date.today().strftime("%Y_%m_%d")
    
    # Try to load the AI-generated text file (check both root and docs directory)
    text_file_path = Path(f"news_digest_ai_{today_str}.txt")
    if not text_file_path.exists():
        text_file_path = Path(f"docs/news_digest_ai_{today_str}.txt")
    
    if not text_file_path.exists():
        print(f"   ⚠️ Latest AI text file not found in root or docs directory")
        return {}

    with open(text_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract metadata from the text file
    ai_enabled = "ENABLED" in content
    
    # Extract main digest content
    digest_start_marker = "==================================================\n\n"
    digest_end_marker = "\n\nThis digest provides a synthesis"
    
    main_digest_match = re.search(
        re.escape(digest_start_marker) + r"(.*?)" + re.escape(digest_end_marker),
        content, re.DOTALL
    )
    main_digest_content = main_digest_match.group(1).strip() if main_digest_match else "Today's news digest."

    # Load audio stats
    audio_file_path = Path(f"docs/audio/news_digest_ai_{today_str}.mp3")
    duration_s = 0
    if audio_file_path.exists():
        try:
            from pydub import AudioSegment
            audio = AudioSegment.from_mp3(audio_file_path)
            duration_s = len(audio) / 1000.0
        except Exception as e:
            print(f"   ⚠️ Could not get audio duration with pydub: {e}")
            # Fallback estimation
            word_count = len(main_digest_content.split())
            duration_s = word_count / 2.0  # Estimate 2 words per second
    else:
        print(f"   ⚠️ Audio file not found: {audio_file_path}")

    # Format duration in website format (Xmin Ysec)
    minutes = int(duration_s // 60)
    seconds = int(duration_s % 60)
    if minutes > 0:
        duration_formatted = f"{minutes}min {seconds}sec"
    else:
        duration_formatted = f"{seconds}sec"

    word_count = len(main_digest_content.split())

    return {
        "date_formatted": date.today().strftime("%B %d, %Y"),
        "date_iso": date.today().strftime("%Y-%m-%d"),
        "audio_file": f"audio/news_digest_ai_{today_str}.mp3",
        "text_file": f"news_digest_ai_{today_str}.txt",
        "digest_content": main_digest_content,
        "ai_enabled": ai_enabled,
        "duration_s": duration_s,
        "duration_formatted": duration_formatted,
        "word_count": word_count
    }

def update_html_template(data: Dict) -> str:
    """Updates the HTML template with the latest digest data."""
    html_template_path = Path('docs/index.html')
    if not html_template_path.exists():
        print(f"❌ HTML template not found: {html_template_path}")
        return ""

    with open(html_template_path, 'r', encoding='utf-8') as f:
        html = f.read()

    if not data:
        print("   ⚠️ No digest data to update")
        return html

    # Update title
    title_pattern = r'<title>AudioNews\.uk - Daily Voice News Digest - .*? - .*?</title>'
    new_title = f'<title>AudioNews.uk - Daily Voice News Digest - {data["date_formatted"]}</title>'
    html = re.sub(title_pattern, new_title, html)

    # Update meta description
    desc_pattern = r'<meta name="description" content="Daily AI-generated audio news digest.*?">'
    new_desc = f'<meta name="description" content="Daily AI-generated audio news digest for {data["date_formatted"]} brought to you by Dynamic Devices. Professional Irish voice, screen reader optimized.">'
    html = re.sub(desc_pattern, new_desc, html)

    # Update date in the digest title
    date_pattern = r'<time datetime="[\d-]+" class="digest-date">.*?</time>'
    new_date = f'<time datetime="{data["date_iso"]}" class="digest-date">{data["date_formatted"]}</time>'
    html = re.sub(date_pattern, new_date, html)

    # Update audio source
    audio_pattern = r'<source src="audio/news_digest_ai_[\d_]+\.mp3" type="audio/mpeg">'
    new_audio = f'<source src="{data["audio_file"]}" type="audio/mpeg">'
    html = re.sub(audio_pattern, new_audio, html)

    # Update download links
    download_pattern = r'href="audio/news_digest_ai_[\d_]+\.mp3"'
    new_download = f'href="{data["audio_file"]}"'
    html = re.sub(download_pattern, new_download, html)

    # Update transcript link
    transcript_pattern = r'href="news_digest_ai_[\d_]+\.txt"'
    new_transcript = f'href="{data["text_file"]}"'
    html = re.sub(transcript_pattern, new_transcript, html)

    return html

def main():
    """Main function to update the website"""
    print("🌐 Starting simple website update...")
    
    # Load the latest digest data
    digest_data = load_latest_digest_data()
    
    # Update HTML template
    updated_html = update_html_template(digest_data)
    
    if updated_html:
        # Write updated HTML
        with open('docs/index.html', 'w', encoding='utf-8') as f:
            f.write(updated_html)
        
        print(f"✅ Simple website updated successfully")
        if digest_data:
            print(f"   📅 Date: {digest_data['date_formatted']}")
            print(f"   🎧 Audio: {digest_data['audio_file']}")
            print(f"   📊 Duration: {digest_data['duration_formatted']}")
            print(f"   🤖 AI: {'Enabled' if digest_data['ai_enabled'] else 'Fallback'}")
    else:
        print("❌ Failed to update website")

if __name__ == "__main__":
    main()