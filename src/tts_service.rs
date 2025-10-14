use anyhow::{Context, Result};
use reqwest::Client;
use serde::{Deserialize, Serialize};
use std::env;
use base64::{Engine, engine::general_purpose::STANDARD as BASE64};

use crate::AudioConfig;

#[derive(Debug, Clone)]
pub struct TTSService {
    service_type: TTSServiceType,
    client: Client,
    config: AudioConfig,
}

#[derive(Debug, Clone)]
enum TTSServiceType {
    Azure {
        subscription_key: String,
        region: String,
    },
    Google {
        api_key: String,
    },
    Local,
}

#[derive(Serialize)]
struct AzureSSMLRequest {
    #[serde(rename = "ssml")]
    ssml_content: String,
}

#[derive(Serialize)]
struct GoogleTTSRequest {
    input: GoogleTTSInput,
    voice: GoogleTTSVoice,
    #[serde(rename = "audioConfig")]
    audio_config: GoogleAudioConfig,
}

#[derive(Serialize)]
struct GoogleTTSInput {
    text: String,
}

#[derive(Serialize)]
struct GoogleTTSVoice {
    #[serde(rename = "languageCode")]
    language_code: String,
    name: String,
    #[serde(rename = "ssmlGender")]
    ssml_gender: String,
}

#[derive(Serialize)]
struct GoogleAudioConfig {
    #[serde(rename = "audioEncoding")]
    audio_encoding: String,
    #[serde(rename = "speakingRate")]
    speaking_rate: f32,
    #[serde(rename = "pitch")]
    pitch: f32,
}

#[derive(Deserialize)]
struct GoogleTTSResponse {
    #[serde(rename = "audioContent")]
    audio_content: String,
}

impl TTSService {
    pub fn new(service_name: &str, config: &AudioConfig) -> Result<Self> {
        let client = Client::new();
        
        let service_type = match service_name.to_lowercase().as_str() {
            "azure" => {
                let subscription_key = env::var("AZURE_SPEECH_KEY")
                    .context("AZURE_SPEECH_KEY environment variable not set. Please set it to your Azure Speech Services subscription key.")?;
                let region = env::var("AZURE_SPEECH_REGION")
                    .unwrap_or_else(|_| "westeurope".to_string());
                
                TTSServiceType::Azure {
                    subscription_key,
                    region,
                }
            }
            "google" => {
                let api_key = env::var("GOOGLE_CLOUD_API_KEY")
                    .context("GOOGLE_CLOUD_API_KEY environment variable not set")?;
                
                TTSServiceType::Google { api_key }
            }
            "local" => TTSServiceType::Local,
            _ => return Err(anyhow::anyhow!("Unsupported TTS service: {}", service_name)),
        };
        
        Ok(Self {
            service_type,
            client,
            config: config.clone(),
        })
    }
    
    pub async fn synthesize_speech(&self, text: &str) -> Result<Vec<u8>> {
        match &self.service_type {
            TTSServiceType::Azure { subscription_key, region } => {
                self.synthesize_azure_speech(text, subscription_key, region).await
            }
            TTSServiceType::Google { api_key } => {
                self.synthesize_google_speech(text, api_key).await
            }
            TTSServiceType::Local => {
                self.synthesize_local_speech(text).await
            }
        }
    }
    
    async fn synthesize_azure_speech(&self, text: &str, subscription_key: &str, region: &str) -> Result<Vec<u8>> {
        // Azure Speech Services SSML format
        let ssml = format!(
            r#"<speak version='1.0' xml:lang='en-IE' xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='https://www.w3.org/2001/mstts'>
                <voice name='{}'>
                    <prosody rate='{:.1}'>
                        {}
                    </prosody>
                </voice>
            </speak>"#,
            self.config.voice_name,
            self.config.speaking_rate,
            html_escape::encode_text(text)
        );
        
        let url = format!(
            "https://{}.tts.speech.microsoft.com/cognitiveservices/v1",
            region
        );
        
        let response = self.client
            .post(&url)
            .header("Ocp-Apim-Subscription-Key", subscription_key)
            .header("Content-Type", "application/ssml+xml")
            .header("X-Microsoft-OutputFormat", "audio-24khz-48kbitrate-mono-mp3")
            .header("User-Agent", "AudioTranscriptionTool/1.0")
            .body(ssml)
            .send()
            .await
            .context("Failed to send request to Azure Speech Services")?;
        
        if !response.status().is_success() {
            let status = response.status();
            let error_text = response.text().await.unwrap_or_else(|_| "Unknown error".to_string());
            return Err(anyhow::anyhow!(
                "Azure Speech Services error ({}): {}",
                status,
                error_text
            ));
        }
        
        let audio_data = response
            .bytes()
            .await
            .context("Failed to read audio data from Azure response")?;
        
        Ok(audio_data.to_vec())
    }
    
