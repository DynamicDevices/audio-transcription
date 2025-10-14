#!/usr/bin/env python3
"""
Generate audio for top Guardian articles
Fetches the current top articles and creates premium audio versions
"""

import asyncio
import edge_tts
import os
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import unicodedata
from pydub import AudioSegment
import time

def fetch_top_guardian_articles(num_articles=3):
    """Fetch top articles from Guardian homepage"""
    print(f"🔍 Fetching top {num_articles} Guardian articles...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get("https://www.theguardian.com", headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for main article links
        article_links = []
        
        # Try different selectors for Guardian articles
        selectors = [
            'a[data-link-name*="article"]',
            'a[href*="/2025/"]',  # Current year articles
            '.fc-item__link',
            '.u-faux-block-link__overlay'
        ]
        
        for selector in selectors:
            links = soup.select(selector)
            for link in links:
                href = link.get('href', '')
                if href and '/2025/' in href and href.startswith('/'):
                    full_url = f"https://www.theguardian.com{href}"
                    if full_url not in [item['url'] for item in article_links]:
                        title = link.get_text(strip=True) or "No title"
                        article_links.append({
                            'url': full_url,
                            'title': title[:100] + "..." if len(title) > 100 else title
                        })
                        if len(article_links) >= num_articles:
                            break
            if len(article_links) >= num_articles:
                break
        
        if not article_links:
            # Fallback: use some recent Guardian articles
            print("⚠️  Could not fetch live articles, using recent examples...")
            article_links = [
                {
                    'url': 'https://www.theguardian.com/world/2025/oct/04/greta-thunberg-israel-gaza-sweden',
                    'title': 'Greta Thunberg tells Swedish officials she is being subjected to harsh treatment'
                },
                {
                    'url': 'https://www.theguardian.com/politics/2025/oct/14/uk-politics-latest-news',
                    'title': 'UK Politics Latest News'
                },
                {
                    'url': 'https://www.theguardian.com/world/2025/oct/14/world-news-latest',
                    'title': 'World News Latest'
                }
            ]
        
        print(f"✅ Found {len(article_links)} articles:")
        for i, article in enumerate(article_links[:num_articles], 1):
            print(f"   {i}. {article['title']}")
            print(f"      {article['url']}")
        
        return article_links[:num_articles]
        
    except Exception as e:
        print(f"❌ Error fetching articles: {e}")
        return []

def extract_article(url):
    """Extract article content from Guardian URL"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract title
        title_selectors = [
            'h1[data-gu-name="headline"]',
            'h1.content__headline',
            'h1',
            '.content__headline'
        ]
        
        title = "Unknown Title"
        for selector in title_selectors:
            title_elem = soup.select_one(selector)
            if title_elem:
                title = title_elem.get_text(strip=True)
                break
        
        # Extract author
        author = None
        author_selectors = [
            'a[rel="author"]',
            '.byline a',
            '[data-gu-name="meta"] a'
        ]
        
        for selector in author_selectors:
            author_elem = soup.select_one(selector)
            if author_elem:
                author = author_elem.get_text(strip=True)
                break
        
        # Extract date
        date = None
        date_selectors = [
            'time[datetime]',
            '.content__dateline time',
            '[data-gu-name="meta"] time'
        ]
        
        for selector in date_selectors:
            date_elem = soup.select_one(selector)
            if date_elem:
                date = date_elem.get('datetime') or date_elem.get_text(strip=True)
                break
        
        # Extract main content
        content_selectors = [
            'div[data-gu-name="body"]',
            '.content__article-body',
            '#maincontent',
            'article'
        ]
        
        content = ""
        for selector in content_selectors:
            content_div = soup.select_one(selector)
            if content_div:
                # Get all paragraphs
                paragraphs = content_div.find_all('p')
                if paragraphs:
                    content = ' '.join([p.get_text(separator=" ", strip=True) for p in paragraphs if p.get_text(strip=True)])
                    break
        
        if not content:
            # Fallback: try to get any paragraphs
            paragraphs = soup.find_all('p')
            if paragraphs:
                content = ' '.join([p.get_text(separator=" ", strip=True) for p in paragraphs[:10] if p.get_text(strip=True)])
        
        return {
            'title': title,
            'author': author,
            'published_date': date,
            'content': content,
            'url': url
        }
        
    except Exception as e:
        print(f"❌ Error extracting article from {url}: {e}")
        return None

def clean_text_for_speech(text):
    """Clean text for optimal speech synthesis"""
    if not text:
        return ""
    
    # Normalize Unicode characters
    text = unicodedata.normalize('NFKD', text)
    
    # Replace smart quotes and dashes
    text = re.sub(r"['']", "'", text)
    text = re.sub(r'[""]', '"', text)
    text = re.sub(r"[–—]", ", ", text)
    
    # Clean up whitespace and line breaks
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\r+', ' ', text)
    text = re.sub(r'\t+', ' ', text)
    
    # Remove URLs
    text = re.sub(r'https?://\S+', '', text)
    
    # Clean up punctuation spacing
    text = re.sub(r'\s*\.\s*', '. ', text)
    text = re.sub(r'\s*,\s*', ', ', text)
    text = re.sub(r'\s*;\s*', '; ', text)
    text = re.sub(r'\s*:\s*', ': ', text)
    
    # Remove excessive spaces
    text = re.sub(r'\s{2,}', ' ', text)
    
    return text.strip()

def create_audio_content(article, cleaned_content):
    """Create the final text content for audio with accessibility intro"""
    if not article or not cleaned_content:
        return ""
    
    # Create short, informative intro
    intro_parts = ["Here's a Guardian news report"]
    
    if article.get('title'):
        # Add topic hint from title
        title_lower = article['title'].lower()
        if any(word in title_lower for word in ['politics', 'election', 'government', 'minister', 'mp']):
            intro_parts.append("about UK politics")
        elif any(word in title_lower for word in ['world', 'international', 'global', 'country']):
            intro_parts.append("about world news")
        elif any(word in title_lower for word in ['climate', 'environment', 'green', 'carbon']):
            intro_parts.append("about climate and environment")
        elif any(word in title_lower for word in ['economy', 'business', 'market', 'finance']):
            intro_parts.append("about business and economy")
        elif any(word in title_lower for word in ['health', 'nhs', 'medical', 'covid']):
            intro_parts.append("about health")
        elif any(word in title_lower for word in ['technology', 'tech', 'digital', 'ai']):
            intro_parts.append("about technology")
    
    if article.get('author'):
        intro_parts.append(f"by {article['author']}")
    
    intro = ". ".join(intro_parts) + ". "
    
    return intro + cleaned_content

async def generate_edge_audio(text, voice_name, output_filename):
    """Generate audio using Edge TTS"""
    communicate = edge_tts.Communicate(text, voice_name)
    with open(output_filename, "wb") as file:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                file.write(chunk["data"])

async def main():
    """Main function to generate audio for top Guardian articles"""
    print("🎵 GUARDIAN TOP ARTICLES AUDIO GENERATOR")
    print("=" * 50)
    
    # Fetch top articles
    articles = fetch_top_guardian_articles(3)
    
    if not articles:
        print("❌ Could not fetch any articles. Exiting.")
        return
    
    voice_name = "en-IE-EmilyNeural"  # Irish Emily voice
    generated_files = []
    
    print(f"\n🎤 Generating audio with {voice_name}...")
    print("=" * 50)
    
    for i, article_info in enumerate(articles, 1):
        print(f"\n📰 Processing Article {i}: {article_info['title'][:60]}...")
        
        # Extract full article content
        article = extract_article(article_info['url'])
        
        if not article or not article['content']:
            print(f"   ❌ Could not extract content from article {i}")
            continue
        
        # Clean and prepare text
        cleaned_text = clean_text_for_speech(article['content'])
        final_text = create_audio_content(article, cleaned_text)
        
        if not final_text:
            print(f"   ❌ No content to convert for article {i}")
            continue
        
        # Create safe filename
        safe_title = re.sub(r'[^\w\s-]', '', article['title'])[:50]
        safe_title = re.sub(r'\s+', '_', safe_title)
        
        output_filename = f"guardian_top_{i}_{safe_title}.mp3"
        text_filename = f"guardian_top_{i}_{safe_title}.txt"
        
        # Save text for reference
        with open(text_filename, 'w', encoding='utf-8') as f:
            f.write(f"TITLE: {article['title']}\n")
            f.write(f"AUTHOR: {article.get('author', 'Unknown')}\n")
            f.write(f"URL: {article['url']}\n")
            f.write(f"DATE: {article.get('published_date', 'Unknown')}\n")
            f.write("=" * 60 + "\n\n")
            f.write(final_text)
        
        print(f"   📄 Text saved: {text_filename}")
        print(f"   🎤 Generating audio: {output_filename}")
        
        # Generate audio
        try:
            await generate_edge_audio(final_text, voice_name, output_filename)
            
            # Analyze audio
            audio = AudioSegment.from_mp3(output_filename)
            duration_s = len(audio) / 1000.0
            word_count = len(final_text.split())
            words_per_second = word_count / duration_s if duration_s > 0 else 0
            file_size_kb = os.path.getsize(output_filename) / 1024
            
            generated_files.append({
                'filename': output_filename,
                'text_file': text_filename,
                'title': article['title'],
                'author': article.get('author', 'Unknown'),
                'url': article['url'],
                'duration': duration_s,
                'words': word_count,
                'wps': words_per_second,
                'size_kb': file_size_kb
            })
            
            print(f"   ✅ Audio created: {duration_s:.1f}s, {word_count} words, {words_per_second:.2f} WPS, {file_size_kb:.0f}KB")
            
        except Exception as e:
            print(f"   ❌ Error generating audio: {e}")
    
    # Create summary report
    if generated_files:
        print(f"\n📊 AUDIO GENERATION SUMMARY")
        print("=" * 50)
        print(f"✅ Successfully generated {len(generated_files)} audio files:")
        
        total_duration = 0
        total_words = 0
        
        for i, file_info in enumerate(generated_files, 1):
            print(f"\n🎧 {i}. {file_info['filename']}")
            print(f"   📰 Title: {file_info['title'][:70]}...")
            print(f"   👤 Author: {file_info['author']}")
            print(f"   ⏱️  Duration: {file_info['duration']:.1f}s ({file_info['duration']/60:.1f} minutes)")
            print(f"   📝 Words: {file_info['words']}")
            print(f"   🎯 Speed: {file_info['wps']:.2f} WPS")
            print(f"   💾 Size: {file_info['size_kb']:.0f}KB")
            print(f"   🔗 URL: {file_info['url']}")
            
            total_duration += file_info['duration']
            total_words += file_info['words']
        
        avg_wps = total_words / total_duration if total_duration > 0 else 0
        
        print(f"\n📈 TOTALS:")
        print(f"   Total Duration: {total_duration:.1f}s ({total_duration/60:.1f} minutes)")
        print(f"   Total Words: {total_words}")
        print(f"   Average Speed: {avg_wps:.2f} WPS")
        
        print(f"\n🎯 ALL AUDIO FILES READY FOR TESTING!")
        print(f"   Voice: Irish Emily Neural (Premium)")
        print(f"   Format: MP3 (WhatsApp compatible)")
        print(f"   Quality: Professional accessibility standard")
        
    else:
        print("\n❌ No audio files were generated successfully.")

if __name__ == "__main__":
    asyncio.run(main())
