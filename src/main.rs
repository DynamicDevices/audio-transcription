use anyhow::{Context, Result};
use clap::Parser;
use std::path::PathBuf;

use audio_transcription::{ArticleContent, AudioConfig};
use audio_transcription::article_extractor::ArticleExtractor;
use audio_transcription::tts_service::TTSService;
use audio_transcription::audio_processor::AudioProcessor;

#[derive(Parser, Debug)]
#[command(author, version, about = "Convert web articles to high-quality audio for accessibility")]
struct Args {
    /// URL of the article to convert
    #[arg(short, long)]
    url: String,
    
    /// Output file path (default: auto-generated)
    #[arg(short, long)]
    output: Option<PathBuf>,
    
    /// TTS service to use (azure, google, or local)
    #[arg(short, long, default_value = "azure")]
    service: String,
    
    /// Voice name/ID (service-specific)
    #[arg(short, long, default_value = "en-IE-EmilyNeural")]
    voice: String,
    
    /// Speaking rate (0.5 to 2.0)
    #[arg(short, long, default_value = "0.9")]
    rate: f32,
    
    /// Maximum article length in characters (for conciseness)
    #[arg(short, long, default_value = "5000")]
    max_length: usize,
    
    /// Verbose output
    #[arg(long)]
    verbose: bool,
}

#[tokio::main]
async fn main() -> Result<()> {
    let args = Args::parse();
    
    if args.verbose {
        env_logger::init();
    }
    
    println!("🎧 Audio Transcription Tool for Accessibility");
    println!("Converting: {}", args.url);
    
    // Step 1: Extract article content
    println!("📖 Extracting article content...");
    let mut extractor = ArticleExtractor::new();
    let article = extractor.extract(&args.url)
        .await
        .context("Failed to extract article content")?;
    
    if args.verbose {
        println!("Article title: {}", article.title);
        println!("Content length: {} characters", article.content.len());
    }
    
    // Step 2: Process and optimize content for audio
    let processed_content = process_content_for_audio(&article, args.max_length)?;
    
    // Step 3: Configure TTS
    let mut audio_config = AudioConfig::default();
    audio_config.voice_name = args.voice;
    audio_config.speaking_rate = args.rate;
    
    // Step 4: Generate audio
    println!("🎙️  Generating audio with Irish female voice...");
    let tts_service = TTSService::new(&args.service, &audio_config)?;
    let audio_data = tts_service.synthesize_speech(&processed_content)
        .await
        .context("Failed to generate speech")?;
    
    // Step 5: Process and save audio
    println!("💾 Processing and saving audio...");
    let output_path = args.output.unwrap_or_else(|| {
        let filename = format!("article_{}.mp3", uuid::Uuid::new_v4().simple());
        PathBuf::from(filename)
    });
    
    let audio_processor = AudioProcessor::new();
    audio_processor.save_optimized_audio(&audio_data, &output_path, &audio_config)
        .context("Failed to save audio file")?;
    
    println!("✅ Audio file created successfully!");
    println!("📱 File: {} (optimized for WhatsApp)", output_path.display());
    println!("📊 Duration: ~{:.1} minutes", estimate_duration(&processed_content));
    
    Ok(())
}

fn process_content_for_audio(article: &ArticleContent, max_length: usize) -> Result<String> {
    let mut content = format!("Article: {}\n\n", article.title);
    
    if let Some(author) = &article.author {
        content.push_str(&format!("By {}\n\n", author));
    }
    
    if let Some(date) = &article.published_date {
        content.push_str(&format!("Published {}\n\n", date));
    }
    
    // Clean up the article content for better speech synthesis
    let cleaned_content = clean_text_for_speech(&article.content);
    
    // Truncate if too long, but try to end at sentence boundaries
    if cleaned_content.len() > max_length {
        content.push_str(&truncate_at_sentence(&cleaned_content, max_length));
        content.push_str("\n\nThis article has been shortened for audio. The full version is available at the original link.");
    } else {
        content.push_str(&cleaned_content);
    }
    
    Ok(content)
}

fn clean_text_for_speech(text: &str) -> String {
    use regex::Regex;
    
    let mut cleaned = text.to_string();
    
    // Remove or replace problematic characters/patterns for TTS
    let patterns = vec![
        (Regex::new(r"https?://[^\s]+").unwrap(), ""), // Remove URLs
        (Regex::new(r"\s+").unwrap(), " "), // Normalize whitespace
        (Regex::new(r#"["""]"#).unwrap(), "\""), // Normalize smart quotes
        (Regex::new(r#"[''']"#).unwrap(), "'"), // Normalize smart apostrophes
        (Regex::new(r"–|—").unwrap(), " - "), // Replace em/en dashes
        (Regex::new(r"\n\s*\n").unwrap(), "\n\n"), // Normalize paragraphs
    ];
    
    for (pattern, replacement) in patterns {
        cleaned = pattern.replace_all(&cleaned, replacement).to_string();
    }
    
    cleaned.trim().to_string()
}

fn truncate_at_sentence(text: &str, max_length: usize) -> String {
    if text.len() <= max_length {
        return text.to_string();
    }
    
    // Find the last sentence ending before max_length
    let truncated = &text[..max_length];
    if let Some(pos) = truncated.rfind(". ") {
        format!("{}.", &truncated[..pos])
    } else if let Some(pos) = truncated.rfind("! ") {
        format!("{}!", &truncated[..pos])
    } else if let Some(pos) = truncated.rfind("? ") {
        format!("{}?", &truncated[..pos])
    } else {
        // Fallback: find last space
        if let Some(pos) = truncated.rfind(' ') {
            format!("{}...", &truncated[..pos])
        } else {
            format!("{}...", truncated)
        }
    }
}

fn estimate_duration(text: &str) -> f32 {
    // Rough estimate: ~150-200 words per minute for clear speech
    let word_count = text.split_whitespace().count() as f32;
    word_count / 175.0 // Conservative estimate
}
