#!/usr/bin/env python3
"""
Website Update Script for Daily News Digest
Updates the accessible newspaper website with latest AI-generated content
"""

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
    
    # Find the latest audio and text files
    audio_files = glob.glob(f"news_digest_ai_{today_str}.mp3")
    text_files = glob.glob(f"news_digest_ai_{today_str}.txt")
    
    if not audio_files or not text_files:
        print("⚠️ No digest files found for today")
        return {}
    
    audio_file = audio_files[0]
    text_file = text_files[0]
    
    # Get file stats
    audio_size = os.path.getsize(audio_file)
    
    # Parse text file for content
    with open(text_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract metadata from content
    ai_enabled = "AI-ENHANCED" in content.upper()
    sources = extract_sources_from_content(content)
    themes = extract_themes_from_content(content)
    
    # Calculate duration estimate (rough estimate: 150 words per minute)
    word_count = len(content.split())
    duration_seconds = (word_count / 150) * 60
    
    return {
        'date': date.today().strftime("%Y-%m-%d"),
        'date_formatted': date.today().strftime("%B %d, %Y"),
        'audio_file': f"audio/{os.path.basename(audio_file)}",
        'text_file': os.path.basename(text_file),
        'audio_size_bytes': audio_size,
        'audio_size_kb': audio_size / 1024,
        'duration_seconds': duration_seconds,
        'duration_formatted': format_duration(duration_seconds),
        'word_count': word_count,
        'ai_enabled': ai_enabled,
        'sources': sources,
        'themes': themes,
        'content': content
    }

def extract_sources_from_content(content: str) -> List[str]:
    """Extract news sources mentioned in the content"""
    sources = []
    source_patterns = [
        r'BBC News',
        r'Guardian',
        r'Independent',
        r'Sky News',
        r'Telegraph'
    ]
    
    for pattern in source_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            sources.append(pattern)
    
    return sources

def extract_themes_from_content(content: str) -> List[Dict]:
    """Extract news themes from the content"""
    themes = []
    theme_patterns = {
        'politics': ['politics', 'government', 'minister', 'parliament'],
        'international': ['international', 'europe', 'war', 'conflict'],
        'technology': ['technology', 'tech', 'ai', 'digital'],
        'economy': ['economy', 'market', 'business', 'financial'],
        'health': ['health', 'nhs', 'medical'],
        'climate': ['climate', 'environment', 'green']
    }
    
    for theme_name, keywords in theme_patterns.items():
        if any(re.search(keyword, content, re.IGNORECASE) for keyword in keywords):
            # Count stories for this theme (rough estimate)
            story_count = sum(1 for keyword in keywords if re.search(keyword, content, re.IGNORECASE))
            themes.append({
                'name': theme_name,
                'title': theme_name.capitalize(),
                'story_count': min(story_count, 5),  # Cap at 5
                'icon': get_theme_icon(theme_name)
            })
    
    return themes

def get_theme_icon(theme: str) -> str:
    """Get emoji icon for theme"""
    icons = {
        'politics': '🏛️',
        'international': '🌍',
        'technology': '💻',
        'economy': '💼',
        'health': '🏥',
        'climate': '🌱'
    }
    return icons.get(theme, '📰')

def format_duration(seconds: float) -> str:
    """Format duration in human readable format"""
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes} minutes {seconds} seconds" if minutes > 0 else f"{seconds} seconds"

def load_recent_digests() -> List[Dict]:
    """Load information about recent digest files"""
    digests = []
    
    # Look for digest files from the last 7 days
    for i in range(1, 8):
        check_date = date.today() - timedelta(days=i)
        date_str = check_date.strftime("%Y_%m_%d")
        
        audio_files = glob.glob(f"news_digest_ai_{date_str}.mp3")
        if audio_files:
            audio_file = audio_files[0]
            size_kb = os.path.getsize(audio_file) / 1024
            
            # Estimate duration from file size (rough: 1MB ≈ 8 minutes)
            duration_estimate = (size_kb / 1024) * 8 * 60  # seconds
            
            digests.append({
                'date': check_date.strftime("%Y-%m-%d"),
                'date_formatted': check_date.strftime("%B %d, %Y"),
                'audio_file': f"audio/{os.path.basename(audio_file)}",
                'size_kb': size_kb,
                'duration_formatted': format_duration(duration_estimate)
            })
    
    return digests

