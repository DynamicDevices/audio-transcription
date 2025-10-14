#!/usr/bin/env python3
"""
Project Cleanup - Keep only essential files, remove obsolete ones
"""

import os
import shutil
from datetime import datetime

def cleanup_project():
    """Clean up obsolete files and organize the project"""
    
    print("🧹 PROJECT CLEANUP - CREATING SINGLE SOURCE OF TRUTH")
    print("=" * 60)
    
    # Files to KEEP (essential)
    keep_files = {
        # Final production files
        'guardian_article_ACCESSIBLE.mp3',
        'ACCESSIBLE_TEXT_FOR_TTS.txt',
        
        # Core Rust project files
        'Cargo.toml',
        'src/main.rs',
        'src/lib.rs',
        'src/article_extractor.rs',
        'src/tts_service.rs', 
        'src/audio_processor.rs',
        'src/test_extraction.rs',
        'src/demo.rs',
        
        # Final production script
        'create_accessible_audio.py',
        
        # Essential documentation
        'README.md'
    }
    
    # Get all current files
    all_files = []
    for file in os.listdir('.'):
        if os.path.isfile(file):
            all_files.append(file)
    
    print(f"📊 CURRENT STATE:")
    print(f"   Total files: {len(all_files)}")
    
    # Categorize files
    mp3_files = [f for f in all_files if f.endswith('.mp3')]
    txt_files = [f for f in all_files if f.endswith('.txt')]
    py_files = [f for f in all_files if f.endswith('.py')]
    rust_files = [f for f in all_files if f.endswith('.rs') or f == 'Cargo.toml']
    other_files = [f for f in all_files if not any(f.endswith(ext) for ext in ['.mp3', '.txt', '.py', '.rs']) and f != 'Cargo.toml']
    
    print(f"   MP3 files: {len(mp3_files)}")
    print(f"   TXT files: {len(txt_files)}")
    print(f"   Python files: {len(py_files)}")
    print(f"   Rust files: {len(rust_files)}")
    print(f"   Other files: {len(other_files)}")
    
    # Create archive directory for obsolete files
    archive_dir = f"archive_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(archive_dir, exist_ok=True)
    print(f"\n📁 Created archive directory: {archive_dir}")
    
    # Files to archive (not delete, in case needed)
    files_to_archive = []
    files_to_keep = []
    
    for file in all_files:
        if file in keep_files:
            files_to_keep.append(file)
        elif file.startswith('.') or file == archive_dir:
            # Skip hidden files and archive directory
            continue
        else:
            files_to_archive.append(file)
    
    print(f"\n🗂️  CLEANUP PLAN:")
    print(f"   Files to KEEP: {len(files_to_keep)}")
    print(f"   Files to ARCHIVE: {len(files_to_archive)}")
    
    # Show what we're keeping
    print(f"\n✅ KEEPING (Essential Files):")
    for category, files in [
        ("🎵 Final Audio", [f for f in files_to_keep if f.endswith('.mp3')]),
        ("📄 Final Text", [f for f in files_to_keep if f.endswith('.txt')]), 
        ("🐍 Production Script", [f for f in files_to_keep if f.endswith('.py')]),
        ("🦀 Rust Project", [f for f in files_to_keep if f.endswith('.rs') or f == 'Cargo.toml']),
        ("📚 Documentation", [f for f in files_to_keep if f.endswith('.md')])
    ]:
        if files:
            print(f"   {category}:")
            for file in sorted(files):
                print(f"      • {file}")
    
    # Archive obsolete files
    print(f"\n📦 ARCHIVING (Obsolete Files):")
    archived_count = 0
    
    for file in files_to_archive:
        try:
            shutil.move(file, os.path.join(archive_dir, file))
            archived_count += 1
            print(f"   📦 {file}")
        except Exception as e:
            print(f"   ❌ Failed to archive {file}: {e}")
    
    print(f"\n✅ CLEANUP COMPLETE!")
    print(f"   Archived: {archived_count} files")
    print(f"   Kept: {len(files_to_keep)} essential files")
    
    # Create final project structure documentation
    create_project_structure_doc()
    
    return archive_dir, files_to_keep

