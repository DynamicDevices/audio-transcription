#!/usr/bin/env python3
"""
Professional HTML Text Cleaning - Using Industry-Standard Tools
Clean HTML properly BEFORE TTS to eliminate all formatting artifacts
"""

import requests
from newspaper import Article
from readability import Document
import html2text
import bleach
from gtts import gTTS
import re
import unicodedata

def method1_newspaper3k(url):
    """Method 1: Using Newspaper3k - Professional article extraction"""
    
    print("📰 METHOD 1: Newspaper3k extraction")
    
    try:
        article = Article(url)
        article.download()
        article.parse()
        
        title = article.title
        authors = article.authors
        text = article.text
        
        print(f"   Title: {title}")
        print(f"   Authors: {authors}")
        print(f"   Text length: {len(text)} chars")
        print(f"   First 100 chars: '{text[:100]}...'")
        
        return {
            'title': title,
            'authors': authors,
            'text': text,
            'method': 'newspaper3k'
        }
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

def method2_readability(url):
    """Method 2: Using Readability - Mozilla's algorithm"""
    
    print("\n📖 METHOD 2: Readability extraction")
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers)
        
        doc = Document(response.content)
        
        title = doc.title()
        content = doc.summary()
        
        # Convert HTML to clean text using html2text
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        h.ignore_emphasis = True
        h.body_width = 0  # No line wrapping
        
        clean_text = h.handle(content)
        
        # Remove markdown artifacts
        clean_text = re.sub(r'\n+', ' ', clean_text)  # Remove newlines
        clean_text = re.sub(r'\s+', ' ', clean_text)  # Normalize spaces
        clean_text = clean_text.strip()
        
        print(f"   Title: {title}")
        print(f"   Text length: {len(clean_text)} chars")
        print(f"   First 100 chars: '{clean_text[:100]}...'")
        
        return {
            'title': title,
            'text': clean_text,
            'method': 'readability'
        }
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

def method3_html2text_bleach(url):
    """Method 3: html2text + bleach for maximum cleaning"""
    
    print("\n🧹 METHOD 3: html2text + bleach cleaning")
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers)
        
        # First, use bleach to clean HTML
        cleaned_html = bleach.clean(
            response.text,
            tags=['p', 'div', 'h1', 'h2', 'h3', 'span', 'article'],
            attributes={},
            strip=True
        )
        
        # Then convert to text
        h = html2text.HTML2Text()
        h.ignore_links = True
        h.ignore_images = True
        h.ignore_emphasis = True
        h.ignore_tables = True
        h.body_width = 0
        h.ul_item_mark = ''  # Remove bullet points
        
        text = h.handle(cleaned_html)
        
        # Aggressive cleaning for TTS
        text = re.sub(r'\n+', ' ', text)  # Remove all newlines
        text = re.sub(r'\s+', ' ', text)  # Normalize spaces
        text = re.sub(r'[#*_`]', '', text)  # Remove markdown
        text = text.strip()
        
        print(f"   Text length: {len(text)} chars")
        print(f"   First 100 chars: '{text[:100]}...'")
        
        return {
            'text': text,
            'method': 'html2text+bleach'
        }
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

def clean_text_for_perfect_tts(text):
    """Apply final cleaning specifically for TTS naturalness"""
    
    print("\n🎙️  FINAL TTS OPTIMIZATION:")
    
    # Unicode normalization
    text = unicodedata.normalize('NFKD', text)
    
    # Remove or fix problematic characters for TTS
    
    # Fix smart quotes and apostrophes
    text = re.sub(r'[""]', '"', text)
    text = re.sub(r"['']", "'", text)
    
    # Remove or replace em/en dashes
    text = re.sub(r'[–—]', ' ', text)
    
    # Fix ellipsis
    text = re.sub(r'…', '...', text)
    
    # Remove extra punctuation that causes pauses
    text = re.sub(r'[;:]', ',', text)  # Replace with commas (shorter pauses)
    
    # Fix parenthetical statements (major pause causers)
    text = re.sub(r'\([^)]*\)', '', text)  # Remove completely
    
    # Fix quote attribution patterns
    text = re.sub(r',\s*"([^"]+)",\s*([^.]+)\.', r'. \2 said "\1".', text)
    
    # Normalize whitespace around punctuation
    text = re.sub(r'\s*([.!?])\s*', r'\1 ', text)
    text = re.sub(r'\s*,\s*', r', ', text)
    
    # Remove multiple consecutive spaces
    text = re.sub(r'\s+', ' ', text)
    
    # Clean up sentence boundaries
    text = re.sub(r'\.([A-Z])', r'. \1', text)
    
    text = text.strip()
    
    print(f"   Final length: {len(text)} chars")
    
    # Check for the problematic "Swedish officials" phrase
    if "swedish officials" in text.lower():
        pos = text.lower().find("swedish officials")
        context_start = max(0, pos - 50)
        context_end = min(len(text), pos + 100)
        context = text[context_start:context_end]
        print(f"   Swedish officials context: '...{context}...'")
    
    return text

