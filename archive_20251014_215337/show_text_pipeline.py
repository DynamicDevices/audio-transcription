#!/usr/bin/env python3
"""
Show Text Processing Pipeline - Create visible text file before TTS conversion
"""

import requests
from bs4 import BeautifulSoup
from gtts import gTTS
import re

def extract_and_save_text_pipeline():
    """Extract text and save each step so you can see the exact process"""
    
    print("📝 TEXT PROCESSING PIPELINE")
    print("=" * 50)
    
    url = "https://www.theguardian.com/world/2025/oct/04/greta-thunberg-israel-gaza-sweden"
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
    
    # Step 1: Get raw HTML
    print("STEP 1: Fetching raw HTML...")
    response = requests.get(url, headers=headers)
    raw_html = response.text
    
    with open('step1_raw_html.txt', 'w', encoding='utf-8') as f:
        f.write(raw_html)
    print(f"   ✅ Saved: step1_raw_html.txt ({len(raw_html):,} chars)")
    
    # Step 2: Parse HTML
    print("\nSTEP 2: Parsing HTML with BeautifulSoup...")
    soup = BeautifulSoup(raw_html, 'lxml')
    
    # Step 3: Find content div
    print("\nSTEP 3: Finding main content div...")
    content_div = soup.select_one('div[data-gu-name="body"]')
    
    if content_div:
        with open('step3_content_div_html.txt', 'w', encoding='utf-8') as f:
            f.write(str(content_div))
        print(f"   ✅ Found content div, saved: step3_content_div_html.txt")
    else:
        print("   ❌ Content div not found!")
        return
    
    # Step 4: Extract paragraphs
    print("\nSTEP 4: Extracting paragraphs...")
    paragraphs = []
    paragraph_details = []
    
    for i, p in enumerate(content_div.find_all('p')):
        raw_text = p.get_text()
        clean_text = p.get_text(separator=' ', strip=True)
        normalized_text = re.sub(r'\s+', ' ', clean_text)
        
        paragraph_details.append({
            'index': i,
            'raw_html': str(p),
            'raw_text': raw_text,
            'clean_text': clean_text,
            'normalized_text': normalized_text,
            'length': len(normalized_text)
        })
        
        if len(normalized_text) > 20:  # Only keep substantial paragraphs
            paragraphs.append(normalized_text)
    
    # Save paragraph analysis
    with open('step4_paragraph_analysis.txt', 'w', encoding='utf-8') as f:
        f.write("PARAGRAPH EXTRACTION ANALYSIS\n")
        f.write("=" * 40 + "\n\n")
        
        for para in paragraph_details:
            f.write(f"PARAGRAPH {para['index']}:\n")
            f.write(f"Length: {para['length']} chars\n")
            f.write(f"Included: {'YES' if para['length'] > 20 else 'NO'}\n")
            f.write(f"Raw HTML: {para['raw_html']}\n")
            f.write(f"Raw Text: {repr(para['raw_text'])}\n")
            f.write(f"Clean Text: {repr(para['clean_text'])}\n")
            f.write(f"Normalized: {repr(para['normalized_text'])}\n")
            f.write("-" * 40 + "\n\n")
    
    print(f"   ✅ Extracted {len(paragraphs)} paragraphs from {len(paragraph_details)} total")
    print(f"   ✅ Saved analysis: step4_paragraph_analysis.txt")
    
    # Step 5: Join paragraphs
    print("\nSTEP 5: Joining paragraphs...")
    joined_text = ' '.join(paragraphs)
    
    with open('step5_joined_paragraphs.txt', 'w', encoding='utf-8') as f:
        f.write("JOINED PARAGRAPHS (before cleaning)\n")
        f.write("=" * 40 + "\n\n")
        f.write(f"Length: {len(joined_text)} characters\n")
        f.write(f"Word count: {len(joined_text.split())} words\n\n")
        f.write("TEXT:\n")
        f.write(joined_text)
        f.write("\n\nREPR (shows hidden characters):\n")
        f.write(repr(joined_text))
    
    print(f"   ✅ Joined text: {len(joined_text)} chars")
    print(f"   ✅ Saved: step5_joined_paragraphs.txt")
    
    # Step 6: Remove line ending artifacts
    print("\nSTEP 6: Removing line ending artifacts...")
    clean_text = joined_text
    
    # Remove ALL possible line ending characters
    clean_text = re.sub(r'[\r\n\f\v\x0b\x0c\x1c\x1d\x1e\x85\u2028\u2029]+', ' ', clean_text)
    clean_text = re.sub(r'\t+', ' ', clean_text)
    clean_text = re.sub(r'\s+', ' ', clean_text)
    clean_text = re.sub(r'[\u00A0\u1680\u2000-\u200B\u202F\u205F\u3000\uFEFF]+', ' ', clean_text)
    
    with open('step6_no_line_artifacts.txt', 'w', encoding='utf-8') as f:
        f.write("TEXT WITH LINE ENDING ARTIFACTS REMOVED\n")
        f.write("=" * 45 + "\n\n")
        f.write(f"Length: {len(clean_text)} characters\n")
        f.write(f"Word count: {len(clean_text.split())} words\n")
        f.write(f"Contains \\n: {'YES' if chr(10) in clean_text else 'NO'}\n")
        f.write(f"Contains \\r: {'YES' if chr(13) in clean_text else 'NO'}\n")
        f.write(f"Contains \\t: {'YES' if chr(9) in clean_text else 'NO'}\n\n")
        f.write("TEXT:\n")
        f.write(clean_text)
        f.write("\n\nREPR (shows hidden characters):\n")
        f.write(repr(clean_text))
    
    print(f"   ✅ Cleaned text: {len(clean_text)} chars")
    print(f"   ✅ Saved: step6_no_line_artifacts.txt")
    
    # Step 7: Apply phrase optimizations
    print("\nSTEP 7: Applying phrase optimizations...")
    optimized_text = clean_text
    
    # Show original problematic phrase
    original_phrase = "she is being subjected to harsh treatment"
    optimized_phrase = "she faces harsh treatment"
    
    if original_phrase in optimized_text:
        print(f"   🎯 Found problematic phrase: '{original_phrase}'")
        optimized_text = optimized_text.replace(original_phrase, optimized_phrase)
        print(f"   ✅ Replaced with: '{optimized_phrase}'")
    else:
        print(f"   ℹ️  Problematic phrase not found in text")
    
    # Other optimizations
    optimized_text = re.sub(r'[""]', '', optimized_text)  # Remove smart quotes
    optimized_text = re.sub(r"['']", '', optimized_text)  # Remove smart apostrophes  
    optimized_text = re.sub(r'[–—]', ' ', optimized_text)  # Remove dashes
    optimized_text = re.sub(r', including ([^,]+)', r' with \1', optimized_text)  # Fix "including"
    optimized_text = re.sub(r'\s+', ' ', optimized_text)  # Final space normalization
    
    with open('step7_phrase_optimized.txt', 'w', encoding='utf-8') as f:
        f.write("TEXT WITH PHRASE OPTIMIZATIONS\n")
        f.write("=" * 35 + "\n\n")
        f.write(f"Length: {len(optimized_text)} characters\n")
        f.write(f"Word count: {len(optimized_text.split())} words\n\n")
        f.write("OPTIMIZATIONS APPLIED:\n")
        f.write(f"- Replaced '{original_phrase}' with '{optimized_phrase}'\n")
        f.write("- Removed smart quotes\n")
        f.write("- Removed dashes\n")
        f.write("- Fixed 'including' constructions\n")
        f.write("- Normalized all spacing\n\n")
        f.write("TEXT:\n")
        f.write(optimized_text)
    
    print(f"   ✅ Optimized text: {len(optimized_text)} chars")
    print(f"   ✅ Saved: step7_phrase_optimized.txt")
    
    # Step 8: Truncate if needed
    print("\nSTEP 8: Truncating to reasonable length...")
    final_text = optimized_text
    
    if len(final_text) > 3500:
        truncated = final_text[:3500]
        last_period = truncated.rfind('. ')
        if last_period > 3000:
            final_text = truncated[:last_period + 1]
        print(f"   ✅ Truncated from {len(optimized_text)} to {len(final_text)} chars")
    else:
        print(f"   ℹ️  No truncation needed")
    
    # Step 9: Add introduction
    print("\nSTEP 9: Adding introduction...")
    intro = "Guardian news report about Greta Thunberg by Lorenzo Tondo. "
    complete_text = intro + final_text
    
    # Step 10: Save final text for TTS
    print("\nSTEP 10: Saving final text for TTS conversion...")
    
    with open('FINAL_TEXT_FOR_TTS.txt', 'w', encoding='utf-8') as f:
        f.write("FINAL TEXT THAT WILL BE CONVERTED TO AUDIO\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Total length: {len(complete_text)} characters\n")
        f.write(f"Word count: {len(complete_text.split())} words\n")
        f.write(f"Estimated duration: {len(complete_text.split()) / 180:.1f} minutes\n\n")
        f.write("INTRODUCTION:\n")
        f.write(f"'{intro}'\n\n")
        f.write("MAIN CONTENT:\n")
        f.write(f"'{final_text}'\n\n")
        f.write("COMPLETE TEXT FOR TTS:\n")
        f.write("-" * 30 + "\n")
        f.write(complete_text)
        f.write("\n" + "-" * 30 + "\n\n")
        f.write("TEXT REPRESENTATION (shows all characters):\n")
        f.write(repr(complete_text))
    
    print(f"   ✅ Final text: {len(complete_text)} chars, {len(complete_text.split())} words")
    print(f"   ✅ Saved: FINAL_TEXT_FOR_TTS.txt")
    
    return complete_text

def main():
    print("🔍 SHOWING COMPLETE TEXT PROCESSING PIPELINE")
    print("=" * 60)
    
    final_text = extract_and_save_text_pipeline()
    
    print(f"\n📋 PIPELINE COMPLETE!")
    print(f"=" * 25)
    print(f"Files created:")
    print(f"   📄 step1_raw_html.txt - Original HTML")
    print(f"   📄 step3_content_div_html.txt - Extracted content div")
    print(f"   📄 step4_paragraph_analysis.txt - Paragraph breakdown")
    print(f"   📄 step5_joined_paragraphs.txt - Joined paragraphs")
    print(f"   📄 step6_no_line_artifacts.txt - Line endings removed")
    print(f"   📄 step7_phrase_optimized.txt - Phrase optimizations")
    print(f"   📄 FINAL_TEXT_FOR_TTS.txt - ⭐ FINAL TEXT FOR AUDIO")
    print(f"\n🎯 CHECK 'FINAL_TEXT_FOR_TTS.txt' to see exactly what gets converted to audio!")

if __name__ == "__main__":
    main()
