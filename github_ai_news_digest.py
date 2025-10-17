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
import argparse
from dataclasses import dataclass

# AI provider - Anthropic Claude
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    print("❌ ERROR: Anthropic library not installed. Run: pip install anthropic")

# Multi-language configuration
LANGUAGE_CONFIGS = {
    'en_GB': {
        'name': 'English (UK)',
        'native_name': 'English (UK)',
        'sources': {
            'BBC News': 'https://www.bbc.co.uk/news',
            'Guardian': 'https://www.theguardian.com/uk',
            'Independent': 'https://www.independent.co.uk',
            'Sky News': 'https://news.sky.com',
            'Telegraph': 'https://www.telegraph.co.uk'
        },
        'voice': 'en-IE-EmilyNeural',
        'greeting': 'Good morning',
        'themes': ['politics', 'economy', 'health', 'international', 'climate', 'technology', 'crime'],
        'output_dir': 'docs/en_GB',
        'audio_dir': 'docs/en_GB/audio',
        'service_name': 'AudioNews UK'
    },
    'fr_FR': {
        'name': 'French (France)',
        'native_name': 'Français',
        'sources': {
            'Le Monde': 'https://www.lemonde.fr/',
            'Le Figaro': 'https://www.lefigaro.fr/',
            'Libération': 'https://www.liberation.fr/',
            'France 24': 'https://www.france24.com/fr/'
        },
        'voice': 'fr-FR-DeniseNeural',
        'greeting': 'Bonjour',
        'themes': ['politique', 'économie', 'santé', 'international', 'climat', 'technologie', 'société'],
        'output_dir': 'docs/fr_FR',
        'audio_dir': 'docs/fr_FR/audio',
        'service_name': 'AudioNews France'
    },
    'de_DE': {
        'name': 'German (Germany)',
        'native_name': 'Deutsch',
        'sources': {
            'Der Spiegel': 'https://www.spiegel.de/',
            'Die Zeit': 'https://www.zeit.de/',
            'Süddeutsche Zeitung': 'https://www.sueddeutsche.de/',
            'Frankfurter Allgemeine': 'https://www.faz.net/'
        },
        'voice': 'de-DE-KatjaNeural',
        'greeting': 'Guten Morgen',
        'themes': ['politik', 'wirtschaft', 'gesundheit', 'international', 'klima', 'technologie', 'gesellschaft'],
        'output_dir': 'docs/de_DE',
        'audio_dir': 'docs/de_DE/audio',
        'service_name': 'AudioNews Deutschland'
    },
    'es_ES': {
        'name': 'Spanish (Spain)',
        'native_name': 'Español',
        'sources': {
            'El País': 'https://elpais.com/',
            'El Mundo': 'https://www.elmundo.es/',
            'ABC': 'https://www.abc.es/',
            'La Vanguardia': 'https://www.lavanguardia.com/'
        },
        'voice': 'es-ES-ElviraNeural',
        'greeting': 'Buenos días',
        'themes': ['política', 'economía', 'salud', 'internacional', 'clima', 'tecnología', 'crimen'],
        'output_dir': 'docs/es_ES',
        'audio_dir': 'docs/es_ES/audio',
        'service_name': 'AudioNews España'
    },
    'it_IT': {
        'name': 'Italian (Italy)',
        'native_name': 'Italiano',
        'sources': {
            'Corriere della Sera': 'https://www.corriere.it/',
            'La Repubblica': 'https://www.repubblica.it/',
            'La Gazzetta dello Sport': 'https://www.gazzetta.it/',
            'Il Sole 24 Ore': 'https://www.ilsole24ore.com/'
        },
        'voice': 'it-IT-ElsaNeural',
        'greeting': 'Buongiorno',
        'themes': ['politica', 'economia', 'salute', 'internazionale', 'clima', 'tecnologia', 'crimine'],
        'output_dir': 'docs/it_IT',
        'audio_dir': 'docs/it_IT/audio',
        'service_name': 'AudioNews Italia'
    },
    'nl_NL': {
        'name': 'Dutch (Netherlands)',
        'native_name': 'Nederlands',
        'sources': {
            'NOS': 'https://nos.nl/',
            'De Telegraaf': 'https://www.telegraaf.nl/',
            'Volkskrant': 'https://www.volkskrant.nl/',
            'NRC': 'https://www.nrc.nl/'
        },
        'voice': 'nl-NL-ColetteNeural',
        'greeting': 'Goedemorgen',
        'themes': ['politiek', 'economie', 'gezondheid', 'internationaal', 'klimaat', 'technologie', 'misdaad'],
        'output_dir': 'docs/nl_NL',
        'audio_dir': 'docs/nl_NL/audio',
        'service_name': 'AudioNews Nederland'
    },
    'en_GB_LON': {
        'name': 'English (London)',
        'native_name': 'English (London)',
        'sources': {
            'Evening Standard': 'https://www.standard.co.uk/',
            'Time Out London': 'https://www.timeout.com/london/news',
            'MyLondon': 'https://www.mylondon.news/',
            'BBC London': 'https://www.bbc.co.uk/news/england/london',
            'ITV London': 'https://www.itv.com/news/london'
        },
        'voice': 'en-IE-EmilyNeural',
        'greeting': 'Good morning London',
        'themes': ['transport', 'housing', 'westminster', 'culture', 'crime', 'business', 'tfl'],
        'output_dir': 'docs/en_GB_LON',
        'audio_dir': 'docs/en_GB_LON/audio',
        'service_name': 'AudioNews London'
    },
    'en_GB_LIV': {
        'name': 'English (Liverpool)',
        'native_name': 'English (Liverpool)',
        'sources': {
            'Liverpool Echo': 'https://www.liverpoolecho.co.uk/',
            'Liverpool FC': 'https://www.liverpoolfc.com/news',
            'BBC Merseyside': 'https://www.bbc.co.uk/news/england/merseyside',
            'Radio City': 'https://www.radiocity.co.uk/news/liverpool-news/',
            'The Guide Liverpool': 'https://www.theguideliverpool.com/news/'
        },
        'voice': 'en-IE-EmilyNeural',
        'greeting': 'Good morning Liverpool',
        'themes': ['football', 'merseyside', 'culture', 'waterfront', 'music', 'business', 'transport'],
        'output_dir': 'docs/en_GB_LIV',
        'audio_dir': 'docs/en_GB_LIV/audio',
        'service_name': 'AudioNews Liverpool'
    }
}

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
    
    def __init__(self, language='en_GB'):
        self.language = language
        self.config = LANGUAGE_CONFIGS.get(language, LANGUAGE_CONFIGS['en_GB'])
        self.sources = self.config['sources']
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        self.voice_name = self.config['voice']
        
        # Initialize GitHub Copilot API
        self.setup_github_ai()
    
    def setup_github_ai(self):
        """
        Setup AI integration with Anthropic (primary provider)
        """
        anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        
        # Enhanced debugging
        print(f"🔍 Debug - Checking AI setup:")
        print(f"   - ANTHROPIC_AVAILABLE (library): {ANTHROPIC_AVAILABLE}")
        print(f"   - ANTHROPIC_API_KEY (env): {'✅ Present (length: ' + str(len(anthropic_key)) + ')' if anthropic_key else '❌ Missing'}")
        print(f"   - Language: {self.language}")
        
        if anthropic_key and ANTHROPIC_AVAILABLE:
            try:
                self.anthropic_client = anthropic.Anthropic(api_key=anthropic_key)
                self.ai_provider = 'anthropic'
                self.ai_enabled = True
                print("🤖 AI Analysis: ANTHROPIC ENABLED")
                print(f"   ✅ Successfully initialized Anthropic client")
            except Exception as init_error:
                error_msg = f"🚨 CRITICAL ERROR: Failed to initialize Anthropic client: {init_error}"
                print(error_msg)
                print(f"   🔍 API key starts with: {anthropic_key[:20]}..." if anthropic_key and len(anthropic_key) > 20 else "   🔍 API key too short or invalid")
                raise Exception(f"Anthropic initialization failed: {init_error}")
        else:
            # CRITICAL: For professional news service, AI MUST work
            error_msg = "🚨 CRITICAL ERROR: AI Analysis is REQUIRED for professional news service"
            if not ANTHROPIC_AVAILABLE:
                error_msg += "\n❌ Anthropic library not installed"
            elif not anthropic_key:
                error_msg += "\n❌ ANTHROPIC_API_KEY environment variable not found"
            else:
                error_msg += "\n❌ Unknown issue with Anthropic setup"
            
            print(error_msg)
            print("💡 This service requires Anthropic API access")
            print("🔧 Please configure ANTHROPIC_API_KEY and retry")
            
            # Enhanced debugging for CI environment
            print(f"🔍 Environment variables present:")
            print(f"   - ANTHROPIC_API_KEY: {'✅ Present' if anthropic_key else '❌ Missing'}")
            print(f"   - ANTHROPIC_AVAILABLE: {ANTHROPIC_AVAILABLE}")
            print(f"   - Current working directory: {os.getcwd()}")
            print(f"   - Language: {self.language}")
            
            # FAIL FAST - don't produce garbage content
            raise Exception("AI Analysis requires valid ANTHROPIC_API_KEY. Cannot continue without it.")
    
    def get_selectors_for_language(self) -> List[str]:
        """Get language and source-specific CSS selectors"""
        base_selectors = [
            'h1, h2, h3',
            '[data-testid*="headline"]',
            '.headline',
            '.title',
            'article h1, article h2'
        ]
        
        if self.language == 'fr_FR':
            # French news site specific selectors
            french_selectors = [
                '.article__title',           # Le Monde
                '.fig-headline',             # Le Figaro
                '.teaser__title',           # Libération
                '.t-content__title',        # France 24
                '.article-title',
                '.titre',
                '.headline-title'
            ]
            return base_selectors + french_selectors
        
        elif self.language == 'de_DE':
            # German news site specific selectors
            german_selectors = [
                '.article-title',           # Der Spiegel
                '.zon-teaser__title',       # Die Zeit
                '.entry-title',             # Süddeutsche Zeitung
                '.js-headline',             # FAZ
                '.headline',
                '.titel',
                '.schlagzeile'
            ]
            return base_selectors + german_selectors
        
        elif self.language == 'es_ES':
            # Spanish news site specific selectors
            spanish_selectors = [
                '.c_h_t',                   # El País
                '.ue-c-cover-content__headline',  # El Mundo
                '.titular',                 # ABC
                '.tit',                     # La Vanguardia
                '.headline',
                '.titulo',
                '.cabecera'
            ]
            return base_selectors + spanish_selectors
        
        elif self.language == 'it_IT':
            # Italian news site specific selectors
            italian_selectors = [
                '.title-art',               # Corriere della Sera
                '.entry-title',             # La Repubblica
                '.gazzetta-title',          # Gazzetta dello Sport
                '.article-title',           # Il Sole 24 Ore
                '.headline',
                '.titolo',
                '.intestazione'
            ]
            return base_selectors + italian_selectors
        
        elif self.language == 'nl_NL':
            # Dutch news site specific selectors
            dutch_selectors = [
                '.sc-1x7olzq',              # NOS
                '.ArticleTeaser__title',    # De Telegraaf
                '.teaser__title',           # Volkskrant
                '.article__title',          # NRC
                '.headline',
                '.titel',
                '.kop'
            ]
            return base_selectors + dutch_selectors
        
        elif self.language in ['en_GB_LON', 'en_GB_LIV']:
            # London/Liverpool specific selectors (extends UK selectors)
            uk_selectors = [
                '.fc-item__title',          # Guardian
                '.story-headline',          # BBC
                '.headline-text',           # Independent
                '.standard-headline',       # Evening Standard
                '.echo-headline',           # Liverpool Echo
                '.article-headline'
            ]
            return base_selectors + uk_selectors
        
        else:
            # Default UK news site specific selectors
            uk_selectors = [
                '.fc-item__title',          # Guardian
                '.story-headline',          # BBC
                '.headline-text'            # Independent
            ]
            return base_selectors + uk_selectors

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
            
            # Get language-specific selectors
            selectors = self.get_selectors_for_language()
            
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
        Use GitHub AI to intelligently categorize and analyze stories - REQUIRED for professional service
        """
        if not self.ai_enabled or not all_stories:
            raise Exception("🚨 CRITICAL: AI Analysis is REQUIRED. Cannot produce professional news digest without AI analysis.")
        
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
            
            RESPONSE FORMAT: Return ONLY a valid JSON object. No explanations, no markdown, no text outside the JSON.
            
            JSON Format:
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
            6. Return ONLY the JSON object, absolutely no other text
            7. Use only these themes: politics, economy, health, international, climate, technology, crime
            8. Rate significance 1-10 based on coverage breadth and uniqueness
            9. Focus on stories with cross-source coverage but avoid duplicates
            10. CRITICAL: Your response must be valid JSON that can be parsed by json.loads()
            """
            
            # Use Anthropic Claude for AI analysis
            response = self.anthropic_client.messages.create(
                    model="claude-sonnet-4-5-20250929",
                    max_tokens=1500,
                    temperature=0.1,  # Lower temperature for more consistent JSON
                    messages=[
                        {"role": "user", "content": f"""You are an expert news analyst. CRITICAL: Eliminate duplicate stories about the same events. Focus on uniqueness and avoid redundancy. 

{ai_prompt}

CRITICAL: Respond with ONLY the JSON object. No explanations, no markdown, no text before or after. Start your response with {{ and end with }}."""}
                    ]
                )
                
                # Extract and clean the response text
                response_text = response.content[0].text.strip()
                print(f"   🔍 Raw AI response length: {len(response_text)} chars")
                print(f"   🔍 Response starts with: {response_text[:50]}")
                print(f"   🔍 Response ends with: {response_text[-50:]}")
                
                # Clean the response - remove any markdown formatting
                cleaned_text = response_text
                if cleaned_text.startswith('```json'):
                    cleaned_text = cleaned_text[7:]  # Remove ```json
                if cleaned_text.startswith('```'):
                    cleaned_text = cleaned_text[3:]   # Remove ```
                if cleaned_text.endswith('```'):
                    cleaned_text = cleaned_text[:-3]  # Remove trailing ```
                
                cleaned_text = cleaned_text.strip()
                
                # Try to extract JSON from the response
                try:
                    ai_analysis = json.loads(cleaned_text)
                    print(f"   ✅ JSON parsed successfully: {len(ai_analysis)} themes")
                except json.JSONDecodeError as json_error:
                    print(f"   ❌ JSON parsing failed: {json_error}")
                    print(f"   📝 Cleaned text: {cleaned_text[:500]}")
                    
                    # Try to extract JSON using regex as fallback
                    import re
                    json_match = re.search(r'\{.*\}', cleaned_text, re.DOTALL)
                    if json_match:
                        try:
                            json_str = json_match.group()
                            ai_analysis = json.loads(json_str)
                            print(f"   ✅ JSON extracted with regex: {len(ai_analysis)} themes")
                        except json.JSONDecodeError:
                            raise Exception(f"Claude returned invalid JSON even after regex extraction: {json_error}. Full response: {response_text}")
                    else:
                        raise Exception(f"No JSON found in Claude response: {json_error}. Full response: {response_text}")
            
            
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
            print("   🚨 CRITICAL: Cannot continue without AI analysis")
            raise Exception(f"AI Analysis failed and fallback is not acceptable for professional service: {e}")
    
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
    
    def get_synthesis_prompt(self, theme: str, stories: List[NewsStory]) -> str:
        """Generate language-specific synthesis prompt"""
        headlines = chr(10).join([f"- {story.title}" for story in stories[:3]])
        
        if self.language == 'fr_FR':
            return f"""
            Créez un résumé d'actualités concis et informatif sur {theme} pour les auditeurs malvoyants.
            
            Sujets clés basés sur les titres actuels:
            {headlines}
            
            Exigences:
            - Créez du contenu original (NE copiez PAS les titres)
            - Écrivez pour la consommation audio (phrases claires et fluides)
            - Gardez sous 80 mots
            - NE mentionnez PAS les sources d'information spécifiques
            - NE mentionnez PAS combien de sources couvrent ceci
            - Concentrez-vous sur ce qui se passe, pas sur qui le rapporte
            - ÉVITEZ le contenu répétitif - synthétisez en UN récit cohérent
            - Si plusieurs histoires concernent le même événement, combinez-les en un résumé
            - Commencez par: "Dans l'actualité {theme} aujourd'hui..."
            """
        elif self.language == 'de_DE':
            return f"""
            Erstellen Sie eine prägnante, informative Nachrichtenzusammenfassung über {theme} für sehbehinderte Zuhörer.
            
            Wichtige Themen basierend auf aktuellen Schlagzeilen:
            {headlines}
            
            Anforderungen:
            - Erstellen Sie originelle Inhalte (kopieren Sie NICHT die Schlagzeilen)
            - Schreiben Sie für den Audio-Konsum (klare, fließende Sätze)
            - Bleiben Sie unter 80 Wörtern
            - Erwähnen Sie KEINE spezifischen Nachrichtenquellen
            - Erwähnen Sie NICHT, wie viele Quellen dies abdecken
            - Konzentrieren Sie sich darauf, was passiert, nicht wer darüber berichtet
            - VERMEIDEN Sie wiederholende Inhalte - synthetisieren Sie zu EINER kohärenten Erzählung
            - Wenn mehrere Geschichten dasselbe Ereignis betreffen, kombinieren Sie sie zu einer Zusammenfassung
            - Beginnen Sie mit: "In den {theme}-Nachrichten heute..."
            """
        elif self.language == 'es_ES':
            return f"""
            Cree un resumen de noticias conciso e informativo sobre {theme} para oyentes con discapacidad visual.
            
            Temas clave basados en titulares actuales:
            {headlines}
            
            Requisitos:
            - Cree contenido original (NO copie los titulares)
            - Escriba para consumo de audio (oraciones claras y fluidas)
            - Manténgase bajo 80 palabras
            - NO mencione fuentes de noticias específicas
            - NO mencione cuántas fuentes cubren esto
            - Concéntrese en lo que está pasando, no en quién lo informa
            - EVITE contenido repetitivo - sintetice en UNA narrativa coherente
            - Si múltiples historias se refieren al mismo evento, combínelas en un resumen
            - Comience con: "En las noticias de {theme} hoy..."
            """
        elif self.language == 'it_IT':
            return f"""
            Crea un riassunto delle notizie conciso e informativo su {theme} per ascoltatori ipovedenti.
            
            Argomenti chiave basati sui titoli attuali:
            {headlines}
            
            Requisiti:
            - Crea contenuto originale (NON copiare i titoli)
            - Scrivi per il consumo audio (frasi chiare e scorrevoli)
            - Rimani sotto le 80 parole
            - NON menzionare fonti di notizie specifiche
            - NON menzionare quante fonti coprono questo
            - Concentrati su cosa sta succedendo, non su chi lo riporta
            - EVITA contenuti ripetitivi - sintetizza in UNA narrazione coerente
            - Se più storie riguardano lo stesso evento, combinale in un riassunto
            - Inizia con: "Nelle notizie di {theme} oggi..."
            """
        elif self.language == 'nl_NL':
            return f"""
            Maak een beknopte, informatieve nieuwssamenvatting over {theme} voor visueel gehandicapte luisteraars.
            
            Belangrijke onderwerpen gebaseerd op huidige koppen:
            {headlines}
            
            Vereisten:
            - Maak originele inhoud (kopieer NIET de koppen)
            - Schrijf voor audioconsumptie (duidelijke, vloeiende zinnen)
            - Blijf onder 80 woorden
            - Vermeld GEEN specifieke nieuwsbronnen
            - Vermeld NIET hoeveel bronnen dit dekken
            - Focus op wat er gebeurt, niet op wie het rapporteert
            - VERMIJD repetitieve inhoud - synthetiseer tot ÉÉN samenhangende verhaal
            - Als meerdere verhalen over hetzelfde evenement gaan, combineer ze tot één samenvatting
            - Begin met: "In het {theme} nieuws vandaag..."
            """
        elif self.language in ['en_GB_LON', 'en_GB_LIV']:
            city = 'London' if self.language == 'en_GB_LON' else 'Liverpool'
            return f"""
            Create a concise, informative news summary about {theme} news for visually impaired listeners in {city}.
            
            Key topics to cover based on current headlines:
            {headlines}
            
            Requirements:
            - Create original content (do NOT copy headlines)
            - Write for audio consumption (clear, flowing sentences)
            - Keep under 80 words
            - Focus on {city}-specific news and impacts
            - DO NOT mention specific news sources
            - DO NOT mention how many sources cover this
            - Focus on what's happening, not who's reporting it
            - AVOID repetitive content - synthesize into ONE coherent narrative
            - If multiple stories relate to the same event, combine them into one summary
            - Begin with: "In {city} {theme} news today..."
            """
        else:  # Default to English
            return f"""
            Create a concise, informative news summary about {theme} news for visually impaired listeners.
            
            Key topics to cover based on current headlines:
            {headlines}
            
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
    
    def get_system_message(self) -> str:
        """Generate language-specific system message for AI"""
        if self.language == 'fr_FR':
            return "Vous créez du contenu d'actualités accessible pour les utilisateurs malvoyants. Écrivez clairement et de manière conversationnelle pour la consommation audio. Ne copiez jamais le texte original - synthétisez toujours. Évitez le contenu répétitif - combinez des histoires similaires en un récit cohérent."
        elif self.language == 'de_DE':
            return "Sie erstellen barrierefreie Nachrichteninhalte für sehbehinderte Nutzer. Schreiben Sie klar und gesprächig für den Audio-Konsum. Kopieren Sie niemals den ursprünglichen Text - synthetisieren Sie immer. Vermeiden Sie wiederholende Inhalte - kombinieren Sie ähnliche Geschichten zu einer kohärenten Erzählung."
        else:  # Default to English
            return "You are creating accessible news content for visually impaired users. Write clearly and conversationally for audio consumption. Never copy original text - always synthesize. Avoid repetitive content - combine similar stories into one coherent narrative."

    async def ai_synthesize_content(self, theme: str, stories: List[NewsStory]) -> str:
        """
        Use GitHub AI to create intelligent, coherent content synthesis
        """
        if not self.ai_enabled:
            raise Exception("🚨 CRITICAL: AI Analysis is REQUIRED. Cannot produce professional news digest without AI analysis.")
        
        if not stories:
            return ""
        
        try:
            story_info = []
            for story in stories[:5]:  # Top 5 stories
                info = f"- {story.title} (Source: {story.source}"
                if story.significance_score:
                    info += f", Significance: {story.significance_score}/10"
                info += ")"
                story_info.append(info)
            
            sources = list(set(story.source for story in stories))
            
            ai_prompt = self.get_synthesis_prompt(theme, stories)
            
            # Use Anthropic Claude for content synthesis
            system_msg = self.get_system_message()
            response = self.anthropic_client.messages.create(
                model="claude-sonnet-4-5-20250929",
                max_tokens=300,
                temperature=0.4,
                messages=[
                    {"role": "user", "content": f"{system_msg} {ai_prompt}"}
                ]
            )
            return response.content[0].text.strip()
            
        except Exception as e:
            print(f"   ⚠️ AI synthesis failed for {theme}: {e}")
            print("   🚨 CRITICAL: Cannot continue without AI analysis")
            raise Exception(f"AI Analysis failed and fallback is not acceptable for professional service: {e}")
    
    
    async def create_ai_enhanced_digest(self, all_stories: List[NewsStory]) -> str:
        """
        Create comprehensive digest using AI analysis
        """
        today = date.today().strftime("%B %d, %Y")
        
        # AI analyze all stories
        themes = await self.ai_analyze_stories(all_stories)
        
        if not themes:
            return "No significant news themes identified today."
        
        # Create language-specific introduction
        greeting = self.config['greeting']
        service_name = self.config['service_name']
        
        if self.language == 'fr_FR':
            digest = f"{greeting}. Voici votre résumé d'actualités françaises pour {today}, présenté par Dynamic Devices. "
        elif self.language == 'de_DE':
            digest = f"{greeting}. Hier ist Ihre deutsche Nachrichtenzusammenfassung für {today}, präsentiert von Dynamic Devices. "
        else:
            digest = f"{greeting}. Here's your UK news digest for {today}, brought to you by Dynamic Devices. "
        
        # Add AI-synthesized content for each theme
        for theme, stories in themes.items():
            if stories:
                theme_content = await self.ai_synthesize_content(theme, stories)
                if theme_content:
                    digest += f"\n\n{theme_content}"
        
        # Language-specific closing
        if self.language == 'fr_FR':
            digest += "\n\nCe résumé fournit une synthèse des actualités les plus importantes d'aujourd'hui. "
            digest += "Tout le contenu est une analyse originale conçue pour l'accessibilité. "
            digest += "Pour une couverture complète, visitez directement les sites d'actualités."
        elif self.language == 'de_DE':
            digest += "\n\nDiese Zusammenfassung bietet eine Synthese der wichtigsten Nachrichten von heute. "
            digest += "Alle Inhalte sind ursprüngliche Analysen, die für die Barrierefreiheit entwickelt wurden. "
            digest += "Für eine vollständige Berichterstattung besuchen Sie direkt die Nachrichten-Websites."
        else:
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
        # Balanced retries to avoid timeouts while maintaining voice quality
        max_retries = 3
        retry_delay = 10  # seconds - reasonable delay for service recovery
        
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    print(f"   🔄 Retry attempt {attempt + 1}/{max_retries}")
                    
                # Ensure the directory exists
                os.makedirs(os.path.dirname(output_filename), exist_ok=True)
                
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
                        # Try gTTS fallback in CI environment only
                        if os.environ.get('GITHUB_ACTIONS') == 'true':
                            print(f"   🔄 CI Environment detected - attempting gTTS fallback for voice consistency")
                            return await self.generate_gtts_fallback(digest_text, output_filename)
                        else:
                            print(f"   🎤 VOICE CONSISTENCY: Failing rather than degrading to robotic voice")
                            print(f"   📋 See GitHub Issue #17 for voice quality concerns")
                            raise Exception(f"Edge TTS authentication failed after {max_retries} attempts: {error_msg}")
                else:
                    # Non-authentication error, fail fast to maintain voice quality
                    print(f"   ❌ Non-retryable Edge TTS error: {error_msg}")
                    print(f"   🎤 VOICE CONSISTENCY: Failing rather than degrading to robotic voice")
                    print(f"   📋 See GitHub Issue #17 for voice quality concerns")
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
    
    async def generate_gtts_fallback(self, digest_text: str, output_filename: str):
        """
        Fallback to Google TTS when Edge TTS fails in CI environment
        """
        print(f"   🔄 Attempting Google TTS fallback...")
        
        try:
            from gtts import gTTS
            import tempfile
            
            # Map our language codes to gTTS language codes
            lang_map = {
                'en-IE-EmilyNeural': 'en',
                'fr-FR-DeniseNeural': 'fr', 
                'de-DE-KatjaNeural': 'de',
                'es-ES-ElviraNeural': 'es',
                'it-IT-ElsaNeural': 'it',
                'nl-NL-ColetteNeural': 'nl'
            }
            
            gtts_lang = lang_map.get(self.voice_name, 'en')
            print(f"   🎤 Using Google TTS with language: {gtts_lang}")
            
            # Ensure the directory exists
            os.makedirs(os.path.dirname(output_filename), exist_ok=True)
            
            # Generate audio with gTTS
            tts = gTTS(text=digest_text, lang=gtts_lang, slow=False)
            tts.save(output_filename)
            
            # Analyze the generated audio
            file_size_kb = os.path.getsize(output_filename) / 1024
            word_count = len(digest_text.split())
            duration_s = word_count / 2.0  # Estimate 2 words per second for gTTS
            words_per_second = 2.0
            
            print(f"   ✅ Google TTS fallback successful: {duration_s:.1f}s (estimated), {word_count} words, {words_per_second:.2f} WPS, {file_size_kb:.0f}KB")
            print(f"   ⚠️ Note: Voice quality may differ from Edge TTS")
            
            return {
                'filename': output_filename,
                'duration': duration_s,
                'words': word_count,
                'wps': words_per_second,
                'size_kb': file_size_kb
            }
            
        except Exception as fallback_error:
            print(f"   ❌ Google TTS fallback also failed: {fallback_error}")
            raise Exception(f"Both Edge TTS and Google TTS failed: {fallback_error}")
    
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
        text_filename = f"{self.config['output_dir']}/news_digest_ai_{today_str}.txt"
        audio_filename = f"{self.config['audio_dir']}/news_digest_ai_{today_str}.mp3"
        
        # Check if files exist AND audio file has reasonable size (>50KB)
        audio_size = os.path.getsize(audio_filename) if os.path.exists(audio_filename) else 0
        
        if os.path.exists(text_filename) and os.path.exists(audio_filename) and audio_size > 50000:
            print(f"\n💰 COST OPTIMIZATION: Today's content already exists")
            print(f"   ✅ Text: {text_filename}")
            print(f"   ✅ Audio: {audio_filename} ({audio_size:,} bytes)")
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
                'ai_enabled': self.ai_enabled,
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
        # Ensure the directory exists for text file
        os.makedirs(os.path.dirname(text_filename), exist_ok=True)
        
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
    Generate AI-enhanced daily digest using GitHub infrastructure with comprehensive error handling
    """
    parser = argparse.ArgumentParser(description='Generate multi-language AI news digest')
    parser.add_argument('--language', '-l', 
                       choices=['en_GB', 'fr_FR', 'de_DE', 'es_ES', 'it_IT', 'nl_NL', 'en_GB_LON', 'en_GB_LIV'], 
                       default='en_GB',
                       help='Language for news digest (default: en_GB)')
    
    args = parser.parse_args()
    
    print(f"🌍 Language: {LANGUAGE_CONFIGS[args.language]['native_name']}")
    print(f"🎤 Voice: {LANGUAGE_CONFIGS[args.language]['voice']}")
    print(f"📁 Output: {LANGUAGE_CONFIGS[args.language]['output_dir']}")
    
    try:
        print(f"🔧 Initializing digest generator...")
        digest_generator = GitHubAINewsDigest(language=args.language)
        print(f"✅ Digest generator initialized successfully")
        
        print(f"🚀 Starting digest generation...")
        result = await digest_generator.generate_daily_ai_digest()
        print(f"✅ Digest generation completed successfully")
        
        if result:
            print(f"\n🎉 SUCCESS: AI-enhanced digest ready!")
            print(f"   🤖 AI Analysis: {'ENABLED' if result['ai_enabled'] else 'FALLBACK'}")
            print(f"   🎧 Audio: {result['audio_file']}")
            print(f"   📄 Text: {result['text_file']}")
        else:
            print(f"\n⚠️ WARNING: No result returned from digest generation")
            exit(1)
            
    except Exception as e:
        print(f"\n❌ CRITICAL ERROR in {args.language} generation:")
        print(f"   🔍 Error type: {type(e).__name__}")
        print(f"   📝 Error message: {str(e)}")
        
        # Print stack trace for debugging
        import traceback
        print(f"\n📋 Full stack trace:")
        traceback.print_exc()
        
        # Exit with error code
        print(f"\n💥 Exiting with error code 1")
        exit(1)

if __name__ == "__main__":
    asyncio.run(main())
