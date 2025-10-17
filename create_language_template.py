#!/usr/bin/env python3
"""
Create language-specific pages from the master template (en_GB)
Ensures all pages have identical structure with only language-specific content
"""

import os
import re
from datetime import date

def create_language_page(language='fr_FR'):
    """Create a language-specific page based on the English template"""
    
    # Language-specific configuration
    lang_config = {
        'en_GB': {
            'title': 'AudioNews.uk',
            'subtitle': 'Daily Voice News Digest',
            'tagline': 'Brought to you by Dynamic Devices',
            'section_today': "Today's Audio Digest",
            'section_description': 'Updated daily at 6:00 AM UK time',
            'date_title': 'UK News Summary',
            'audio_description': "Today's news digest. Use your browser's audio controls or download for offline listening.",
            'download_button': 'Download MP3',
            'share_button': 'Copy Auto-Play Link',
            'download_help': 'Download MP3 file to your device for WhatsApp sharing or offline listening',
            'share_help': 'Copy link that will automatically start playing when opened - perfect for WhatsApp sharing',
            'recent_heading': 'Recent Digests',
            'recent_description': "Catch up on previous days' news summaries",
            'about_heading': 'About This Service',
            'footer_service': 'AudioNews.uk',
            'footer_by': 'Service by',
            'footer_love': 'Built with ❤️ for accessibility',
            'meta_description_prefix': 'Daily AI-generated audio news digest for',
            'meta_description_suffix': 'brought to you by Dynamic Devices. Professional Irish voice, screen reader optimized.',
            'og_title': 'AudioNews.uk - Daily Voice News Digest for Visually Impaired Users',
            'og_description': 'Professional Irish voice delivers daily UK news digest. AI-enhanced, accessible design, WhatsApp sharing. Perfect for blind and visually impaired users. Updated daily 6AM.',
            'canonical_url': 'https://audionews.uk/en_GB/',
            'locale': 'en_GB',
            'lang_code': 'en',
            'voice_description': 'Irish voice'
        },
        'fr_FR': {
            'title': 'AudioNews France',
            'subtitle': 'Digest Audio Quotidien',
            'tagline': 'Présenté par Dynamic Devices',
            'section_today': "Digest Audio d'Aujourd'hui",
            'section_description': 'Mis à jour quotidiennement à 6h00 (heure du Royaume-Uni)',
            'date_title': 'Résumé des Actualités',
            'audio_description': "Résumé d'actualités d'aujourd'hui. Utilisez les contrôles audio de votre navigateur ou téléchargez pour écouter hors ligne.",
            'download_button': 'Télécharger MP3',
            'share_button': 'Copier le Lien Auto-Play',
            'download_help': 'Téléchargez le fichier MP3 sur votre appareil pour le partager sur WhatsApp ou écouter hors ligne',
            'share_help': 'Copiez le lien qui se lancera automatiquement - parfait pour le partage WhatsApp',
            'recent_heading': 'Digests Récents',
            'recent_description': 'Rattrapez les résumés des jours précédents',
            'about_heading': 'À Propos de ce Service',
            'footer_service': 'AudioNews France',
            'footer_by': 'Service par',
            'footer_love': 'Créé avec ❤️ pour l\'accessibilité',
            'meta_description_prefix': 'Résumé quotidien d\'actualités audio généré par IA pour',
            'meta_description_suffix': 'présenté par Dynamic Devices. Voix française professionnelle, optimisé pour lecteurs d\'écran.',
            'og_title': 'AudioNews France - Digest Audio Quotidien pour Utilisateurs Malvoyants',
            'og_description': 'Voix française professionnelle diffuse un digest d\'actualités quotidien. Synthèse IA, design accessible, partage WhatsApp. Parfait pour les utilisateurs aveugles et malvoyants.',
            'canonical_url': 'https://audionews.uk/fr_FR/',
            'locale': 'fr_FR',
            'lang_code': 'fr',
            'voice_description': 'voix française'
        },
        'de_DE': {
            'title': 'AudioNews Deutschland',
            'subtitle': 'Tägliche Audio-Nachrichtenzusammenfassung',
            'tagline': 'Präsentiert von Dynamic Devices',
            'section_today': 'Heutiger Audio-Digest',
            'section_description': 'Täglich um 6:00 Uhr (UK-Zeit) aktualisiert',
            'date_title': 'Nachrichtenzusammenfassung',
            'audio_description': 'Heutige Nachrichtenzusammenfassung. Verwenden Sie die Audio-Steuerelemente Ihres Browsers oder laden Sie für Offline-Hören herunter.',
            'download_button': 'MP3 Herunterladen',
            'share_button': 'Auto-Play-Link Kopieren',
            'download_help': 'Laden Sie die MP3-Datei auf Ihr Gerät zum WhatsApp-Teilen oder Offline-Hören herunter',
            'share_help': 'Link kopieren, der automatisch abgespielt wird - perfekt zum WhatsApp-Teilen',
            'recent_heading': 'Aktuelle Digests',
            'recent_description': 'Holen Sie die Nachrichtenzusammenfassungen der letzten Tage nach',
            'about_heading': 'Über diesen Service',
            'footer_service': 'AudioNews Deutschland',
            'footer_by': 'Service von',
            'footer_love': 'Mit ❤️ für Barrierefreiheit entwickelt',
            'meta_description_prefix': 'Tägliche KI-generierte Audio-Nachrichtenzusammenfassung für',
            'meta_description_suffix': 'präsentiert von Dynamic Devices. Professionelle deutsche Stimme, für Screenreader optimiert.',
            'og_title': 'AudioNews Deutschland - Täglicher Audio-Nachrichten-Digest für Sehbehinderte',
            'og_description': 'Professionelle deutsche Stimme liefert täglichen Nachrichten-Digest. KI-verstärkt, zugängliches Design, WhatsApp-Sharing. Perfekt für blinde und sehbehinderte Nutzer.',
            'canonical_url': 'https://audionews.uk/de_DE/',
            'locale': 'de_DE',
            'lang_code': 'de',
            'voice_description': 'deutsche Stimme'
        }
    }
    
    if language not in lang_config:
        print(f"❌ Unsupported language: {language}")
        return False
    
    cfg = lang_config[language]
    
    # Read the English template
    template_path = 'docs/en_GB/index.html'
    if not os.path.exists(template_path):
        print(f"❌ Template not found: {template_path}")
        return False
    
    with open(template_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Replace language-specific content
    
    # HTML lang attribute
    html = re.sub(r'<html lang="[^"]*">', f'<html lang="{cfg["lang_code"]}">', html)
    
    # Meta tags
    html = html.replace('AudioNews.uk - Daily Voice News Digest', f'{cfg["title"]} - {cfg["subtitle"]}')
    html = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{cfg["meta_description_prefix"]} {{date}} {cfg["meta_description_suffix"]}">',
        html
    )
    
    # Canonical URL
    html = re.sub(r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{cfg["canonical_url"]}">', html)
    
    # Open Graph
    html = re.sub(r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{cfg["canonical_url"]}">', html)
    html = re.sub(r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{cfg["og_title"]}">', html)
    html = re.sub(r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{cfg["og_description"]}">', html)
    html = re.sub(r'<meta property="og:locale" content="[^"]*">', f'<meta property="og:locale" content="{cfg["locale"]}">', html)
    
    # Twitter Card
    html = re.sub(r'<meta name="twitter:url" content="[^"]*">', f'<meta name="twitter:url" content="{cfg["canonical_url"]}">', html)
    html = re.sub(r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{cfg["title"]}">', html)
    
    # Header
    html = re.sub(
        r'(<h1 class="site-title">.*?<span class="site-icon"[^>]*>📰</span>\s*)AudioNews\.uk',
        f'\\1{cfg["title"]}',
        html,
        flags=re.DOTALL
    )
    html = re.sub(
        r'<p class="site-tagline">Brought to you by Dynamic Devices</p>',
        f'<p class="site-tagline">{cfg["tagline"]}</p>',
        html
    )
    
    # Language selector - update active state
    if language == 'en_GB':
        html = re.sub(
            r'<a href="/en_GB/" class="lang-link"',
            '<a href="/en_GB/" class="lang-link active" aria-current="page"',
            html
        )
    elif language == 'fr_FR':
        html = re.sub(
            r'<a href="/fr_FR/" class="lang-link"',
            '<a href="/fr_FR/" class="lang-link active" aria-current="page"',
            html
        )
        html = re.sub(
            r'<a href="/en_GB/" class="lang-link active" aria-current="page"',
            '<a href="/en_GB/" class="lang-link"',
            html
        )
    elif language == 'de_DE':
        html = re.sub(
            r'<a href="/de_DE/" class="lang-link"',
            '<a href="/de_DE/" class="lang-link active" aria-current="page"',
            html
        )
        html = re.sub(
            r'<a href="/en_GB/" class="lang-link active" aria-current="page"',
            '<a href="/en_GB/" class="lang-link"',
            html
        )
    
    # Main content sections
    html = re.sub(
        r'<span class="section-icon"[^>]*>🎧</span>\s*Today\'s Audio Digest',
        f'<span class="section-icon" aria-hidden="true">🎧</span>\n                    {cfg["section_today"]}',
        html
    )
    html = re.sub(
        r'<p class="section-description">Updated daily at 6:00 AM UK time</p>',
        f'<p class="section-description">{cfg["section_description"]}</p>',
        html
    )
    html = re.sub(
        r'- UK News Summary',
        f'- {cfg["date_title"]}',
        html
    )
    html = re.sub(
        r'Today\'s news digest\. Use your browser\'s audio controls or download for offline listening\.',
        cfg["audio_description"],
        html
    )
    
    # Buttons
    html = re.sub(
        r'(<span class="button-icon"[^>]*>⬇️</span>\s*)Download MP3',
        f'\\1{cfg["download_button"]}',
        html
    )
    html = re.sub(
        r'(<span class="button-icon"[^>]*>📱</span>\s*)Copy Auto-Play Link',
        f'\\1{cfg["share_button"]}',
        html
    )
    
    # Help text
    html = re.sub(
        r'Download MP3 file to your device for WhatsApp sharing or offline listening',
        cfg["download_help"],
        html
    )
    html = re.sub(
        r'Copy link that will automatically start playing when opened - perfect for WhatsApp sharing',
        cfg["share_help"],
        html
    )
    
    # Recent digests section
    html = re.sub(
        r'(<span class="section-icon"[^>]*>📅</span>\s*)Recent Digests',
        f'\\1{cfg["recent_heading"]}',
        html
    )
    html = re.sub(
        r'Catch up on previous days\' news summaries',
        cfg["recent_description"],
        html
    )
    
    # About section (if exists)
    html = re.sub(
        r'About This Service',
        cfg["about_heading"],
        html
    )
    
    # Footer
    html = re.sub(
        r'<strong>AudioNews\.uk</strong> - Service by',
        f'<strong>{cfg["footer_service"]}</strong> - {cfg["footer_by"]}',
        html
    )
    html = re.sub(
        r'Built with ❤️ for accessibility',
        cfg["footer_love"],
        html
    )
    
    # Write the new page
    output_path = f'docs/{language}/index.html'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ Created {language} page: {output_path}")
    return True

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        language = sys.argv[1]
    else:
        print("Usage: python3 create_language_template.py <language>")
        print("Languages: fr_FR, de_DE")
        sys.exit(1)
    
    success = create_language_page(language)
    sys.exit(0 if success else 1)