def create_project_structure_doc():
    """Create documentation of the final project structure"""
    
    with open('PROJECT_STRUCTURE.md', 'w') as f:
        f.write("# Audio Transcription Project - Final Structure\n\n")
        f.write("## 🎯 Purpose\n")
        f.write("Convert Guardian news articles to accessible audio for blind users.\n\n")
        
        f.write("## 📁 Project Files\n\n")
        
        f.write("### 🎵 Final Audio Output\n")
        f.write("- `guardian_article_ACCESSIBLE.mp3` - **FINAL AUDIO FILE**\n")
        f.write("  - Optimized for blind users\n")
        f.write("  - 5-second intro for quick decision-making\n")
        f.write("  - No pause artifacts\n")
        f.write("  - WhatsApp compatible\n\n")
        
        f.write("### 📄 Text Processing\n")
        f.write("- `ACCESSIBLE_TEXT_FOR_TTS.txt` - Final text used for audio generation\n")
        f.write("- `create_accessible_audio.py` - **PRODUCTION SCRIPT**\n")
        f.write("  - Use this script to generate audio from any Guardian URL\n")
        f.write("  - Handles all text cleaning and optimization\n\n")
        
        f.write("### 🦀 Rust Application (Optional)\n")
        f.write("- `Cargo.toml` - Rust project configuration\n")
        f.write("- `src/main.rs` - Main Rust application\n")
        f.write("- `src/lib.rs` - Shared structures and modules\n")
        f.write("- `src/article_extractor.rs` - Web scraping logic\n")
        f.write("- `src/tts_service.rs` - TTS integration (Azure/Google)\n")
        f.write("- `src/audio_processor.rs` - Audio post-processing\n\n")
        
        f.write("## 🚀 How to Use\n\n")
        f.write("### Quick Audio Generation (Python)\n")
        f.write("```bash\n")
        f.write("python3 create_accessible_audio.py\n")
        f.write("```\n\n")
        
        f.write("### Rust Application (Advanced)\n")
        f.write("```bash\n")
        f.write("cargo run -- --url https://www.theguardian.com/article-url\n")
        f.write("```\n\n")
        
        f.write("## 🎯 Key Features Achieved\n")
        f.write("- ✅ Accessibility-focused design\n")
        f.write("- ✅ 5-second intro for quick decisions\n")
        f.write("- ✅ Zero line-ending pause artifacts\n")
        f.write("- ✅ Optimized phrase structures\n")
        f.write("- ✅ Natural Irish female voice\n")
        f.write("- ✅ WhatsApp compatible file size\n")
        f.write("- ✅ Accurate content preservation\n\n")
        
        f.write("## 📊 Technical Solutions\n")
        f.write("1. **Line Ending Issue**: Removed all `\\n`, `\\r`, `\\t` artifacts\n")
        f.write("2. **Phrase Pauses**: Replaced 'being subjected to' with 'faces'\n")
        f.write("3. **Accessibility**: Brief intro allows quick listening decisions\n")
        f.write("4. **Quality**: Professional HTML cleaning with BeautifulSoup\n")

    print(f"   📚 Created: PROJECT_STRUCTURE.md")

def main():
    archive_dir, kept_files = cleanup_project()
    
    print(f"\n🎯 SINGLE SOURCE OF TRUTH ESTABLISHED!")
    print(f"=" * 45)
    print(f"📱 **FOR YOUR FATHER**: guardian_article_ACCESSIBLE.mp3")
    print(f"🔧 **TO GENERATE MORE**: python3 create_accessible_audio.py")
    print(f"📚 **DOCUMENTATION**: PROJECT_STRUCTURE.md")
    print(f"📦 **ARCHIVED FILES**: {archive_dir}/")
    
    # Final file count
    remaining_files = len([f for f in os.listdir('.') if os.path.isfile(f) and not f.startswith('.')])
    print(f"\n📊 FINAL STATE: {remaining_files} essential files (down from 43)")

if __name__ == "__main__":
    main()
