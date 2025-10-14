#!/usr/bin/env python3
"""
Fix Swedish Officials Delay - Test alternative phrasings
"""

from gtts import gTTS
import os
from pydub import AudioSegment

def test_swedish_officials_alternatives():
    """Test different ways to say 'Swedish officials' more naturally"""
    
    print("🎯 FIXING 'SWEDISH OFFICIALS' DELAY")
    print("=" * 40)
    
    alternatives = [
        ("original", "Swedish officials"),
        ("sweden_officials", "Sweden officials"),
        ("swedish_authorities", "Swedish authorities"), 
        ("sweden_authorities", "Sweden authorities"),
        ("swedish_government", "Swedish government"),
        ("sweden_government", "Sweden government"),
        ("officials_from_sweden", "officials from Sweden"),
        ("authorities_from_sweden", "authorities from Sweden"),
        ("swedish_embassy", "Swedish embassy"),
        ("sweden_embassy", "Sweden embassy"),
        ("swedish_diplomats", "Swedish diplomats"),
        ("sweden_diplomats", "Sweden diplomats")
    ]
    
    results = {}
    
    for name, phrase in alternatives:
        try:
            tts = gTTS(text=phrase, lang='en', tld='ie', slow=False)
            filename = f"test_{name}.mp3"
            tts.save(filename)
            
            audio = AudioSegment.from_mp3(filename)
            duration = len(audio) / 1000.0
            word_count = len(phrase.split())
            wps = word_count / duration if duration > 0 else 0
            
            results[name] = {
                'phrase': phrase,
                'duration': duration,
                'words': word_count,
                'wps': wps
            }
            
            improvement = wps - 1.07  # vs original
            print(f"{name}: '{phrase}' -> {duration:.2f}s ({wps:.2f} wps) [{improvement:+.2f}]")
            
            os.remove(filename)
            
        except Exception as e:
            print(f"{name}: Error - {e}")
    
    # Find best alternative
    if results:
        best = max(results.items(), key=lambda x: x[1]['wps'])
        print(f"\n🏆 BEST ALTERNATIVE: {best[0]}")
        print(f"   Phrase: '{best[1]['phrase']}'")
        print(f"   Speed: {best[1]['wps']:.2f} wps")
        print(f"   Improvement: {best[1]['wps'] - 1.07:+.2f} wps vs original")
    
    return results

def test_full_sentence_with_fix():
    """Test the full sentence with the best alternative"""
    
    print(f"\n🧪 TESTING FULL SENTENCE WITH FIX")
    print("=" * 40)
    
    # Original problematic sentence
    original = "The environmental campaigner Greta Thunberg has told Swedish officials she faces harsh treatment in Israeli custody"
    
    # Test different fixes
    alternatives = [
        ("original", original),
        ("sweden_officials", original.replace("Swedish officials", "Sweden officials")),
        ("swedish_authorities", original.replace("Swedish officials", "Swedish authorities")),
        ("officials_from_sweden", original.replace("Swedish officials", "officials from Sweden")),
        ("swedish_embassy", original.replace("Swedish officials", "Swedish embassy staff"))
    ]
    
    for name, sentence in alternatives:
        try:
            tts = gTTS(text=sentence, lang='en', tld='ie', slow=False)
            filename = f"full_{name}.mp3"
            tts.save(filename)
            
            audio = AudioSegment.from_mp3(filename)
            duration = len(audio) / 1000.0
            word_count = len(sentence.split())
            wps = word_count / duration if duration > 0 else 0
            
            print(f"{name}: {duration:.2f}s ({wps:.2f} wps)")
            print(f"   Text: '{sentence}'")
            
            os.remove(filename)
            
        except Exception as e:
            print(f"{name}: Error - {e}")

def main():
    # Test alternatives for "Swedish officials"
    alternatives = test_swedish_officials_alternatives()
    
    # Test full sentence with best fix
    test_full_sentence_with_fix()
    
    print(f"\n✅ SWEDISH OFFICIALS DELAY ANALYSIS COMPLETE!")

if __name__ == "__main__":
    main()
