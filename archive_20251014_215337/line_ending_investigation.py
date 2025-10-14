#!/usr/bin/env python3
"""
Line Ending Investigation - Test How Different Text Formatting Affects TTS Pauses
"""

import requests
from bs4 import BeautifulSoup
from gtts import gTTS
import re
import os

def test_line_ending_effects():
    """Test how different line ending patterns affect TTS timing"""
    
    print("🔍 TESTING LINE ENDING EFFECTS ON TTS")
    print("=" * 60)
    
    # Base text from Guardian article
    base_text = "The environmental campaigner Greta Thunberg has told Swedish officials she is being subjected to harsh treatment in Israeli custody after her detention and removal from a flotilla carrying aid to Gaza according to correspondence seen by the Guardian"
    
    # Test different formatting patterns
    test_cases = [
        ("no_breaks", base_text),
        ("single_newlines", base_text.replace(" ", "\n")),
        ("double_newlines", base_text.replace(" ", "\n\n")),
        ("paragraph_breaks", base_text.replace(". ", ".\n\n")),
        ("html_style", base_text.replace(". ", ".</p>\n<p>")),
        ("mixed_spacing", base_text.replace(" ", "  ").replace(".", ".\n")),
        ("tab_separated", base_text.replace(" ", "\t")),
        ("cr_lf_windows", base_text.replace(" ", "\r\n")),
    ]
    
    results = {}
    
    for test_name, test_text in test_cases:
        print(f"\n🧪 Testing: {test_name}")
        print(f"   Text preview: '{test_text[:50]}...'")
        print(f"   Text representation: {repr(test_text[:50])}")
        
        try:
            tts = gTTS(text=test_text, lang='en', tld='ie', slow=False)
            filename = f"test_lineending_{test_name}.mp3"
            tts.save(filename)
            
            # Get file size and estimate timing
            file_size = os.path.getsize(filename)
            
            # Load and get actual duration
            from pydub import AudioSegment
            audio = AudioSegment.from_mp3(filename)
            duration = len(audio) / 1000.0
            
            word_count = len(base_text.split())  # Same words in all tests
            words_per_second = word_count / duration if duration > 0 else 0
            
            results[test_name] = {
                'duration': duration,
                'file_size': file_size,
                'wps': words_per_second
            }
            
            print(f"   Duration: {duration:.2f}s")
            print(f"   Words/sec: {words_per_second:.2f}")
            print(f"   File size: {file_size} bytes")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results[test_name] = None
    
    # Analyze results
    print(f"\n📊 LINE ENDING ANALYSIS RESULTS:")
    print(f"{'TEST':<20} {'DURATION':<10} {'WORDS/SEC':<10} {'SIZE':<10}")
    print("-" * 60)
    
    baseline = results.get('no_breaks')
    
    for test_name, data in results.items():
        if data:
            duration_diff = f"+{data['duration'] - baseline['duration']:.2f}s" if baseline else "N/A"
            print(f"{test_name:<20} {data['duration']:<10.2f} {data['wps']:<10.2f} {data['file_size']:<10}")
            if baseline and test_name != 'no_breaks':
                print(f"{'':>20} ({duration_diff} vs baseline)")
    
    return results

def extract_raw_html_and_analyze():
    """Extract raw HTML and show exactly what formatting artifacts exist"""
    
    print(f"\n🔍 RAW HTML ANALYSIS - FINDING LINE ENDING ARTIFACTS")
    print("=" * 70)
    
    url = "https://www.theguardian.com/world/2025/oct/04/greta-thunberg-israel-gaza-sweden"
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
    
    response = requests.get(url, headers=headers)
    raw_html = response.text
    
    # Find the Swedish officials phrase in raw HTML
    search_phrase = "swedish officials"
    
    print(f"🎯 SEARCHING FOR '{search_phrase}' IN RAW HTML:")
    
    matches = []
    start_pos = 0
    while True:
        pos = raw_html.lower().find(search_phrase, start_pos)
        if pos == -1:
            break
        
        # Extract context around the match
        context_start = max(0, pos - 150)
        context_end = min(len(raw_html), pos + 150)
        context = raw_html[context_start:context_end]
        
        matches.append((pos, context))
        start_pos = pos + 1
    
    for i, (pos, context) in enumerate(matches):
        print(f"\nMATCH {i+1} at position {pos}:")
        print("Raw HTML context:")
        print(repr(context))  # Show all hidden characters
        print("\nVisible context:")
        print(context)
        print("-" * 50)
    
    return matches

