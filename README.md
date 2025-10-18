# AudioNews - AI-Powered News Digests for Accessibility

[![CI/CD](https://github.com/DynamicDevices/daily-voice-news/actions/workflows/daily-news-digest.yml/badge.svg)](https://github.com/DynamicDevices/daily-voice-news/actions/workflows/daily-news-digest.yml)
[![Release](https://img.shields.io/github/v/release/DynamicDevices/daily-voice-news)](https://github.com/DynamicDevices/daily-voice-news/releases/latest)
[![Live](https://img.shields.io/badge/Live-AudioNews.uk-success)](https://audionews.uk)
[![WCAG 2.1 AA](https://img.shields.io/badge/WCAG%202.1-AA-blue)](https://audionews.uk)

**Professional audio news service for visually impaired users • 8 languages • Daily updates • Zero cost**

🌐 **[audionews.uk](https://audionews.uk)** • Updated daily at 6 AM UK time

---

## 🎯 What It Does

Converts news headlines into natural-sounding audio digests using AI analysis and Microsoft Edge TTS. Designed specifically for visually impaired users who need accessible news content.

### Key Features

- **8 Languages**: English (UK/London/Liverpool), French, German, Spanish, Italian, Dutch
- **AI-Enhanced**: Claude 4.5 Sonnet analyzes and synthesizes content from multiple sources
- **Premium Voices**: Natural neural voices via Microsoft Edge TTS
- **Accessible**: WCAG 2.1 AA compliant, screen reader optimized
- **Automated**: GitHub Actions generates and deploys daily
- **Copyright Compliant**: Synthesizes original summaries, never copies articles

## 📁 Project Structure

```
audio-transcription/
├── scripts/              # Python scripts
│   ├── github_ai_news_digest.py      # Main generator
│   ├── update_website.py             # Website updater
│   ├── update_language_website.py    # Language page updater
│   ├── create_all_language_pages.py  # Page generator
│   └── add_language.py               # Add new language
├── config/               # Configuration
│   ├── ai_prompts.json               # AI prompts & model settings
│   ├── voice_config.json             # Voice & TTS settings
│   └── README.md                     # Config documentation
├── docs/                 # GitHub Pages website
│   ├── en_GB/, fr_FR/, de_DE/, ...  # Language pages
│   ├── shared/                       # Shared assets
│   └── index.html                    # Main entry
├── templates/            # HTML templates
├── archive/              # Old/unused files
└── .github/workflows/    # CI/CD automation
```

## 🚀 Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Generate digest for English
python scripts/github_ai_news_digest.py --language en_GB

# Update website
python scripts/update_website.py
```

### GitHub Actions Setup

1. Enable GitHub Pages (source: `main` branch, `/docs` folder)
2. Add secret: `ANTHROPIC_API_KEY`
3. Workflow runs automatically daily at 5:00 UTC (6:00 AM UK)

## 🔧 Configuration

AI prompts and voice settings are externalized to JSON files for easy updates:

- **`config/ai_prompts.json`**: System messages, analysis/synthesis prompts, model settings
- **`config/voice_config.json`**: Voice configurations, TTS settings, retry logic

See [`config/README.md`](config/README.md) for detailed documentation.

## 🍴 Forking & Customization

Want to create your own customized news service? Here's how:

### 1. Fork the Repository

Click the **Fork** button at the top of this page to create your own copy.

### 2. Set Up Secrets

In your fork, go to **Settings → Secrets and variables → Actions** and add:

```
ANTHROPIC_API_KEY = your_anthropic_api_key_here
```

Get your API key from [Anthropic Console](https://console.anthropic.com/).

### 3. Customize AI Prompts

Edit `config/ai_prompts.json` to change:
- System messages (tone, style, instructions)
- Analysis prompts (how stories are categorized)
- Synthesis prompts (how summaries are generated)
- AI model settings (temperature, max tokens)

### 4. Customize Voices

Edit `config/voice_config.json` to:
- Change voices (browse [Microsoft Edge TTS voices](https://speech.microsoft.com/portal/voicegallery))
- Adjust retry logic
- Configure TTS settings

### 5. Customize News Sources

Edit `scripts/github_ai_news_digest.py`:
- Modify `LANGUAGE_CONFIGS` to add/change news sources
- Change greetings, themes, or output directories

### 6. Enable GitHub Pages

1. Go to **Settings → Pages**
2. Set **Source** to `main` branch, `/docs` folder
3. Set custom domain (optional)

### 7. Test Your Changes

```bash
# Test locally first
python scripts/github_ai_news_digest.py --language en_GB

# Check the generated files
ls docs/en_GB/audio/
```

### 8. Deploy

Push to `main` branch - GitHub Actions will automatically:
- Generate daily digests at 5:00 UTC
- Deploy to GitHub Pages
- Store audio files in Git LFS

## 🤝 Contributing

**Pull requests are gratefully appreciated!** Help improve this project:

### Areas for Contribution

- 🌍 **New languages** - Add support for more regions
- 🎤 **Voice improvements** - Better voice selection or quality
- 🤖 **AI enhancements** - Improved prompts or analysis
- ♿ **Accessibility** - Better screen reader support
- 🎨 **UI/UX** - Design improvements
- 📚 **Documentation** - Clearer guides
- 🐛 **Bug fixes** - Report or fix issues

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit with clear messages (`git commit -m '✨ Add amazing feature'`)
6. Push to your fork (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Contribution Guidelines

- Keep accessibility as the top priority
- Maintain copyright compliance
- Test changes locally before submitting
- Document new features in README or config files
- Follow existing code style
- Add comments for complex logic

**All contributions, big or small, are valued and appreciated!** 🙏

## ⚖️ Copyright & Ethics

This service synthesizes original content from multiple news sources:

✅ Creates transformative summaries through AI analysis  
✅ Provides accessibility service for disabled users (fair use)  
✅ Never copies substantial portions of articles  
✅ Respects paywalls and access restrictions  

See [`docs/COPYRIGHT_AND_ETHICS.md`](docs/COPYRIGHT_AND_ETHICS.md) for complete legal framework.

## 🌍 Adding New Languages

1. Add voice configuration to `config/voice_config.json`
2. Add AI prompts to `config/ai_prompts.json`
3. Add language config to `scripts/github_ai_news_digest.py`
4. Run `python scripts/create_all_language_pages.py`

## 📊 Tech Stack

- **AI**: Anthropic Claude 4.5 Sonnet
- **TTS**: Microsoft Edge TTS (neural voices)
- **CI/CD**: GitHub Actions
- **Hosting**: GitHub Pages
- **Storage**: Git LFS for audio files
- **PWA**: Service Worker + manifest

## 📞 Support

- **Live Service**: [audionews.uk](https://audionews.uk)
- **Issues**: [GitHub Issues](https://github.com/DynamicDevices/daily-voice-news/issues)
- **Organization**: [Dynamic Devices](https://github.com/DynamicDevices)

---

**© 2025 Dynamic Devices • Open Source • Made with ♿ accessibility in mind**