    async fn synthesize_google_speech(&self, text: &str, api_key: &str) -> Result<Vec<u8>> {
        // Use Google Cloud TTS with Irish voice
        let voice_name = if self.config.voice_name.starts_with("en-IE") {
            self.config.voice_name.clone()
        } else {
            "en-IE-Standard-A".to_string() // Google's Irish female voice
        };
        
        let request = GoogleTTSRequest {
            input: GoogleTTSInput {
                text: text.to_string(),
            },
            voice: GoogleTTSVoice {
                language_code: "en-IE".to_string(),
                name: voice_name,
                ssml_gender: "FEMALE".to_string(),
            },
            audio_config: GoogleAudioConfig {
                audio_encoding: "MP3".to_string(),
                speaking_rate: self.config.speaking_rate,
                pitch: 0.0,
            },
        };
        
        let url = format!("https://texttospeech.googleapis.com/v1/text:synthesize?key={}", api_key);
        
        let response = self.client
            .post(&url)
            .header("Content-Type", "application/json")
            .json(&request)
            .send()
            .await
            .context("Failed to send request to Google Cloud TTS")?;
        
        if !response.status().is_success() {
            let status = response.status();
            let error_text = response.text().await.unwrap_or_else(|_| "Unknown error".to_string());
            return Err(anyhow::anyhow!(
                "Google Cloud TTS error ({}): {}",
                status,
                error_text
            ));
        }
        
        let tts_response: GoogleTTSResponse = response
            .json()
            .await
            .context("Failed to parse Google TTS response")?;
        
        let audio_data = BASE64
            .decode(&tts_response.audio_content)
            .context("Failed to decode base64 audio content")?;
        
        Ok(audio_data)
    }
    
    async fn synthesize_local_speech(&self, text: &str) -> Result<Vec<u8>> {
        // Fallback to local TTS using espeak or festival
        use std::process::Command;
        use std::fs;
        
        let temp_file = format!("/tmp/tts_output_{}.wav", uuid::Uuid::new_v4().simple());
        
        // Try espeak first (more likely to be available)
        let output = Command::new("espeak")
            .args(&[
                "-v", "en-irish+f3", // Irish female voice variant 3
                "-s", "160", // Speaking speed (words per minute)
                "-a", "100", // Amplitude
                "-g", "10",  // Gap between words
                "-f", "-",   // Read from stdin
                "-w", &temp_file, // Write to file
            ])
            .arg(text)
            .output();
        
        match output {
            Ok(output) if output.status.success() => {
                let audio_data = fs::read(&temp_file)
                    .context("Failed to read generated audio file")?;
                
                // Clean up temporary file
                let _ = fs::remove_file(&temp_file);
                
                Ok(audio_data)
            }
            _ => {
                // Fallback: Try festival
                let festival_output = Command::new("festival")
                    .args(&["--tts", "--pipe"])
                    .arg(text)
                    .output();
                
                match festival_output {
                    Ok(_) => {
                        // Festival is more complex to integrate, this is a placeholder
                        Err(anyhow::anyhow!(
                            "Local TTS failed. Please install espeak: sudo apt-get install espeak"
                        ))
                    }
                    Err(_) => {
                        Err(anyhow::anyhow!(
                            "No local TTS system available. Please install espeak or configure cloud TTS services."
                        ))
                    }
                }
            }
        }
    }
    
    pub fn get_available_irish_voices() -> Vec<(&'static str, &'static str, &'static str)> {
        // Returns (service, voice_id, description)
        vec![
            ("azure", "en-IE-EmilyNeural", "Emily - Irish female, natural and warm"),
            ("azure", "en-IE-ConnorNeural", "Connor - Irish male, clear and friendly"),
            ("google", "en-IE-Standard-A", "Google Irish female voice"),
            ("google", "en-IE-Wavenet-A", "Google Irish female voice (WaveNet - higher quality)"),
            ("local", "en-irish+f3", "eSpeak Irish female voice"),
        ]
    }
}
