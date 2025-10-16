#!/usr/bin/env python3
"""
HTML Template Generator for AudioNews Multi-Language Sites

This script generates complete HTML pages from modular templates and language-specific content.
It separates design/structure from content, making maintenance much easier.

Usage:
    python generate_html.py --language en_GB
    python generate_html.py --language fr_FR --date "2025-01-16"
"""

import json
import os
import argparse
from datetime import datetime
from typing import Dict, Any
import re

class HTMLGenerator:
    def __init__(self):
        self.templates_dir = "templates"
        self.base_template = None
        self.components = {}
        self.language_data = {}
        
    def load_base_template(self) -> str:
        """Load the base HTML template"""
        base_path = os.path.join(self.templates_dir, "base", "base.html")
        with open(base_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def load_component(self, component_name: str) -> str:
        """Load a specific HTML component"""
        component_path = os.path.join(self.templates_dir, "components", f"{component_name}.html")
        with open(component_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def load_language_data(self, language_code: str) -> Dict[str, Any]:
        """Load language-specific content"""
        lang_path = os.path.join(self.templates_dir, "languages", f"{language_code}.json")
        with open(lang_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def find_latest_files(self, language_code: str, date_str: str = None) -> Dict[str, str]:
        """Find the latest audio and text files for the given language and date"""
        if date_str is None:
            date_str = datetime.now().strftime('%Y-%m-%d')
        
        # Look for files in the language-specific directory
        audio_dir = f"docs/{language_code}/audio"
        text_dir = f"docs/{language_code}"
        
        audio_file = None
        text_file = None
        
        # Find audio file
        if os.path.exists(audio_dir):
            for filename in os.listdir(audio_dir):
                if filename.startswith(f"news_digest_ai_{date_str}") and filename.endswith(".mp3"):
                    audio_file = f"audio/{filename}"
                    break
        
        # Find text file
        if os.path.exists(text_dir):
            for filename in os.listdir(text_dir):
                if filename.startswith(f"news_digest_ai_{date_str}") and filename.endswith(".txt"):
                    text_file = filename
                    break
        
        return {
            'audio_file': audio_file,
            'text_file': text_file,
            'date': date_str
        }
    
    def format_date(self, date_str: str, language_code: str) -> str:
        """Format date according to language conventions"""
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        
        if language_code == 'en_GB':
            return date_obj.strftime('%A, %d %B %Y')
        elif language_code == 'fr_FR':
            # French date format
            months_fr = [
                'janvier', 'février', 'mars', 'avril', 'mai', 'juin',
                'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'
            ]
            days_fr = [
                'lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche'
            ]
            day_name = days_fr[date_obj.weekday()]
            month_name = months_fr[date_obj.month - 1]
            return f"{day_name} {date_obj.day} {month_name} {date_obj.year}"
        elif language_code == 'de_DE':
            # German date format
            months_de = [
                'Januar', 'Februar', 'März', 'April', 'Mai', 'Juni',
                'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember'
            ]
            days_de = [
                'Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag'
            ]
            day_name = days_de[date_obj.weekday()]
            month_name = months_de[date_obj.month - 1]
            return f"{day_name}, {date_obj.day}. {month_name} {date_obj.year}"
        
        return date_str
    
    def simple_mustache_render(self, template: str, data: Dict[str, Any]) -> str:
        """Simple mustache-like template rendering"""
        result = template
        
        # Handle simple {{variable}} replacements
        for key, value in data.items():
            if isinstance(value, str):
                result = result.replace(f"{{{{{key}}}}}", value)
                result = result.replace(f"{{{{{{key}}}}}}", value)  # Triple braces for unescaped HTML
        
        # Handle simple array iterations {{#array}}...{{/array}}
        for key, value in data.items():
            if isinstance(value, list):
                # Find the section
                pattern = f"{{{{#{key}}}}}(.*?){{{{/{key}}}}}"
                match = re.search(pattern, result, re.DOTALL)
                if match:
                    section_template = match.group(1)
                    rendered_items = []
                    for item in value:
                        if isinstance(item, str):
                            rendered_items.append(section_template.replace("{{{.}}}", item))
                    result = result.replace(match.group(0), "".join(rendered_items))
        
        return result
    
    def generate_html(self, language_code: str, date_str: str = None) -> str:
        """Generate complete HTML for the specified language"""
        # Load all components
        base_template = self.load_base_template()
        language_data = self.load_language_data(language_code)
        files_info = self.find_latest_files(language_code, date_str)
        
        # Prepare template variables
        formatted_date = self.format_date(files_info['date'], language_code)
        
        template_vars = {
            # Basic page info
            'LANGUAGE_CODE': language_data['language_code'],
            'LOCALE': language_data['locale'],
            'PAGE_TITLE': language_data['page']['title'].replace('{{DATE}}', formatted_date),
            'PAGE_DESCRIPTION': language_data['page']['description'].replace('{{DATE}}', formatted_date),
            'PAGE_KEYWORDS': language_data['page']['keywords'],
            
            # Site info
            'SITE_NAME': language_data['site']['name'],
            'SITE_SERVICE_NAME': language_data['site']['service_name'],
            'SITE_TAGLINE': language_data['site']['tagline'],
            'SITE_FLAG': language_data['site']['flag'],
            
            # Navigation
            'SKIP_LINK_TEXT': language_data['navigation']['skip_link'],
            
            # Sections
            'TODAYS_DIGEST_TITLE': language_data['sections']['todays_digest']['title'],
            'TODAYS_DIGEST_DESCRIPTION': language_data['sections']['todays_digest']['description'],
            'DATE_DISPLAY': language_data['sections']['todays_digest']['date_format'].replace('{{DATE}}', formatted_date),
            'ABOUT_TITLE': language_data['sections']['about']['title'],
            
            # Audio
            'AUDIO_FILE': files_info['audio_file'] or 'audio/placeholder.mp3',
            'AUDIO_FILENAME': f"news_digest_{files_info['date']}.mp3",
            'AUDIO_DESCRIPTION': language_data['audio']['description'],
            'AUDIO_FALLBACK': language_data['audio']['fallback'].replace('{{AUDIO_FILE}}', files_info['audio_file'] or '#'),
            'DOWNLOAD_BUTTON': language_data['audio']['download_button'],
            'SHARE_BUTTON': language_data['audio']['share_button'],
            'DOWNLOAD_HELP': language_data['audio']['download_help'],
            'SHARE_HELP': language_data['audio']['share_help'],
            
            # About content
            'WHAT_YOU_GET_TITLE': language_data['about_content']['what_you_get']['title'],
            'WHAT_YOU_GET_ITEMS': language_data['about_content']['what_you_get']['items'],
            'ACCESSIBILITY_TITLE': language_data['about_content']['accessibility']['title'],
            'ACCESSIBILITY_ITEMS': language_data['about_content']['accessibility']['items'],
            'CONTACT_TITLE': language_data['about_content']['contact']['title'],
            'CONTACT_ITEMS': language_data['about_content']['contact']['items'],
            
            # Development status (for languages in development)
            'DEVELOPMENT_STATUS_TITLE': language_data['about_content'].get('development_status', {}).get('title', ''),
            'DEVELOPMENT_STATUS_ITEMS': language_data['about_content'].get('development_status', {}).get('items', []),
            
            # Footer
            'FOOTER_COPYRIGHT': language_data['footer']['copyright'],
            
            # JavaScript strings
            'COPY_SUCCESS': language_data['javascript']['copy_success'],
            'COPY_ANNOUNCEMENT': language_data['javascript']['copy_announcement'],
            'COPY_ERROR': language_data['javascript']['copy_error'],
            'COPY_FALLBACK': language_data['javascript']['copy_fallback'],
        }
        
        # Load and render components
        components = {
            'SEO_META': self.simple_mustache_render(self.load_component('seo_meta'), template_vars),
            'STRUCTURED_DATA': self.simple_mustache_render(self.load_component('structured_data'), template_vars),
            'CRITICAL_CSS': self.load_component('critical_css'),
            'HEADER': self.simple_mustache_render(self.load_component('header'), template_vars),
            'MAIN_CONTENT': (
                self.simple_mustache_render(self.load_component('audio_player'), template_vars) +
                self.simple_mustache_render(self.load_component('about_section'), template_vars)
            ),
            'FOOTER': self.simple_mustache_render(self.load_component('footer'), template_vars),
            'SCRIPTS': self.simple_mustache_render(self.load_component('scripts'), template_vars),
        }
        
        # Add components to template vars
        template_vars.update(components)
        
        # Render final HTML
        return self.simple_mustache_render(base_template, template_vars)
    
    def save_html(self, html_content: str, language_code: str) -> str:
        """Save generated HTML to the appropriate location"""
        output_path = f"docs/{language_code}/index.html"
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return output_path

def main():
    parser = argparse.ArgumentParser(description='Generate HTML from modular templates')
    parser.add_argument('--language', '-l', 
                       choices=['en_GB', 'fr_FR', 'de_DE'], 
                       required=True,
                       help='Language code for the HTML to generate')
    parser.add_argument('--date', '-d',
                       help='Date for content (YYYY-MM-DD format, defaults to today)')
    parser.add_argument('--output', '-o',
                       help='Output file path (defaults to docs/{language}/index.html)')
    
    args = parser.parse_args()
    
    generator = HTMLGenerator()
    
    try:
        print(f"🌍 Generating HTML for {args.language}...")
        html_content = generator.generate_html(args.language, args.date)
        
        if args.output:
            output_path = args.output
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
        else:
            output_path = generator.save_html(html_content, args.language)
        
        print(f"✅ HTML generated successfully: {output_path}")
        print(f"📊 File size: {len(html_content):,} characters")
        
        # Show component breakdown
        lines = html_content.split('\n')
        print(f"📏 Total lines: {len(lines)}")
        
    except FileNotFoundError as e:
        print(f"❌ Error: Template file not found - {e}")
        return 1
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in language file - {e}")
        return 1
    except Exception as e:
        print(f"❌ Error generating HTML: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
