# Regional Localization: Static Site Strategy

## Architecture Overview

Since GitHub Pages only supports static hosting, we implement regional localization through:

1. **Build-time generation** of regional content
2. **Client-side detection** and routing  
3. **Static file serving** for each region

## Implementation Plan

### Phase 1: Enhanced CI for Regional Generation

```yaml
# .github/workflows/daily-news-digest.yml
- name: 🌍 Generate Regional Content
  run: |
    # Define regional configurations
    REGIONAL_CONFIGS=(
      "en_GB:England:BBC,Guardian,Independent"
      "en_GB_SCT:Scotland:BBC_Scotland,Herald,Scotsman"
      "en_GB_WAL:Wales:BBC_Wales,WalesOnline,WesternMail"
      "es_ES:Spain:ElPais,ElMundo,ABC"
      "es_ES_CAT:Catalonia:LaVanguardia,ElPeriodico,Ara"
    )
    
    for CONFIG in "${REGIONAL_CONFIGS[@]}"; do
      LANG=$(echo $CONFIG | cut -d: -f1)
      REGION=$(echo $CONFIG | cut -d: -f2) 
      SOURCES=$(echo $CONFIG | cut -d: -f3)
      
      echo "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Generating $REGION content ($LANG)"
      python github_ai_news_digest.py \
        --language $LANG \
        --region $REGION \
        --sources $SOURCES
    done
```

### Phase 2: Directory Structure

```
docs/
├── index.html                    # Root redirect page
├── en_GB/                        # General UK
│   ├── index.html
│   ├── audio/
│   └── news_digest_ai_*.txt
├── en_GB_SCT/                    # Scotland
│   ├── index.html
│   ├── audio/
│   └── news_digest_ai_*.txt
├── en_GB_WAL/                    # Wales  
│   ├── index.html
│   ├── audio/
│   └── news_digest_ai_*.txt
├── es_ES_CAT/                    # Catalonia
│   ├── index.html
│   ├── audio/
│   └── news_digest_ai_*.txt
└── shared/                       # Common assets
    ├── css/
    ├── js/
    └── images/
```

### Phase 3: Enhanced Python Configuration

```python
# github_ai_news_digest.py
REGIONAL_CONFIGS = {
    'en_GB_SCT': {
        'name': 'English (Scotland)',
        'native_name': 'English (Scotland)',
        'region': 'Scotland',
        'country': 'GB',
        'sources': {
            'BBC Scotland': {
                'url': 'https://www.bbc.co.uk/news/scotland',
                'selectors': {
                    'headlines': 'h3.gs-c-promo-heading__title',
                    'links': 'a.gs-c-promo-heading'
                }
            },
            'Herald Scotland': {
                'url': 'https://www.heraldscotland.com/',
                'selectors': {
                    'headlines': '.headline',
                    'links': '.headline a'
                }
            }
        },
        'voice': 'en-GB-RyanNeural',
        'greeting': 'Good morning Scotland',
        'themes': [
            'scottish_parliament', 'highlands', 'edinburgh', 'glasgow', 
            'scottish_economy', 'north_sea', 'scottish_culture'
        ],
        'output_dir': 'docs/en_GB_SCT',
        'audio_dir': 'docs/en_GB_SCT/audio',
        'service_name': 'AudioNews Scotland'
    },
    
    'es_ES_CAT': {
        'name': 'Catalan (Catalonia)',
        'native_name': 'Català (Catalunya)', 
        'region': 'Catalonia',
        'country': 'ES',
        'sources': {
            'La Vanguardia': {
                'url': 'https://www.lavanguardia.com/local/barcelona',
                'selectors': {
                    'headlines': '.tit-noticia',
                    'links': '.tit-noticia a'
                }
            }
        },
        'voice': 'ca-ES-JoanaNeural',  # Catalan voice!
        'greeting': 'Bon dia Catalunya',
        'themes': [
            'generalitat', 'barcelona', 'independence', 'catalan_culture',
            'mediterranean', 'tourism', 'fc_barcelona'
        ],
        'output_dir': 'docs/es_ES_CAT',
        'audio_dir': 'docs/es_ES_CAT/audio', 
        'service_name': 'AudioNews Catalunya'
    }
}
```

### Phase 4: Client-Side Regional Detection

