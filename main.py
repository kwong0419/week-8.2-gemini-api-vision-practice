# Imports
import os
import json
import base64
import requests
from io import BytesIO
from PIL import Image, ImageDraw
from dotenv import load_dotenv
from urllib.parse import urlparse
import google.generativeai as genai

def setup_api():
    """Initialize API and get model"""
    try:
        load_dotenv()
        api_key = os.getenv('API_KEY')
        if not api_key:
            raise ValueError("API_KEY not found in environment variables")
        
        genai.configure(api_key=api_key)
        
        # Create the model with configuration
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            safety_settings=[],
            generation_config={
                "temperature": 0.7,
                "top_p": 1,
                "top_k": 32,
                "max_output_tokens": 2048,
            }
        )
        
        return model
        
    except Exception as e:
        raise Exception(f"Failed to setup API: {str(e)}")

def is_valid_url(url_string):
    """Validate if string is a proper URL"""
    try:
        result = urlparse(url_string)
        return all([result.scheme, result.netloc])
    except:
        return False

def validate_file(filename):
    """Validate file extension"""
    allowed_extensions = ['.jpg', '.jpeg', '.png', '.gif']
    ext = os.path.splitext(filename)[1].lower()
    return ext in allowed_extensions

def download_file(url, local_filename):
    """Download file from URL"""
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return local_filename
    except Exception as e:
        raise Exception(f"Failed to download file: {str(e)}")

def download_and_validate_image(url, filename):
    """Download and validate an image from URL"""
    if not is_valid_url(url):
        raise ValueError("Invalid URL format")
    
    if not validate_file(filename):
        raise ValueError("Invalid file extension")
    
    return download_file(url, filename)

def generate_palette(model, image1_path, image2_path, n_colors=5):
    """Generate color palette"""
    try:
        # Open images
        img1 = Image.open(image1_path)
        img2 = Image.open(image2_path)
        
        # Create prompt for the model
        prompt = """Analyze these two images and create a color palette. Return your response in this exact JSON format:
        {
            "strategy": "Brief explanation of color selection strategy",
            "colors": [
                {
                    "hex": "#HEXCODE",
                    "source": "image1",
                    "description": "Brief color description",
                    "usage": "Suggested usage"
                }
            ]
        }
        Extract 2 colors from first image, 2 from second image, and create 1 blended color."""

        # Get response from model
        response = model.generate_content([prompt, img1, img2])
        
        # Extract the JSON string from the response text
        # Look for JSON structure between curly braces
        response_text = response.text
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1
        json_str = response_text[json_start:json_end]
        
        # Parse JSON
        palette_data = json.loads(json_str)
        return palette_data
        
    except Exception as e:
        raise Exception(f"Failed to generate palette: {str(e)}")

def create_palette_visualization(palette_data):
    """Create palette swatch"""
    try:
        colors = [color["hex"] for color in palette_data["colors"]]
        width = 500
        height = 100
        
        # Create new image
        img = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(img)
        
        # Draw color rectangles
        section_width = width // len(colors)
        for i, color in enumerate(colors):
            draw.rectangle(
                [i * section_width, 0, (i + 1) * section_width, height],
                fill=color
            )
        
        # Convert to base64
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode()
        
    except Exception as e:
        raise Exception(f"Failed to create palette visualization: {str(e)}")

def image_to_base64(image_path):
    """Convert image to base64 string"""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except Exception as e:
        raise Exception(f"Failed to convert image to base64: {str(e)}")

def generate_color_details(palette_data):
    """Generate HTML for color details"""
    html = ""
    for color in palette_data["colors"]:
        html += f"""
        <div class="palette-info">
            <div class="color-box" style="background-color: {color['hex']}"></div>
            <div>
                <strong>Hex Code:</strong> {color['hex']}<br>
                <strong>Source:</strong> {color['source']}<br>
                <strong>Description:</strong> {color['description']}<br>
                <strong>Suggested Usage:</strong> {color['usage']}
            </div>
        </div>
        """
    return html

def generate_html_report(image1_path, image2_path, palette_data):
    """Generate HTML report with all components"""
    try:
        # Get base64 strings
        img1_base64 = image_to_base64(image1_path)
        img2_base64 = image_to_base64(image2_path)
        palette_base64 = create_palette_visualization(palette_data)
        
        # Read HTML template
        with open('html-skeleton.html', 'r') as f:
            template = f.read()
        
        # Replace placeholders
        html = template.replace('REPLACE_WITH_BASE64_IMAGE1', f'data:image/jpeg;base64,{img1_base64}')
        html = html.replace('REPLACE_WITH_BASE64_IMAGE2', f'data:image/jpeg;base64,{img2_base64}')
        html = html.replace('REPLACE_WITH_BASE64_PALETTE', f'data:image/png;base64,{palette_base64}')
        html = html.replace('REPLACE_WITH_STRATEGY', palette_data['strategy'])
        
        # Insert color details
        color_details = generate_color_details(palette_data)
        html = html.replace('<!-- Additional color details will be generated here -->', color_details)
        
        return html
        
    except Exception as e:
        raise Exception(f"Failed to generate HTML report: {str(e)}")

def main():
    try:
        # Initialize API and get model
        model = setup_api()
        
        #Get URLs and filenames from user
        # Get first image
        url1 = input("Enter the URL for the first image: ")
        filename1 = "image1.jpg"
        image1_path = download_and_validate_image(url1, filename1)
        print("First image downloaded successfully!")
        
        # Get second image
        url2 = input("Enter the URL for the second image: ")
        filename2 = "image2.jpg"
        image2_path = download_and_validate_image(url2, filename2)
        print("Second image downloaded successfully!")
        
        # Generate palette
        print("Analyzing images and generating palette...")
        palette_data = generate_palette(model, image1_path, image2_path)
        
        # Generate HTML report
        print("Generating HTML report...")
        html_content = generate_html_report(image1_path, image2_path, palette_data)
        
        # Get output filename
        output_file = input("Enter the output filename (with .html extension): ")
        
        # Save HTML report
        with open(output_file, 'w') as f:
            f.write(html_content)
        
        # Remove downloaded images
        os.remove(image1_path)
        os.remove(image2_path)
        
        print(f"Report generated successfully! Check {output_file}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
