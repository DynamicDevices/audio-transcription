# Daily Voice News - Professional Audio News for Visually Impaired Users

**Brought to you by Dynamic Devices**

## 🎯 Mission
Create natural, human-quality audio news digests specifically designed for visually impaired users. This project synthesizes information from multiple UK news sources to create original, accessible audio content that respects copyright while providing valuable accessibility services.

## 🎧 **Live Service**

📱 **Website**: [https://audionews.uk](https://audionews.uk)

- 🕕 **Updated daily** at 6:00 AM UK time (BST/GMT)
- 🎵 **Auto-play sharing** via `?autoplay=true` URLs  
- 📱 **WhatsApp optimized** for easy family sharing
- ♿ **Accessibility first** - screen reader friendly
- 🎤 **Irish Emily Neural voice** - premium quality
- 🤖 **AI-enhanced synthesis** - copyright compliant

## ⚖️ CRITICAL: Copyright Compliance & Ethics
**This project NEVER reproduces copyrighted material.** Instead, it operates under strict ethical guidelines:

- ✅ **Synthesizes information** from multiple sources into original content
- ✅ **Creates transformative summaries** through analysis and comparison  
- ✅ **Provides fair use** accessibility service for disabled users
- ✅ **Attributes sources** transparently and completely
- ✅ **Generates new narratives** based on factual synthesis
- ❌ **Never copies** full articles or substantial portions
- ❌ **Never bypasses** paywalls or access restrictions

**📋 See `COPYRIGHT_AND_ETHICS.md` for complete legal and ethical framework.**

## 📁 Project Structure

```
daily-voice-news/
├── 📄 github_ai_news_digest.py    # Main AI digest generator
├── 📄 create_premium_edge_audio.py # Single article processor
├── 📄 update_website.py            # Dynamic website updates
├── 🌐 docs/                        # GitHub Pages website
│   ├── index.html                  # Accessible newspaper layout
│   ├── css/newspaper.css           # Mobile-first styling
│   ├── js/accessibility.js         # Screen reader enhancements
│   └── audio/                      # Generated MP3 files
├── 🤖 .github/workflows/           # Automated CI/CD
│   └── daily-news-digest.yml       # Daily generation workflow
├── 📋 requirements.txt             # Python dependencies
└── 📚 docs/                        # Documentation
    ├── COPYRIGHT_AND_ETHICS.md     # Legal framework
    └── GITHUB_ACTIONS_SETUP.md     # CI/CD instructions
```

## 🚀 **Key Features**

### **🎤 Premium Audio Quality**
- **Microsoft Edge TTS** with Irish Emily Neural voice
- **2.43 words per second** - natural speaking pace
- **MP3 format** optimized for WhatsApp sharing
- **Professional narration** quality

### **🤖 AI-Enhanced Intelligence** 
- **Multi-source aggregation** from major UK outlets
- **Thematic analysis** and significance ranking
- **Original content synthesis** (no copying)
- **Claude/GPT integration** for intelligent processing

### **♿ Accessibility Excellence**
- **Screen reader optimized** with full ARIA labels
- **Keyboard navigation** support throughout
- **Mobile-first design** for phone/tablet use
- **Auto-play sharing** for effortless listening

### **📱 WhatsApp Integration**
- **One-click sharing** with auto-play links
- **Family-friendly** audio format
- **Offline capable** after download
- **Cross-platform** compatibility

## 🛠️ **Technical Implementation**

### **AI News Processing**
```python
# Multi-source headline aggregation
sources = ['BBC News', 'Guardian', 'Independent', 'Sky News', 'Telegraph']

# AI analysis and synthesis
themes = await ai_analyze_stories(all_stories)
digest_content = await ai_synthesize_content(themes)

# Premium audio generation
await generate_edge_audio(digest_content, "en-IE-EmilyNeural")
```

### **GitHub Actions Automation**
- **Daily execution** at 6:00 AM UK time
- **AI API integration** (OpenAI/Anthropic)
- **Website deployment** to GitHub Pages
- **Audio file management** and archival

### **Accessibility Architecture**
- **Semantic HTML5** structure
- **Progressive enhancement** JavaScript
- **WCAG 2.1 AA compliance**
- **Service Worker** for offline functionality

## 🔧 **Setup & Development**

### **Local Development**
```bash
# Clone repository
git clone https://github.com/DynamicDevices/daily-voice-news.git
cd daily-voice-news

# Install dependencies
pip install -r requirements.txt

# Generate today's digest
python github_ai_news_digest.py

# Update website
python update_website.py
```

### **GitHub Actions Setup**
1. **Enable GitHub Pages** in repository settings
2. **Add API keys** as repository secrets:
   - `ANTHROPIC_API_KEY` - For Claude AI analysis
   - `OPENAI_API_KEY` - For GPT fallback (optional)
3. **Workflow runs automatically** daily at 6 AM UTC

## 📊 **Performance Metrics**

### **Audio Quality Breakthrough**
- **gTTS Problems**: 13-14% pause time, 1.90 WPS, basic synthesis
- **Edge TTS Solution**: <2% pause time, 2.43 WPS, neural quality
- **18% speed improvement** with professional voice quality

### **Accessibility Impact**
- **Screen reader optimized** for blind/partially sighted users
- **WhatsApp sharing** enables family support networks  
- **Daily consistency** builds reliable news routine at 6 AM UK time
- **Zero cost** accessibility service

## 🏆 **Engineering Achievements**

1. **Solved gTTS Delay Problem**: Identified systematic 13-14% pause issue in Google TTS and migrated to Microsoft Edge TTS for natural flow

2. **Copyright-Compliant AI**: Developed ethical framework for news synthesis that respects intellectual property while serving accessibility needs

3. **Auto-Play Sharing**: Implemented `?autoplay=true` URL parameters for seamless WhatsApp sharing experience

4. **Accessibility Excellence**: Full WCAG 2.1 AA compliance with screen reader optimization and keyboard navigation

5. **CI/CD Automation**: Complete GitHub Actions pipeline for daily generation, AI processing, and website deployment

## 🎯 **For Visually Impaired Users**

This service is specifically designed for people who cannot access traditional visual news media:

- **🎧 Immediate listening** - no navigation required
- **📱 Easy sharing** - family can send via WhatsApp  
- **♿ Screen reader friendly** - works with JAWS, NVDA, VoiceOver
- **⌨️ Keyboard accessible** - no mouse required
- **🔄 Consistent schedule** - reliable daily updates at 6 AM UK time

## 📞 **Support & Contact**

- **🌐 Live Service**: [https://audionews.uk](https://audionews.uk)
- **📧 Issues**: [GitHub Issues](https://github.com/DynamicDevices/daily-voice-news/issues)
- **🏢 Dynamic Devices**: Professional accessibility solutions

---

**© 2025 Dynamic Devices • Open Source • Made with ♿ accessibility in mind**