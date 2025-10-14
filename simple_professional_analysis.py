#!/usr/bin/env python3
"""
Simplified Professional Audio Analysis - Detect delays without numpy.long issues
"""

import numpy as np
from pydub import AudioSegment
from pydub.silence import detect_silence, detect_nonsilent
import matplotlib.pyplot as plt
import os

def analyze_audio_delays_simple(audio_file):
    """Simplified professional analysis using pydub"""
    
    print(f"🔬 AUDIO DELAY ANALYSIS: {audio_file}")
    print("=" * 50)
    
    if not os.path.exists(audio_file):
        print(f"❌ File not found: {audio_file}")
        return None
    
    try:
        # Load audio
        audio = AudioSegment.from_mp3(audio_file)
        
        # Basic properties
        duration_ms = len(audio)
        duration_s = duration_ms / 1000.0
        sample_rate = audio.frame_rate
        channels = audio.channels
        
        print(f"📊 Basic Properties:")
        print(f"   Duration: {duration_s:.2f} seconds")
        print(f"   Sample Rate: {sample_rate} Hz")
        print(f"   Channels: {channels}")
        print(f"   Format: {audio.sample_width * 8}-bit")
        
        # Convert to mono for analysis
        if channels > 1:
            audio = audio.set_channels(1)
        
        # Calculate RMS levels
        samples = np.array(audio.get_array_of_samples())
        
        # RMS calculation in windows
        window_size = int(sample_rate * 0.025)  # 25ms windows
        hop_size = int(sample_rate * 0.01)      # 10ms hop
        
        rms_values = []
        times = []
        
        for i in range(0, len(samples) - window_size, hop_size):
            window = samples[i:i + window_size]
            rms = np.sqrt(np.mean(window.astype(np.float64) ** 2))
            rms_values.append(rms)
            times.append(i / sample_rate)
        
        rms_values = np.array(rms_values)
        
        # Convert to dB
        rms_db = 20 * np.log10(rms_values + 1e-10)  # Add small value to avoid log(0)
        
        # Silence detection using multiple thresholds
        print(f"\n🔇 SILENCE ANALYSIS:")
        
        # Dynamic threshold based on audio content
        rms_mean = np.mean(rms_db)
        rms_std = np.std(rms_db)
        
        # Multiple silence thresholds
        thresholds = [
            ("Conservative", rms_mean - 2 * rms_std),
            ("Moderate", rms_mean - 1.5 * rms_std), 
            ("Aggressive", rms_mean - 1 * rms_std)
        ]
        
        silence_results = {}
        
        for threshold_name, threshold_db in thresholds:
            # Convert dB threshold back to amplitude for pydub
            threshold_amp = 10 ** (threshold_db / 20)
            
            # Detect silence using pydub (expects amplitude values)
            silences = detect_silence(
                audio, 
                min_silence_len=50,  # 50ms minimum
                silence_thresh=int(threshold_amp * 1000)  # pydub uses different scale
            )
            
            # Convert to seconds
            silences_sec = [(start/1000, end/1000, (end-start)/1000) for start, end in silences]
            
            silence_results[threshold_name] = silences_sec
            
            total_silence = sum(duration for _, _, duration in silences_sec)
            silence_percent = (total_silence / duration_s) * 100
            
            print(f"   {threshold_name} ({threshold_db:.1f} dB): {len(silences_sec)} silences, {silence_percent:.1f}% total")
            
            # Show first few silences
            for i, (start, end, duration) in enumerate(silences_sec[:5]):
                print(f"      {i+1}. {start:.2f}s - {end:.2f}s ({duration:.3f}s)")
            
            if len(silences_sec) > 5:
                print(f"      ... and {len(silences_sec) - 5} more")
        
        # Voice activity analysis
        print(f"\n🎤 VOICE ACTIVITY ANALYSIS:")
        
        # Detect non-silent segments (voice activity)
        voice_segments = detect_nonsilent(
            audio,
            min_silence_len=50,
            silence_thresh=int(np.mean(rms_values) * 500)  # Adjusted threshold
        )
        
        voice_segments_sec = [(start/1000, end/1000, (end-start)/1000) for start, end in voice_segments]
        
        print(f"   Voice segments: {len(voice_segments_sec)}")
        
        if len(voice_segments_sec) > 1:
            # Calculate gaps between voice segments
            gaps = []
            for i in range(len(voice_segments_sec) - 1):
                gap_start = voice_segments_sec[i][1]  # End of current segment
                gap_end = voice_segments_sec[i+1][0]  # Start of next segment
                gap_duration = gap_end - gap_start
                
                if gap_duration > 0.01:  # Only gaps > 10ms
                    gaps.append((gap_start, gap_end, gap_duration))
            
            print(f"   Inter-speech gaps: {len(gaps)}")
            
            if gaps:
                gap_durations = [duration for _, _, duration in gaps]
                print(f"   Mean gap: {np.mean(gap_durations):.3f}s")
                print(f"   Max gap: {np.max(gap_durations):.3f}s")
                print(f"   Std gap: {np.std(gap_durations):.3f}s")
                
                # Show longest gaps
                sorted_gaps = sorted(gaps, key=lambda x: x[2], reverse=True)
                print(f"   Longest gaps:")
                for i, (start, end, duration) in enumerate(sorted_gaps[:5]):
                    print(f"      {i+1}. {start:.2f}s - {end:.2f}s ({duration:.3f}s)")
        
        # Energy analysis
        print(f"\n⚡ ENERGY ANALYSIS:")
        
        energy_stats = {
            'mean_rms_db': np.mean(rms_db),
            'std_rms_db': np.std(rms_db),
            'min_rms_db': np.min(rms_db),
            'max_rms_db': np.max(rms_db),
            'dynamic_range_db': np.max(rms_db) - np.min(rms_db)
        }
        
        for stat_name, value in energy_stats.items():
            print(f"   {stat_name}: {value:.2f}")
        
        # Create visualization
        print(f"\n📈 Creating visualization...")
        
        plt.figure(figsize=(15, 8))
        
        # Subplot 1: Waveform
        plt.subplot(3, 1, 1)
        time_axis = np.linspace(0, duration_s, len(samples))
        plt.plot(time_axis, samples, alpha=0.7, linewidth=0.5)
        plt.title(f'Waveform: {os.path.basename(audio_file)}')
        plt.ylabel('Amplitude')
        plt.grid(True, alpha=0.3)
        
        # Subplot 2: RMS Energy
        plt.subplot(3, 1, 2)
        plt.plot(times, rms_db, 'b-', linewidth=1)
        
        # Plot silence thresholds
        colors = ['red', 'orange', 'yellow']
        for i, (threshold_name, threshold_db) in enumerate(thresholds):
            plt.axhline(y=threshold_db, color=colors[i], linestyle='--', 
                       label=f'{threshold_name} ({threshold_db:.1f} dB)', alpha=0.7)
        
        plt.title('RMS Energy (dB)')
        plt.ylabel('dB')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Subplot 3: Voice Activity
        plt.subplot(3, 1, 3)
        
        # Plot voice segments
        for start, end, duration in voice_segments_sec:
            plt.axvspan(start, end, alpha=0.3, color='green', label='Voice' if start == voice_segments_sec[0][0] else "")
        
        # Plot silence gaps
        if 'gaps' in locals() and gaps:
            for start, end, duration in gaps[:10]:  # Show first 10 gaps
                plt.axvspan(start, end, alpha=0.5, color='red', label='Gap' if start == gaps[0][0] else "")
        
        plt.title('Voice Activity Detection')
        plt.xlabel('Time (s)')
        plt.ylabel('Activity')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        plot_filename = audio_file.replace('.mp3', '_delay_analysis.png').replace('.wav', '_delay_analysis.png')
        plt.savefig(plot_filename, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"   Saved: {plot_filename}")
        
        # Return analysis results
        analysis_result = {
            'file': audio_file,
            'duration': duration_s,
            'silence_results': silence_results,
            'voice_segments': voice_segments_sec,
            'gaps': gaps if 'gaps' in locals() else [],
            'energy_stats': energy_stats,
            'plot_file': plot_filename
        }
        
        return analysis_result
        
    except Exception as e:
        print(f"❌ Error analyzing {audio_file}: {e}")
        import traceback
        traceback.print_exc()
        return None

