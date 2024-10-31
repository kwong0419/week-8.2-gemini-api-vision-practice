# Function Flow and Data Connections

## Sequential Program Flow

**Note:** You are note required to use these functions or the exact layout of the functions. However, you will want to use the `setup_api()` function to initialize the API and get the model.

### 1. Program Initialization
```
main() → setup_api()
```
- `setup_api()` initializes and returns configured Gemini model
- This model instance is stored in main() for later use
- Required before any AI operations can occur

### 2. First Image Processing
```
main() → download_and_validate_image(url1, filename1)
    → is_valid_url(url1) validates URL format
    → validate_file(filename1) checks extension
    → download_file(url1, filename1) retrieves image
```
- Returns path to first downloaded image
- Path is stored in main() as image1_path
- Any failure stops program with error message

### 3. Second Image Processing
```
main() → download_and_validate_image(url2, filename2)
    → is_valid_url(url2) validates URL format
    → validate_file(filename2) checks extension
    → download_file(url2, filename2) retrieves image
```
- Returns path to second downloaded image
- Path is stored in main() as image2_path
- Uses same validation chain as first image

### 4. Palette Generation
```
main() → generate_palette(model, image1_path, image2_path)
```
- Uses model from setup_api()
- Uses both image paths from previous steps
- Returns palette_data JSON containing:
  - Color strategy
  - Color hex codes
  - Color sources
  - Usage recommendations

### 5. HTML Report Creation
```
main() → generate_html_report(image1_path, image2_path, palette_data)
    → image_to_base64(image1_path) converts first image
    → image_to_base64(image2_path) converts second image
    → create_palette_visualization(palette_data) creates color strip
    → generate_color_details(palette_data) creates color descriptions
```
- Combines all previous data into final HTML report
- Returns complete HTML string ready to save

### 6. File Operations and Cleanup
```
main() 
    → writes HTML report to file
    → removes downloaded images
```
- Saves final report
- Cleans up temporary image files
- Provides success message

## Data Flow Between Functions

### Image Data Flow:
```
URL → downloaded file → PIL Image → base64 string → HTML embedding
```

### Color Data Flow:
```
Images → AI analysis → JSON palette data → visual palette → HTML color details
```

### Report Assembly Flow:
```
All components → HTML template → formatted report → saved file
```

## Key Connection Points

1. **API Model Usage**
   - Created in setup_api()
   - Used in generate_palette()
   - Links initialization to analysis

2. **Image Paths**
   - Created in download_and_validate_image()
   - Used in:
     - generate_palette()
     - generate_html_report()
     - image_to_base64()
   - Finally removed in cleanup

3. **Palette Data**
   - Generated in generate_palette()
   - Used in:
     - create_palette_visualization()
     - generate_color_details()
     - generate_html_report()

4. **Base64 Images**
   - Created from both original images and palette
   - All combined in final HTML report

This flow ensures that:
- Each function has necessary inputs when called
- Data transformations happen in logical order
- Resources are properly managed
- Dependencies are clearly defined

Would you like me to expand on any particular connection or flow in more detail?