```javascript
// docs/index.html (root redirect page)
class RegionalDetector {
    constructor() {
        this.regionalRoutes = {
            'GB': {
                'Scotland': '/en_GB_SCT/',
                'Wales': '/en_GB_WAL/',
                'Northern Ireland': '/en_GB_NIR/',
                'England': '/en_GB/'
            },
            'ES': {
                'Catalonia': '/es_ES_CAT/',
                'Basque Country': '/es_ES_EUS/',
                'Andalusia': '/es_ES_AND/',
                'default': '/es_ES/'
            },
            'FR': {
                'Île-de-France': '/fr_FR_IDF/',  # Paris region
                'Provence-Alpes-Côte d\'Azur': '/fr_FR_PAC/',
                'default': '/fr_FR/'
            }
        };
    }
    
    async detectAndRedirect() {
        try {
            // Check URL parameter first
            const urlParams = new URLSearchParams(window.location.search);
            const forcedLang = urlParams.get('lang');
            if (forcedLang) {
                window.location.href = `/${forcedLang}/`;
                return;
            }
            
            // Check localStorage
            const savedRegion = localStorage.getItem('audioNewsRegion');
            if (savedRegion) {
                window.location.href = `/${savedRegion}/`;
                return;
            }
            
            // Geolocation detection
            const response = await fetch('https://ipapi.co/json/');
            const data = await response.json();
            
            const countryRoutes = this.regionalRoutes[data.country_code];
            if (countryRoutes) {
                const route = countryRoutes[data.region] || countryRoutes.default;
                if (route) {
                    // Save preference
                    const regionCode = route.replace(/\//g, '');
                    localStorage.setItem('audioNewsRegion', regionCode);
                    
                    window.location.href = route;
                    return;
                }
            }
            
            // Default fallback
            window.location.href = '/en_GB/';
            
        } catch (error) {
            console.log('Regional detection failed, using default');
            window.location.href = '/en_GB/';
        }
    }
}

// Auto-redirect on page load
new RegionalDetector().detectAndRedirect();
```

### Phase 5: Regional Content Generation

```python
def get_regional_sources(self, region_code):
    """Get news sources specific to the region"""
    config = REGIONAL_CONFIGS.get(region_code, REGIONAL_CONFIGS['en_GB'])
    
    sources = {}
    for name, source_config in config['sources'].items():
        sources[name] = source_config['url']
    
    return sources

def get_regional_selectors(self, region_code):
    """Get CSS selectors optimized for regional news sites"""
    config = REGIONAL_CONFIGS.get(region_code, REGIONAL_CONFIGS['en_GB'])
    
    selectors = {}
    for name, source_config in config['sources'].items():
        selectors[name] = source_config['selectors']
    
    return selectors

def get_regional_synthesis_prompt(self, region_code):
    """Get AI prompt tailored to regional context"""
    config = REGIONAL_CONFIGS[region_code]
    
    return f"""
    You are creating a news digest for {config['region']} in {config['name']}.
    
    Focus on themes relevant to {config['region']}:
    {', '.join(config['themes'])}
    
    Regional context:
    - Local politics and governance
    - Regional economy and business
    - Cultural events and traditions
    - Geographic and environmental issues specific to {config['region']}
    
    Greeting: "{config['greeting']}"
    Service: "{config['service_name']}"
    
    Create a natural, engaging summary that feels locally relevant.
    """
```

## Benefits of This Approach

### ✅ Advantages
- **Static hosting compatible** - works with GitHub Pages
- **Fast performance** - pre-generated content, no server processing
- **SEO friendly** - separate URLs for each region
- **Offline capable** - static files can be cached
- **Cost effective** - no server costs, just GitHub Pages

### ⚠️ Considerations  
- **Build time increases** - more regions = longer CI
- **Storage usage** - multiple copies of similar content
- **Maintenance complexity** - more configurations to manage
- **Content synchronization** - ensuring consistency across regions

## Implementation Priority

### Phase 1: UK Regions (Immediate)
- Scotland (`en_GB_SCT`)
- Wales (`en_GB_WAL`) 
- Northern Ireland (`en_GB_NIR`)

### Phase 2: Spanish Regions
- Catalonia (`es_ES_CAT`)
- Basque Country (`es_ES_EUS`)

### Phase 3: Other European Regions
- Bavaria (`de_DE_BAY`)
- Île-de-France (`fr_FR_IDF`)

This approach gives us true regional localization while working within GitHub Pages' static hosting constraints.
