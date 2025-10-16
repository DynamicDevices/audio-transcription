#!/usr/bin/env python3
"""
Language Addition Tool for AudioNews Multi-Language Service
Automatically creates all necessary files for a new language
"""

import os
import json
import argparse
import shutil
from pathlib import Path
from datetime import date

# Language configuration templates
LANGUAGE_CONFIGS = {
    'de_DE': {
        'name': 'German (Germany)',
        'native_name': 'Deutsch',
        'flag': '🇩🇪',
        'voice': 'de-DE-KatjaNeural',
        'greeting': 'Guten Morgen',
        'country_codes': ['DE', 'AT', 'CH'],
        'sources': {
            'Der Spiegel': 'https://www.spiegel.de/',
            'Die Zeit': 'https://www.zeit.de/',
            'Süddeutsche Zeitung': 'https://www.sueddeutsche.de/',
            'Frankfurter Allgemeine': 'https://www.faz.net/'
        },
        'themes': ['politik', 'wirtschaft', 'gesundheit', 'international', 'klima', 'technologie', 'gesellschaft'],
        'service_name': 'AudioNews Deutschland',
        'translations': {
            'title': 'AudioNews Deutschland - Tägliche Audio-Nachrichten',
            'description': 'Professioneller täglicher Audio-Nachrichtendienst für sehbehinderte Nutzer. KI-Synthese deutscher Nachrichten mit Katja Neural Stimme.',
            'tagline': 'Professionelle Audio-Nachrichten für sehbehinderte Nutzer',
            'audio_description': 'Heutige Nachrichtenzusammenfassung. Verwenden Sie die Audio-Steuerelemente Ihres Browsers oder laden Sie für Offline-Hören herunter.',
            'download_button': '📱 Für WhatsApp herunterladen',
            'development_message': 'Service vorübergehend in Entwicklung.',
            'development_description': 'Der AudioNews Deutschland Service ist derzeit in Entwicklung. Bald können Sie eine tägliche Zusammenfassung deutscher Nachrichten mit professioneller deutscher KI-Stimme hören.',
            'features_title': 'Kommende Funktionen:',
            'footer_text': 'Service von',
            'footer_tagline': 'Entwickelt mit ❤️ für Barrierefreiheit'
        }
    },
    'es_ES': {
        'name': 'Spanish (Spain)',
        'native_name': 'Español',
        'flag': '🇪🇸',
        'voice': 'es-ES-ElviraNeural',
        'greeting': 'Buenos días',
        'country_codes': ['ES'],
        'sources': {
            'El País': 'https://elpais.com/',
            'El Mundo': 'https://www.elmundo.es/',
            'ABC': 'https://www.abc.es/',
            'La Vanguardia': 'https://www.lavanguardia.com/'
        },
        'themes': ['política', 'economía', 'salud', 'internacional', 'clima', 'tecnología', 'sociedad'],
        'service_name': 'AudioNews España',
        'translations': {
            'title': 'AudioNews España - Noticias Audio Diarias',
            'description': 'Servicio profesional diario de noticias en audio para usuarios con discapacidad visual. Síntesis IA de noticias españolas con voz Elvira Neural.',
            'tagline': 'Noticias de audio profesionales para usuarios con discapacidad visual',
            'audio_description': 'Resumen de noticias de hoy. Use los controles de audio de su navegador o descargue para escuchar sin conexión.',
            'download_button': '📱 Descargar para WhatsApp',
            'development_message': 'Servicio temporalmente en desarrollo.',
            'development_description': 'El servicio AudioNews España está actualmente en desarrollo. Pronto podrá escuchar un resumen diario de noticias españolas con voz IA española profesional.',
            'features_title': 'Características próximas:',
            'footer_text': 'Servicio por',
            'footer_tagline': 'Diseñado con ❤️ para accesibilidad'
        }
    },
    'it_IT': {
        'name': 'Italian (Italy)',
        'native_name': 'Italiano',
        'flag': '🇮🇹',
        'voice': 'it-IT-ElsaNeural',
        'greeting': 'Buongiorno',
        'country_codes': ['IT'],
        'sources': {
            'Corriere della Sera': 'https://www.corriere.it/',
            'La Repubblica': 'https://www.repubblica.it/',
            'La Gazzetta dello Sport': 'https://www.gazzetta.it/',
            'Il Sole 24 Ore': 'https://www.ilsole24ore.com/'
        },
        'themes': ['politica', 'economia', 'salute', 'internazionale', 'clima', 'tecnologia', 'società'],
        'service_name': 'AudioNews Italia',
        'translations': {
            'title': 'AudioNews Italia - Notizie Audio Quotidiane',
            'description': 'Servizio professionale quotidiano di notizie audio per utenti ipovedenti. Sintesi IA di notizie italiane con voce Elsa Neural.',
            'tagline': 'Notizie audio professionali per utenti ipovedenti',
            'audio_description': 'Riassunto delle notizie di oggi. Usa i controlli audio del tuo browser o scarica per ascolto offline.',
            'download_button': '📱 Scarica per WhatsApp',
            'development_message': 'Servizio temporaneamente in sviluppo.',
            'development_description': 'Il servizio AudioNews Italia è attualmente in sviluppo. Presto potrai ascoltare un riassunto quotidiano delle notizie italiane con voce IA italiana professionale.',
            'features_title': 'Caratteristiche in arrivo:',
            'footer_text': 'Servizio di',
            'footer_tagline': 'Progettato con ❤️ per l\'accessibilità'
        }
    }
}

