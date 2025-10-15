#!/usr/bin/env python3
"""
AudioNews.uk Email Domain Test Script
Tests Google Workspace domain setup and email aliases
"""

import smtplib
import socket
import subprocess
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys

def test_dns_configuration():
    """Test DNS records for Google Workspace"""
    print("📧 Testing DNS Configuration...")
    
    tests = []
    
    # Test MX records
    try:
        result = subprocess.run(['nslookup', '-type=MX', 'audionews.uk'], 
                               capture_output=True, text=True)
        if 'aspmx.l.google.com' in result.stdout:
            tests.append(("✅", "MX Records", "Properly configured for Google Workspace"))
        else:
            tests.append(("❌", "MX Records", "Not pointing to Google Workspace"))
    except Exception as e:
        tests.append(("❌", "MX Records", f"Check failed: {e}"))
    
    # Test SPF record
    try:
        result = subprocess.run(['nslookup', '-type=TXT', 'audionews.uk'], 
                               capture_output=True, text=True)
        if 'include:_spf.google.com' in result.stdout:
            tests.append(("✅", "SPF Record", "Google Workspace SPF configured"))
        else:
            tests.append(("⚠️", "SPF Record", "No Google SPF record found"))
    except Exception as e:
        tests.append(("❌", "SPF Record", f"Check failed: {e}"))
    
    # Test Google verification
    try:
        result = subprocess.run(['nslookup', '-type=TXT', 'audionews.uk'], 
                               capture_output=True, text=True)
        if 'google-site-verification' in result.stdout:
            tests.append(("✅", "Domain Verification", "Google verification record found"))
        else:
            tests.append(("❌", "Domain Verification", "No Google verification record"))
    except Exception as e:
        tests.append(("❌", "Domain Verification", f"Check failed: {e}"))
    
    return tests

def test_smtp_connectivity():
    """Test SMTP connectivity to Google's mail servers"""
    print("\n🔌 Testing SMTP Connectivity...")
    
    tests = []
    
    try:
        # Test Gmail SMTP
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        tests.append(("✅", "Gmail SMTP", "Connection successful on port 587"))
        server.quit()
    except Exception as e:
        tests.append(("❌", "Gmail SMTP", f"Connection failed: {e}"))
    
    try:
        # Test Google Workspace SMTP  
        server = smtplib.SMTP('smtp.gmail.com', 465)
        tests.append(("✅", "Gmail SMTP SSL", "Connection successful on port 465"))
        server.quit()
    except Exception as e:
        tests.append(("⚠️", "Gmail SMTP SSL", f"SSL connection issue: {e}"))
    
    return tests

def suggest_email_aliases():
    """Suggest professional email aliases for AudioNews.uk"""
    print("\n📮 Suggested Email Aliases for AudioNews.uk:")
    
    aliases = [
        ("contact@audionews.uk", "General inquiries and contact"),
        ("support@audionews.uk", "Technical support and accessibility help"),
        ("feedback@audionews.uk", "User feedback and suggestions"),
        ("accessibility@audionews.uk", "Accessibility-specific feedback"),
        ("press@audionews.uk", "Media inquiries and press contacts"),
        ("hello@audionews.uk", "Friendly general contact"),
        ("news@audionews.uk", "News-related correspondence"),
        ("admin@audionews.uk", "Administrative contacts")
    ]
    
    return aliases

def test_email_sending(sender_email=None, sender_password=None, test_recipient=None):
    """Test sending email from audionews.uk domain (requires authentication)"""
    if not all([sender_email, sender_password, test_recipient]):
        print("\n📧 Email Sending Test: Skipped (authentication required)")
        return [("⚠️", "Email Sending", "Requires Gmail credentials to test")]
    
    print(f"\n📤 Testing Email Sending from {sender_email}...")
    
    try:
        # Create test message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = test_recipient
        msg['Subject'] = "AudioNews.uk Domain Test - Email Working!"
        
        body = """
Hello!

This is a test email from the AudioNews.uk domain to verify that Google Workspace 
email forwarding is working correctly.

If you receive this email, the domain setup is successful!

Best regards,
AudioNews.uk Team
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        
        return [("✅", "Email Sending", f"Test email sent successfully to {test_recipient}")]
        
    except Exception as e:
        return [("❌", "Email Sending", f"Failed to send test email: {e}")]

def main():
    """Run all tests"""
    print("🎧 AUDIONEWS.UK GOOGLE WORKSPACE DOMAIN TEST")
    print("=" * 60)
    print("Testing Google Workspace setup for AudioNews.uk domain")
    print("=" * 60)
    
    all_tests = []
    
    # Run DNS tests
    all_tests.extend(test_dns_configuration())
    
    # Run SMTP tests
    all_tests.extend(test_smtp_connectivity())
    
    # Run email sending test (optional)
    all_tests.extend(test_email_sending())
    
    # Display results
    print(f"\n📊 TEST RESULTS SUMMARY")
    print("-" * 40)
    
    passed = 0
    warnings = 0
    failed = 0
    
    for status, test_name, description in all_tests:
        print(f"{status} {test_name:<20} {description}")
        if status == "✅":
            passed += 1
        elif status == "⚠️":
            warnings += 1
        else:
            failed += 1
    
    print("-" * 40)
    print(f"✅ Passed: {passed}  ⚠️  Warnings: {warnings}  ❌ Failed: {failed}")
    
    # Show suggested aliases
    print("\n" + "=" * 60)
    aliases = suggest_email_aliases()
    for email, description in aliases:
        print(f"📧 {email:<25} - {description}")
    
    print("\n" + "=" * 60)
    print("🎯 NEXT STEPS:")
    print("1. Create email aliases in Google Workspace Admin Console")
    print("2. Test sending emails to the aliases you create")
    print("3. Update AudioNews.uk website with professional contact emails")
    print("4. Set up email signatures with AudioNews.uk branding")
    print("=" * 60)
    
    return passed > failed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
