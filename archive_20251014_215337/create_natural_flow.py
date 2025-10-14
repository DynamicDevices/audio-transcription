#!/usr/bin/env python3
"""
Create Natural Flowing Audio - Fix Pauses and Improve Speech Flow
"""

import requests
from bs4 import BeautifulSoup
from gtts import gTTS
import re
import sys

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

def create_natural_flowing_text(article, max_length=4000):
    """Create text optimized for natural speech flow"""
    
    # Start with raw content
    content = article['content']
    
    # STEP 1: Clean up problematic formatting
    # Remove URLs
    content = re.sub(r'https?://[^\s]+', '', content)
    
    # Remove "Exclusive:" prefix
    content = re.sub(r'^Exclusive:\s*', '', content, flags=re.IGNORECASE)
    
    # Normalize quotes (but keep them - they're important for speech)
    content = re.sub(r'[""]', '"', content)
    content = re.sub(r"['']", "'", content)
    
    # STEP 2: Fix paragraph breaks that cause long pauses
    # Replace double newlines with single space (removes paragraph pauses)
    content = re.sub(r'\n\n+', ' ', content)
    
    # Replace single newlines with space
    content = re.sub(r'\n', ' ', content)
    
    # STEP 3: Fix sentence flow for natural speech
    # Ensure proper spacing after periods
    content = re.sub(r'\.([A-Z])', r'. \1', content)
    
    # Fix spacing around quotes for better flow
    content = re.sub(r'"\s*([A-Z])', r'" \1', content)
    content = re.sub(r'([.!?])\s*"', r'\1"', content)
    
    # STEP 4: Replace problematic punctuation that causes weird pauses
    # Replace em/en dashes with commas (more natural for speech)
    content = re.sub(r'\s*[–—]\s*', ', ', content)
    
    # Fix multiple spaces
    content = re.sub(r'\s+', ' ', content)
    
    # STEP 5: Truncate if needed, but maintain sentence flow
    if len(content) > max_length:
        truncated = content[:max_length]
        # Find last complete sentence
        last_sentence = max(
            truncated.rfind('. '),
            truncated.rfind('! '),
            truncated.rfind('? ')
        )
        if last_sentence > max_length * 0.8:
            content = truncated[:last_sentence + 1]
        else:
            # Find last comma for a more natural break
            last_comma = truncated.rfind(', ')
            if last_comma > max_length * 0.9:
                content = truncated[:last_comma] + '.'
            else:
                content = truncated + '.'
    
    # STEP 6: Create natural introduction
    intro = f"Here's a Guardian news report about Greta Thunberg"
    if article['author']:
        intro += f", reported by {article['author']}"
    intro += ". "
    
    # STEP 7: Combine and final cleanup
    full_text = intro + content.strip()
    
    # Final cleanup - ensure no double spaces or weird punctuation
    full_text = re.sub(r'\s+', ' ', full_text)
    full_text = re.sub(r'\s*([.!?,:;])\s*', r'\1 ', full_text)
    
    return full_text.strip()

def main():
    url = "https://www.theguardian.com/world/2025/oct/04/greta-thunberg-israel-gaza-sweden"
    
    print("🎧 Creating Natural Flowing Audio - No Awkward Pauses")
    print("====================================================")
    
    # Extract article
    article = extract_guardian_article(url)
    if not article:
        print("❌ Failed to extract article content")
        return 1
    
    print(f"✅ Article extracted: {article['title'][:60]}...")
    
    # Create natural flowing text
    print("🎙️  Optimizing text for natural speech flow...")
    audio_text = create_natural_flowing_text(article)
    
    word_count = len(audio_text.split())
    duration_minutes = word_count / 175
    
    print(f"📊 Optimized text: {word_count} words, ~{duration_minutes:.1f} minutes")
    
    # Show how it will sound
    print("\n🎯 NATURAL FLOW PREVIEW:")
    print("-" * 50)
    preview = audio_text[:300] + "..."
    print(f'"{preview}"')
    print("-" * 50)
    
    # Create audio with better settings for natural flow
    print("\n🎵 Generating natural-flowing audio...")
    
    try:
        # Use gTTS with settings optimized for natural speech
        tts = gTTS(
            text=audio_text, 
            lang='en', 
            tld='ie',  # Irish accent
            slow=False  # Normal speed for natural flow
        )
        
        filename = "guardian_article_natural_flow.mp3"
        tts.save(filename)
        
        print("✅ SUCCESS! Natural flowing audio created!")
        print(f"📱 File: {filename}")
        print(f"🎧 Duration: ~{duration_minutes:.1f} minutes")
        print("")
        print("🎙️  Improvements made:")
        print("   ✅ Removed paragraph breaks that caused long pauses")
        print("   ✅ Fixed sentence transitions for smooth flow")
        print("   ✅ Replaced dashes with commas (more natural)")
        print("   ✅ Optimized punctuation spacing")
        print("   ✅ Natural introduction without awkward breaks")
        print("   ✅ Continuous narrative flow")
        print("")
        print("👨‍🦯 Much smoother listening experience!")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error creating audio file: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
