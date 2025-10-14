#!/usr/bin/env python3
"""
Deep Audio Analysis - Find Exact Sources of Unnatural Delays
Analyze waveform, timing, and TTS behavior to eliminate all pauses
"""

import numpy as np
from pydub import AudioSegment
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
from gtts import gTTS
import re
import os
import time

def analyze_audio_waveform_detailed(filename):
    """Deep analysis of audio waveform to find exact pause locations"""
    
    print(f"\n🔍 DEEP WAVEFORM ANALYSIS: {filename}")
    print("=" * 60)
    
    # Load audio
    audio = AudioSegment.from_mp3(filename)
    
    # Convert to numpy array for detailed analysis
    samples = np.array(audio.get_array_of_samples())
    if audio.channels == 2:
        samples = samples.reshape((-1, 2))
        samples = samples.mean(axis=1)  # Convert to mono
    
    sample_rate = audio.frame_rate
    duration = len(samples) / sample_rate
    
    print(f"📊 Audio Properties:")
    print(f"   Duration: {duration:.2f} seconds")
    print(f"   Sample Rate: {sample_rate} Hz")
    print(f"   Total Samples: {len(samples):,}")
    
    # Calculate RMS energy in small windows (50ms)
    window_size = int(sample_rate * 0.05)  # 50ms windows
    hop_size = int(sample_rate * 0.01)     # 10ms hops for precision
    
    rms_values = []
    time_stamps = []
    
    for i in range(0, len(samples) - window_size, hop_size):
        window = samples[i:i + window_size]
        rms = np.sqrt(np.mean(window.astype(np.float64) ** 2))
        rms_values.append(rms)
        time_stamps.append(i / sample_rate)
    
    rms_values = np.array(rms_values)
    time_stamps = np.array(time_stamps)
    
    # Calculate dynamic threshold based on audio statistics
    mean_rms = np.mean(rms_values)
    std_rms = np.std(rms_values)
    
    # Multiple threshold levels for different types of pauses
    silence_threshold_strict = mean_rms * 0.05    # Very quiet (definite pause)
    silence_threshold_loose = mean_rms * 0.15     # Somewhat quiet (potential pause)
    
    print(f"📈 RMS Statistics:")
    print(f"   Mean RMS: {mean_rms:.4f}")
    print(f"   Std RMS: {std_rms:.4f}")
    print(f"   Strict Silence Threshold: {silence_threshold_strict:.4f}")
    print(f"   Loose Silence Threshold: {silence_threshold_loose:.4f}")
    
    # Find pause segments with different strictness levels
    strict_pauses = find_pause_segments(rms_values, time_stamps, silence_threshold_strict, min_duration=0.15)
    loose_pauses = find_pause_segments(rms_values, time_stamps, silence_threshold_loose, min_duration=0.1)
    
    print(f"\n⏸️  DETECTED PAUSES:")
    print(f"   Strict pauses (>0.15s): {len(strict_pauses)}")
    print(f"   Loose pauses (>0.1s): {len(loose_pauses)}")
    
    # Analyze pause patterns
    if strict_pauses:
        pause_durations = [end - start for start, end in strict_pauses]
        avg_pause = np.mean(pause_durations)
        max_pause = np.max(pause_durations)
        
        print(f"\n📊 PAUSE ANALYSIS:")
        print(f"   Average pause: {avg_pause:.3f}s")
        print(f"   Longest pause: {max_pause:.3f}s")
        print(f"   Total pause time: {sum(pause_durations):.2f}s ({sum(pause_durations)/duration*100:.1f}% of audio)")
        
        print(f"\n🎯 PROBLEMATIC PAUSES (>0.2s):")
        for i, (start, end) in enumerate(strict_pauses):
            pause_duration = end - start
            if pause_duration > 0.2:
                print(f"   Pause {i+1}: {start:.2f}s - {end:.2f}s (duration: {pause_duration:.3f}s)")
    
    return {
        'duration': duration,
        'strict_pauses': strict_pauses,
        'loose_pauses': loose_pauses,
        'rms_stats': {
            'mean': mean_rms,
            'std': std_rms,
            'strict_threshold': silence_threshold_strict,
            'loose_threshold': silence_threshold_loose
        }
    }

