#!/usr/bin/env python3
"""
Ethical News Digest Generator for Visually Impaired Users
Synthesizes information from multiple UK media sources to create original audio content
Respects copyright while providing valuable accessibility service
"""

import asyncio
import edge_tts
import os
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, date
import json
from typing import List, Dict, Optional
import time

class EthicalNewsDigest:
    """
    Ethical news synthesis system that aggregates information from multiple sources
    and creates original audio content for visually impaired users
    """
    
    def __init__(self):
        self.sources = {
            'BBC News': 'https://www.bbc.co.uk/news',
            'Guardian': 'https://www.theguardian.com/uk',
            'Independent': 'https://www.independent.co.uk',
            'Sky News': 'https://news.sky.com',
            'Telegraph': 'https://www.telegraph.co.uk',
        }
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        self.voice_name = "en-IE-EmilyNeural"  # Irish Emily for consistency
    
    def fetch_headlines_from_source(self, source_name: str, url: str) -> List[Dict]:
        """
        Extract headlines and brief descriptions from a news source
        Only extracts factual information, not full articles
        """
        try:
            print(f"📡 Scanning {source_name}...")
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            headlines = []
            
            # Generic selectors that work across most news sites
            selectors = [
                'h1, h2, h3',  # Standard headline tags
                '[data-testid*="headline"]',  # BBC-style
                '.fc-item__title',  # Guardian-style
                '.headline',  # Generic headline class
                '.title'  # Generic title class
            ]
            
            seen_headlines = set()
            
            for selector in selectors:
                elements = soup.select(selector)
                for element in elements[:20]:  # Limit to avoid overwhelming
                    text = element.get_text(strip=True)
                    if (text and 
                        len(text) > 20 and  # Filter out very short text
                        len(text) < 200 and  # Filter out very long text
                        text not in seen_headlines and
                        not text.lower().startswith(('cookie', 'accept', 'subscribe', 'sign up'))):
                        
                        # Extract associated link if available
                        link = None
                        link_elem = element.find('a') or element.find_parent('a')
                        if link_elem and link_elem.get('href'):
                            href = link_elem.get('href')
                            if href.startswith('/'):
                                link = url + href
                            elif href.startswith('http'):
                                link = href
                        
                        headlines.append({
                            'title': text,
                            'source': source_name,
                            'link': link,
                            'timestamp': datetime.now().isoformat()
                        })
                        seen_headlines.add(text)
                        
                        if len(headlines) >= 10:  # Limit per source
                            break
                
                if headlines:
                    break  # If we found headlines with one selector, don't need others
            
            print(f"   ✅ Found {len(headlines)} headlines from {source_name}")
            return headlines
            
        except Exception as e:
            print(f"   ❌ Error fetching from {source_name}: {e}")
            return []
    
    def aggregate_all_sources(self) -> Dict[str, List[Dict]]:
        """
        Aggregate headlines from all configured sources
        """
        print("🔍 AGGREGATING NEWS FROM MULTIPLE SOURCES")
        print("=" * 50)
        
        all_headlines = {}
        
        for source_name, url in self.sources.items():
            headlines = self.fetch_headlines_from_source(source_name, url)
            all_headlines[source_name] = headlines
            time.sleep(1)  # Be respectful to servers
        
        return all_headlines
    
    def identify_common_themes(self, all_headlines: Dict[str, List[Dict]]) -> Dict[str, List[Dict]]:
        """
        Identify stories being covered by multiple sources
        This helps us focus on the most significant news
        """
        print("\n🔄 IDENTIFYING COMMON THEMES ACROSS SOURCES")
        print("=" * 50)
        
        # Simple keyword-based theme detection
        theme_keywords = {
            'politics': ['government', 'minister', 'parliament', 'election', 'policy', 'mp', 'labour', 'conservative', 'politics'],
            'economy': ['economy', 'inflation', 'bank', 'interest', 'market', 'business', 'financial', 'gdp', 'recession'],
            'health': ['health', 'nhs', 'medical', 'hospital', 'covid', 'vaccine', 'doctor', 'patient'],
            'international': ['ukraine', 'russia', 'china', 'usa', 'europe', 'war', 'conflict', 'international'],
            'climate': ['climate', 'environment', 'green', 'carbon', 'renewable', 'energy', 'pollution'],
            'technology': ['technology', 'tech', 'ai', 'digital', 'cyber', 'internet', 'data'],
            'crime': ['police', 'court', 'crime', 'arrest', 'investigation', 'trial', 'sentence']
        }
        
        themes = {}
        
        for theme, keywords in theme_keywords.items():
            theme_stories = []
            
            for source_name, headlines in all_headlines.items():
                for headline in headlines:
                    title_lower = headline['title'].lower()
                    if any(keyword in title_lower for keyword in keywords):
                        theme_stories.append(headline)
            
            if len(theme_stories) >= 2:  # Only include themes with multiple sources
                themes[theme] = theme_stories
                print(f"   📊 {theme.capitalize()}: {len(theme_stories)} stories across sources")
        
        return themes
    
    def synthesize_theme_content(self, theme: str, stories: List[Dict]) -> str:
        """
        Create original synthesized content from multiple source headlines
        This creates new, transformative content rather than copying
        """
        if not stories:
            return ""
        
        # Count sources covering this theme
        sources = list(set(story['source'] for story in stories))
        
        # Create synthesized narrative
        intro = f"In {theme} news today, "
        
        if len(sources) > 1:
            intro += f"multiple sources including {', '.join(sources[:3])} are reporting on "
        else:
            intro += f"{sources[0]} reports on "
        
        # Identify most common story elements (very basic synthesis)
        story_elements = []
        for story in stories[:3]:  # Focus on top stories
            # Extract key elements (this is a simplified approach)
            title = story['title']
            
            # Basic story classification and synthesis
            if 'government' in title.lower() or 'minister' in title.lower():
                story_elements.append("government developments")
            elif 'economy' in title.lower() or 'market' in title.lower():
                story_elements.append("economic developments") 
            elif 'health' in title.lower() or 'nhs' in title.lower():
                story_elements.append("healthcare developments")
            else:
                # Extract first few words as topic
                words = title.split()[:4]
                story_elements.append(" ".join(words).lower())
        
        if story_elements:
            content = intro + f"developments including {', '.join(story_elements[:2])}. "
            content += f"This story is being covered by {len(sources)} major UK news outlets, "
            content += f"indicating significant public interest. "
            
            # Add source attribution
            content += f"For detailed coverage, sources include {', '.join(sources)}. "
            
            return content
        
        return ""
    
    def create_daily_digest(self, all_headlines: Dict[str, List[Dict]], themes: Dict[str, List[Dict]]) -> str:
        """
        Create a comprehensive daily news digest
        """
        today = date.today().strftime("%B %d, %Y")
        
        digest = f"Good morning. Here's your UK news digest for {today}. "
        digest += "This summary synthesizes information from multiple major UK news sources "
        digest += "to provide you with the most significant stories of the day. "
        
        # Add theme-based content
        for theme, stories in themes.items():
            if stories:
                theme_content = self.synthesize_theme_content(theme, stories)
                if theme_content:
                    digest += f"\n\nIn {theme} news: {theme_content}"
        
        # Add source summary
        total_sources = len([source for source, headlines in all_headlines.items() if headlines])
        total_stories = sum(len(headlines) for headlines in all_headlines.values())
        
        digest += f"\n\nThis digest synthesizes information from {total_sources} major UK news sources, "
        digest += f"covering {total_stories} stories to bring you the most relevant updates. "
        digest += "All information is compiled from publicly available headlines and represents "
        digest += "a synthesis of multiple perspectives rather than reproduction of any single source. "
        
        digest += "\n\nFor complete coverage, we recommend visiting the original sources directly. "
        digest += "This digest is provided as an accessibility service for visually impaired users."
        
        return digest
    
    async def generate_audio_digest(self, digest_text: str, output_filename: str):
        """
        Generate professional audio from the synthesized digest
        """
        print(f"\n🎤 Generating audio digest: {output_filename}")
        
        communicate = edge_tts.Communicate(digest_text, self.voice_name)
        with open(output_filename, "wb") as file:
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    file.write(chunk["data"])
        
        # Analyze the generated audio
        from pydub import AudioSegment
        audio = AudioSegment.from_mp3(output_filename)
        duration_s = len(audio) / 1000.0
        word_count = len(digest_text.split())
        words_per_second = word_count / duration_s if duration_s > 0 else 0
        file_size_kb = os.path.getsize(output_filename) / 1024
        
        print(f"   ✅ Audio created: {duration_s:.1f}s, {word_count} words, {words_per_second:.2f} WPS, {file_size_kb:.0f}KB")
        
        return {
            'filename': output_filename,
            'duration': duration_s,
            'words': word_count,
            'wps': words_per_second,
            'size_kb': file_size_kb
        }
    
    async def generate_daily_digest(self):
        """
        Main function to generate daily ethical news digest
        """
        print("📰 ETHICAL NEWS DIGEST GENERATOR")
        print("🎯 Creating synthesized content for visually impaired users")
        print("⚖️ Respecting copyright through fair use and transformation")
        print("=" * 60)
        
        # Step 1: Aggregate headlines from multiple sources
        all_headlines = self.aggregate_all_sources()
        
        # Step 2: Identify common themes
        themes = self.identify_common_themes(all_headlines)
        
        if not themes:
            print("\n⚠️ No common themes found across sources")
            return
        
        # Step 3: Create synthesized digest
        digest_text = self.create_daily_digest(all_headlines, themes)
        
        # Step 4: Save text version
        today_str = date.today().strftime("%Y_%m_%d")
        text_filename = f"news_digest_{today_str}.txt"
        audio_filename = f"news_digest_{today_str}.mp3"
        
        with open(text_filename, 'w', encoding='utf-8') as f:
            f.write("ETHICAL NEWS DIGEST - SYNTHESIZED CONTENT\n")
            f.write("=" * 50 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("Sources: Multiple UK news outlets (see content for attribution)\n")
            f.write("Type: Synthesized content for accessibility (not reproduction)\n")
            f.write("=" * 50 + "\n\n")
            f.write(digest_text)
        
        print(f"\n📄 Text digest saved: {text_filename}")
        
        # Step 5: Generate audio
        audio_stats = await self.generate_audio_digest(digest_text, audio_filename)
        
        # Step 6: Create summary report
        print(f"\n📊 DAILY DIGEST SUMMARY")
        print("=" * 30)
        print(f"📅 Date: {date.today().strftime('%B %d, %Y')}")
        print(f"📰 Sources: {len(all_headlines)} news outlets")
        print(f"🎯 Themes: {len(themes)} major topics")
        print(f"⏱️ Duration: {audio_stats['duration']:.1f}s ({audio_stats['duration']/60:.1f} minutes)")
        print(f"📝 Words: {audio_stats['words']}")
        print(f"🎤 Speed: {audio_stats['wps']:.2f} WPS")
        print(f"💾 Size: {audio_stats['size_kb']:.0f}KB")
        print(f"🎧 Audio: {audio_filename}")
        print(f"📄 Text: {text_filename}")
        
        print(f"\n✅ ETHICAL DIGEST COMPLETE")
        print("🎯 Provides value through synthesis and analysis")
        print("⚖️ Respects copyright through fair use principles")
        print("♿ Serves visually impaired community with accessible content")
        
        return {
            'audio_file': audio_filename,
            'text_file': text_filename,
            'stats': audio_stats,
            'themes': list(themes.keys()),
            'sources': len(all_headlines)
        }

async def main():
    """
    Generate today's ethical news digest
    """
    digest_generator = EthicalNewsDigest()
    result = await digest_generator.generate_daily_digest()
    
    if result:
        print(f"\n🎉 SUCCESS: Daily digest ready for visually impaired users!")
        print(f"   Audio: {result['audio_file']}")
        print(f"   Text: {result['text_file']}")

if __name__ == "__main__":
    asyncio.run(main())
