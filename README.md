# AI-Powered Email Assistant

## Overview
This project is an AI-powered email assistant that automatically fetches unread emails, analyzes their content using a Hugging Face AI model, and sends automated replies based on extracted information.

## Features
- Connects to an email inbox using IMAP.
- Fetches unread emails and extracts relevant content.
- Uses a Hugging Face AI model for text analysis.
- Generates automated responses based on email content.
- Sends replies via SMTP.

## Installation

### Prerequisites
- Python 3.8+
- IMAP and SMTP email credentials
- A Hugging Face API key

### Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/email-ai-assistant.git
   cd email-ai-assistant
   ```

## Configuration
1. Set up environment variables for email credentials and Hugging Face API key:
   ```sh
   export EMAIL_ADDRESS="your-email@example.com"
   export EMAIL_PASSWORD="your-email-password"
   export SMTP_SERVER="smtp.example.com"
   export IMAP_SERVER="imap.example.com"
   export HUGGINGFACE_API_KEY="your-huggingface-api-key"
   ```
   On Windows (PowerShell):
   ```powershell
   $env:EMAIL_ADDRESS="your-email@example.com"
   $env:EMAIL_PASSWORD="your-email-password"
   $env:SMTP_SERVER="smtp.example.com"
   $env:IMAP_SERVER="imap.example.com"
   $env:HUGGINGFACE_API_KEY="your-huggingface-api-key"
   ```

## Usage
Run the email assistant script:
```sh
python main.py
```
The script will:
- Check for unread emails.
- Extract content and analyze it.
- Generate and send an appropriate reply.
