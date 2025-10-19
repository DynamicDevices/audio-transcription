#!/usr/bin/env python3
"""
Fix SEO metadata for non-English language pages.
The issue: Italian/Spanish/Dutch pages have English "UK news" and "Irish voice" in meta tags.
"""

import re
from pathlib import Path

# Language-specific SEO metadata
LANGUAGE_METADATA = {
    'es_ES': {
        'og_title': 'AudioNews España - Resumen Diario de Noticias en Audio for Visually Impaired Users',
        'og_description': 'Voz española profesional ofrece resumen diario de noticias. Diseño accesible mejorado por IA, compartible en WhatsApp. Perfecto para usuarios ciegos y con discapacidad visual. Actualizado diariamente a las 6 AM.',
        'twitter_title': 'AudioNews España - Noticias de Voz Diarias para Accesibilidad',
        'twitter_description': 'Voz española profesional ofrece resumen diario de noticias españolas. Diseño accesible mejorado por IA, compartible en WhatsApp. Perfecto para usuarios con discapacidad visual.',
        'keywords': 'noticias de audio, noticias de voz, resumen diario de noticias, noticias accesibles, noticias para ciegos, noticias para discapacitados visuales, noticias de España en audio, compartir noticias WhatsApp, resumen de noticias IA, Dynamic Devices',
        'service_description': 'Servicio profesional de resumen diario de noticias en audio para usuarios con discapacidad visual, con síntesis de noticias españolas mejorada por IA y tecnología de voz neural española.',
        'website_description': 'Servicio de resumen de noticias de voz diaria que proporciona noticias de audio accesibles para usuarios con discapacidad visual en toda España',
        'voice_description': 'Resumen de noticias diario mejorado por IA entregado con voz española profesional, optimizado para accesibilidad y compartir en WhatsApp'
    },
    'it_IT': {
        'og_title': 'AudioNews Italia - Notiziario Audio Quotidiano for Visually Impaired Users',
        'og_description': 'Voce italiana professionale offre notiziario quotidiano. Design accessibile potenziato dall\'IA, condivisibile su WhatsApp. Perfetto per utenti ciechi e ipovedenti. Aggiornato quotidianamente alle 6:00.',
        'twitter_title': 'AudioNews Italia - Notizie Vocali Quotidiane per l\'Accessibilità',
        'twitter_description': 'Voce italiana professionale offre notiziario quotidiano italiano. Design accessibile potenziato dall\'IA, condivisibile su WhatsApp. Perfetto per utenti ipovedenti.',
        'keywords': 'notizie audio, notizie vocali, notiziario quotidiano, notizie accessibili, notizie per ciechi, notizie per ipovedenti, notizie italiane audio, condivisione notizie WhatsApp, notiziario IA, Dynamic Devices',
        'service_description': 'Servizio professionale di notiziario audio quotidiano per utenti ipovedenti, con sintesi di notizie italiane potenziata dall\'IA e tecnologia vocale neurale italiana.',
        'website_description': 'Servizio di notiziario vocale quotidiano che fornisce notizie audio accessibili per utenti ipovedenti in tutta l\'Italia',
        'voice_description': 'Notiziario quotidiano potenziato dall\'IA fornito con voce italiana professionale, ottimizzato per accessibilità e condivisione su WhatsApp'
    },
    'nl_NL': {
        'og_title': 'AudioNews Nederland - Dagelijks Audio Nieuwsoverzicht for Visually Impaired Users',
        'og_description': 'Professionele Nederlandse stem levert dagelijks nieuwsoverzicht. AI-versterkt, toegankelijk ontwerp, deelbaar via WhatsApp. Perfect voor blinde en slechtziende gebruikers. Dagelijks bijgewerkt om 6:00 uur.',
        'twitter_title': 'AudioNews Nederland - Dagelijkse Gesproken Nieuws voor Toegankelijkheid',
        'twitter_description': 'Professionele Nederlandse stem levert dagelijks Nederlands nieuwsoverzicht. AI-versterkt, toegankelijk ontwerp, deelbaar via WhatsApp. Perfect voor slechtziende gebruikers.',
        'keywords': 'audio nieuws, gesproken nieuws, dagelijks nieuwsoverzicht, toegankelijk nieuws, nieuws voor blinden, nieuws voor slechtzienden, Nederlands audio nieuws, WhatsApp nieuws delen, AI nieuwsoverzicht, Dynamic Devices',
        'service_description': 'Professionele dagelijkse audio nieuwsoverzicht service voor slechtziende gebruikers, met AI-versterkte Nederlandse nieuwssynthese en Nederlandse neurale stem technologie.',
        'website_description': 'Dagelijkse gesproken nieuwsoverzicht service die toegankelijk audio nieuws biedt voor slechtziende gebruikers in heel Nederland',
        'voice_description': 'AI-versterkt dagelijks nieuwsoverzicht geleverd met professionele Nederlandse stem, geoptimaliseerd voor toegankelijkheid en WhatsApp delen'
    }
}

def fix_language_metadata(lang_code):
    """Fix metadata for a specific language page."""
    html_path = Path(f'docs/{lang_code}/index.html')
    
    if not html_path.exists():
        print(f"⚠️  {lang_code}: Page not found, skipping")
        return
    
    metadata = LANGUAGE_METADATA.get(lang_code)
    if not metadata:
        print(f"⚠️  {lang_code}: No metadata defined, skipping")
        return
    
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Fix Open Graph title
    html = re.sub(
        r'<meta property="og:title" content="[^"]*"',
        f'<meta property="og:title" content="{metadata["og_title"]}"',
        html
    )
    
    # Fix Open Graph description
    html = re.sub(
        r'<meta property="og:description" content="[^"]*"',
        f'<meta property="og:description" content="{metadata["og_description"]}"',
        html
    )
    
    # Fix Twitter title
    html = re.sub(
        r'<meta name="twitter:title" content="[^"]*"',
        f'<meta name="twitter:title" content="{metadata["twitter_title"]}"',
        html
    )
    
    # Fix Twitter description
    html = re.sub(
        r'<meta name="twitter:description" content="[^"]*"',
        f'<meta name="twitter:description" content="{metadata["twitter_description"]}"',
        html
    )
    
    # Fix keywords
    html = re.sub(
        r'<meta name="keywords" content="[^"]*"',
        f'<meta name="keywords" content="{metadata["keywords"]}"',
        html
    )
    
    # Fix structured data descriptions
    html = re.sub(
        r'"description": "Professional daily audio news digest service[^"]*"',
        f'"description": "{metadata["service_description"]}"',
        html
    )
    
    html = re.sub(
        r'"description": "Daily voice news digest service providing[^"]*"',
        f'"description": "{metadata["website_description"]}"',
        html
    )
    
    html = re.sub(
        r'"description": "AI-enhanced daily news digest delivered in professional[^"]*"',
        f'"description": "{metadata["voice_description"]}"',
        html
    )
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ {lang_code}: Metadata fixed")

if __name__ == '__main__':
    print("🔧 Fixing language-specific metadata...")
    print()
    
    for lang_code in ['es_ES', 'it_IT', 'nl_NL']:
        fix_language_metadata(lang_code)
    
    print()
    print("✅ All metadata fixes complete!")