def create_language_directory(language_code):
    """Create the directory structure for a new language"""
    lang_dir = Path(f"docs/{language_code}")
    lang_dir.mkdir(exist_ok=True)
    (lang_dir / "audio").mkdir(exist_ok=True)
    return lang_dir

def generate_html_page(language_code, config):
    """Generate the HTML page for a new language"""
    today = date.today().strftime("%B %d, %Y")
    translations = config['translations']
    
    html_content = f'''<!DOCTYPE html>
<html lang="{language_code.split('_')[0]}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{translations['title']} - {today}</title>
    <meta name="description" content="{translations['description']}">
    
    <!-- SEO Meta Tags -->
    <meta name="keywords" content="audio news, voice news, daily news digest, accessible news, news for blind, visually impaired news, {config['native_name']} news audio">
    <meta name="author" content="Dynamic Devices">
    <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
    <meta name="googlebot" content="index, follow">
    <link rel="canonical" href="https://audionews.uk/{language_code}/">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://audionews.uk/{language_code}/">
    <meta property="og:title" content="{translations['title']}">
    <meta property="og:description" content="{translations['description']}">
    <meta property="og:image" content="https://audionews.uk/images/audionews-social-card-{language_code.lower()}.png">
    <meta property="og:site_name" content="{config['service_name']}">
    <meta property="og:locale" content="{language_code}">
    
    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:url" content="https://audionews.uk/{language_code}/">
    <meta name="twitter:title" content="{config['service_name']}">
    <meta name="twitter:description" content="{translations['description']}">
    <meta name="twitter:image" content="https://audionews.uk/images/audionews-social-card-{language_code.lower()}.png">
    <meta name="twitter:creator" content="@DynamicDevices">
    
    <!-- Additional Meta Tags -->
    <meta name="application-name" content="{config['service_name']}">
    <meta name="msapplication-TileColor" content="#1a365d">
    <meta name="format-detection" content="telephone=no">
    
    <!-- Structured Data -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "{config['service_name']}",
        "url": "https://audionews.uk/{language_code}/",
        "description": "{translations['description']}",
        "inLanguage": "{language_code}",
        "accessibilityFeature": [
            "audioDescription",
            "screenReaderSupport",
            "keyboardNavigation"
        ],
        "audience": {{
            "@type": "Audience",
            "audienceType": "visually impaired users"
        }}
    }}
    </script>

    <!-- Critical CSS -->
    <style>
        /* Same critical CSS as other language pages */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #2d3748;
            background-color: #f7fafc;
            font-size: 16px;
        }}
        
        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 1rem;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 2rem;
            padding: 2rem 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            font-weight: 300;
        }}
        
        .header .tagline {{
            font-size: 1.1rem;
            opacity: 0.9;
        }}
        
        .digest-card {{
            background: white;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 2rem;
            overflow: hidden;
        }}
        
        .digest-header {{
            background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
            color: white;
            padding: 1.5rem;
            text-align: center;
        }}
        
        .audio-player-container {{
            padding: 2rem;
            text-align: center;
        }}
        
        .audio-description {{
            font-size: 1.1rem;
            color: #4a5568;
            margin-bottom: 1.5rem;
        }}
        
        .digest-content {{
            padding: 2rem;
            font-size: 1.1rem;
            line-height: 1.8;
        }}
        
        .footer {{
            text-align: center;
            padding: 2rem 0;
            color: #718096;
            border-top: 1px solid #e2e8f0;
            margin-top: 3rem;
        }}
        
        .footer a {{
            color: #4299e1;
            text-decoration: none;
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 2rem;
            }}
        }}
    </style>
    
    <!-- Load shared CSS -->
    <link rel="preload" href="../shared/css/newspaper.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
    <noscript><link rel="stylesheet" href="../shared/css/newspaper.css"></noscript>
    
    <!-- Web App Manifest -->
    <link rel="manifest" href="manifest.json">
    
    <!-- Favicon -->
    <link rel="icon" href="../shared/images/favicon.ico" type="image/x-icon">
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>{config['flag']} {config['service_name']}</h1>
            <p class="tagline">{translations['tagline']}</p>
        </header>
        
        <main role="main">
            <article class="digest-card">
                <header class="digest-header">
                    <h2 class="digest-date">{translations['title']} - {today}</h2>
                </header>
                
                <div class="audio-player-container">
                    <p class="audio-description">
                        {translations['audio_description']}
                    </p>
                    
                    <audio controls preload="metadata">
                        <source src="audio/news_digest_ai_2025_10_16.mp3" type="audio/mpeg">
                        Your browser does not support the audio element.
                    </audio>
                    
                    <div style="margin-top: 1.5rem;">
                        <a download="audionews-{language_code.lower()}-2025-10-16.mp3" 
                           href="audio/news_digest_ai_2025_10_16.mp3" 
                           style="display: inline-block; background: linear-gradient(135deg, #48bb78 0%, #38a169 100%); color: white; text-decoration: none; padding: 0.75rem 1.5rem; border-radius: 25px; font-weight: 500;">
                            {translations['download_button']}
                        </a>
                    </div>
                </div>
                
                <div class="digest-content">
                    <p><strong>{translations['development_message']}</strong></p>
                    <p>{translations['development_description']}</p>
                    <p><strong>{translations['features_title']}</strong></p>
                    <ul style="margin-left: 2rem; margin-bottom: 1.5rem;">
                        <li>📰 Daily news synthesis from major {config['native_name']} sources</li>
                        <li>🎤 Professional {config['voice']} voice</li>
                        <li>♿ Fully accessible WCAG 2.1 AA compliant design</li>
                        <li>📱 WhatsApp sharing optimized for families</li>
                        <li>🤖 AI analysis with Claude 4.5 Sonnet</li>
                        <li>🕖 Daily automatic updates</li>
                    </ul>
                    <p>Meanwhile, you can check our complete English service at <a href="../en_GB/" style="color: #4299e1;">AudioNews UK</a>.</p>
                </div>
            </article>
        </main>
        
        <footer class="footer">
            <p>
                <strong>{config['service_name']}</strong> - {translations['footer_text']} 
                <a href="https://dynamicdevices.co.uk">Dynamic Devices</a>
            </p>
            <p>{translations['footer_tagline']} • <a href="../en_GB/">🇬🇧 English</a> • <a href="../fr_FR/">🇫🇷 Français</a> • <a href="../">🌍 Choose Language</a></p>
        </footer>
    </div>

    <!-- JavaScript -->
    <script src="../shared/js/accessibility.js" defer></script>
    
    <!-- Service worker -->
    <script>
        window.addEventListener('load', function() {{
            if ('serviceWorker' in navigator) {{
                navigator.serviceWorker.register('../sw.js');
            }}
        }});
    </script>
</body>
</html>'''
    
    return html_content

