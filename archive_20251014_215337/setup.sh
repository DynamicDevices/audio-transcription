#!/bin/bash

# Audio Transcription Tool - Setup Script
# This script helps set up the environment for the audio transcription tool

echo "🎧 Audio Transcription Tool Setup"
echo "=================================="

# Check if Rust is installed
if ! command -v cargo &> /dev/null; then
    echo "❌ Rust is not installed. Please install it from https://rustup.rs/"
    exit 1
fi

echo "✅ Rust is installed"

# Build the project
echo "🔨 Building the project..."
if cargo build --release; then
    echo "✅ Build successful"
else
    echo "❌ Build failed. Please check the error messages above."
    exit 1
fi

echo ""
echo "🎙️  TTS Service Configuration"
echo "=============================="

# Check for TTS service configuration
echo "Choose your TTS service:"
echo "1. Azure Cognitive Services (Recommended - best Irish voices)"
echo "2. Google Cloud Text-to-Speech"
echo "3. Local eSpeak (basic quality, no API needed)"
echo ""

read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        echo ""
        echo "Azure Cognitive Services Setup:"
        echo "1. Create an Azure account at https://azure.microsoft.com/"
        echo "2. Create a Speech Services resource"
        echo "3. Get your subscription key and region"
        echo ""
        echo "Then set these environment variables:"
        echo "export AZURE_SPEECH_KEY=\"your_subscription_key_here\""
        echo "export AZURE_SPEECH_REGION=\"westeurope\""
        echo ""
        echo "Add these to your ~/.bashrc or ~/.zshrc to make them permanent"
        ;;
    2)
        echo ""
        echo "Google Cloud TTS Setup:"
        echo "1. Create a Google Cloud account at https://cloud.google.com/"
        echo "2. Enable the Text-to-Speech API"
        echo "3. Create an API key"
        echo ""
        echo "Then set this environment variable:"
        echo "export GOOGLE_CLOUD_API_KEY=\"your_api_key_here\""
        echo ""
        echo "Add this to your ~/.bashrc or ~/.zshrc to make it permanent"
        ;;
    3)
        echo ""
        echo "Installing eSpeak locally..."
        if command -v apt-get &> /dev/null; then
            sudo apt-get update && sudo apt-get install -y espeak
        elif command -v brew &> /dev/null; then
            brew install espeak
        elif command -v yum &> /dev/null; then
            sudo yum install -y espeak
        else
            echo "Please install eSpeak manually for your system"
        fi
        echo "✅ Local TTS setup complete"
        ;;
    *)
        echo "Invalid choice. Please run the script again."
        exit 1
        ;;
esac

echo ""
echo "🚀 Setup Complete!"
echo "=================="
echo ""
echo "To test the tool with the Guardian article example:"
echo ""
echo "./target/release/audio-transcription \\"
echo "  --url \"https://www.theguardian.com/world/2025/oct/04/greta-thunberg-israel-gaza-sweden\" \\"
echo "  --verbose"
echo ""
echo "For more options, see: ./target/release/audio-transcription --help"
echo ""
echo "📖 Full documentation: README.md"
