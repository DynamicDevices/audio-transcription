#!/usr/bin/env python3
"""
Professional Audio Delay Analysis - Use librosa and advanced tools to detect delays
"""

import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
from scipy import signal
from pydub import AudioSegment
import os
import webrtcvad
import wave
import contextlib

def analyze_audio_delays_professional(audio_file):
    """Professional analysis of audio delays using librosa"""
    
    print(f"🔬 PROFESSIONAL AUDIO ANALYSIS: {audio_file}")
    print("=" * 50)
    
    if not os.path.exists(audio_file):
        print(f"❌ File not found: {audio_file}")
        return None
    
    try:
        # Load audio with librosa
        y, sr = librosa.load(audio_file, sr=None)
        duration = len(y) / sr
        
        print(f"📊 Basic Properties:")
        print(f"   Duration: {duration:.2f} seconds")
        print(f"   Sample Rate: {sr} Hz")
        print(f"   Samples: {len(y)}")
        
        # 1. RMS Energy Analysis (detect silence/speech)
        print(f"\n🔊 RMS Energy Analysis:")
        
        # Calculate RMS energy in frames
        frame_length = int(0.025 * sr)  # 25ms frames
        hop_length = int(0.01 * sr)     # 10ms hop
        
        rms = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)[0]
        times = librosa.frames_to_time(np.arange(len(rms)), sr=sr, hop_length=hop_length)
        
        # Find silence thresholds
        rms_db = librosa.amplitude_to_db(rms, ref=np.max)
        silence_threshold = np.percentile(rms_db, 20)  # Bottom 20% as silence
        
        print(f"   RMS silence threshold: {silence_threshold:.2f} dB")
        
        # Detect silent regions
        silent_frames = rms_db < silence_threshold
        silent_regions = []
        
        in_silence = False
        silence_start = 0
        
        for i, is_silent in enumerate(silent_frames):
            if is_silent and not in_silence:
                silence_start = times[i]
                in_silence = True
            elif not is_silent and in_silence:
                silence_end = times[i]
                silence_duration = silence_end - silence_start
                if silence_duration > 0.1:  # Only count silences > 100ms
                    silent_regions.append((silence_start, silence_end, silence_duration))
                in_silence = False
        
        print(f"   Silent regions (>100ms): {len(silent_regions)}")
        for i, (start, end, duration) in enumerate(silent_regions[:10]):  # Show first 10
            print(f"      {i+1:2d}. {start:.2f}s - {end:.2f}s ({duration:.3f}s)")
        
        # 2. Spectral Analysis (detect unnatural pauses)
        print(f"\n🌊 Spectral Analysis:")
        
        # Calculate spectral centroid (brightness)
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        
        # Calculate zero crossing rate (voice activity)
        zcr = librosa.feature.zero_crossing_rate(y)[0]
        
        # Calculate spectral rolloff
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
        
        print(f"   Mean spectral centroid: {np.mean(spectral_centroids):.2f} Hz")
        print(f"   Mean zero crossing rate: {np.mean(zcr):.4f}")
        print(f"   Mean spectral rolloff: {np.mean(spectral_rolloff):.2f} Hz")
        
        # 3. Voice Activity Detection using WebRTC VAD
        print(f"\n🎤 Voice Activity Detection:")
        
        # Convert to 16kHz for WebRTC VAD
        y_16k = librosa.resample(y, orig_sr=sr, target_sr=16000)
        
        # Convert to 16-bit PCM
        y_16bit = (y_16k * 32767).astype(np.int16)
        
        # WebRTC VAD
        vad = webrtcvad.Vad(2)  # Aggressiveness level 2 (0-3)
        
        frame_duration = 30  # 30ms frames for VAD
        frame_size = int(16000 * frame_duration / 1000)
        
        vad_results = []
        for i in range(0, len(y_16bit) - frame_size, frame_size):
            frame = y_16bit[i:i + frame_size].tobytes()
            is_speech = vad.is_speech(frame, 16000)
            time_stamp = i / 16000
            vad_results.append((time_stamp, is_speech))
        
        # Find speech gaps
        speech_gaps = []
        in_gap = False
        gap_start = 0
        
        for time_stamp, is_speech in vad_results:
            if not is_speech and not in_gap:
                gap_start = time_stamp
                in_gap = True
            elif is_speech and in_gap:
                gap_end = time_stamp
                gap_duration = gap_end - gap_start
                if gap_duration > 0.05:  # Only count gaps > 50ms
                    speech_gaps.append((gap_start, gap_end, gap_duration))
                in_gap = False
        
        print(f"   Speech gaps (>50ms): {len(speech_gaps)}")
        for i, (start, end, duration) in enumerate(speech_gaps[:10]):
            print(f"      {i+1:2d}. {start:.2f}s - {end:.2f}s ({duration:.3f}s)")
        
        # 4. Tempo and Rhythm Analysis
        print(f"\n🎵 Tempo Analysis:")
        
        # Onset detection
        onset_frames = librosa.onset.onset_detect(y=y, sr=sr, units='time')
        
        if len(onset_frames) > 1:
            # Calculate inter-onset intervals
            intervals = np.diff(onset_frames)
            
            print(f"   Onsets detected: {len(onset_frames)}")
            print(f"   Mean interval: {np.mean(intervals):.3f}s")
            print(f"   Std interval: {np.std(intervals):.3f}s")
            print(f"   Max interval: {np.max(intervals):.3f}s")
            
            # Find unusually long intervals (potential delays)
            long_intervals = intervals[intervals > np.mean(intervals) + 2 * np.std(intervals)]
            print(f"   Unusually long intervals: {len(long_intervals)}")
            
            if len(long_intervals) > 0:
                print(f"   Long interval durations: {long_intervals}")
        
        # 5. Create Visualization
        print(f"\n📈 Creating visualization...")
        
        plt.figure(figsize=(15, 10))
        
        # Subplot 1: Waveform
        plt.subplot(4, 1, 1)
        librosa.display.waveshow(y, sr=sr, alpha=0.8)
        plt.title(f'Waveform: {audio_file}')
        plt.ylabel('Amplitude')
        
        # Subplot 2: RMS Energy
        plt.subplot(4, 1, 2)
        plt.plot(times, rms_db)
        plt.axhline(y=silence_threshold, color='r', linestyle='--', label='Silence Threshold')
        plt.title('RMS Energy (dB)')
        plt.ylabel('dB')
        plt.legend()
        
        # Subplot 3: Spectral Centroid
        plt.subplot(4, 1, 3)
        plt.plot(times, spectral_centroids)
        plt.title('Spectral Centroid')
        plt.ylabel('Hz')
        
        # Subplot 4: Voice Activity
        plt.subplot(4, 1, 4)
        vad_times = [t for t, _ in vad_results]
        vad_speech = [1 if is_speech else 0 for _, is_speech in vad_results]
        plt.plot(vad_times, vad_speech, 'g-', linewidth=2)
        plt.title('Voice Activity Detection')
        plt.ylabel('Speech/Silence')
        plt.xlabel('Time (s)')
        
        plt.tight_layout()
        
        plot_filename = audio_file.replace('.mp3', '_analysis.png').replace('.wav', '_analysis.png')
        plt.savefig(plot_filename, dpi=150, bbox_inches='tight')
        plt.close()
        
        print(f"   Saved visualization: {plot_filename}")
        
        # 6. Summary Report
        analysis_result = {
            'file': audio_file,
            'duration': duration,
            'sample_rate': sr,
            'silent_regions': silent_regions,
            'speech_gaps': speech_gaps,
            'rms_silence_threshold': silence_threshold,
            'spectral_stats': {
                'centroid_mean': np.mean(spectral_centroids),
                'zcr_mean': np.mean(zcr),
                'rolloff_mean': np.mean(spectral_rolloff)
            },
            'visualization': plot_filename
        }
        
        return analysis_result
        
    except Exception as e:
        print(f"❌ Error analyzing {audio_file}: {e}")
        return None