def generate_manifest(language_code, config):
    """Generate PWA manifest for a new language"""
    translations = config['translations']
    
    manifest = {
        "name": f"{config['service_name']} - {translations['title']}",
        "short_name": f"AudioNews {config['native_name'][:2]}",
        "description": translations['description'],
        "start_url": f"/{language_code}/",
        "display": "standalone",
        "background_color": "#1a365d",
        "theme_color": "#667eea",
        "orientation": "portrait-primary",
        "lang": language_code,
        "dir": "ltr",
        "scope": f"/{language_code}/",
        "icons": [
            {
                "src": "../shared/images/icon-192x192.png",
                "sizes": "192x192",
                "type": "image/png",
                "purpose": "any maskable"
            },
            {
                "src": "../shared/images/icon-512x512.png",
                "sizes": "512x512",
                "type": "image/png",
                "purpose": "any maskable"
            }
        ],
        "categories": ["news", "accessibility", "audio"],
        "shortcuts": [
            {
                "name": "Today's News",
                "short_name": "Today",
                "description": "Listen to today's news",
                "url": f"/{language_code}/?today=true",
                "icons": [
                    {
                        "src": "../shared/images/shortcut-today.png",
                        "sizes": "96x96"
                    }
                ]
            }
        ]
    }
    
    return json.dumps(manifest, indent=2, ensure_ascii=False)

