#!/usr/bin/env python3
"""
Audio Analysis Engineer Tool
Generate audio, then analyze the actual waveform to detect pauses and timing issues
"""

import requests
from bs4 import BeautifulSoup
from gtts import gTTS
import librosa
import numpy as np
from pydub import AudioSegment
import matplotlib.pyplot as plt
import re
import os

def extract_article_text():
    """Extract the Guardian article text"""
    url = "https://www.theguardian.com/world/2025/oct/04/greta-thunberg-israel-gaza-sweden"
    
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract content
    paragraphs = soup.find_all('p')
    content_paragraphs = [p.get_text().strip() for p in paragraphs 
                         if p.get_text().strip() and len(p.get_text().strip()) > 50]
    
    return ' '.join(content_paragraphs)

def create_test_audio_versions():
    """Create multiple versions to test pause issues"""
    
    base_content = extract_article_text()
    
    # Remove "Exclusive:" prefix
    base_content = re.sub(r'^Exclusive:\s*', '', base_content, flags=re.IGNORECASE)
    
    # Truncate to manageable length
    if len(base_content) > 2000:
        base_content = base_content[:2000]
        last_period = base_content.rfind('. ')
        if last_period > 1500:
            base_content = base_content[:last_period + 1]
    
    versions = {}
    
    # VERSION 1: Original with paragraph breaks (should have long pauses)
    print("🎵 Creating Version 1: With paragraph breaks...")
    version1 = "Here's a Guardian news report about Greta Thunberg.\n\nThe report is by Lorenzo Tondo.\n\n" + base_content
    tts1 = gTTS(text=version1, lang='en', tld='ie', slow=False)
    tts1.save("test_v1_with_breaks.mp3")
    versions['v1_with_breaks'] = version1
    
    # VERSION 2: No paragraph breaks but with "including" clause
    print("🎵 Creating Version 2: No breaks but with 'including'...")
    version2 = "Here's a Guardian news report about Greta Thunberg, reported by Lorenzo Tondo. " + base_content.replace('\n\n', ' ').replace('\n', ' ')
    tts2 = gTTS(text=version2, lang='en', tld='ie', slow=False)
    tts2.save("test_v2_with_including.mp3")
    versions['v2_with_including'] = version2
    
    # VERSION 3: Fixed "including" clause
    print("🎵 Creating Version 3: Fixed 'including' clause...")
    version3 = version2.replace(
        "harsh treatment, including insufficient amounts of both water and food",
        "harsh treatment with insufficient water and food"
    )
    version3 = re.sub(r', including ([^,]+),', r' with \1,', version3)
    tts3 = gTTS(text=version3, lang='en', tld='ie', slow=False)
    tts3.save("test_v3_fixed_including.mp3")
    versions['v3_fixed_including'] = version3
    
    return versions

def analyze_audio_pauses(filename, text_content):
    """Analyze actual audio file for pause detection"""
    
    print(f"\n🔍 ANALYZING: {filename}")
    print("=" * 50)
    
    try:
        # Load audio file
        y, sr = librosa.load(filename)
        
        # Calculate RMS (Root Mean Square) energy to detect silence/pauses
        rms = librosa.feature.rms(y=y, frame_length=2048, hop_length=512)[0]
        
        # Convert to time axis
        times = librosa.frames_to_time(np.arange(len(rms)), sr=sr, hop_length=512)
        
        # Detect silence (pauses) - threshold based on mean RMS
        silence_threshold = np.mean(rms) * 0.1  # 10% of mean energy
        silent_frames = rms < silence_threshold
        
        # Find pause segments longer than 0.3 seconds
        min_pause_duration = 0.3  # seconds
        min_pause_frames = int(min_pause_duration * sr / 512)
        
        pauses = []
        in_pause = False
        pause_start = 0
        
        for i, is_silent in enumerate(silent_frames):
            if is_silent and not in_pause:
                pause_start = i
                in_pause = True
            elif not is_silent and in_pause:
                pause_duration = i - pause_start
                if pause_duration >= min_pause_frames:
                    pause_time_start = times[pause_start]
                    pause_time_end = times[i]
                    pause_duration_sec = pause_time_end - pause_time_start
                    pauses.append((pause_time_start, pause_time_end, pause_duration_sec))
                in_pause = False
        
        # Report findings
        print(f"📊 AUDIO STATISTICS:")
        print(f"   Duration: {len(y)/sr:.2f} seconds")
        print(f"   Sample Rate: {sr} Hz")
        print(f"   RMS Mean: {np.mean(rms):.6f}")
        print(f"   Silence Threshold: {silence_threshold:.6f}")
        
        print(f"\n⏸️  DETECTED PAUSES (>{min_pause_duration}s):")
        if pauses:
            for i, (start, end, duration) in enumerate(pauses):
                print(f"   Pause {i+1}: {start:.2f}s - {end:.2f}s (duration: {duration:.2f}s)")
                
                # Try to correlate with text
                # Estimate words per second (typical speech is ~2.5 words/second)
                words = text_content.split()
                wps = len(words) / (len(y)/sr)
                word_position = int(start * wps)
                
                if word_position < len(words):
                    context_start = max(0, word_position - 5)
                    context_end = min(len(words), word_position + 5)
                    context = ' '.join(words[context_start:context_end])
                    print(f"      Context: '...{context}...'")
        else:
            print("   No significant pauses detected!")
        
        return pauses
        
    except Exception as e:
        print(f"❌ Error analyzing {filename}: {e}")
        return []

def main():
    print("🎧 AUDIO ENGINEERING ANALYSIS")
    print("=" * 60)
    print("Generating test audio files and analyzing actual pause patterns...")
    
    # Create test versions
    versions = create_test_audio_versions()
    
    # Analyze each version
    results = {}
    
    for version_name, text in versions.items():
        filename = f"test_{version_name}.mp3"
        if os.path.exists(filename):
            pauses = analyze_audio_pauses(filename, text)
            results[version_name] = pauses
    
    # Compare results
    print(f"\n📋 ENGINEERING ANALYSIS SUMMARY")
    print("=" * 60)
    
    for version_name, pauses in results.items():
        print(f"\n{version_name.upper()}:")
        print(f"  Total pauses: {len(pauses)}")
        if pauses:
            avg_pause = np.mean([p[2] for p in pauses])
            max_pause = max([p[2] for p in pauses])
            print(f"  Average pause: {avg_pause:.2f}s")
            print(f"  Longest pause: {max_pause:.2f}s")
        else:
            print(f"  No significant pauses detected")
    
    # Find the specific "subjected to" issue
    print(f"\n🎯 SEARCHING FOR 'SUBJECTED TO' PAUSE:")
    for version_name, text in versions.items():
        if "she has been subjected to" in text.lower():
            print(f"\n{version_name}:")
            # Find the position in text
            pos = text.lower().find("she has been subjected to")
            context = text[max(0, pos-50):pos+100]
            print(f"  Text context: '...{context}...'")
            
            # Check if this version has pauses
            if version_name in results and results[version_name]:
                print(f"  Has {len(results[version_name])} pauses - INVESTIGATE THIS VERSION")
            else:
                print(f"  No significant pauses - THIS VERSION IS BETTER")
    
    print(f"\n✅ ANALYSIS COMPLETE")
    print(f"📁 Audio files saved for manual inspection:")
    for version_name in versions.keys():
        filename = f"test_{version_name}.mp3"
        if os.path.exists(filename):
            print(f"   - {filename}")

if __name__ == "__main__":
    main()
