# Configuration Files

This directory contains JSON configuration files that control AI prompts and voice settings for the AudioNews service.

## Files

### `ai_prompts.json`
Controls all AI-related prompts and model settings.

**Structure:**
- `system_messages`: Language-specific system messages for the AI (instructions for accessible content creation)
- `analysis_prompt`: Configuration for news story analysis and categorization
  - `template`: The prompt template for analyzing headlines
  - `system_instruction`: Wrapper instruction emphasizing duplicate elimination
  - `region_names`: Language-specific region names (e.g., "UK", "French", "German")
- `synthesis_prompts`: Language-specific prompts for generating audio content
  - Each language has a `template` field with placeholders for `{theme}` and `{headlines}`
  - Each language has a `max_words` field (currently 80 for all languages)
- `ai_model`: Claude model configuration
  - `name`: Model identifier (e.g., "claude-sonnet-4-5-20250929")
  - `analysis_max_tokens`: Max tokens for story analysis (1500)
  - `analysis_temperature`: Temperature for analysis (0.1 for consistency)
  - `synthesis_max_tokens`: Max tokens for content synthesis (300)
  - `synthesis_temperature`: Temperature for synthesis (0.4 for creativity)

**Supported Languages:**
- `en_GB`: English (UK)
- `en_GB_LON`: English (London)
- `en_GB_LIV`: English (Liverpool)
- `fr_FR`: French (France)
- `de_DE`: German (Germany)
- `es_ES`: Spanish (Spain)
- `it_IT`: Italian (Italy)
- `nl_NL`: Dutch (Netherlands)

### `voice_config.json`
Controls voice settings and TTS configuration.

**Structure:**
- `voices`: Language-specific voice configurations
  - `name`: Edge TTS voice identifier (e.g., "en-IE-EmilyNeural")
  - `display_name`: Human-readable voice name
  - `language`: Language description
  - `gender`: Voice gender
  - `provider`: TTS provider (currently "Edge TTS")
- `tts_settings`: Edge TTS connection settings
  - `edge_tts`:
    - `max_retries`: Number of retry attempts (5)
    - `initial_retry_delay`: Initial delay in seconds (5)
    - `retry_backoff_multiplier`: Backoff multiplier for exponential delay (1.5)
    - `force_ipv4`: Force IPv4 connections for GitHub Actions compatibility (true)
    - `ssl_verify`: SSL certificate verification (true)
  - `fallback`:
    - `enabled`: Whether fallback is enabled (false)
    - `provider`: Fallback provider if Edge TTS fails ("google_tts")
- `audio_settings`: Audio file settings
  - `format`: Audio format ("mp3")
  - `quality`: Quality level ("high")
  - `estimated_words_per_second`: Speech rate estimation (2.0)
  - `min_file_size_kb`: Minimum acceptable file size (100)

## Usage

These configuration files are automatically loaded when `github_ai_news_digest.py` is imported:

```python
from github_ai_news_digest import AI_PROMPTS_CONFIG, VOICE_CONFIG
```

## Editing Guidelines

### Adding a New Language

1. **In `ai_prompts.json`:**
   - Add system message to `system_messages` object
   - Add region name to `analysis_prompt.region_names`
   - Add synthesis prompt template to `synthesis_prompts`

2. **In `voice_config.json`:**
   - Add voice configuration to `voices` object with appropriate Edge TTS voice

3. **In `github_ai_news_digest.py`:**
   - Add language configuration to `LANGUAGE_CONFIGS` dictionary

### Changing AI Model

Update the `ai_model` section in `ai_prompts.json`:
```json
{
  "ai_model": {
    "name": "claude-sonnet-4-5-20250929",
    "analysis_max_tokens": 1500,
    "analysis_temperature": 0.1,
    "synthesis_max_tokens": 300,
    "synthesis_temperature": 0.4
  }
}
```

### Changing Voice

Update the voice name in `voice_config.json`:
```json
{
  "voices": {
    "en_GB": {
      "name": "en-IE-EmilyNeural",
      ...
    }
  }
}
```

Available Edge TTS voices: https://speech.microsoft.com/portal/voicegallery

### Adjusting Retry Logic

Update `tts_settings.edge_tts` in `voice_config.json`:
```json
{
  "tts_settings": {
    "edge_tts": {
      "max_retries": 5,
      "initial_retry_delay": 5,
      "retry_backoff_multiplier": 1.5
    }
  }
}
```

## Testing Changes

After editing configuration files, test that they load correctly:

```bash
python3 -c "from github_ai_news_digest import AI_PROMPTS_CONFIG, VOICE_CONFIG; print('✅ Config loaded')"
```

## Version Control

Always commit configuration changes with clear descriptions:
```bash
git add config/
git commit -m "🔧 Update AI prompts for better synthesis" 
```

