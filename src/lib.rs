pub mod article_extractor;
pub mod tts_service;
pub mod audio_processor;

use serde::{Deserialize, Serialize};

#[derive(Debug, Serialize, Deserialize)]
pub struct ArticleContent {
    pub title: String,
    pub author: Option<String>,
    pub published_date: Option<String>,
    pub content: String,
    pub summary: Option<String>,
    pub url: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AudioConfig {
    pub voice_name: String,
    pub speaking_rate: f32,
    pub output_format: String,
    pub sample_rate: u32,
}

impl Default for AudioConfig {
    fn default() -> Self {
        Self {
            voice_name: "en-IE-EmilyNeural".to_string(), // Azure Irish female voice
            speaking_rate: 0.9,
            output_format: "mp3".to_string(),
            sample_rate: 24000,
        }
    }
}