def update_html_template(digest_data: Dict, recent_digests: List[Dict]) -> str:
    """Update the HTML template with current data"""
    
    # Read the template
    template_path = Path('docs/index.html')
    if not template_path.exists():
        print("❌ Template file not found")
        return ""
    
    with open(template_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    if not digest_data:
        print("⚠️ No digest data available, keeping existing HTML")
        return html
    
    # Update today's digest section
    html = update_todays_digest(html, digest_data)
    
    # Update news sections
    html = update_news_sections(html, digest_data['themes'])
    
    # Update recent digests
    html = update_recent_digests_section(html, recent_digests)
    
    # Update meta information
    html = update_meta_information(html, digest_data)
    
    return html

def update_todays_digest(html: str, data: Dict) -> str:
    """Update the today's digest section"""
    
    # Update date and title
    date_pattern = r'<time datetime="[^"]*" class="digest-date">[^<]*</time>'
    new_date = f'<time datetime="{data["date"]}" class="digest-date">{data["date_formatted"]}</time>'
    html = re.sub(date_pattern, new_date, html)
    
    # Update audio source
    audio_pattern = r'<source src="[^"]*" type="audio/mpeg">'
    new_audio = f'<source src="{data["audio_file"]}" type="audio/mpeg">'
    html = re.sub(audio_pattern, new_audio, html)
    
    # Update download links
    download_pattern = r'href="[^"]*\.mp3"'
    new_download = f'href="{data["audio_file"]}"'
    html = re.sub(download_pattern, new_download, html)
    
    # Update transcript link
    transcript_pattern = r'href="[^"]*\.txt"'
    new_transcript = f'href="{data["text_file"]}"'
    html = re.sub(transcript_pattern, new_transcript, html)
    
    # Update metadata
    duration_pattern = r'<span class="meta-value">(\d+) minutes (\d+) seconds</span>'
    new_duration = f'<span class="meta-value">{data["duration_formatted"]}</span>'
    html = re.sub(duration_pattern, new_duration, html, count=1)
    
    sources_pattern = r'<span class="meta-value">([^<]*)</span>'
    sources_text = ', '.join(data['sources']) if data['sources'] else 'Multiple UK sources'
    new_sources = f'<span class="meta-value">{sources_text}</span>'
    html = re.sub(sources_pattern, new_sources, html, count=1)
    
    ai_status = "Enhanced" if data['ai_enabled'] else "Fallback Mode"
    html = re.sub(r'<span class="meta-value">Enhanced</span>', f'<span class="meta-value">{ai_status}</span>', html)
    
    return html

def update_news_sections(html: str, themes: List[Dict]) -> str:
    """Update the news sections grid"""
    
    if not themes:
        return html
    
    # Build new sections HTML
    sections_html = ""
    
    for theme in themes[:3]:  # Show top 3 themes
        section_html = f'''
                <article class="section-card">
                    <header class="card-header">
                        <h3 class="card-title">
                            <span class="card-icon" aria-hidden="true">{theme['icon']}</span>
                            {theme['title']}
                        </h3>
                        <p class="card-summary">{get_theme_description(theme['name'])}</p>
                    </header>
                    <div class="card-content">
                        <p class="story-count"><strong>{theme['story_count']} stories</strong> from multiple sources</p>
                        <ul class="story-highlights">
                            <li>Coverage across major UK outlets</li>
                            <li>AI-analyzed for significance</li>
                            <li>Synthesized for accessibility</li>
                        </ul>
                    </div>
                </article>'''
        sections_html += section_html
    
    # Replace the sections grid content
    sections_pattern = r'(<div class="sections-grid">)(.*?)(</div>)'
    replacement = f'\\1{sections_html}\\3'
    html = re.sub(sections_pattern, replacement, html, flags=re.DOTALL)
    
    return html

def get_theme_description(theme: str) -> str:
    """Get description for theme"""
    descriptions = {
        'politics': 'Government developments and parliamentary news',
        'international': 'Global events and foreign relations',
        'technology': 'Tech industry and digital developments',
        'economy': 'Economic news and market updates',
        'health': 'Healthcare and medical developments',
        'climate': 'Environmental and climate news'
    }
    return descriptions.get(theme, 'Latest developments')

def update_recent_digests_section(html: str, recent_digests: List[Dict]) -> str:
    """Update recent digests section"""
    
    if not recent_digests:
        return html
    
    # Build recent digests HTML
    digests_html = ""
    
    for digest in recent_digests[:5]:  # Show last 5 days
        digest_html = f'''
                <article class="digest-item">
                    <h3 class="digest-item-title">
                        <time datetime="{digest['date']}">{digest['date_formatted']}</time>
                    </h3>
                    <p class="digest-item-meta">{digest['duration_formatted']} • AI Enhanced</p>
                    <div class="digest-item-actions">
                        <a href="{digest['audio_file']}" class="mini-button">Play</a>
                        <a href="{digest['audio_file']}" download class="mini-button">Download</a>
                    </div>
                </article>'''
        digests_html += digest_html
    
    # Replace the digests list content
    digests_pattern = r'(<div class="digests-list">)(.*?)(</div>)'
    replacement = f'\\1{digests_html}\\3'
    html = re.sub(digests_pattern, replacement, html, flags=re.DOTALL)
    
    return html

def update_meta_information(html: str, data: Dict) -> str:
    """Update meta tags and page information"""
    
    # Update page title
    title_pattern = r'<title>[^<]*</title>'
    new_title = f'<title>Daily News Digest - {data["date_formatted"]} - Accessible Audio News</title>'
    html = re.sub(title_pattern, new_title, html)
    
    # Update meta description
    desc_pattern = r'<meta name="description" content="[^"]*">'
    sources_text = ', '.join(data['sources'][:3]) if data['sources'] else 'major UK sources'
    new_desc = f'<meta name="description" content="Daily AI-generated audio news digest for {data["date_formatted"]} from {sources_text}. Professional Irish voice, screen reader optimized.">'
    html = re.sub(desc_pattern, new_desc, html)
    
    return html

def main():
    """Main function to update the website"""
    print("🌐 Starting website update...")
    
    # Load the latest digest data
    digest_data = load_latest_digest_data()
    
    # Load recent digests
    recent_digests = load_recent_digests()
    
    # Update HTML template
    updated_html = update_html_template(digest_data, recent_digests)
    
    if updated_html:
        # Write updated HTML
        with open('docs/index.html', 'w', encoding='utf-8') as f:
            f.write(updated_html)
        
        print(f"✅ Website updated successfully")
        if digest_data:
            print(f"   📅 Date: {digest_data['date_formatted']}")
            print(f"   🎧 Audio: {digest_data['audio_file']}")
            print(f"   📊 Duration: {digest_data['duration_formatted']}")
            print(f"   🤖 AI: {'Enabled' if digest_data['ai_enabled'] else 'Fallback'}")
            print(f"   📰 Sources: {len(digest_data['sources'])}")
            print(f"   🎯 Themes: {len(digest_data['themes'])}")
    else:
        print("❌ Failed to update website")

if __name__ == "__main__":
    main()
