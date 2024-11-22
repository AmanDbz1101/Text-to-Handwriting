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


def text_to_handwritten(text, font_path):
    

    # Create an image
    image= Image.open('page_right.webp')
    draw = ImageDraw.Draw(image)

    # Load a font
    font_width= 28
    font = ImageFont.truetype(font_path, font_width)

    max_width = 745# Width of the box
    x=168
    y=113
    wrapped_lines = wrap_text(x, y,text, font, max_width, draw)
    i=0
    for line in wrapped_lines:
        if(y<940):
            draw.text((x, y), line, font=font, fill="black")
            y+=33.5
            
        else:
            # Save and display the image
            image.save(f"handwritten_text_{i}.png")
            image= Image.open('page_right.webp')
            
            draw = ImageDraw.Draw(image)
            y=113
            i+=1
    image.save(f"handwritten_text_{i}.png")
    return i
            

text = st.text_area("Enter your text", height=200)
font_path = "Caveat-Regular.ttf"  # Replace with your handwriting font file
# output_path = "handwritten_text.png"
if text:
    i = text_to_handwritten(text, font_path)

    images =[]
    for a in range(i+1):
        images.append(f"handwritten_text_{a}.png")
        st.image(images[a])
        
    if (i!=0):
        # Open and convert all images to RGB
        image_list = [Image.open(img).convert("RGB") for img in images]

        # Save all images into a single PDF
        image_list[0].save("combined.pdf", save_all=True, append_images=image_list[1:])
    else:
        # Convert to RGB 
        image = Image.open("handwritten_text_0.png").convert("RGB")

        # Save the image as a PDF
        image.save("combined.pdf", "PDF")

 
# PDF content (binary data)
with open("combined.pdf", "rb") as pdf_file:  # Replace with your PDF file path
    pdf_data = pdf_file.read()

# Create a download button
st.download_button(
    label="Download PDF",
    data=pdf_data,
    file_name="Handwritten_text.pdf",  # Name of the file to be downloaded
    mime="application/pdf"    # MIME type for PDFs
)