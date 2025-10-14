#!/usr/bin/env python3
"""
Create Audio File for Guardian Article
Generates an MP3 file from the Guardian article for WhatsApp sharing
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
        
        # Extract date
        date_elem = soup.find('time')
        date = date_elem.get('datetime') or date_elem.get_text().strip() if date_elem else None
        
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
            'date': date,
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
    
    return text.strip()

def create_audio_content(article, max_length=4000):
    """Create the text content that will be converted to audio"""
    content_parts = []
    
    # Add title
    content_parts.append(f"Article: {article['title']}")
    
    # Add author if available
    if article['author']:
        content_parts.append(f"By {article['author']}")
    
    # Add date if available
    if article['date']:
        content_parts.append(f"Published {article['date']}")
    
    # Clean the main content
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
        
        content_parts.append(cleaned_content)
        content_parts.append("This article has been shortened for audio. The full version is available at the original link.")
    else:
        content_parts.append(cleaned_content)
    
    return '\n\n'.join(content_parts)

def main():
    url = "https://www.theguardian.com/world/2025/oct/04/greta-thunberg-israel-gaza-sweden"
    
    print("🎧 Creating Audio File for Your Father")
    print("=====================================")
    print(f"📖 Extracting article from: {url}")
    
    # Extract article
    article = extract_guardian_article(url)
    if not article:
        print("❌ Failed to extract article content")
        return 1
    
    print(f"✅ Article extracted successfully!")
    print(f"   Title: {article['title']}")
    print(f"   Author: {article['author'] or 'Unknown'}")
    print(f"   Content length: {len(article['content'])} characters")
    
    # Create audio content
    print("🎙️  Processing content for audio...")
    audio_text = create_audio_content(article)
    
    # Estimate duration
    word_count = len(audio_text.split())
    duration_minutes = word_count / 175  # ~175 words per minute
    
    print(f"📊 Audio will be ~{duration_minutes:.1f} minutes long")
    print(f"📝 Processing {word_count} words...")
    
    # Create audio file using gTTS (Google Text-to-Speech)
    print("🎵 Generating audio file...")
    
    try:
        # Use Irish English accent (closest to what you requested)
        tts = gTTS(text=audio_text, lang='en', tld='ie', slow=False)
        
        # Save to file
        filename = "guardian_article_for_father.mp3"
        tts.save(filename)
        
        print("✅ SUCCESS! Audio file created!")
        print(f"📱 File: {filename}")
        print(f"🎧 Duration: ~{duration_minutes:.1f} minutes")
        print(f"📊 Ready to share on WhatsApp!")
        print("")
        print("🎙️  Voice: Irish English female voice (Google TTS)")
        print("📄 Content: Accurate Guardian article with proper attribution")
        print("")
        print(f"👨‍🦯 Your father can now listen to this news article!")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error creating audio file: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
