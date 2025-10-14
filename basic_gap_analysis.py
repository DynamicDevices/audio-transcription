#!/usr/bin/env python3
"""
Basic Audio Delay Detection - Simple but effective approach
"""

from pydub import AudioSegment
from pydub.silence import detect_silence
import numpy as np
import matplotlib.pyplot as plt
import os

def analyze_audio_gaps_basic(audio_file):
    """Basic gap analysis using fixed thresholds"""
    
    print(f"🔍 BASIC DELAY ANALYSIS: {audio_file}")
    print("=" * 45)
    
    if not os.path.exists(audio_file):
        print(f"❌ File not found: {audio_file}")
        return None
    
    try:
        # Load audio
        audio = AudioSegment.from_mp3(audio_file)
        
        # Basic properties
        duration_ms = len(audio)
        duration_s = duration_ms / 1000.0
        
        print(f"📊 Properties: {duration_s:.2f}s, {audio.frame_rate}Hz")
        
        # Convert to mono
        if audio.channels > 1:
            audio = audio.set_channels(1)
        
        # Test multiple silence thresholds (in dBFS)
        thresholds = [-50, -40, -35, -30, -25]
        
        print(f"\n🔇 Gap Detection:")
        
        best_result = None
        
        for threshold_db in thresholds:
            try:
                # Detect silences
                silences = detect_silence(
                    audio,
                    min_silence_len=50,    # 50ms minimum
                    silence_thresh=threshold_db
                )
                
                # Convert to seconds
                gaps = [(start/1000, end/1000, (end-start)/1000) for start, end in silences]
                
                # Filter out very short gaps
                significant_gaps = [gap for gap in gaps if gap[2] > 0.1]  # >100ms
                
                total_gap_time = sum(gap[2] for gap in significant_gaps)
                gap_percentage = (total_gap_time / duration_s) * 100
                
                print(f"   {threshold_db:3d}dB: {len(significant_gaps):2d} gaps ({gap_percentage:.1f}% silence)")
                
                # Track best result (reasonable number of gaps)
                if 2 <= len(significant_gaps) <= 20 and best_result is None:
                    best_result = {
                        'threshold': threshold_db,
                        'gaps': significant_gaps,
                        'total_gap_time': total_gap_time,
                        'gap_percentage': gap_percentage
                    }
                
            except Exception as e:
                print(f"   {threshold_db:3d}dB: Error - {str(e)[:30]}...")
        
        if best_result:
            gaps = best_result['gaps']
            print(f"\n🎯 Best threshold: {best_result['threshold']}dB")
            print(f"   Detected {len(gaps)} significant gaps:")
            
            # Show gaps in time order
            for i, (start, end, duration) in enumerate(gaps[:10]):  # Show first 10
                print(f"      {i+1:2d}. {start:5.2f}s - {end:5.2f}s ({duration:.3f}s)")
            
            if len(gaps) > 10:
                print(f"      ... and {len(gaps) - 10} more gaps")
            
            # Find longest gaps (potential problems)
            sorted_gaps = sorted(gaps, key=lambda x: x[2], reverse=True)
            print(f"\n⚠️  Longest gaps (potential delays):")
            for i, (start, end, duration) in enumerate(sorted_gaps[:5]):
                print(f"      {i+1}. {start:5.2f}s - {end:5.2f}s ({duration:.3f}s)")
        
        else:
            print(f"\n⚠️  Could not find suitable gap detection threshold")
            best_result = {'gaps': [], 'threshold': -40, 'gap_percentage': 0}
        
        # Create simple visualization
        print(f"\n📊 Creating waveform visualization...")
        
        # Get audio samples
        samples = np.array(audio.get_array_of_samples())
        time_axis = np.linspace(0, duration_s, len(samples))
        
        # Create plot
        plt.figure(figsize=(15, 6))
        
        # Plot waveform
        plt.subplot(2, 1, 1)
        plt.plot(time_axis, samples, alpha=0.7, linewidth=0.5)
        plt.title(f'Waveform: {os.path.basename(audio_file)}')
        plt.ylabel('Amplitude')
        plt.grid(True, alpha=0.3)
        
        # Highlight gaps if found
        if best_result and best_result['gaps']:
            for start, end, duration in best_result['gaps']:
                plt.axvspan(start, end, alpha=0.3, color='red', 
                           label='Gap' if start == best_result['gaps'][0][0] else "")
            plt.legend()
        
        # Plot RMS energy
        plt.subplot(2, 1, 2)
        
        # Calculate RMS in chunks
        chunk_size = int(audio.frame_rate * 0.05)  # 50ms chunks
        rms_values = []
        rms_times = []
        
        for i in range(0, len(samples), chunk_size):
            chunk = samples[i:i + chunk_size]
            if len(chunk) > 0:
                rms = np.sqrt(np.mean(chunk.astype(np.float64) ** 2))
                rms_values.append(rms)
                rms_times.append(i / audio.frame_rate)
        
        plt.plot(rms_times, rms_values, 'b-', linewidth=1)
        plt.title('RMS Energy')
        plt.xlabel('Time (s)')
        plt.ylabel('RMS')
        plt.grid(True, alpha=0.3)
        
        # Highlight gaps on RMS plot too
        if best_result and best_result['gaps']:
            for start, end, duration in best_result['gaps']:
                plt.axvspan(start, end, alpha=0.3, color='red')
        
        plt.tight_layout()
        
        plot_filename = audio_file.replace('.mp3', '_gaps.png').replace('.wav', '_gaps.png')
        plt.savefig(plot_filename, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"   Saved: {plot_filename}")
        
        return {
            'file': audio_file,
            'duration': duration_s,
            'analysis': best_result,
            'plot': plot_filename
        }
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

