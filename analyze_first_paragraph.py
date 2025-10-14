#!/usr/bin/env python3
"""
First Paragraph Analysis - Identify specific delay points in opening text
"""

import requests
from bs4 import BeautifulSoup
from gtts import gTTS
import re
import os
from pydub import AudioSegment

def extract_first_paragraph():
    """Extract and analyze just the first paragraph for delay issues"""
    
    print("🔍 FIRST PARAGRAPH DELAY ANALYSIS")
    print("=" * 45)
    
    url = "https://www.theguardian.com/world/2025/oct/04/greta-thunberg-israel-gaza-sweden"
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    
    # Get first paragraph from main content
    content_div = soup.select_one('div[data-gu-name="body"]')
    first_p = content_div.find('p')
    
    # Extract text with different methods to compare
    raw_text = first_p.get_text()
    clean_text = first_p.get_text(separator=' ', strip=True)
    normalized_text = re.sub(r'\s+', ' ', clean_text.strip())
    
    print("📝 FIRST PARAGRAPH EXTRACTION:")
    print(f"Raw text: '{raw_text}'")
    print(f"Raw repr: {repr(raw_text)}")
    print(f"\nClean text: '{clean_text}'")
    print(f"Clean repr: {repr(clean_text)}")
    print(f"\nNormalized: '{normalized_text}'")
    print(f"Normalized repr: {repr(normalized_text)}")
    
    return normalized_text

def test_sentence_segments(paragraph):
    """Break paragraph into smaller segments and test each for timing"""
    
    print(f"\n🧪 SENTENCE SEGMENT TESTING")
    print("=" * 35)
    
    # Split into natural segments
    segments = [
        "The environmental campaigner Greta Thunberg",
        "has told Swedish officials", 
        "she faces harsh treatment",
        "in Israeli custody",
        "after her detention and removal",
        "from a flotilla carrying aid to Gaza",
        "according to correspondence seen by the Guardian"
    ]
    
    timing_results = {}
    
    for i, segment in enumerate(segments, 1):
        print(f"\nSegment {i}: '{segment}'")
        
        try:
            # Create TTS for this segment
            tts = gTTS(text=segment, lang='en', tld='ie', slow=False)
            filename = f"segment_{i}.mp3"
            tts.save(filename)
            
            # Analyze timing
            audio = AudioSegment.from_mp3(filename)
            duration = len(audio) / 1000.0
            word_count = len(segment.split())
            wps = word_count / duration if duration > 0 else 0
            
            timing_results[i] = {
                'text': segment,
                'duration': duration,
                'words': word_count,
                'wps': wps
            }
            
            print(f"   Duration: {duration:.2f}s")
            print(f"   Words: {word_count}")
            print(f"   Words/sec: {wps:.2f}")
            
            # Clean up
            os.remove(filename)
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return timing_results

def test_cumulative_segments(segments_data):
    """Test cumulative building of segments to find where delays start"""
    
    print(f"\n📈 CUMULATIVE SEGMENT TESTING")
    print("=" * 35)
    
    cumulative_text = ""
    
    for i, (seg_num, data) in enumerate(segments_data.items(), 1):
        if i == 1:
            cumulative_text = data['text']
        else:
            cumulative_text += " " + data['text']
        
        print(f"\nCumulative {i}: '{cumulative_text}'")
        
        try:
            tts = gTTS(text=cumulative_text, lang='en', tld='ie', slow=False)
            filename = f"cumulative_{i}.mp3"
            tts.save(filename)
            
            audio = AudioSegment.from_mp3(filename)
            duration = len(audio) / 1000.0
            word_count = len(cumulative_text.split())
            wps = word_count / duration if duration > 0 else 0
            
            print(f"   Duration: {duration:.2f}s")
            print(f"   Words: {word_count}")
            print(f"   Words/sec: {wps:.2f}")
            
            # Calculate if this segment added unusual delay
            if i > 1:
                expected_duration = sum(segments_data[j]['duration'] for j in range(1, i+1))
                delay_difference = duration - expected_duration
                print(f"   Expected: {expected_duration:.2f}s")
                print(f"   Actual: {duration:.2f}s")
                print(f"   Delay: {delay_difference:+.2f}s")
            
            os.remove(filename)
            
        except Exception as e:
            print(f"   ❌ Error: {e}")

def test_problematic_phrases():
    """Test specific phrases that might cause delays"""
    
    print(f"\n🎯 PROBLEMATIC PHRASE TESTING")
    print("=" * 35)
    
    test_phrases = [
        "Swedish officials",
        "she faces harsh treatment", 
        "in Israeli custody",
        "after her detention and removal",
        "from a flotilla carrying aid to Gaza",
        "according to correspondence seen by the Guardian",
        # Test potential problem areas
        "Swedish officials she faces",
        "faces harsh treatment in",
        "treatment in Israeli custody",
        "custody after her detention",
        "detention and removal from",
        "removal from a flotilla"
    ]
    
    results = {}
    
    for phrase in test_phrases:
        try:
            tts = gTTS(text=phrase, lang='en', tld='ie', slow=False)
            filename = f"phrase_test.mp3"
            tts.save(filename)
            
            audio = AudioSegment.from_mp3(filename)
            duration = len(audio) / 1000.0
            word_count = len(phrase.split())
            wps = word_count / duration if duration > 0 else 0
            
            results[phrase] = {
                'duration': duration,
                'words': word_count,
                'wps': wps
            }
            
            print(f"'{phrase}': {duration:.2f}s ({wps:.2f} wps)")
            
            os.remove(filename)
            
        except Exception as e:
            print(f"'{phrase}': Error - {e}")
    
    # Find slowest phrases
    if results:
        slowest = min(results.items(), key=lambda x: x[1]['wps'])
        fastest = max(results.items(), key=lambda x: x[1]['wps'])
        
        print(f"\n📊 ANALYSIS:")
        print(f"   Slowest: '{slowest[0]}' ({slowest[1]['wps']:.2f} wps)")
        print(f"   Fastest: '{fastest[0]}' ({fastest[1]['wps']:.2f} wps)")
    
    return results

def main():
    # Extract first paragraph
    first_paragraph = extract_first_paragraph()
    
    # Test individual segments
    segment_results = test_sentence_segments(first_paragraph)
    
    # Test cumulative building
    if segment_results:
        test_cumulative_segments(segment_results)
    
    # Test specific problematic phrases
    phrase_results = test_problematic_phrases()
    
    print(f"\n✅ FIRST PARAGRAPH ANALYSIS COMPLETE!")
    print(f"🎯 Check the output above to identify specific delay points")

if __name__ == "__main__":
    main()
