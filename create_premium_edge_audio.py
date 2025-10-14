#!/usr/bin/env python3
"""
Create High-Quality Audio with Microsoft Edge TTS

Edge TTS offers professional neural voices for free - much better than gTTS
"""

import asyncio
import edge_tts
import os
import subprocess
from pydub import AudioSegment

async def create_edge_tts_audio(text, voice="en-IE-EmilyNeural", output_file="guardian_edge_PREMIUM.mp3"):
    """Generate high-quality audio using Microsoft Edge TTS"""
    
    print(f"🎤 Generating premium audio with Edge TTS...")
    print(f"   Voice: {voice}")
    
    try:
        # Create TTS communication
        communicate = edge_tts.Communicate(text, voice)
        
        # Generate audio
        temp_file = output_file.replace('.mp3', '.mp3.temp')
        await communicate.save(temp_file)
        
        if os.path.exists(temp_file):
            # Rename to final file
            os.rename(temp_file, output_file)
            print(f"✅ Premium audio created: {output_file}")
            return output_file
        else:
            print(f"❌ Failed to create audio file")
            return None
            
    except Exception as e:
        print(f"❌ Edge TTS error: {e}")
        return None

async def test_multiple_edge_voices():
    """Test different Edge TTS voices to find the best one"""
    
    print(f"🎵 TESTING MULTIPLE EDGE TTS VOICES")
    print("=" * 40)
    
    test_text = "Guardian news. This is a test of voice quality and natural speech flow for visually impaired users."
    
    # High-quality female voices
    voices = [
        ("en-IE-EmilyNeural", "Irish Emily (Neural)"),
        ("en-GB-SoniaNeural", "British Sonia (Neural)"), 
        ("en-US-JennyNeural", "American Jenny (Neural)"),
        ("en-AU-NatashaNeural", "Australian Natasha (Neural)"),
        ("en-CA-ClaraNeural", "Canadian Clara (Neural)")
    ]
    
    results = []
    
    for voice_id, voice_name in voices:
        try:
            print(f"\n🎤 Testing {voice_name}...")
            
            filename = f"edge_voice_{voice_id.replace('-', '_')}.mp3"
            
            communicate = edge_tts.Communicate(test_text, voice_id)
            await communicate.save(filename)
            
            if os.path.exists(filename):
                # Analyze timing
                try:
                    audio = AudioSegment.from_mp3(filename)
                    duration = len(audio) / 1000.0
                    word_count = len(test_text.split())
                    wps = word_count / duration
                    
                    results.append((voice_name, voice_id, wps, filename))
                    print(f"   ✅ {voice_name}: {wps:.2f} WPS")
                    
                except Exception as e:
                    print(f"   ⚠️ Created file but analysis failed: {e}")
                    results.append((voice_name, voice_id, 0, filename))
            else:
                print(f"   ❌ Failed to create {filename}")
                
        except Exception as e:
            print(f"   ❌ {voice_name} failed: {e}")
    
    # Show results
    if results:
        print(f"\n📊 EDGE TTS VOICE COMPARISON:")
        print(f"{'VOICE':<25} {'WPS':<6} {'FILE'}")
        print("-" * 50)
        
        for voice_name, voice_id, wps, filename in results:
            wps_str = f"{wps:.2f}" if wps > 0 else "N/A"
            print(f"{voice_name:<25} {wps_str:<6} {filename}")
        
        # Find best performance
        if any(r[2] > 0 for r in results):
            best = max((r for r in results if r[2] > 0), key=lambda x: x[2])
            print(f"\n🏆 FASTEST: {best[0]} ({best[2]:.2f} WPS)")
    
    return results

