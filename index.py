from PIL import Image, ImageDraw, ImageFont
import streamlit as st 


def wrap_text(x, y, text, font, max_width, draw):
    """
    Wraps text to fit within a given width.
    """
    lines = []
    sentences= text.split('\n')
    current_line = []
    for sentence in sentences:
        words = sentence.split()  # Split text into words
            
        for word in words:
            # Add the word to the current line and measure its width
            test_line = ' '.join(current_line + [word])
            bbox = draw.textbbox((x, y), test_line, font=font, spacing = 10)
            if (bbox[2]<= max_width):
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]  # Start a new line
        lines.append(' '.join(current_line))
        current_line=[]
    # Add the last line
    if current_line:
        lines.append(' '.join(current_line))

    return lines


def text_to_handwritten(text, font_path, output_path):
    

    # Create an image
    image= Image.open('page_right.webp')
    # image = Image.new('RGB', (1000, 800), 'white')
    draw = ImageDraw.Draw(image)

    # Load a font
    font_width= 28
    font = ImageFont.truetype(font_path, font_width)

    max_width = 745# Width of the box
    x=168
    y=113
    wrapped_lines = wrap_text(x, y,text, font, max_width, draw)

    for line in wrapped_lines:
        if(y<940):
            draw.text((x, y), line, font=font, fill="black")
            y+=33.5

    # Save and display the image
    image.save(output_path)

text = st.text_area("Enter your text")
font_path = "Caveat-Regular.ttf"  # Replace with your handwriting font file
output_path = "handwritten_text.png"

text_to_handwritten(text, font_path, output_path)

st.image(output_path)