def find_pause_segments(rms_values, time_stamps, threshold, min_duration=0.1):
    """Find continuous segments below threshold"""
    
    silent_frames = rms_values < threshold
    pauses = []
    
    in_pause = False
    pause_start = 0
    
    for i, is_silent in enumerate(silent_frames):
        if is_silent and not in_pause:
            pause_start = time_stamps[i]
            in_pause = True
        elif not is_silent and in_pause:
            pause_end = time_stamps[i]
            pause_duration = pause_end - pause_start
            if pause_duration >= min_duration:
                pauses.append((pause_start, pause_end))
            in_pause = False
    
    # Handle case where audio ends in silence
    if in_pause and len(time_stamps) > 0:
        pause_end = time_stamps[-1]
        pause_duration = pause_end - pause_start
        if pause_duration >= min_duration:
            pauses.append((pause_start, pause_end))
    
    return pauses

def analyze_tts_behavior():
    """Analyze how gTTS behaves with different text patterns"""
    
    print(f"\n🔬 TTS BEHAVIOR ANALYSIS")
    print("=" * 50)
    
    # Test different text patterns that might cause pauses
    test_cases = [
        ("No punctuation", "Swedish officials she has been subjected to harsh treatment"),
        ("With comma", "Swedish officials, she has been subjected to harsh treatment"),
        ("With period", "Swedish officials. She has been subjected to harsh treatment"),
        ("With quotes", 'Swedish officials "she has been subjected to harsh treatment"'),
        ("With dash", "Swedish officials - she has been subjected to harsh treatment"),
        ("With parentheses", "Swedish officials (she has been subjected to harsh treatment)"),
        ("Long sentence", "The environmental campaigner Greta Thunberg has told Swedish officials she is being subjected to harsh treatment in Israeli custody after her detention"),
        ("Multiple spaces", "Swedish  officials  she  has  been  subjected  to  harsh  treatment"),
        ("Normalized", "Swedish officials she is being subjected to harsh treatment"),
    ]
    
    results = {}
    
    for name, text in test_cases:
        print(f"\n🧪 Testing: {name}")
        print(f"   Text: '{text}'")
        
        try:
            # Create TTS
            tts = gTTS(text=text, lang='en', tld='ie', slow=False)
            filename = f"test_tts_{name.lower().replace(' ', '_')}.mp3"
            tts.save(filename)
            
            # Quick analysis
            audio = AudioSegment.from_mp3(filename)
            duration = len(audio) / 1000.0
            word_count = len(text.split())
            wps = word_count / duration if duration > 0 else 0
            
            print(f"   Duration: {duration:.2f}s")
            print(f"   Words per second: {wps:.2f}")
            
            results[name] = {
                'filename': filename,
                'duration': duration,
                'wps': wps,
                'text_length': len(text)
            }
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results[name] = None
    
    return results