def create_zero_artifact_extraction():
    """Create extraction with ZERO line ending artifacts"""
    
    print(f"\n🚀 CREATING ZERO-ARTIFACT EXTRACTION")
    print("=" * 50)
    
    url = "https://www.theguardian.com/world/2025/oct/04/greta-thunberg-israel-gaza-sweden"
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    
    # Find content div
    content_div = soup.select_one('div[data-gu-name="body"]')
    
    if not content_div:
        print("❌ Content div not found")
        return None
    
    # Extract text with ZERO artifacts
    paragraphs = []
    
    for p in content_div.find_all('p'):
        # Use get_text with separator=' ' to eliminate ALL line breaks
        text = p.get_text(separator=' ', strip=True)
        
        # Additional cleaning
        text = re.sub(r'\s+', ' ', text)  # Normalize all whitespace to single spaces
        text = text.strip()
        
        if len(text) > 20:  # Skip short paragraphs
            paragraphs.append(text)
    
    # Join paragraphs with SINGLE SPACES (no \n anywhere)
    clean_text = ' '.join(paragraphs)
    
    # AGGRESSIVE artifact removal
    
    # Remove ALL possible line ending characters
    clean_text = re.sub(r'[\r\n\f\v\x0b\x0c\x1c\x1d\x1e\x85\u2028\u2029]+', ' ', clean_text)
    
    # Remove tab characters
    clean_text = re.sub(r'\t+', ' ', clean_text)
    
    # Normalize ALL whitespace to single spaces
    clean_text = re.sub(r'\s+', ' ', clean_text)
    
    # Remove Unicode whitespace characters
    clean_text = re.sub(r'[\u00A0\u1680\u2000-\u200B\u202F\u205F\u3000\uFEFF]+', ' ', clean_text)
    
    clean_text = clean_text.strip()
    
    print(f"✅ Zero-artifact text created:")
    print(f"   Length: {len(clean_text)} characters")
    
    # Check for line ending artifacts
    has_newline = '\n' in clean_text
    has_carriage = '\r' in clean_text  
    has_tab = '\t' in clean_text
    
    print(f"   No newlines: {'✅' if not has_newline else '❌'}")
    print(f"   No carriage returns: {'✅' if not has_carriage else '❌'}")
    print(f"   No tabs: {'✅' if not has_tab else '❌'}")
    
    # Check Swedish officials area
    if "swedish officials" in clean_text.lower():
        pos = clean_text.lower().find("swedish officials")
        context_start = max(0, pos - 50)
        context_end = min(len(clean_text), pos + 100)
        context = clean_text[context_start:context_end]
        print(f"   Swedish officials context: '{context}'")
        print(f"   Context repr: {repr(context)}")
    
    return clean_text

def create_zero_artifact_audio():
    """Create audio with zero formatting artifacts"""
    
    clean_text = create_zero_artifact_extraction()
    
    if not clean_text:
        return
    
    # Truncate to reasonable length
    if len(clean_text) > 3500:
        truncated = clean_text[:3500]
        last_period = truncated.rfind('. ')
        if last_period > 3000:
            clean_text = truncated[:last_period + 1]
    
    # Minimal intro (also artifact-free)
    intro = "Guardian news report about Greta Thunberg by Lorenzo Tondo. "
    
    final_text = intro + clean_text
    
    # Final verification - NO line ending artifacts
    has_newline_final = chr(10) in final_text
    has_carriage_final = chr(13) in final_text
    has_tab_final = chr(9) in final_text
    
    print(f"\n🔍 FINAL VERIFICATION:")
    print(f"   Text contains newlines: {'❌ YES' if has_newline_final else '✅ NO'}")
    print(f"   Text contains carriage returns: {'❌ YES' if has_carriage_final else '✅ NO'}")
    print(f"   Text contains tabs: {'❌ YES' if has_tab_final else '✅ NO'}")
    
    word_count = len(final_text.split())
    duration_est = word_count / 180
    
    print(f"\n🎵 Creating ZERO-ARTIFACT audio:")
    print(f"   Words: {word_count}")
    print(f"   Estimated duration: {duration_est:.1f} minutes")
    
    try:
        tts = gTTS(text=final_text, lang='en', tld='ie', slow=False)
        filename = "guardian_article_ZERO_ARTIFACTS.mp3"
        tts.save(filename)
        
        print(f"✅ SUCCESS! Created: {filename}")
        print(f"🎯 This should have ZERO pause artifacts from line endings!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    # Test line ending effects
    line_ending_results = test_line_ending_effects()
    
    # Analyze raw HTML
    html_matches = extract_raw_html_and_analyze()
    
    # Create zero-artifact version
    create_zero_artifact_audio()
    
    # Cleanup test files
    print(f"\n🧹 Cleaning up test files...")
    for filename in os.listdir('.'):
        if filename.startswith('test_lineending_') and filename.endswith('.mp3'):
            os.remove(filename)
            
    print(f"\n✅ INVESTIGATION COMPLETE!")
    print(f"🎧 Listen to guardian_article_ZERO_ARTIFACTS.mp3 to verify")

if __name__ == "__main__":
    main()
