#!/usr/bin/env python3
"""
Create Engaging Audio File - Natural Introduction Style
Removes boring preface while maintaining accuracy
"""

import requests
from bs4 import BeautifulSoup
from gtts import gTTS
import re
import sys
from datetime import datetime

def extract_guardian_article(url):
    """Extract article content from Guardian URL"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract title
        title_elem = soup.find('h1')
        title = title_elem.get_text().strip() if title_elem else "Guardian Article"
        
        # Extract author
        author_elem = soup.find('a', {'rel': 'author'}) or soup.find(class_='byline')
        author = author_elem.get_text().strip() if author_elem else None
        
        # Extract article content
        content_paragraphs = []
        
        # Try multiple selectors for Guardian content
        selectors = [
            'div[data-gu-name="body"] p',
            '.content__article-body p',
            'article p',
            '.article-body p'
        ]
        
        for selector in selectors:
            paragraphs = soup.select(selector)
            if paragraphs:
                content_paragraphs = [p.get_text().strip() for p in paragraphs if p.get_text().strip()]
                break
        
        if not content_paragraphs:
            # Fallback: get all paragraphs
            paragraphs = soup.find_all('p')
            content_paragraphs = [p.get_text().strip() for p in paragraphs 
                                if p.get_text().strip() and len(p.get_text().strip()) > 50]
        
        content = '\n\n'.join(content_paragraphs)
        
        return {
            'title': title,
            'author': author,
            'content': content,
            'url': url
        }
        
    except Exception as e:
        print(f"Error extracting article: {e}")
        return None

def clean_text_for_speech(text):
    """Clean text for better TTS pronunciation"""
    # Remove URLs
    text = re.sub(r'https?://[^\s]+', '', text)
    
    # Normalize quotes
    text = re.sub(r'[""]', '"', text)
    text = re.sub(r"['']", "'", text)
    
    # Replace em/en dashes
    text = re.sub(r'[–—]', ' - ', text)
    
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove "Exclusive:" prefix if present
    text = re.sub(r'^Exclusive:\s*', '', text)
    
    return text.strip()

def create_engaging_audio_content(article, max_length=4000):
    """Create engaging audio content with natural introduction"""
    
    # Clean the main content first
    cleaned_content = clean_text_for_speech(article['content'])
    
    # Truncate if too long (keep it concise for WhatsApp)
    if len(cleaned_content) > max_length:
        # Try to end at sentence boundary
        truncated = cleaned_content[:max_length]
        last_period = truncated.rfind('. ')
        if last_period > max_length * 0.8:  # If we found a period in the last 20%
            cleaned_content = truncated[:last_period + 1]
        else:
            cleaned_content = truncated + "..."
    
    # Create a natural, engaging introduction
    intro_parts = []
    
    # Natural opening based on the story
    if "Greta Thunberg" in article['title']:
        intro_parts.append("Here's a Guardian news report about Greta Thunberg.")
    elif "Israel" in article['title'] or "Gaza" in article['title']:
        intro_parts.append("This is a breaking news story from The Guardian.")
    else:
        intro_parts.append("Here's today's news from The Guardian.")
    
    # Add author naturally if available
    if article['author']:
        intro_parts.append(f"The report is by {article['author']}.")
    
    # Start the story immediately
    intro = ' '.join(intro_parts) + '\n\n'
    
    # Combine intro with content
    full_content = intro + cleaned_content
    
    return full_content

def main():
    url = "https://www.theguardian.com/world/2025/oct/04/greta-thunberg-israel-gaza-sweden"
    
    print("🎧 Creating Improved Audio File - Natural Style")
    print("===============================================")
    print(f"📖 Extracting article from Guardian...")
    
    # Extract article
    article = extract_guardian_article(url)
    if not article:
        print("❌ Failed to extract article content")
        return 1
    
    print(f"✅ Article extracted successfully!")
    print(f"   Title: {article['title']}")
    print(f"   Author: {article['author'] or 'Unknown'}")
    
    # Create engaging audio content
    print("🎙️  Creating natural, engaging introduction...")
    audio_text = create_engaging_audio_content(article)
    
    # Estimate duration
    word_count = len(audio_text.split())
    duration_minutes = word_count / 175  # ~175 words per minute
    
    print(f"📊 Audio will be ~{duration_minutes:.1f} minutes long")
    print(f"📝 Processing {word_count} words...")
    
    # Show the new introduction style
    print("\n🎯 NEW INTRODUCTION STYLE:")
    print("-" * 40)
    intro_preview = audio_text[:200] + "..."
    print(f'"{intro_preview}"')
    print("-" * 40)
    
    # Create audio file using gTTS
    print("\n🎵 Generating improved audio file...")
    
    try:
        # Use Irish English accent
        tts = gTTS(text=audio_text, lang='en', tld='ie', slow=False)
        
        # Save to file
        filename = "guardian_article_improved.mp3"
        tts.save(filename)
        
        print("✅ SUCCESS! Improved audio file created!")
        print(f"📱 File: {filename}")
        print(f"🎧 Duration: ~{duration_minutes:.1f} minutes")
        print(f"📊 Ready to share on WhatsApp!")
        print("")
        print("🎙️  Improvements made:")
        print("   ✅ Natural, engaging introduction")
        print("   ✅ No boring timestamps or formal preface")
        print("   ✅ Flows like a news podcast")
        print("   ✅ 100% accurate Guardian content")
        print("   ✅ Irish English female voice")
        print("")
        print(f"👨‍🦯 Much better listening experience for your father!")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error creating audio file: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