def create_ultra_optimized_text():
    """Create text specifically optimized to eliminate TTS pauses"""
    
    print(f"\n🚀 CREATING ULTRA-OPTIMIZED TEXT")
    print("=" * 50)
    
    url = "https://www.theguardian.com/world/2025/oct/04/greta-thunberg-israel-gaza-sweden"
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    
    # Extract using our proven method
    content_div = soup.select_one('div[data-gu-name="body"]')
    
    if not content_div:
        return None
    
    paragraphs = []
    for p in content_div.find_all('p'):
        text = p.get_text(separator=' ', strip=True)
        text = re.sub(r'\s+', ' ', text)
        if len(text) > 20:
            paragraphs.append(text)
    
    # Join with single spaces
    raw_text = ' '.join(paragraphs)
    
    print("🔧 APPLYING ULTRA-OPTIMIZATION:")
    
    # ULTRA-AGGRESSIVE optimization for natural speech
    
    # 1. Remove ALL problematic punctuation that causes pauses
    optimized = raw_text
    
    # Remove em/en dashes completely
    optimized = re.sub(r'[–—]', ' ', optimized)
    
    # Replace semicolons with periods (cleaner breaks)
    optimized = re.sub(r';', '.', optimized)
    
    # Fix parenthetical statements that cause pauses
    optimized = re.sub(r'\([^)]+\)', '', optimized)  # Remove all parentheses content
    
    # Fix quote patterns that cause pauses
    optimized = re.sub(r'"([^"]+)"', r'\1', optimized)  # Remove quote marks but keep content
    
    # Replace complex comma constructions
    optimized = re.sub(r', including ([^,]+),', r' with \1,', optimized)
    optimized = re.sub(r', according to ([^,]+),', r'. \1 reports that', optimized)
    
    # Fix multiple consecutive punctuation
    optimized = re.sub(r'[.]{2,}', '.', optimized)
    optimized = re.sub(r'[,]{2,}', ',', optimized)
    
    # Normalize all whitespace
    optimized = re.sub(r'\s+', ' ', optimized)
    
    # Fix sentence boundaries for smooth flow
    optimized = re.sub(r'\.([A-Z])', r'. \1', optimized)
    optimized = re.sub(r',([A-Z])', r', \1', optimized)
    
    # Remove trailing/leading spaces
    optimized = optimized.strip()
    
    print(f"   Original length: {len(raw_text)} chars")
    print(f"   Optimized length: {len(optimized)} chars")
    print(f"   Reduction: {len(raw_text) - len(optimized)} chars")
    
    # Truncate to reasonable length
    if len(optimized) > 3500:
        truncated = optimized[:3500]
        last_period = truncated.rfind('. ')
        if last_period > 3000:
            optimized = truncated[:last_period + 1]
    
    return optimized

def main():
    print("🎧 DEEP AUDIO DELAY ANALYSIS")
    print("=" * 60)
    
    # 1. Analyze our current best file
    current_file = "guardian_article_PERFECT.mp3"
    if os.path.exists(current_file):
        current_analysis = analyze_audio_waveform_detailed(current_file)
    else:
        print(f"❌ {current_file} not found")
        return
    
    # 2. Analyze TTS behavior patterns
    tts_results = analyze_tts_behavior()
    
    # 3. Create ultra-optimized version
    ultra_text = create_ultra_optimized_text()
    
    if ultra_text:
        print(f"\n🎵 CREATING ULTRA-OPTIMIZED AUDIO...")
        
        # Add natural intro
        intro = "Here's a Guardian news report about Greta Thunberg, reported by Lorenzo Tondo. "
        full_text = intro + ultra_text
        
        try:
            tts = gTTS(text=full_text, lang='en', tld='ie', slow=False)
            ultra_filename = "guardian_article_ULTRA_OPTIMIZED.mp3"
            tts.save(ultra_filename)
            
            print(f"✅ Created: {ultra_filename}")
            
            # Analyze the new version
            ultra_analysis = analyze_audio_waveform_detailed(ultra_filename)
            
            # Compare results
            print(f"\n📊 COMPARISON:")
            print(f"   PERFECT version pauses: {len(current_analysis['strict_pauses'])}")
            print(f"   ULTRA version pauses: {len(ultra_analysis['strict_pauses'])}")
            
            improvement = len(current_analysis['strict_pauses']) - len(ultra_analysis['strict_pauses'])
            print(f"   Improvement: {improvement} fewer pauses")
            
        except Exception as e:
            print(f"❌ Error creating ultra version: {e}")
    
    # 4. Clean up test files
    print(f"\n🧹 Cleaning up test files...")
    for filename in os.listdir('.'):
        if filename.startswith('test_tts_') and filename.endswith('.mp3'):
            os.remove(filename)

if __name__ == "__main__":
    main()
