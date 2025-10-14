use anyhow::{Context, Result};
use reqwest::Client;
use scraper::{Html, Selector};
use url::Url;

use crate::ArticleContent;

pub struct ArticleExtractor {
    client: Client,
}

impl ArticleExtractor {
    pub fn new() -> Self {
        let client = Client::builder()
            .user_agent("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
            .build()
            .expect("Failed to create HTTP client");
        
        Self { client }
    }
    
    pub async fn extract(&mut self, url: &str) -> Result<ArticleContent> {
        let _parsed_url = Url::parse(url)
            .context("Invalid URL provided")?;
        
        let html = self.fetch_html(url).await?;
        let document = Html::parse_document(&html);
        
        // Try multiple extraction strategies based on the website
        let content = if url.contains("theguardian.com") {
            self.extract_guardian_article(&document, url)?
        } else if url.contains("bbc.co.uk") || url.contains("bbc.com") {
            self.extract_bbc_article(&document, url)?
        } else if url.contains("nytimes.com") {
            self.extract_nytimes_article(&document, url)?
        } else {
            // Generic extraction for other sites
            self.extract_generic_article(&document, url)?
        };
        
        Ok(content)
    }
    
    async fn fetch_html(&self, url: &str) -> Result<String> {
        let response = self.client
            .get(url)
            .send()
            .await
            .context("Failed to fetch URL")?;
        
        if !response.status().is_success() {
            return Err(anyhow::anyhow!("HTTP error: {}", response.status()));
        }
        
        let html = response
            .text()
            .await
            .context("Failed to read response body")?;
        
        Ok(html)
    }
    
    fn extract_guardian_article(&self, document: &Html, url: &str) -> Result<ArticleContent> {
        // Guardian-specific selectors - updated for current Guardian layout
        let title_selector = Selector::parse("h1[data-gu-name='headline'], h1.content__headline, h1")
            .map_err(|e| anyhow::anyhow!("Invalid selector: {:?}", e))?;
        
        let author_selector = Selector::parse("a[rel='author'], .byline a, .contributor-full-name")
            .map_err(|e| anyhow::anyhow!("Invalid selector: {:?}", e))?;
        
        let date_selector = Selector::parse("time[datetime], .content__dateline time")
            .map_err(|e| anyhow::anyhow!("Invalid selector: {:?}", e))?;
        
        let content_selector = Selector::parse(".content__article-body p, .article-body-commercial-selector p, [data-gu-name='body'] p")
            .map_err(|e| anyhow::anyhow!("Invalid selector: {:?}", e))?;
        
        // Extract title
        let title = document
            .select(&title_selector)
            .next()
            .map(|el| el.text().collect::<String>().trim().to_string())
            .unwrap_or_else(|| "Untitled Article".to_string());
        
        // Extract author
        let author = document
            .select(&author_selector)
            .next()
            .map(|el| el.text().collect::<String>().trim().to_string())
            .filter(|s| !s.is_empty());
        
        // Extract publication date
        let published_date = document
            .select(&date_selector)
            .next()
            .and_then(|el| el.value().attr("datetime").or_else(|| el.text().collect::<Vec<_>>().first().copied()))
            .map(|s| s.trim().to_string())
            .filter(|s| !s.is_empty());
        
        // Extract content paragraphs
        let content_paragraphs: Vec<String> = document
            .select(&content_selector)
            .map(|el| {
                let text = el.text().collect::<String>();
                text.trim().to_string()
            })
            .filter(|p| !p.is_empty() && p.len() > 10) // Filter out very short paragraphs
            .collect();
        
        let content = content_paragraphs.join("\n\n");
        
        if content.is_empty() {
            return Err(anyhow::anyhow!("No article content found"));
        }
        
        Ok(ArticleContent {
            title,
            author,
            published_date,
            content,
            summary: None,
            url: url.to_string(),
        })
    }
    
    fn extract_bbc_article(&self, document: &Html, url: &str) -> Result<ArticleContent> {
        let title_selector = Selector::parse("h1.story-body__h1, h1[data-testid='headline']")
            .map_err(|e| anyhow::anyhow!("Invalid selector: {:?}", e))?;
        
        let content_selector = Selector::parse(".story-body__inner p, [data-component='text-block'] p")
            .map_err(|e| anyhow::anyhow!("Invalid selector: {:?}", e))?;
        
        let date_selector = Selector::parse("time[datetime], .date")
            .map_err(|e| anyhow::anyhow!("Invalid selector: {:?}", e))?;
        
        let title = document
            .select(&title_selector)
            .next()
            .map(|el| el.text().collect::<String>().trim().to_string())
            .unwrap_or_else(|| "BBC Article".to_string());
        
        let published_date = document
            .select(&date_selector)
            .next()
            .and_then(|el| el.value().attr("datetime"))
            .map(|s| s.to_string());
        
        let content_paragraphs: Vec<String> = document
            .select(&content_selector)
            .map(|el| el.text().collect::<String>().trim().to_string())
            .filter(|p| !p.is_empty() && p.len() > 10)
            .collect();
        
        let content = content_paragraphs.join("\n\n");
        
        if content.is_empty() {
            return Err(anyhow::anyhow!("No BBC article content found"));
        }
        
        Ok(ArticleContent {
            title,
            author: None,
            published_date,
            content,
            summary: None,
            url: url.to_string(),
        })
    }
    
    fn extract_nytimes_article(&self, document: &Html, url: &str) -> Result<ArticleContent> {
        let title_selector = Selector::parse("h1[data-testid='headline'], h1.headline")
            .map_err(|e| anyhow::anyhow!("Invalid selector: {:?}", e))?;
        
        let author_selector = Selector::parse("[data-testid='byline'] span, .byline-author")
            .map_err(|e| anyhow::anyhow!("Invalid selector: {:?}", e))?;
        
        let content_selector = Selector::parse(".StoryBodyCompanionColumn p, section[name='articleBody'] p")
            .map_err(|e| anyhow::anyhow!("Invalid selector: {:?}", e))?;
        
        let title = document
            .select(&title_selector)
            .next()
            .map(|el| el.text().collect::<String>().trim().to_string())
            .unwrap_or_else(|| "New York Times Article".to_string());
        
        let author = document
            .select(&author_selector)
            .next()
            .map(|el| el.text().collect::<String>().trim().to_string())
            .filter(|s| !s.is_empty());
        
        let content_paragraphs: Vec<String> = document
            .select(&content_selector)
            .map(|el| el.text().collect::<String>().trim().to_string())
            .filter(|p| !p.is_empty() && p.len() > 10)
            .collect();
        
        let content = content_paragraphs.join("\n\n");
        
        if content.is_empty() {
            return Err(anyhow::anyhow!("No NYT article content found"));
        }
        
        Ok(ArticleContent {
            title,
            author,
            published_date: None,
            content,
            summary: None,
            url: url.to_string(),
        })
    }
    
    fn extract_generic_article(&self, document: &Html, url: &str) -> Result<ArticleContent> {
        // Generic extraction using common patterns
        let title_selectors = vec![
            "h1", "title", ".title", ".headline", ".entry-title", ".post-title"
        ];
        
        let content_selectors = vec![
            "article p", ".content p", ".entry-content p", ".post-content p", 
            ".article-body p", "main p", ".story p"
        ];
        
        let author_selectors = vec![
            ".author", ".byline", ".writer", "[rel='author']"
        ];
        
        // Try to find title
        let mut title = String::new();
        for selector_str in title_selectors {
            if let Ok(selector) = Selector::parse(selector_str) {
                if let Some(element) = document.select(&selector).next() {
                    title = element.text().collect::<String>().trim().to_string();
                    if !title.is_empty() {
                        break;
                    }
                }
            }
        }
        
        if title.is_empty() {
            title = "Article".to_string();
        }
        
        // Try to find author
        let mut author = None;
        for selector_str in author_selectors {
            if let Ok(selector) = Selector::parse(selector_str) {
                if let Some(element) = document.select(&selector).next() {
                    let author_text = element.text().collect::<String>().trim().to_string();
                    if !author_text.is_empty() {
                        author = Some(author_text);
                        break;
                    }
                }
            }
        }
        
        // Try to find content
        let mut content_paragraphs = Vec::new();
        for selector_str in content_selectors {
            if let Ok(selector) = Selector::parse(selector_str) {
                content_paragraphs = document
                    .select(&selector)
                    .map(|el| el.text().collect::<String>().trim().to_string())
                    .filter(|p| !p.is_empty() && p.len() > 20)
                    .collect();
                
                if !content_paragraphs.is_empty() {
                    break;
                }
            }
        }
        
        let content = content_paragraphs.join("\n\n");
        
        if content.is_empty() {
            return Err(anyhow::anyhow!("Could not extract article content from this page"));
        }
        
        Ok(ArticleContent {
            title,
            author,
            published_date: None,
            content,
            summary: None,
            url: url.to_string(),
        })
    }
}

impl Default for ArticleExtractor {
    fn default() -> Self {
        Self::new()
    }
}
