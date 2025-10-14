#!/usr/bin/env python3
"""
Targeted TTS Testing - Test the exact phrase that's causing the pause
"""

from gtts import gTTS
import os
from pydub import AudioSegment
import time

def test_specific_phrase_variations():
    """Test different variations of the 'subjected to' phrase to isolate the pause cause"""
    
    print("🎯 TESTING SPECIFIC PHRASE VARIATIONS")
    print("=" * 50)
    
    # Test variations of the problematic phrase
    test_phrases = [
        ("original", "Swedish officials she is being subjected to harsh treatment"),
        ("no_being", "Swedish officials she is subjected to harsh treatment"),
        ("different_verb", "Swedish officials she is experiencing harsh treatment"),
        ("simpler", "Swedish officials she faces harsh treatment"),
        ("reordered", "She is being subjected to harsh treatment by Swedish officials"),
        ("past_tense", "Swedish officials said she was subjected to harsh treatment"),
        ("active_voice", "Swedish officials subject her to harsh treatment"),
        ("split_sentence", "Swedish officials spoke. She is being subjected to harsh treatment."),
        ("no_passive", "Swedish officials are giving her harsh treatment"),
        ("minimal", "she is being subjected to harsh treatment"),
    ]
    
    results = {}
    
    for name, phrase in test_phrases:
        print(f"\n🧪 Testing: {name}")
        print(f"   Phrase: '{phrase}'")
        
        try:
            # Create TTS
            tts = gTTS(text=phrase, lang='en', tld='ie', slow=False)
            filename = f"test_phrase_{name}.mp3"
            tts.save(filename)
            
            # Analyze timing
            audio = AudioSegment.from_mp3(filename)
            duration = len(audio) / 1000.0
            word_count = len(phrase.split())
            wps = word_count / duration if duration > 0 else 0
            
            results[name] = {
                'phrase': phrase,
                'duration': duration,
                'words': word_count,
                'wps': wps,
                'filename': filename
            }
            
            print(f"   Duration: {duration:.2f}s")
            print(f"   Words/sec: {wps:.2f}")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    # Analysis
    print(f"\n📊 PHRASE TIMING ANALYSIS:")
    print(f"{'VARIATION':<15} {'DURATION':<10} {'WORDS/SEC':<10} {'WORDS':<8}")
    print("-" * 50)
    
    baseline = results.get('original')
    
    for name, data in results.items():
        if data:
            diff = f"(+{data['duration'] - baseline['duration']:.2f}s)" if baseline and name != 'original' else ""
            print(f"{name:<15} {data['duration']:<10.2f} {data['wps']:<10.2f} {data['words']:<8} {diff}")
    
    # Find the fastest version
    if results:
        fastest = min(results.items(), key=lambda x: x[1]['duration'] if x[1] else float('inf'))
        print(f"\n🏆 FASTEST VERSION: {fastest[0]}")
        print(f"   Phrase: '{fastest[1]['phrase']}'")
        print(f"   Duration: {fastest[1]['duration']:.2f}s")
    
    return results

def test_word_by_word_timing():
    """Test individual words to find which specific word causes delay"""
    
    print(f"\n🔍 WORD-BY-WORD TIMING TEST")
    print("=" * 40)
    
    # Break down the problematic phrase
    words = ["Swedish", "officials", "she", "is", "being", "subjected", "to", "harsh", "treatment"]
    
    cumulative_phrases = []
    for i in range(1, len(words) + 1):
        phrase = " ".join(words[:i])
        cumulative_phrases.append((f"words_1_to_{i}", phrase))
    
    print("Testing cumulative word addition:")
    
    results = {}
    
    for name, phrase in cumulative_phrases:
        try:
            tts = gTTS(text=phrase, lang='en', tld='ie', slow=False)
            filename = f"test_{name}.mp3"
            tts.save(filename)
            
            audio = AudioSegment.from_mp3(filename)
            duration = len(audio) / 1000.0
            word_count = len(phrase.split())
            
            results[name] = {
                'phrase': phrase,
                'duration': duration,
                'words': word_count,
                'per_word': duration / word_count if word_count > 0 else 0
            }
            
            print(f"{name}: '{phrase}' -> {duration:.2f}s ({duration/word_count:.2f}s per word)")
            
            # Clean up
            os.remove(filename)
            
        except Exception as e:
            print(f"{name}: Error - {e}")
    
    return results

def create_optimized_phrase():
    """Create the most optimized version of the problematic phrase"""
    
    print(f"\n🚀 CREATING OPTIMIZED PHRASE")
    print("=" * 35)
    
    # Based on our analysis, create the best version
    original = "Swedish officials she is being subjected to harsh treatment"
    
    # Try different optimizations
    optimizations = [
        ("remove_being", "Swedish officials she is subjected to harsh treatment"),
        ("active_voice", "Swedish officials subject her to harsh treatment"),  
        ("simpler_verb", "Swedish officials give her harsh treatment"),
        ("past_tense", "Swedish officials subjected her to harsh treatment"),
        ("different_structure", "She faces harsh treatment from Swedish officials"),
    ]
    
    print("Testing optimized versions:")
    
    best_duration = float('inf')
    best_phrase = original
    best_name = "original"
    
    # Test original
    try:
        tts = gTTS(text=original, lang='en', tld='ie', slow=False)
        tts.save("test_original_phrase.mp3")
        audio = AudioSegment.from_mp3("test_original_phrase.mp3")
        original_duration = len(audio) / 1000.0
        print(f"Original: {original_duration:.2f}s - '{original}'")
        os.remove("test_original_phrase.mp3")
    except Exception as e:
        print(f"Original failed: {e}")
        original_duration = float('inf')
    
    # Test optimizations
    for name, phrase in optimizations:
        try:
            tts = gTTS(text=phrase, lang='en', tld='ie', slow=False)
            filename = f"test_opt_{name}.mp3"
            tts.save(filename)
            
            audio = AudioSegment.from_mp3(filename)
            duration = len(audio) / 1000.0
            
            improvement = original_duration - duration
            print(f"{name}: {duration:.2f}s ({improvement:+.2f}s) - '{phrase}'")
            
            if duration < best_duration:
                best_duration = duration
                best_phrase = phrase
                best_name = name
            
            os.remove(filename)
            
        except Exception as e:
            print(f"{name}: Error - {e}")
    
    print(f"\n🏆 BEST OPTIMIZATION: {best_name}")
    print(f"   Phrase: '{best_phrase}'")
    print(f"   Duration: {best_duration:.2f}s")
    print(f"   Improvement: {original_duration - best_duration:+.2f}s")
    
    return best_phrase

def main():
    # Test phrase variations
    phrase_results = test_specific_phrase_variations()
    
    # Test word-by-word
    word_results = test_word_by_word_timing()
    
    # Create optimized version
    best_phrase = create_optimized_phrase()
    
    # Clean up test files
    print(f"\n🧹 Cleaning up test files...")
    for filename in os.listdir('.'):
        if filename.startswith('test_phrase_') and filename.endswith('.mp3'):
            os.remove(filename)
    
    print(f"\n✅ ANALYSIS COMPLETE!")
    print(f"🎯 The issue appears to be in the phrase structure itself")
    print(f"💡 Best alternative: '{best_phrase}'")

if __name__ == "__main__":
    main()