def compare_extraction_methods(url):
    """Compare all extraction methods and choose the best"""
    
    print("🔬 COMPARING PROFESSIONAL EXTRACTION METHODS")
    print("=" * 60)
    
    methods = [
        method1_newspaper3k,
        method2_readability,
        method3_html2text_bleach
    ]
    
    results = {}
    
    for method_func in methods:
        result = method_func(url)
        if result:
            results[result['method']] = result
    
    # Analyze and choose best method
    print(f"\n📊 COMPARISON RESULTS:")
    
    best_method = None
    best_score = 0
    
    for method_name, data in results.items():
        text = data['text']
        
        # Score based on text quality indicators
        score = 0
        
        # Length (should be substantial but not too long)
        if 2000 <= len(text) <= 8000:
            score += 3
        elif 1000 <= len(text) <= 10000:
            score += 2
        else:
            score += 1
        
        # Should contain key phrases
        if "greta thunberg" in text.lower():
            score += 2
        if "swedish officials" in text.lower():
            score += 2
        if "israeli custody" in text.lower():
            score += 1
        
        # Penalize for artifacts
        if text.count('\n') > 10:
            score -= 2
        if '[]' in text or '()' in text:
            score -= 1
        
        print(f"   {method_name}: Score {score}, Length {len(text)}")
        
        if score > best_score:
            best_score = score
            best_method = method_name
    
    if best_method:
        print(f"\n🏆 WINNER: {best_method} (score: {best_score})")
        return results[best_method]['text']
    else:
        print(f"\n❌ No suitable extraction method found")
        return None

def create_professional_audio():
    """Create audio using professional text extraction"""
    
    url = "https://www.theguardian.com/world/2025/oct/04/greta-thunberg-israel-gaza-sweden"
    
    # Get the best extracted text
    clean_text = compare_extraction_methods(url)
    
    if not clean_text:
        print("❌ Failed to extract clean text")
        return
    
    # Apply final TTS optimization
    optimized_text = clean_text_for_perfect_tts(clean_text)
    
    # Truncate if too long
    if len(optimized_text) > 3500:
        truncated = optimized_text[:3500]
        last_period = truncated.rfind('. ')
        if last_period > 3000:
            optimized_text = truncated[:last_period + 1]
    
    # Add natural introduction
    intro = "Here's a Guardian news report about Greta Thunberg, reported by Lorenzo Tondo. "
    
    final_text = intro + optimized_text
    
    word_count = len(final_text.split())
    duration = word_count / 175
    
    print(f"\n🎵 CREATING PROFESSIONAL AUDIO:")
    print(f"   Words: {word_count}")
    print(f"   Estimated duration: {duration:.1f} minutes")
    
    try:
        tts = gTTS(
            text=final_text,
            lang='en',
            tld='ie',  # Irish accent
            slow=False
        )
        
        filename = "guardian_article_PROFESSIONAL.mp3"
        tts.save(filename)
        
        print(f"✅ SUCCESS! Created: {filename}")
        print(f"🎯 This should have the cleanest text and most natural flow!")
        print(f"📊 File ready for WhatsApp sharing")
        
    except Exception as e:
        print(f"❌ Error creating audio: {e}")

def main():
    create_professional_audio()

if __name__ == "__main__":
    main()
