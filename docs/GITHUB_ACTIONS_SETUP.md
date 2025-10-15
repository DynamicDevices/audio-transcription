# 🔐 GitHub Actions Setup Guide

## Required Repository Secrets

To enable AI-powered daily news digests, you need to add these secrets to your GitHub repository:

### 🚀 **How to Add Secrets**

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**  
3. Click **New repository secret**
4. Add each secret below:

### 🤖 **AI Provider Secrets (Choose One)**

#### **Option 1: OpenAI (Recommended)**
- **Secret Name**: `OPENAI_API_KEY`
- **Secret Value**: Your OpenAI API key (starts with `sk-`)
- **Get it from**: https://platform.openai.com/api-keys
- **Cost**: ~$0.01-0.10 per digest (very affordable)

#### **Option 2: Anthropic Claude**
- **Secret Name**: `ANTHROPIC_API_KEY`  
- **Secret Value**: Your Anthropic API key
- **Get it from**: https://console.anthropic.com/
- **Cost**: Similar to OpenAI

### 🔧 **GitHub Token (Automatic)**
- **Secret Name**: `GITHUB_TOKEN`
- **Status**: ✅ **Already available** (GitHub provides this automatically)
- **Purpose**: Allows the action to commit files and create releases

## 📅 **Automatic Schedule**

Once secrets are configured, the workflow will:
- ✅ **Run daily at 6:00 AM UTC** (7:00 AM BST)
- ✅ **Generate AI-enhanced news digest**
- ✅ **Commit MP3 and text files to repository**
- ✅ **Create GitHub release with downloadable audio**
- ✅ **Upload artifacts for 90-day retention**

## 🎯 **Manual Triggering**

You can also run the digest manually:
1. Go to **Actions** tab in your repository
2. Click **🤖 AI-Powered Daily News Digest**
3. Click **Run workflow**
4. Optionally enable debug mode
5. Click **Run workflow**

## 📊 **What Gets Generated**

### **Files Created:**
- `news_digest_ai_YYYY_MM_DD.mp3` - WhatsApp-ready audio file
- `news_digest_ai_YYYY_MM_DD.txt` - Full transcript with sources

### **GitHub Features:**
- **Releases**: Each digest gets its own release with download links
- **Artifacts**: 90-day backup of all generated files  
- **Issues**: Automatic issue creation if generation fails
- **Commits**: Detailed commit messages with file stats

## 🚨 **Error Handling**

If the workflow fails:
- ✅ **Automatic issue created** with failure details
- ✅ **Email notification** (if GitHub notifications enabled)
- ✅ **Fallback to non-AI mode** if API fails
- ✅ **Detailed logs** available in Actions tab

## 💰 **Cost Estimation**

**OpenAI API Usage:**
- Daily digest: ~2,000-4,000 tokens
- Cost per digest: ~$0.01-0.05
- Monthly cost: ~$0.30-1.50
- **Very affordable for accessibility service!**

## 🎧 **Usage for Visually Impaired Users**

### **Daily Routine:**
1. **6:00 AM**: Digest automatically generated
2. **6:05 AM**: Available in GitHub Releases
3. **Download MP3** from latest release
4. **Send to WhatsApp** or play directly
5. **Professional Irish Emily voice** - natural and clear

### **Access Methods:**
- **GitHub Releases**: https://github.com/your-username/audio-transcription/releases
- **Direct download**: Latest release always has current digest
- **WhatsApp sharing**: MP3 files optimized for mobile sharing

## 🔧 **Troubleshooting**

### **No AI Analysis:**
- Check API key is correctly set in repository secrets
- Verify key has sufficient credits/usage limits
- System will fallback to keyword-based analysis

### **No Audio Generated:**
- Check if `edge-tts` is working (should work on GitHub runners)
- Verify text content was created successfully
- Check workflow logs for specific error messages

### **Files Not Committed:**
- Ensure `GITHUB_TOKEN` has write permissions (should be automatic)
- Check if repository has branch protection rules
- Verify workflow has `contents: write` permission

## ✅ **Testing Setup**

After adding secrets, test the setup:

1. **Manual trigger**: Run workflow manually to test
2. **Check outputs**: Verify MP3 and TXT files are created
3. **Test download**: Download from GitHub release
4. **Verify quality**: Listen to audio for quality and content
5. **WhatsApp test**: Send MP3 to phone and test playback

**Perfect for providing daily, professional news access to visually impaired users! 🎧♿**