def compare_delay_analysis(files):
    """Compare delay analysis across multiple files"""
    
    print(f"\n📊 COMPARATIVE DELAY ANALYSIS")
    print("=" * 50)
    
    results = {}
    
    for file in files:
        if os.path.exists(file):
            print(f"\n" + "="*60)
            result = analyze_audio_delays_simple(file)
            if result:
                results[file] = result
        else:
            print(f"⚠️  File not found: {file}")
    
    if len(results) < 2:
        print(f"\n❌ Need at least 2 files for comparison")
        return results
    
    # Comparison summary
    print(f"\n" + "="*80)
    print(f"📈 DELAY COMPARISON SUMMARY")
    print("="*80)
    
    print(f"{'FILE':<30} {'DURATION':<10} {'GAPS':<8} {'MAX_GAP':<10} {'SILENCE%':<12}")
    print("-" * 80)
    
    best_file = None
    min_gaps = float('inf')
    
    for file, data in results.items():
        filename = os.path.basename(file)
        duration = data['duration']
        gaps = data['gaps']
        num_gaps = len(gaps)
        
        max_gap = max([gap[2] for gap in gaps]) if gaps else 0
        
        # Use moderate silence threshold for comparison
        moderate_silences = data['silence_results'].get('Moderate', [])
        total_silence = sum(duration for _, _, duration in moderate_silences)
        silence_percent = (total_silence / duration) * 100
        
        print(f"{filename:<30} {duration:<10.2f} {num_gaps:<8} {max_gap:<10.3f} {silence_percent:<12.1f}%")
        
        # Track best file (fewest gaps)
        if num_gaps < min_gaps:
            min_gaps = num_gaps
            best_file = filename
    
    print(f"\n🏆 BEST AUDIO (fewest delays): {best_file}")
    
    return results

def main():
    # Test files to analyze
    test_files = [
        "first_paragraph_only.mp3",
        "ultra_clean_gtts_irish.mp3", 
        "ultra_clean_gtts_canadian.mp3",
        "ultra_clean_espeak_female.mp3"
    ]
    
    print("🔬 PROFESSIONAL AUDIO DELAY DETECTION")
    print("=" * 50)
    print("Using pydub silence detection and energy analysis")
    
    # Filter existing files
    existing_files = [f for f in test_files if os.path.exists(f)]
    
    if not existing_files:
        print("❌ No audio files found. Create some test files first.")
        return
    
    print(f"\n📁 Analyzing {len(existing_files)} audio files...")
    
    # Analyze and compare
    results = compare_delay_analysis(existing_files)
    
    print(f"\n✅ PROFESSIONAL DELAY ANALYSIS COMPLETE!")
    print(f"📊 Check the *_delay_analysis.png files for visual analysis")
    print(f"🎯 The file with fewest gaps should sound most natural")

if __name__ == "__main__":
    main()
