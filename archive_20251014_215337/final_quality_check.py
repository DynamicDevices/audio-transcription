#!/usr/bin/env python3
"""
Final Quality Check - Compare Professional vs Previous Versions
"""

import os
from pydub import AudioSegment
import numpy as np

def quick_audio_analysis(filename):
    """Quick analysis of audio quality"""
    
    if not os.path.exists(filename):
        return None
    
    try:
        audio = AudioSegment.from_mp3(filename)
        
        # Basic stats
        duration = len(audio) / 1000.0
        size_mb = os.path.getsize(filename) / (1024*1024)
        
        # Convert to numpy for pause analysis
        samples = np.array(audio.get_array_of_samples())
        if audio.channels == 2:
            samples = samples.reshape((-1, 2)).mean(axis=1)
        
        # Quick RMS analysis
        window_size = int(audio.frame_rate * 0.1)  # 100ms windows
        num_windows = len(samples) // window_size
        
        rms_values = []
        for i in range(num_windows):
            start = i * window_size
            end = start + window_size
            window = samples[start:end]
            rms = np.sqrt(np.mean(window.astype(np.float64) ** 2))
            rms_values.append(rms)
        
        if rms_values:
            mean_rms = np.mean(rms_values)
            silence_threshold = mean_rms * 0.1
            silent_windows = sum(1 for rms in rms_values if rms < silence_threshold)
            silence_percentage = (silent_windows / len(rms_values)) * 100
        else:
            silence_percentage = 0
        
        return {
            'duration': duration,
            'size_mb': size_mb,
            'silence_percentage': silence_percentage,
            'estimated_pauses': silent_windows if rms_values else 0
        }
        
    except Exception as e:
        print(f"Error analyzing {filename}: {e}")
        return None

def main():
    print("🎧 FINAL QUALITY COMPARISON")
    print("=" * 50)
    
    # Files to compare (in order of creation)
    files_to_compare = [
        ("ORIGINAL", "guardian_article_for_father.mp3"),
        ("IMPROVED", "guardian_article_improved.mp3"),
        ("NATURAL FLOW", "guardian_article_natural_flow.mp3"),
        ("PERFECT", "guardian_article_PERFECT.mp3"),
        ("ULTRA OPTIMIZED", "guardian_article_ULTRA_OPTIMIZED.mp3"),
        ("PROFESSIONAL", "guardian_article_PROFESSIONAL.mp3")
    ]
    
    results = {}
    
    print(f"{'VERSION':<15} {'DURATION':<10} {'SIZE':<8} {'SILENCE%':<10} {'EST.PAUSES':<12}")
    print("-" * 70)
    
    for name, filename in files_to_compare:
        analysis = quick_audio_analysis(filename)
        
        if analysis:
            results[name] = analysis
            print(f"{name:<15} {analysis['duration']:<10.1f}s {analysis['size_mb']:<8.1f}MB {analysis['silence_percentage']:<10.1f}% {analysis['estimated_pauses']:<12}")
        else:
            print(f"{name:<15} {'FILE NOT FOUND':<45}")
    
    # Find the best version
    if results:
        print(f"\n🏆 QUALITY RANKING (by silence percentage - lower is better):")
        
        sorted_results = sorted(results.items(), key=lambda x: x[1]['silence_percentage'])
        
        for i, (name, data) in enumerate(sorted_results, 1):
            indicator = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            print(f"   {indicator} {name}: {data['silence_percentage']:.1f}% silence, {data['duration']:.1f}s duration")
        
        best_version = sorted_results[0]
        print(f"\n🎯 RECOMMENDED FILE FOR YOUR FATHER:")
        print(f"   📱 {best_version[0].lower().replace(' ', '_')}.mp3")
        print(f"   ⏱️  Duration: {best_version[1]['duration']:.1f} minutes")
        print(f"   📊 File size: {best_version[1]['size_mb']:.1f}MB (WhatsApp compatible)")
        print(f"   🔇 Silence: {best_version[1]['silence_percentage']:.1f}% (minimal pauses)")
        
        # Map to actual filename
        for name, filename in files_to_compare:
            if name == best_version[0]:
                print(f"   📁 Filename: {filename}")
                break
    
    print(f"\n✅ Analysis complete!")
    print(f"🎧 Listen to the recommended file to verify quality")

if __name__ == "__main__":
    main()
