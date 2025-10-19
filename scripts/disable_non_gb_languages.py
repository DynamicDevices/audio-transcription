#!/usr/bin/env python3
"""
Temporarily disable non-GB languages by greying out their buttons and adding "Coming Soon"
"""

import re
from pathlib import Path

def disable_languages_in_html(html_path):
    """Update HTML to grey out non-GB language buttons."""
    
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Add CSS for disabled language links (if not already present)
    disabled_css = """
        .lang-link.disabled {
            opacity: 0.4;
            cursor: not-allowed;
            pointer-events: none;
            text-decoration: line-through;
        }
        
        .lang-link.disabled:hover {
            transform: none;
            background: rgba(255, 255, 255, 0.1);
        }"""
    
    # Check if disabled CSS already exists
    if '.lang-link.disabled' not in html:
        # Insert before closing </style> tag
        html = re.sub(
            r'(</style>)',
            disabled_css + '\n    \\1',
            html,
            count=1
        )
    
    # Update French link
    html = re.sub(
        r'<a href="/fr_FR/" class="lang-link"([^>]*?)title="Français">🇫🇷 Français</a>',
        r'<a href="/fr_FR/" class="lang-link disabled"\1title="Français (Coming Soon)">🇫🇷 Français <small>(Coming Soon)</small></a>',
        html
    )
    
    # Update German link
    html = re.sub(
        r'<a href="/de_DE/" class="lang-link"([^>]*?)title="Deutsch">🇩🇪 Deutsch</a>',
        r'<a href="/de_DE/" class="lang-link disabled"\1title="Deutsch (Coming Soon)">🇩🇪 Deutsch <small>(Coming Soon)</small></a>',
        html
    )
    
    # Update Spanish link
    html = re.sub(
        r'<a href="/es_ES/" class="lang-link"([^>]*?)title="Español">🇪🇸 Español</a>',
        r'<a href="/es_ES/" class="lang-link disabled"\1title="Español (Coming Soon)">🇪🇸 Español <small>(Coming Soon)</small></a>',
        html
    )
    
    # Update Italian link
    html = re.sub(
        r'<a href="/it_IT/" class="lang-link"([^>]*?)title="Italiano">🇮🇹 Italiano</a>',
        r'<a href="/it_IT/" class="lang-link disabled"\1title="Italiano (Coming Soon)">🇮🇹 Italiano <small>(Coming Soon)</small></a>',
        html
    )
    
    # Update Dutch link
    html = re.sub(
        r'<a href="/nl_NL/" class="lang-link"([^>]*?)title="Nederlands">🇳🇱 Nederlands</a>',
        r'<a href="/nl_NL/" class="lang-link disabled"\1title="Nederlands (Coming Soon)">🇳🇱 Nederlands <small>(Coming Soon)</small></a>',
        html
    )
    
    # Update London link
    html = re.sub(
        r'<a href="/en_GB_LON/" class="lang-link"([^>]*?)title="London">🏴󠁧󠁢󠁥󠁮󠁧󠁿 London</a>',
        r'<a href="/en_GB_LON/" class="lang-link disabled"\1title="London (Coming Soon)">🏴󠁧󠁢󠁥󠁮󠁧󠁿 London <small>(Coming Soon)</small></a>',
        html
    )
    
    # Update Liverpool link
    html = re.sub(
        r'<a href="/en_GB_LIV/" class="lang-link"([^>]*?)title="Liverpool">🏴󠁧󠁢󠁥󠁮󠁧󠁿 Liverpool</a>',
        r'<a href="/en_GB_LIV/" class="lang-link disabled"\1title="Liverpool (Coming Soon)">🏴󠁧󠁢󠁥󠁮󠁧󠁿 Liverpool <small>(Coming Soon)</small></a>',
        html
    )
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return True

def main():
    print("🔧 Disabling non-GB languages...")
    print()
    
    # Update all language pages
    language_pages = [
        'docs/en_GB/index.html',
        'docs/fr_FR/index.html',
        'docs/de_DE/index.html',
        'docs/es_ES/index.html',
        'docs/it_IT/index.html',
        'docs/nl_NL/index.html',
        'docs/index.html'  # Main page
    ]
    
    for page_path in language_pages:
        path = Path(page_path)
        if path.exists():
            disable_languages_in_html(path)
            print(f"✅ Updated: {page_path}")
        else:
            print(f"⚠️  Skipped (not found): {page_path}")
    
    print()
    print("✅ All pages updated - non-GB languages now greyed out")
    print("💡 Only en_GB will be generated in CI")

if __name__ == '__main__':
    main()

