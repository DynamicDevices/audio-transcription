#!/usr/bin/env python3
"""
GitHub AI-Enhanced Ethical News Digest Generator
Uses GitHub Copilot API for intelligent content analysis and synthesis
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
from dataclasses import dataclass

# Optional AI imports - will be imported only if needed
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

@dataclass
class NewsStory:
    title: str
    source: str
    link: Optional[str]
    timestamp: str
    theme: Optional[str] = None
    significance_score: Optional[float] = None

class GitHubAINewsDigest:
    """
    AI-Enhanced news synthesis using GitHub Copilot API
    Provides intelligent analysis while maintaining copyright compliance
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
        
        self.voice_name = "en-IE-EmilyNeural"
        
        # Initialize GitHub Copilot API
        self.setup_github_ai()
    
    def setup_github_ai(self):
        """
        Setup AI integration with multiple providers
        """
        # Try OpenAI first (most common)
        openai_key = os.getenv('OPENAI_API_KEY')
        anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        
        if openai_key and OPENAI_AVAILABLE:
            from openai import OpenAI
            self.openai_client = OpenAI(api_key=openai_key)
            self.ai_provider = 'openai'
            self.ai_enabled = True
            print("🤖 AI Analysis: OPENAI ENABLED")
        elif anthropic_key and ANTHROPIC_AVAILABLE:
            self.anthropic_client = anthropic.Anthropic(api_key=anthropic_key)
            self.ai_provider = 'anthropic'
            self.ai_enabled = True
            print("🤖 AI Analysis: ANTHROPIC ENABLED")
        else:
            self.ai_enabled = False
            self.ai_provider = None
            if not OPENAI_AVAILABLE and not ANTHROPIC_AVAILABLE:
                print("⚠️ AI Analysis: DISABLED (no AI libraries installed)")
            else:
                print("⚠️ AI Analysis: DISABLED (no API keys found)")
    
    def fetch_headlines_from_source(self, source_name: str, url: str) -> List[NewsStory]:
        """
        Extract headlines and create NewsStory objects
        """
        try:
            print(f"📡 Scanning {source_name}...")
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            stories = []
            
            # Enhanced selectors for better extraction
            selectors = [
                'h1, h2, h3',
                '[data-testid*="headline"]',
                '.fc-item__title',
                '.headline',
                '.title',
                'article h1, article h2',
                '.story-headline'
            ]
            
            seen_headlines = set()
            
            for selector in selectors:
                elements = soup.select(selector)
                for element in elements[:15]:
                    text = element.get_text(strip=True)
                    if (text and 
                        len(text) > 15 and 
                        len(text) < 200 and 
                        text not in seen_headlines and
                        not text.lower().startswith(('cookie', 'accept', 'subscribe', 'sign up', 'follow us'))):
                        
                        # Extract link
                        link = None
                        link_elem = element.find('a') or element.find_parent('a')
                        if link_elem and link_elem.get('href'):
                            href = link_elem.get('href')
                            if href.startswith('/'):
                                link = url + href
                            elif href.startswith('http'):
                                link = href
                        
                        story = NewsStory(
                            title=text,
                            source=source_name,
                            link=link,
                            timestamp=datetime.now().isoformat()
                        )
                        
                        stories.append(story)
                        seen_headlines.add(text)
                        
                        if len(stories) >= 12:
                            break
                
                if stories:
                    break
            
            print(f"   ✅ Found {len(stories)} stories from {source_name}")
            return stories
            
        except Exception as e:
            print(f"   ❌ Error fetching from {source_name}: {e}")
            return []
    
    async def ai_analyze_stories(self, all_stories: List[NewsStory]) -> Dict[str, List[NewsStory]]:
        """
        Use GitHub AI to intelligently categorize and analyze stories
        """
        if not self.ai_enabled or not all_stories:
            return self.fallback_categorization(all_stories)
        
        print("\n🤖 AI ANALYSIS: Intelligent story categorization")
        print("=" * 50)
        
        try:
            # Prepare stories for AI analysis
            story_titles = [f"{i+1}. {story.title} (Source: {story.source})" 
                          for i, story in enumerate(all_stories)]
            
            ai_prompt = f"""
            Analyze these UK news headlines and categorize them into themes. 
            CRITICALLY IMPORTANT: Identify duplicate or similar stories about the same event and select only the BEST/MOST COMPREHENSIVE version of each story.
            
            Headlines:
            {chr(10).join(story_titles)}
            
            Please respond with ONLY valid JSON in this exact format:
            {{
                "politics": [{{"index": 1, "significance": 8, "reasoning": "Government policy coverage"}}],
                "international": [{{"index": 2, "significance": 7, "reasoning": "Global affairs"}}],
                "technology": [{{"index": 3, "significance": 6, "reasoning": "Tech developments"}}]
            }}
            
            DEDUPLICATION RULES (CRITICAL):
            1. If multiple headlines cover the SAME story/event (e.g., multiple China stories, same political announcement), select ONLY the most comprehensive one
            2. Look for similar keywords, names, locations, events - these indicate duplicate coverage
            3. For example: If you see "China economy" and "China trade" and "China GDP" - these might be the same story, pick the best one
            4. Prioritize headlines with more specific details over generic ones
            5. Each theme should have UNIQUE, DISTINCT stories - no duplicates allowed
            
            OTHER RULES:
            6. Return ONLY the JSON object, no other text
            7. Use only these themes: politics, economy, health, international, climate, technology, crime
            8. Rate significance 1-10 based on coverage breadth and uniqueness
            9. Focus on stories with cross-source coverage but avoid duplicates
            """
            
            if self.ai_provider == 'openai':
                response = self.openai_client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are an expert news analyst categorizing UK headlines for accessibility services. CRITICAL: Eliminate duplicate stories about the same events. Focus on accuracy, significance, and uniqueness. Never include multiple stories about the same event or topic."},
                        {"role": "user", "content": ai_prompt}
                    ],
                    temperature=0.3,
                    max_tokens=1500
                )
                ai_analysis = json.loads(response.choices[0].message.content)
            
            elif self.ai_provider == 'anthropic':
                response = self.anthropic_client.messages.create(
                    model="claude-sonnet-4-5-20250929",
                    max_tokens=1500,
                    temperature=0.3,
                    messages=[
                        {"role": "user", "content": f"You are an expert news analyst. CRITICAL: Eliminate duplicate stories about the same events. Focus on uniqueness and avoid redundancy. {ai_prompt}"}
                    ]
                )
                ai_analysis = json.loads(response.content[0].text)
            
            # Apply AI analysis to stories and add programmatic deduplication
            themes = {}
            for theme, story_analyses in ai_analysis.items():
                theme_stories = []
                seen_keywords = set()  # Track keywords to prevent similar stories
                
                for analysis in story_analyses:
                    story_idx = analysis['index'] - 1  # Convert to 0-based
                    if 0 <= story_idx < len(all_stories):
                        story = all_stories[story_idx]
                        
                        # Extract key terms for deduplication check
                        story_keywords = set(word.lower() for word in story.title.split() 
                                           if len(word) > 3 and word.isalpha())
                        
                        # Check for significant overlap with existing stories
                        overlap_threshold = 0.4  # 40% keyword overlap indicates duplicate
                        is_duplicate = False
                        
                        for existing_keywords in seen_keywords:
                            if existing_keywords and story_keywords:
                                overlap = len(story_keywords & existing_keywords) / len(story_keywords | existing_keywords)
                                if overlap > overlap_threshold:
                                    is_duplicate = True
                                    print(f"   🔄 Skipping potential duplicate: '{story.title[:50]}...' (overlap: {overlap:.2f})")
                                    break
                        
                        if not is_duplicate:
                            story.theme = theme
                            story.significance_score = analysis['significance']
                            theme_stories.append(story)
                            seen_keywords.add(frozenset(story_keywords))
                
                if theme_stories:
                    # Sort by significance score
                    theme_stories.sort(key=lambda x: x.significance_score or 0, reverse=True)
                    themes[theme] = theme_stories
                    print(f"   🎯 {theme.capitalize()}: {len(theme_stories)} stories (AI analyzed, duplicates removed)")
            
            return themes
            
        except Exception as e:
            print(f"   ⚠️ AI analysis failed: {e}")
            print("   🔄 Falling back to keyword-based categorization")
            return self.fallback_categorization(all_stories)
    
    def fallback_categorization(self, all_stories: List[NewsStory]) -> Dict[str, List[NewsStory]]:
        """
        Fallback to keyword-based categorization if AI fails, with deduplication
        """
        theme_keywords = {
            'politics': ['government', 'minister', 'parliament', 'election', 'policy', 'mp', 'labour', 'conservative'],
            'economy': ['economy', 'inflation', 'bank', 'interest', 'market', 'business', 'financial', 'gdp'],
            'health': ['health', 'nhs', 'medical', 'hospital', 'covid', 'vaccine', 'doctor'],
            'international': ['ukraine', 'russia', 'china', 'usa', 'europe', 'war', 'conflict'],
            'climate': ['climate', 'environment', 'green', 'carbon', 'renewable', 'energy'],
            'technology': ['technology', 'tech', 'ai', 'digital', 'cyber', 'internet'],
            'crime': ['police', 'court', 'crime', 'arrest', 'investigation', 'trial']
        }
        
        themes = {}
        for theme, keywords in theme_keywords.items():
            theme_stories = []
            seen_keywords = set()  # Track keywords to prevent similar stories
            
            for story in all_stories:
                if any(keyword in story.title.lower() for keyword in keywords):
                    # Extract key terms for deduplication check
                    story_keywords = set(word.lower() for word in story.title.split() 
                                       if len(word) > 3 and word.isalpha())
                    
                    # Check for significant overlap with existing stories
                    overlap_threshold = 0.5  # 50% overlap for fallback mode (more strict)
                    is_duplicate = False
                    
                    for existing_keywords in seen_keywords:
                        if existing_keywords and story_keywords:
                            overlap = len(story_keywords & existing_keywords) / len(story_keywords | existing_keywords)
                            if overlap > overlap_threshold:
                                is_duplicate = True
                                break
                    
                    if not is_duplicate:
                        story.theme = theme
                        theme_stories.append(story)
                        seen_keywords.add(frozenset(story_keywords))
            
            if len(theme_stories) >= 2:
                themes[theme] = theme_stories
        
        return themes
    
    async def ai_synthesize_content(self, theme: str, stories: List[NewsStory]) -> str:
        """
        Use GitHub AI to create intelligent, coherent content synthesis
        """
        if not self.ai_enabled or not stories:
            return self.fallback_synthesis(theme, stories)
        
        try:
            story_info = []
            for story in stories[:5]:  # Top 5 stories
                info = f"- {story.title} (Source: {story.source}"
                if story.significance_score:
                    info += f", Significance: {story.significance_score}/10"
                info += ")"
                story_info.append(info)
            
            sources = list(set(story.source for story in stories))
            
            ai_prompt = f"""
            Create a concise, informative news summary about {theme} news for visually impaired listeners.
            
            Key topics to cover based on current headlines:
            {chr(10).join([f"- {story.title}" for story in stories[:3]])}
            
            Requirements:
            - Create original content (do NOT copy headlines)
            - Write for audio consumption (clear, flowing sentences)  
            - Keep under 80 words
            - Do NOT mention specific news sources or outlets
            - Do NOT mention how many sources are covering this
            - Focus on what's happening, not who's reporting it
            - AVOID repetitive content - synthesize into ONE coherent narrative
            - If multiple stories are about the same event, combine them into one summary
            - Start with: "In {theme} news today..."
            """
            
            if self.ai_provider == 'openai':
                response = self.openai_client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are creating accessible news content for visually impaired users. Write clearly and conversationally for audio consumption. Never copy original text - always synthesize. Avoid repetitive content - combine similar stories into one coherent narrative."},
                        {"role": "user", "content": ai_prompt}
                    ],
                    temperature=0.4,
                    max_tokens=300
                )
                return response.choices[0].message.content.strip()
            
            elif self.ai_provider == 'anthropic':
                response = self.anthropic_client.messages.create(
                    model="claude-sonnet-4-5-20250929",
                    max_tokens=300,
                    temperature=0.4,
                    messages=[
                        {"role": "user", "content": f"You are creating accessible news content. Avoid repetitive content - synthesize similar stories into one narrative. {ai_prompt}"}
                    ]
                )
                return response.content[0].text.strip()
            
        except Exception as e:
            print(f"   ⚠️ AI synthesis failed for {theme}: {e}")
            return self.fallback_synthesis(theme, stories)
    
    def fallback_synthesis(self, theme: str, stories: List[NewsStory]) -> str:
        """
        Fallback synthesis method
        """
        return f"In {theme} news today, there are significant developments across multiple areas."
    
    async def create_ai_enhanced_digest(self, all_stories: List[NewsStory]) -> str:
        """
        Create comprehensive digest using AI analysis
        """
        today = date.today().strftime("%B %d, %Y")
        
        # AI analyze all stories
        themes = await self.ai_analyze_stories(all_stories)
        
        if not themes:
            return "No significant news themes identified today."
        
        # Create simple introduction
        digest = f"Good morning. Here's your UK news digest for {today}, brought to you by Dynamic Devices. "
        
        # Add AI-synthesized content for each theme
        for theme, stories in themes.items():
            if stories:
                theme_content = await self.ai_synthesize_content(theme, stories)
                if theme_content:
                    digest += f"\n\n{theme_content}"
        
        # Simple closing
        digest += "\n\nThis digest provides a synthesis of today's most significant news stories. "
        digest += "All content is original analysis designed for accessibility. "
        digest += "For complete coverage, visit news websites directly."
        
        return digest
    
    async def generate_audio_digest(self, digest_text: str, output_filename: str):
        """
        Generate professional audio from AI-synthesized digest using Edge TTS with retry logic
        """
        print(f"\n🎤 Generating AI-enhanced audio: {output_filename}")
        
        # Retry logic for Edge TTS authentication issues
        max_retries = 3
        retry_delay = 5  # seconds
        
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    print(f"   🔄 Retry attempt {attempt + 1}/{max_retries}")
                    
                communicate = edge_tts.Communicate(digest_text, self.voice_name)
                with open(output_filename, "wb") as file:
                    async for chunk in communicate.stream():
                        if chunk["type"] == "audio":
                            file.write(chunk["data"])
                
                print(f"   ✅ Edge TTS audio generated successfully")
                break  # Success, exit retry loop
                
            except Exception as e:
                error_msg = str(e)
                print(f"   ⚠️ Edge TTS attempt {attempt + 1} failed: {error_msg}")
                
                # Check if it's an authentication error that might be temporary
                if "401" in error_msg or "authentication" in error_msg.lower() or "handshake" in error_msg.lower():
                    if attempt < max_retries - 1:  # Not the last attempt
                        print(f"   ⏳ Authentication issue detected, waiting {retry_delay} seconds before retry...")
                        await asyncio.sleep(retry_delay)
                        retry_delay *= 2  # Exponential backoff
                        continue
                    else:
                        print(f"   ❌ All retry attempts exhausted for authentication error")
                        raise Exception(f"Edge TTS authentication failed after {max_retries} attempts: {error_msg}")
                else:
                    # Non-authentication error, don't retry
                    print(f"   ❌ Non-retryable Edge TTS error: {error_msg}")
                    raise Exception(f"Edge TTS failed with non-retryable error: {error_msg}")
        
        # Analyze the generated audio with error handling
        try:
            from pydub import AudioSegment
            audio = AudioSegment.from_mp3(output_filename)
            duration_s = len(audio) / 1000.0
            word_count = len(digest_text.split())
            words_per_second = word_count / duration_s if duration_s > 0 else 0
            file_size_kb = os.path.getsize(output_filename) / 1024
            
            print(f"   ✅ AI Audio created: {duration_s:.1f}s, {word_count} words, {words_per_second:.2f} WPS, {file_size_kb:.0f}KB")
            
        except Exception as analysis_error:
            print(f"   ⚠️ Audio analysis failed: {analysis_error}")
            # Return basic stats without analysis
            file_size_kb = os.path.getsize(output_filename) / 1024 if os.path.exists(output_filename) else 0
            word_count = len(digest_text.split())
            duration_s = word_count / 2.0  # Estimate 2 words per second
            words_per_second = 2.0
            
            print(f"   ✅ AI Audio created: {duration_s:.1f}s (estimated), {word_count} words, {words_per_second:.2f} WPS, {file_size_kb:.0f}KB")
        
        return {
            'filename': output_filename,
            'duration': duration_s,
            'words': word_count,
            'wps': words_per_second,
            'size_kb': file_size_kb
        }
    
    async def generate_daily_ai_digest(self):
        """
        Main function for AI-enhanced daily digest generation
        """
        print("🤖 GITHUB AI-ENHANCED NEWS DIGEST")
        print("🎯 Intelligent analysis for visually impaired users")
        print("⚖️ Copyright-compliant AI synthesis")
        print("=" * 60)
        
        # Check if today's files already exist
        today_str = date.today().strftime("%Y_%m_%d")
        text_filename = f"news_digest_ai_{today_str}.txt"
        audio_filename = f"news_digest_ai_{today_str}.mp3"
        
        if os.path.exists(text_filename) and os.path.exists(audio_filename):
            print(f"\n💰 COST OPTIMIZATION: Today's content already exists")
            print(f"   ✅ Text: {text_filename}")
            print(f"   ✅ Audio: {audio_filename}")
            print(f"   🚀 Skipping regeneration for efficiency")
            
            # Get existing file stats for summary
            audio_size_kb = os.path.getsize(audio_filename) / 1024
            
            print(f"\n🤖 EXISTING DIGEST SUMMARY")
            print("=" * 35)
            print(f"📅 Date: {date.today().strftime('%B %d, %Y')}")
            print(f"🎧 Audio: {audio_filename}")
            print(f"📄 Text: {text_filename}")
            print(f"💾 Size: {audio_size_kb:.1f} KB")
            print(f"🚀 Status: Using existing files (no regeneration needed)")
            
            return {
                'audio_file': audio_filename,
                'text_file': text_filename,
                'regenerated': False,
                'size_kb': audio_size_kb
            }
        
        # Aggregate all stories
        all_stories = []
        for source_name, url in self.sources.items():
            stories = self.fetch_headlines_from_source(source_name, url)
            all_stories.extend(stories)
            time.sleep(1)  # Be respectful
        
        if not all_stories:
            print("❌ No stories found")
            return
        
        print(f"\n📊 Total stories collected: {len(all_stories)}")
        
        # Create AI-enhanced digest
        digest_text = await self.create_ai_enhanced_digest(all_stories)
        
        # Save files (only if they don't exist)
        
        # Save text with metadata
        with open(text_filename, 'w', encoding='utf-8') as f:
            f.write("GITHUB AI-ENHANCED NEWS DIGEST\n")
            f.write("=" * 40 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"AI Analysis: {'ENABLED' if self.ai_enabled else 'DISABLED'}\n")
            f.write("Type: AI-synthesized content for accessibility\n")
            f.write("=" * 40 + "\n\n")
            f.write(digest_text)
        
        print(f"\n📄 AI digest text saved: {text_filename}")
        
        # Generate audio
        audio_stats = await self.generate_audio_digest(digest_text, audio_filename)
        
        # Summary
        print(f"\n🤖 AI-ENHANCED DIGEST COMPLETE")
        print("=" * 35)
        print(f"📅 Date: {date.today().strftime('%B %d, %Y')}")
        print(f"🤖 AI Analysis: {'ENABLED' if self.ai_enabled else 'FALLBACK MODE'}")
        print(f"📰 Stories: {len(all_stories)} from {len(self.sources)} sources")
        print(f"⏱️ Duration: {audio_stats['duration']:.1f}s")
        print(f"🎤 Speed: {audio_stats['wps']:.2f} WPS")
        print(f"🎧 Audio: {audio_filename}")
        print(f"📄 Text: {text_filename}")
        
        return {
            'audio_file': audio_filename,
            'text_file': text_filename,
            'stats': audio_stats,
            'ai_enabled': self.ai_enabled,
            'stories_analyzed': len(all_stories),
            'regenerated': True
        }

async def main():
    """
    Generate AI-enhanced daily digest using GitHub infrastructure
    """
    digest_generator = GitHubAINewsDigest()
    result = await digest_generator.generate_daily_ai_digest()
    
    if result:
        print(f"\n🎉 SUCCESS: AI-enhanced digest ready!")
        print(f"   🤖 AI Analysis: {'ENABLED' if result['ai_enabled'] else 'FALLBACK'}")
        print(f"   🎧 Audio: {result['audio_file']}")
        print(f"   📄 Text: {result['text_file']}")

if __name__ == "__main__":
    asyncio.run(main())
