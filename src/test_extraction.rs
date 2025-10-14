use anyhow::Result;
use audio_transcription::article_extractor::ArticleExtractor;

#[tokio::main]
async fn main() -> Result<()> {
    let mut extractor = ArticleExtractor::new();
    let article = extractor.extract("https://www.theguardian.com/world/2025/oct/04/greta-thunberg-israel-gaza-sweden").await?;
    
    println!("=== Article Extraction Test ===");
    println!("Title: {}", article.title);
    println!("Author: {:?}", article.author);
    println!("Published: {:?}", article.published_date);
    println!("Content length: {}", article.content.len());
    println!("First 500 chars: {}", &article.content[..article.content.len().min(500)]);
    
    Ok(())
}