def compare_audio_files(files):
    """Compare multiple audio files for delay analysis"""
    
    print(f"\n📊 COMPARATIVE DELAY ANALYSIS")
    print("=" * 40)
    
    results = {}
    
    for file in files:
        if os.path.exists(file):
            result = analyze_audio_delays_professional(file)
            if result:
                results[file] = result
        else:
            print(f"⚠️  File not found: {file}")
    
    if len(results) < 2:
        print(f"❌ Need at least 2 files for comparison")
        return
    
    # Compare results
    print(f"\n📈 COMPARISON SUMMARY:")
    print(f"{'FILE':<40} {'DURATION':<10} {'SILENCES':<10} {'GAPS':<8} {'SILENCE%':<10}")
    print("-" * 80)
    
    for file, data in results.items():
        filename = os.path.basename(file)
        duration = data['duration']
        num_silences = len(data['silent_regions'])
        num_gaps = len(data['speech_gaps'])
        
        # Calculate silence percentage
        total_silence = sum(gap[2] for gap in data['silent_regions'])
        silence_percent = (total_silence / duration) * 100
        
        print(f"{filename:<40} {duration:<10.2f} {num_silences:<10} {num_gaps:<8} {silence_percent:<10.1f}%")
    
    # Find the file with least delays
    best_file = min(results.items(), key=lambda x: len(x[1]['speech_gaps']))
    worst_file = max(results.items(), key=lambda x: len(x[1]['speech_gaps']))
    
    print(f"\n🏆 BEST (fewest gaps): {os.path.basename(best_file[0])} ({len(best_file[1]['speech_gaps'])} gaps)")
    print(f"❌ WORST (most gaps): {os.path.basename(worst_file[0])} ({len(worst_file[1]['speech_gaps'])} gaps)")

def main():
    # Analyze existing audio files
    test_files = [
        "first_paragraph_only.mp3",
        "ultra_clean_gtts_irish.mp3", 
        "ultra_clean_gtts_canadian.mp3",
        "ultra_clean_espeak_female.mp3"
    ]
    
    print("🔬 PROFESSIONAL AUDIO DELAY ANALYSIS")
    print("=" * 50)
    print("Using librosa, WebRTC VAD, and spectral analysis")
    
    # Filter existing files
    existing_files = [f for f in test_files if os.path.exists(f)]
    
    if not existing_files:
        print("❌ No audio files found. Create some test files first.")
        return
    
    print(f"\n📁 Found {len(existing_files)} files to analyze:")
    for f in existing_files:
        print(f"   • {f}")
    
    # Analyze each file
    compare_audio_files(existing_files)
    
    print(f"\n✅ PROFESSIONAL ANALYSIS COMPLETE!")
    print(f"🔍 Check the generated *_analysis.png files for visual delay analysis")

if __name__ == "__main__":
    main()
