/**
 * DAILY NEWS DIGEST - ACCESSIBILITY JAVASCRIPT
 * Enhanced functionality for visually impaired users and screen readers
 * Keyboard navigation, audio controls, and progressive enhancement
 */

(function() {
    'use strict';
    
    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
    
    function init() {
        console.log('🎧 Initializing accessibility features...');
        
        // Check URL parameters first
        handleUrlParameters();
        
        // Core accessibility features
        setupKeyboardNavigation();
        setupAudioEnhancements();
        setupProgressiveEnhancement();
        setupShareFunctionality();
        setupAnnouncementRegion();
        setupFocusManagement();
        
        // Performance and user experience
        setupLazyLoading();
        setupOfflineSupport();
        
        console.log('✅ Accessibility features initialized');
    }
    
    /**
     * Handle URL parameters for autoplay and other features
     */
    function handleUrlParameters() {
        const urlParams = new URLSearchParams(window.location.search);
        const autoplay = urlParams.get('autoplay');
        
        if (autoplay === 'true') {
            // Wait for audio to be ready, then attempt autoplay
            setTimeout(function() {
                const audioPlayer = document.querySelector('audio');
                if (audioPlayer) {
                    audioPlayer.play().then(function() {
                        announceToScreenReader('Audio started automatically from shared link');
                        console.log('✅ Autoplay started successfully');
                    }).catch(function(error) {
                        console.log('⚠️ Autoplay prevented by browser:', error);
                        announceToScreenReader('Click play to start audio - autoplay was blocked by your browser for security');
                        
                        // Add visual indicator that autoplay was attempted
                        const audioContainer = document.querySelector('.audio-player-container');
                        if (audioContainer) {
                            const notice = document.createElement('div');
                            notice.className = 'autoplay-notice';
                            notice.innerHTML = '▶️ <strong>Ready to play:</strong> Click play to start your news digest';
                            notice.style.cssText = `
                                background: #e3f2fd;
                                border: 1px solid #2196f3;
                                padding: 8px 12px;
                                border-radius: 4px;
                                margin: 8px 0;
                                font-size: 14px;
                                color: #1565c0;
                            `;
                            audioContainer.insertBefore(notice, audioContainer.firstChild);
                            
                            // Remove notice after user interaction
                            audioPlayer.addEventListener('play', function() {
                                if (notice.parentNode) {
                                    notice.remove();
                                }
                            }, { once: true });
                        }
                    });
                }
            }, 800); // Small delay to ensure audio is loaded
        }
    }
    
    /**
     * Enhanced keyboard navigation for screen reader users
     */
    function setupKeyboardNavigation() {
        // Quick navigation shortcuts
        const shortcuts = {
            '1': () => focusElement('#todays-digest'),
            '2': () => focusElement('#news-sections'), 
            '3': () => focusElement('#recent-digests'),
            '4': () => focusElement('#how-to-use'),
            'p': () => toggleAudioPlayback(),
            'd': () => downloadCurrentDigest(),
            's': () => shareCurrentDigest()
        };
        
        document.addEventListener('keydown', function(e) {
            // Only activate shortcuts when not in form elements
            if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
                return;
            }
            
            const key = e.key.toLowerCase();
            if (shortcuts[key] && (e.altKey || e.ctrlKey)) {
                e.preventDefault();
                shortcuts[key]();
                announceToScreenReader(`Navigated to ${key} section`);
            }
        });
        
        // Add keyboard shortcut hints
        addKeyboardHints();
    }
    
    function addKeyboardHints() {
        const shortcutInfo = document.createElement('div');
        shortcutInfo.className = 'keyboard-shortcuts visually-hidden';
        shortcutInfo.setAttribute('aria-live', 'polite');
        shortcutInfo.innerHTML = `
            <p>Keyboard shortcuts available:</p>
            <ul>
                <li>Alt+1: Today's digest</li>
                <li>Alt+2: News sections</li>
                <li>Alt+3: Recent digests</li>
                <li>Alt+4: How to use</li>
                <li>Alt+P: Play/pause audio</li>
                <li>Alt+D: Download current digest</li>
                <li>Alt+S: Share current digest</li>
            </ul>
        `;
        document.body.appendChild(shortcutInfo);
    }
    
    /**
     * Enhanced audio player functionality
     */
    function setupAudioEnhancements() {
        const audioPlayers = document.querySelectorAll('audio');
        
        audioPlayers.forEach(function(audio, index) {
            // Add enhanced controls
            enhanceAudioPlayer(audio, index);
            
            // Add event listeners for accessibility
            audio.addEventListener('play', function() {
                announceToScreenReader('Audio playback started');
                updatePlaybackStatus(audio, 'playing');
            });
            
            audio.addEventListener('pause', function() {
                announceToScreenReader('Audio playback paused');
                updatePlaybackStatus(audio, 'paused');
            });
            
            audio.addEventListener('ended', function() {
                announceToScreenReader('Audio playback completed');
                updatePlaybackStatus(audio, 'ended');
            });
            
            // Add time updates for screen readers
            audio.addEventListener('timeupdate', function() {
                updateTimeDisplay(audio);
            });
            
            // Error handling
            audio.addEventListener('error', function() {
                announceToScreenReader('Audio playback error. Please try downloading the file instead.');
            });
        });
    }
    
    function enhanceAudioPlayer(audio, index) {
        const container = audio.closest('.audio-player-container');
        if (!container) return;
        
        // Create enhanced controls
        const controls = document.createElement('div');
        controls.className = 'enhanced-audio-controls';
        controls.innerHTML = `
            <div class="audio-time-display" aria-live="polite">
                <span class="current-time">0:00</span> / <span class="total-time">0:00</span>
            </div>
            <div class="audio-speed-controls">
                <label for="speed-${index}">Playback Speed:</label>
                <select id="speed-${index}" class="speed-selector" aria-describedby="speed-help-${index}">
                    <option value="0.5">0.5x (Slow)</option>
                    <option value="0.75">0.75x</option>
                    <option value="1" selected>1x (Normal)</option>
                    <option value="1.25">1.25x</option>
                    <option value="1.5">1.5x (Fast)</option>
                    <option value="2">2x (Very Fast)</option>
                </select>
                <p id="speed-help-${index}" class="help-text">Adjust playback speed for comfortable listening</p>
            </div>
        `;
        
        container.appendChild(controls);
        
        // Speed control functionality
        const speedSelector = controls.querySelector('.speed-selector');
        speedSelector.addEventListener('change', function() {
            audio.playbackRate = parseFloat(this.value);
            announceToScreenReader(`Playback speed changed to ${this.value}x`);
        });
        
        // Store references for global functions
        audio._timeDisplay = controls.querySelector('.audio-time-display');
        audio._currentTimeSpan = controls.querySelector('.current-time');
        audio._totalTimeSpan = controls.querySelector('.total-time');
    }
    
    function updatePlaybackStatus(audio, status) {
        const statusMap = {
            'playing': '▶️ Playing',
            'paused': '⏸️ Paused', 
            'ended': '⏹️ Completed'
        };
        
        if (audio._timeDisplay) {
            audio._timeDisplay.setAttribute('aria-label', statusMap[status] || status);
        }
    }
    
    function updateTimeDisplay(audio) {
        if (!audio._currentTimeSpan || !audio._totalTimeSpan) return;
        
        const current = formatTime(audio.currentTime);
        const total = formatTime(audio.duration);
        
        audio._currentTimeSpan.textContent = current;
        audio._totalTimeSpan.textContent = total;
    }
    
    function formatTime(seconds) {
        if (isNaN(seconds)) return '0:00';
        
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = Math.floor(seconds % 60);
        return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
    }
    
    /**
     * Progressive enhancement for better UX
     */
    function setupProgressiveEnhancement() {
        // Add loading states
        const audioElements = document.querySelectorAll('audio');
        audioElements.forEach(function(audio) {
            audio.addEventListener('loadstart', function() {
                addLoadingIndicator(audio);
            });
            
            audio.addEventListener('canplay', function() {
                removeLoadingIndicator(audio);
            });
        });
        
        // Enhance buttons with loading states
        const actionButtons = document.querySelectorAll('.action-button');
        actionButtons.forEach(function(button) {
            button.addEventListener('click', function() {
                if (this.classList.contains('download-button')) {
                    showDownloadFeedback(this);
                }
            });
        });
    }
    
    function addLoadingIndicator(audio) {
        const container = audio.closest('.audio-player-container');
        if (!container) return;
        
        const indicator = document.createElement('div');
        indicator.className = 'loading-indicator';
        indicator.innerHTML = '⏳ Loading audio...';
        indicator.setAttribute('aria-live', 'polite');
        
        container.appendChild(indicator);
    }
    
    function removeLoadingIndicator(audio) {
        const container = audio.closest('.audio-player-container');
        if (!container) return;
        
        const indicator = container.querySelector('.loading-indicator');
        if (indicator) {
            indicator.remove();
            announceToScreenReader('Audio loaded and ready to play');
        }
    }
    
    function showDownloadFeedback(button) {
        const originalText = button.innerHTML;
        button.innerHTML = '<span class="button-icon">⬇️</span> Downloading...';
        button.disabled = true;
        
        setTimeout(function() {
            button.innerHTML = '<span class="button-icon">✅</span> Downloaded!';
            announceToScreenReader('Download started. Check your downloads folder.');
            
            setTimeout(function() {
                button.innerHTML = originalText;
                button.disabled = false;
            }, 2000);
        }, 1000);
    }
    
    /**
     * Share functionality with accessibility
     */
    function setupShareFunctionality() {
        // Make the share function globally available
        window.copyShareLink = function() {
            const currentUrl = window.location.href;
            const baseUrl = window.location.origin + window.location.pathname;
            
            // Create share URL with autoplay parameter
            const shareUrl = `${baseUrl}?autoplay=true`;
            
            // Try modern clipboard API first
            if (navigator.clipboard && navigator.clipboard.writeText) {
                navigator.clipboard.writeText(shareUrl).then(function() {
                    announceToScreenReader('Share link copied to clipboard. Audio will auto-start when opened.');
                    showShareFeedback('✅ Auto-play link copied!');
                }).catch(function() {
                    fallbackCopyToClipboard(shareUrl);
                });
            } else {
                fallbackCopyToClipboard(shareUrl);
            }
        };
    }
    
    function fallbackCopyToClipboard(text) {
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        textArea.style.top = '-999999px';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        
        try {
            document.execCommand('copy');
            announceToScreenReader('Share link copied to clipboard. Audio will auto-start when opened.');
            showShareFeedback('✅ Auto-play link copied!');
        } catch (err) {
            announceToScreenReader('Could not copy link. Please copy the page URL manually and add ?autoplay=true');
            showShareFeedback('❌ Copy failed. Please copy URL manually.');
        }
        
        document.body.removeChild(textArea);
    }
    
    function showShareFeedback(message) {
        const shareButton = document.querySelector('.share-button');
        if (!shareButton) return;
        
        const originalText = shareButton.innerHTML;
        shareButton.innerHTML = message;
        
        setTimeout(function() {
            shareButton.innerHTML = originalText;
        }, 3000);
    }
    
    /**
     * Screen reader announcement region
     */
    function setupAnnouncementRegion() {
        const announcer = document.createElement('div');
        announcer.id = 'screen-reader-announcer';
        announcer.className = 'visually-hidden';
        announcer.setAttribute('aria-live', 'assertive');
        announcer.setAttribute('aria-atomic', 'true');
        document.body.appendChild(announcer);
    }
    
    function announceToScreenReader(message) {
        const announcer = document.getElementById('screen-reader-announcer');
        if (announcer) {
            announcer.textContent = message;
            
            // Clear after announcement
            setTimeout(function() {
                announcer.textContent = '';
            }, 1000);
        }
    }
    
    /**
     * Focus management for better navigation
     */
    function setupFocusManagement() {
        // Remember last focused element before navigation
        let lastFocusedElement = null;
        
        document.addEventListener('focusin', function(e) {
            lastFocusedElement = e.target;
        });
        
        // Restore focus after dynamic content updates
        window.restoreFocus = function() {
            if (lastFocusedElement && document.contains(lastFocusedElement)) {
                lastFocusedElement.focus();
            }
        };
        
        // Skip link functionality
        const skipLink = document.querySelector('.skip-link');
        if (skipLink) {
            skipLink.addEventListener('click', function(e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.focus();
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            });
        }
    }
    
    /**
     * Utility functions for global use
     */
    function focusElement(selector) {
        const element = document.querySelector(selector);
        if (element) {
            element.focus();
            element.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    }
    
    function toggleAudioPlayback() {
        const audio = document.querySelector('audio');
        if (audio) {
            if (audio.paused) {
                audio.play();
            } else {
                audio.pause();
            }
        }
    }
    
    function downloadCurrentDigest() {
        const downloadButton = document.querySelector('.download-button');
        if (downloadButton) {
            downloadButton.click();
        }
    }
    
    function shareCurrentDigest() {
        const shareButton = document.querySelector('.share-button');
        if (shareButton) {
            shareButton.click();
        }
    }
    
    /**
     * Lazy loading for performance
     */
    function setupLazyLoading() {
        // Lazy load audio files when user interacts
        const audioElements = document.querySelectorAll('audio[data-src]');
        
        const loadAudio = function(audio) {
            if (audio.dataset.src) {
                audio.src = audio.dataset.src;
                audio.removeAttribute('data-src');
                audio.load();
            }
        };
        
        // Load on first interaction
        audioElements.forEach(function(audio) {
            ['focus', 'mouseenter', 'touchstart'].forEach(function(event) {
                audio.addEventListener(event, function() {
                    loadAudio(audio);
                }, { once: true });
            });
        });
    }
    
    /**
     * Offline support notifications
     */
    function setupOfflineSupport() {
        window.addEventListener('online', function() {
            announceToScreenReader('Connection restored. All features available.');
        });
        
        window.addEventListener('offline', function() {
            announceToScreenReader('You are offline. Downloaded audio files will still work.');
        });
    }
    
    // Export functions for global use
    window.NewsDigestAccessibility = {
        announceToScreenReader: announceToScreenReader,
        focusElement: focusElement,
        toggleAudioPlayback: toggleAudioPlayback,
        downloadCurrentDigest: downloadCurrentDigest,
        shareCurrentDigest: shareCurrentDigest,
        copyShareLink: window.copyShareLink
    };
    
})();