def compare_audio_gaps(files):
    """Compare gap analysis across files"""
    
    print(f"\n📊 AUDIO GAP COMPARISON")
    print("=" * 40)
    
    results = {}
    
    for file in files:
        if os.path.exists(file):
            print(f"\n" + "-"*50)
            result = analyze_audio_gaps_basic(file)
            if result:
                results[file] = result
    
    if len(results) < 2:
        print(f"\n⚠️  Need multiple files for comparison")
        return results
    
    # Summary table
    print(f"\n" + "="*70)
    print(f"📈 GAP COMPARISON SUMMARY")
    print("="*70)
    print(f"{'FILE':<25} {'DURATION':<10} {'GAPS':<6} {'SILENCE%':<10} {'MAX_GAP':<10}")
    print("-" * 70)
    
    best_file = None
    min_gaps = float('inf')
    
    for file, data in results.items():
        filename = os.path.basename(file)
        duration = data['duration']
        
        if data['analysis'] and data['analysis']['gaps']:
            gaps = data['analysis']['gaps']
            num_gaps = len(gaps)
            silence_percent = data['analysis']['gap_percentage']
            max_gap = max(gap[2] for gap in gaps)
        else:
            num_gaps = 0
            silence_percent = 0
            max_gap = 0
        
        print(f"{filename:<25} {duration:<10.2f} {num_gaps:<6} {silence_percent:<10.1f}% {max_gap:<10.3f}s")
        
        if num_gaps < min_gaps:
            min_gaps = num_gaps
            best_file = filename
    
    print(f"\n🏆 BEST (fewest gaps): {best_file}")
    
    return results

def main():
    # Files to analyze
    test_files = [
        "first_paragraph_only.mp3",
        "ultra_clean_gtts_irish.mp3",
        "ultra_clean_gtts_canadian.mp3", 
        "ultra_clean_espeak_female.mp3"
    ]
    
    print("🔍 BASIC AUDIO GAP DETECTION")
    print("=" * 40)
    
    existing_files = [f for f in test_files if os.path.exists(f)]
    
    if not existing_files:
        print("❌ No audio files found")
        return
    
    print(f"Analyzing {len(existing_files)} files...")
    
    results = compare_audio_gaps(existing_files)
    
    print(f"\n✅ ANALYSIS COMPLETE!")
    print(f"📊 Check the *_gaps.png files for visual gap analysis")
    print(f"🎯 Files with fewer gaps should sound more natural")

if __name__ == "__main__":
    main()
