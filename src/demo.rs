use anyhow::{Context, Result};
use audio_transcription::{ArticleContent, AudioConfig};
use audio_transcription::article_extractor::ArticleExtractor;
use std::fs::File;
use std::io::Write;
use regex::Regex;

#[tokio::main]
async fn main() -> Result<()> {
    println!("🎧 Audio Transcription Tool - Demo Mode");
    println!("Converting: https://www.theguardian.com/world/2025/oct/04/greta-thunberg-israel-gaza-sweden");
    
    // Step 1: Extract article content
    println!("📖 Extracting article content...");
    let mut extractor = ArticleExtractor::new();
    let article = extractor.extract("https://www.theguardian.com/world/2025/oct/04/greta-thunberg-israel-gaza-sweden")
        .await
        .context("Failed to extract article content")?;
    
    println!("Article title: {}", article.title);
    println!("Content length: {} characters", article.content.len());
    
    // Step 2: Process content for audio (same as the real app)
    let processed_content = process_content_for_audio(&article, 5000)?;
    
    println!("🎙️  Processing content for Irish female voice...");
    println!("📝 Saving processed text (would be converted to audio)...");
    
    // Save the processed content to a text file to show what would be spoken
    let mut file = File::create("demo_article_processed.txt")?;
    file.write_all(processed_content.as_bytes())?;
    
    println!("✅ Demo completed successfully!");
    println!("📄 Processed text saved to: demo_article_processed.txt");
    println!("📊 Duration estimate: ~{:.1} minutes", estimate_duration(&processed_content));
    println!("");
    println!("🎙️  This text would be converted to audio using:");
    println!("   - Service: Azure Cognitive Services");
    println!("   - Voice: en-IE-EmilyNeural (Irish female)");
    println!("   - Rate: 0.9x (natural pace)");
    println!("   - Format: MP3 (WhatsApp compatible)");
    println!("");
    println!("📖 First few sentences of processed content:");
    let sentences: Vec<&str> = processed_content.split(". ").take(3).collect();
    for sentence in sentences {
        println!("   {}", sentence.trim());
    }
    
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