async def create_full_article_edge():
    """Create full Guardian article with best Edge TTS voice"""
    
    print(f"\n🎯 CREATING FULL ARTICLE WITH PREMIUM EDGE TTS")
    print("=" * 50)
    
    # Use the same text processing as before
    import requests
    from bs4 import BeautifulSoup
    import re
    
    # Extract article
    url = "https://www.theguardian.com/world/2025/oct/04/greta-thunberg-israel-gaza-sweden"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract content
    title_tag = soup.find('h1', {'data-gu-name': 'headline'}) or soup.find('h1')
    title = title_tag.get_text(strip=True) if title_tag else "Guardian Article"
    
    author_tag = soup.find('a', {'rel': 'author'}) or soup.find('address')
    author = author_tag.get_text(strip=True) if author_tag else "Guardian Staff"
    
    main_content_div = soup.find('div', {'data-gu-name': 'body'})
    if main_content_div:
        paragraphs = main_content_div.find_all('p')
        content = " ".join([p.get_text(separator=" ", strip=True) for p in paragraphs])
    else:
        content_div = soup.find('div', class_='article-body-commercial-selector') or soup.find('article')
        content = content_div.get_text(separator=" ", strip=True) if content_div else ""
    
    # Clean text
    content = re.sub(r'[\r\n\t]+', ' ', content)
    content = re.sub(r'[\u00A0\u1680\u2000-\u200B\u202F\u205F\u3000\uFEFF]+', ' ', content)
    content = re.sub(r'https?://[^\s]+', '', content)
    content = re.sub(r'[""]', '"', content)
    content = re.sub(r"['']", "'", content)
    content = re.sub(r'[–—]', ', ', content)
    content = re.sub(r'\s+', ' ', content)
    
    # Limit length
    if len(content) > 4000:
        content = content[:4000].rsplit('.', 1)[0] + '.'
    
    # Create accessibility intro
    intro = f"Guardian news. {title.split(':')[0].strip()}. By {author}."
    full_text = f"{intro} {content}"
    
    print(f"✅ Text ready: {len(full_text.split())} words")
    
    # Generate with best Irish voice
    audio_file = await create_edge_tts_audio(
        full_text, 
        "en-IE-EmilyNeural", 
        "guardian_edge_PREMIUM_QUALITY.mp3"
    )
    
    if audio_file:
        # Analyze final result
        try:
            audio = AudioSegment.from_mp3(audio_file)
            duration = len(audio) / 1000.0
            word_count = len(full_text.split())
            wps = word_count / duration
            file_size = os.path.getsize(audio_file)
            
            print(f"\n📊 PREMIUM AUDIO ANALYSIS:")
            print(f"   Duration: {duration:.1f} seconds ({duration/60:.1f} minutes)")
            print(f"   Words: {word_count}")
            print(f"   WPS: {wps:.2f}")
            print(f"   File size: {file_size/1024:.0f}KB")
            
            if wps >= 2.5:
                print(f"🎉 EXCELLENT! Premium quality achieved!")
            elif wps >= 2.0:
                print(f"✅ GOOD! Much better than gTTS")
            else:
                print(f"⚠️ Still room for improvement")
            
            # Save text for reference
            with open("edge_premium_text.txt", 'w', encoding='utf-8') as f:
                f.write(f"# PREMIUM EDGE TTS TEXT\n")
                f.write(f"# Voice: en-IE-EmilyNeural\n")
                f.write(f"# Title: {title}\n")
                f.write(f"# Author: {author}\n\n")
                f.write(full_text)
            
            print(f"\n🎧 PREMIUM AUDIO: {audio_file}")
            print(f"📄 Text saved: edge_premium_text.txt")
            print(f"🎯 This should have professional voice quality!")
            
        except Exception as e:
            print(f"⚠️ Analysis failed: {e}")
            print(f"🎧 Audio created: {audio_file}")

async def main():
    print("🎤 CREATING PREMIUM QUALITY TTS AUDIO")
    print("=" * 45)
    print("Using Microsoft Edge TTS - professional neural voices")
    print("This addresses gTTS limitations with premium technology")
    print()
    
    # Test multiple voices first
    voice_results = await test_multiple_edge_voices()
    
    # Create full article with best voice
    await create_full_article_edge()
    
    print(f"\n🎯 WHY EDGE TTS IS BETTER THAN gTTS:")
    print(f"   ✅ Neural AI voices (not concatenative)")
    print(f"   ✅ Professional prosody and flow")
    print(f"   ✅ No network chunking delays")
    print(f"   ✅ Consistent high quality")
    print(f"   ✅ Still free to use")

if __name__ == "__main__":
    asyncio.run(main())