def update_main_config(language_code, config):
    """Update the main language configuration files"""
    
    # Update github_ai_news_digest.py LANGUAGE_CONFIGS
    config_entry = {
        'name': config['name'],
        'native_name': config['native_name'],
        'sources': config['sources'],
        'voice': config['voice'],
        'greeting': config['greeting'],
        'themes': config['themes'],
        'output_dir': f'docs/{language_code}',
        'audio_dir': f'docs/{language_code}/audio',
        'service_name': config['service_name']
    }
    
    print(f"📝 Add this to LANGUAGE_CONFIGS in github_ai_news_digest.py:")
    print(f"    '{language_code}': {json.dumps(config_entry, indent=8, ensure_ascii=False)},")
    
    # Update docs/config/languages.json
    try:
        with open('docs/config/languages.json', 'r', encoding='utf-8') as f:
            main_config = json.load(f)
        
        main_config['supported_languages'][language_code] = {
            'name': config['name'],
            'native_name': config['native_name'],
            'flag': config['flag'],
            'direction': 'ltr',
            'voice': config['voice'],
            'country_codes': config['country_codes'],
            'sources': config['sources'],
            'themes': config['themes'],
            'update_time': '07:00',
            'timezone': 'Europe/Berlin' if language_code.startswith('de') else 'Europe/Madrid' if language_code.startswith('es') else 'Europe/Rome',
            'greeting': config['greeting'],
            'service_name': config['service_name']
        }
        
        with open('docs/config/languages.json', 'w', encoding='utf-8') as f:
            json.dump(main_config, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Updated docs/config/languages.json")
        
    except Exception as e:
        print(f"⚠️ Could not update main config: {e}")

def add_language(language_code):
    """Add a new language to the AudioNews service"""
    
    if language_code not in LANGUAGE_CONFIGS:
        print(f"❌ Language {language_code} not supported yet.")
        print(f"Available languages: {', '.join(LANGUAGE_CONFIGS.keys())}")
        return False
    
    config = LANGUAGE_CONFIGS[language_code]
    
    print(f"🌍 Adding {config['native_name']} ({language_code}) to AudioNews...")
    print(f"🎤 Voice: {config['voice']}")
    print(f"📰 Sources: {', '.join(config['sources'].keys())}")
    
    # Create directory structure
    lang_dir = create_language_directory(language_code)
    print(f"📁 Created directory: {lang_dir}")
    
    # Generate HTML page
    html_content = generate_html_page(language_code, config)
    with open(lang_dir / "index.html", 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"📄 Created HTML page: {lang_dir}/index.html")
    
    # Generate manifest
    manifest_content = generate_manifest(language_code, config)
    with open(lang_dir / "manifest.json", 'w', encoding='utf-8') as f:
        f.write(manifest_content)
    print(f"📱 Created PWA manifest: {lang_dir}/manifest.json")
    
    # Update main configuration
    update_main_config(language_code, config)
    
    print(f"\n🎉 {config['native_name']} language added successfully!")
    print(f"🌐 URL: https://audionews.uk/{language_code}/")
    print(f"📝 Next steps:")
    print(f"   1. Update github_ai_news_digest.py with the config shown above")
    print(f"   2. Update root index.html to include {language_code} in redirect logic")
    print(f"   3. Test locally: http://localhost:8081/{language_code}/")
    print(f"   4. Commit and push changes")
    
    return True

def main():
    """Main function with command line interface"""
    parser = argparse.ArgumentParser(description='Add a new language to AudioNews service')
    parser.add_argument('language_code', 
                       nargs='?',
                       choices=list(LANGUAGE_CONFIGS.keys()),
                       help='Language code to add (e.g., de_DE, es_ES, it_IT)')
    parser.add_argument('--list', '-l', action='store_true',
                       help='List available languages')
    
    args = parser.parse_args()
    
    if args.list:
        print("🌍 Available languages to add:")
        for code, config in LANGUAGE_CONFIGS.items():
            print(f"   {code}: {config['flag']} {config['native_name']} ({config['name']})")
        return
    
    if not args.language_code:
        parser.print_help()
        return
    
    success = add_language(args.language_code)
    if not success:
        exit(1)

if __name__ == "__main__":
    main()
