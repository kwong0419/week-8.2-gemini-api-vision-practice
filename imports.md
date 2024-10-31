# Imports Guide

## External Libraries (Need to Install)

### 1. Google Generative AI
```python
import google.generativeai as genai
```
- **Installation**: `pip install google-generativeai`
- **Documentation**: [Google Generative AI Python SDK](https://github.com/google/generative-ai-python)
- **Purpose**: Provides access to Google's Gemini model for image analysis and color palette generation
- **Key Features Used**: Image analysis, text generation, JSON response handling

### 2. Requests
```python
import requests
```
- **Installation**: `pip install requests`
- **Documentation**: [Requests: HTTP for Humans](https://requests.readthedocs.io/)
- **Purpose**: Downloads images from URLs using HTTP requests
- **Key Features Used**: GET requests, response handling, streaming file downloads

### 3. Pillow (PIL)
```python
from PIL import Image, ImageDraw
```
- **Installation**: `pip install Pillow`
- **Documentation**: [Pillow (PIL Fork)](https://pillow.readthedocs.io/)
- **Purpose**: Image processing and manipulation library
- **Key Features Used**: Opening images, creating new images, drawing shapes

### 4. Python-dotenv
```python
from dotenv import load_dotenv
```
- **Installation**: `pip install python-dotenv`
- **Documentation**: [python-dotenv](https://github.com/theskumar/python-dotenv)
- **Purpose**: Loads environment variables from a .env file
- **Key Features Used**: Loading API keys securely

## Built-in Python Libraries (No Installation Required)

### 1. Base64
```python
import base64
```
- **Documentation**: [base64 — Base16, Base32, Base64 Data Encodings](https://docs.python.org/3/library/base64.html)
- **Purpose**: Encodes binary data to ASCII characters and decodes it back
- **Key Features Used**: Converting images to base64 strings for HTML embedding

### 2. JSON
```python
import json
```
- **Documentation**: [json — JSON encoder and decoder](https://docs.python.org/3/library/json.html)
- **Purpose**: Handles JSON data encoding and decoding
- **Key Features Used**: Parsing API responses, formatting data

### 3. OS
```python
import os
```
- **Documentation**: [os — Miscellaneous operating system interfaces](https://docs.python.org/3/library/os.html)
- **Purpose**: Provides operating system dependent functionality
- **Key Features Used**: File operations, environment variables, path manipulations

### 4. IO (BytesIO)
```python
from io import BytesIO
```
- **Documentation**: [io — Core tools for working with streams](https://docs.python.org/3/library/io.html)
- **Purpose**: Implements file-like objects that work with bytes in memory
- **Key Features Used**: Converting images to bytes for base64 encoding

### 5. URLParse
```python
from urllib.parse import urlparse
```
- **Documentation**: [urllib.parse — Parse URLs into components](https://docs.python.org/3/library/urllib.parse.html)
- **Purpose**: Provides functions for parsing URLs
- **Key Features Used**: URL validation and component extraction

## Installation Command

You can install all required external libraries at once using:
```bash
pip install google-generativeai requests Pillow python-dotenv
```

## Important Notes

1. **Virtual Environment**: It's recommended to create a virtual environment before installing packages:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Version Compatibility**: This project was tested with:
   - Python 3.7+
   - Latest versions of all external libraries as of 2024

3. **.env File**: Create a .env file in your project root with your API key:
   ```
   API_KEY=your_google_api_key_here
   ```

Would you like me to provide more details about any of these libraries or explain how they work together in the project?