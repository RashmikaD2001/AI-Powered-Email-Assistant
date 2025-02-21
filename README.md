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

### Create a .env file and add the following environment variables:
- EMAIL_USER=
- EMAIL_PASSWORD=
- IMAP_HOST='imap.gmail.com'
- SMTP_SERVER='smtp.gmail.com'
- SMTP_PORT=587
- IMAP_PORT=993
- HUGGINGFACE_API_TOKEN=

Create a whitelist.yaml file for managing email whitelisting.

## Configuration

Load environment variables from the .env file in your script.

## Usage
Run the email assistant script:
```sh
python main.py
```
The script will:
- Check for unread emails.
- Extract content and analyze it.
- Generate and send an appropriate reply.
