#!/usr/bin/env python3
"""
Simple Audio Analysis - Measure actual durations and detect timing issues
"""

import os
from pydub import AudioSegment
import numpy as np

def analyze_audio_timing(filename):
    """Analyze audio file timing using pydub"""
    
    print(f"\n🔍 ANALYZING: {filename}")
    print("=" * 40)
    
    try:
        # Load audio
        audio = AudioSegment.from_mp3(filename)
        
        # Basic stats
        duration_ms = len(audio)
        duration_sec = duration_ms / 1000.0
        
        print(f"📊 BASIC STATS:")
        print(f"   Duration: {duration_sec:.2f} seconds")
        print(f"   Sample Rate: {audio.frame_rate} Hz")
        print(f"   Channels: {audio.channels}")
        print(f"   Frame Width: {audio.frame_width}")
        
        # Convert to raw audio data
        raw_data = audio.raw_data
        
        # Convert to numpy array for analysis
        if audio.sample_width == 1:
            audio_array = np.frombuffer(raw_data, dtype=np.int8)
        elif audio.sample_width == 2:
            audio_array = np.frombuffer(raw_data, dtype=np.int16)
        elif audio.sample_width == 4:
            audio_array = np.frombuffer(raw_data, dtype=np.int32)
        else:
            print(f"   Unsupported sample width: {audio.sample_width}")
            return
        
        # Calculate RMS in chunks to detect pauses
        chunk_size = audio.frame_rate // 10  # 0.1 second chunks
        num_chunks = len(audio_array) // chunk_size
        
        rms_values = []
        for i in range(num_chunks):
            start = i * chunk_size
            end = start + chunk_size
            chunk = audio_array[start:end]
            rms = np.sqrt(np.mean(chunk.astype(np.float64) ** 2))
            rms_values.append(rms)
        
        if rms_values:
            mean_rms = np.mean(rms_values)
            silence_threshold = mean_rms * 0.1  # 10% of mean
            
            print(f"   Mean RMS: {mean_rms:.2f}")
            print(f"   Silence Threshold: {silence_threshold:.2f}")
            
            # Find silent chunks (potential pauses)
            silent_chunks = []
            for i, rms in enumerate(rms_values):
                if rms < silence_threshold:
                    time_sec = i * 0.1
                    silent_chunks.append(time_sec)
            
            print(f"\n⏸️  POTENTIAL PAUSES:")
            if silent_chunks:
                # Group consecutive silent chunks
                pause_groups = []
                current_group = [silent_chunks[0]]
                
                for i in range(1, len(silent_chunks)):
                    if silent_chunks[i] - silent_chunks[i-1] <= 0.2:  # Within 0.2s
                        current_group.append(silent_chunks[i])
                    else:
                        if len(current_group) >= 3:  # At least 0.3s pause
                            pause_groups.append((current_group[0], current_group[-1]))
                        current_group = [silent_chunks[i]]
                
                # Don't forget the last group
                if len(current_group) >= 3:
                    pause_groups.append((current_group[0], current_group[-1]))
                
                if pause_groups:
                    for i, (start, end) in enumerate(pause_groups):
                        duration = end - start + 0.1
                        print(f"   Pause {i+1}: {start:.1f}s - {end+0.1:.1f}s (duration: {duration:.1f}s)")
                else:
                    print("   No significant pauses detected")
            else:
                print("   No silent periods detected")
        
        return duration_sec, len(rms_values) if rms_values else 0
        
    except Exception as e:
        print(f"❌ Error analyzing {filename}: {e}")
        return None, None

def compare_versions():
    """Compare the different audio versions"""
    
    files_to_analyze = [
        "test_v1_with_breaks.mp3",
        "test_v2_with_including.mp3", 
        "test_v3_fixed_including.mp3"
    ]
    
    results = {}
    
    for filename in files_to_analyze:
        if os.path.exists(filename):
            duration, chunks = analyze_audio_timing(filename)
            results[filename] = (duration, chunks)
    
    print(f"\n📋 COMPARISON SUMMARY")
    print("=" * 50)
    
    for filename, (duration, chunks) in results.items():
        if duration:
            version_name = filename.replace("test_", "").replace(".mp3", "")
            print(f"{version_name.upper()}:")
            print(f"  Duration: {duration:.2f}s")
            print(f"  Analysis chunks: {chunks}")
    
    return results

def listen_test_instructions():
    """Provide instructions for manual listening test"""
    
    print(f"\n👂 MANUAL LISTENING TEST INSTRUCTIONS")
    print("=" * 50)
    print("As engineers, we need to listen to the actual files:")
    print()
    print("1. Listen to test_v1_with_breaks.mp3")
    print("   - Should have obvious pauses after 'Greta Thunberg' and 'Lorenzo Tondo'")
    print()
    print("2. Listen to test_v2_with_including.mp3") 
    print("   - Listen specifically to 'subjected to harsh treatment, including insufficient'")
    print("   - Note any unnatural pauses")
    print()
    print("3. Listen to test_v3_fixed_including.mp3")
    print("   - Same section should now say 'subjected to harsh treatment with insufficient'")
    print("   - Should flow more naturally")
    print()
    print("🎯 SPECIFIC TEST:")
    print("Listen for the phrase 'she has been subjected to harsh treatment'")
    print("- Does it pause unnaturally after 'to'?")
    print("- Which version sounds most natural?")
    print()
    print("📊 REPORT FINDINGS:")
    print("Tell me which version has the pause issue and at what timestamp!")

def main():
    print("🎧 ENGINEERING AUDIO ANALYSIS")
    print("=" * 60)
    
    # Analyze the generated test files
    results = compare_versions()
    
    # Provide listening test instructions
    listen_test_instructions()
    
    # List available files for inspection
    print(f"\n📁 GENERATED TEST FILES:")
    test_files = [f for f in os.listdir('.') if f.startswith('test_') and f.endswith('.mp3')]
    for f in test_files:
        size_mb = os.path.getsize(f) / (1024*1024)
        print(f"   {f} ({size_mb:.1f}MB)")

if __name__ == "__main__":
    main()
