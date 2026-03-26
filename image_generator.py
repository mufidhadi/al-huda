from PIL import Image, ImageDraw, ImageFont
import io
import textwrap
import os
import arabic_reshaper
from bidi.algorithm import get_display

def get_font(size, is_arabic=False):
    # Use fonts bundled with the project
    font_paths = [
        "NotoSans-Regular.ttf",
        "arial.ttf"
    ]
    
    if is_arabic:
        font_paths = [
            "NotoSansArabic-Regular.ttf",
        ] + font_paths

    for path in font_paths:
        try:
            return ImageFont.truetype(path, size)
        except:
            continue
    
    return ImageFont.load_default()

def generate_share_image(
    title: str, 
    content_ar: str = "", 
    content_id: str = "", 
    show_branding: bool = True
):
    # 1. Setup Canvas (1080x1080)
    width, height = 1080, 1080
    bg_color = (255, 255, 255)
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)
    
    # 2. Setup Fonts
    font_title = get_font(40)
    font_ar = get_font(65, is_arabic=True)
    font_id = get_font(45)
    font_brand = get_font(35)

    # 3. Draw Header (Title)
    draw.text((width/2, 80), title, font=font_title, fill=(100, 100, 100), anchor="mm")
    
    # Draw a divider line
    draw.line([(width*0.1, 150), (width*0.9, 150)], fill=(220, 220, 220), width=2)
    
    current_y = 200
    padding = 100
    
    # 4. Draw Arabic Content
    if content_ar:
        # Reshape and handle Bidi
        reshaped_text = arabic_reshaper.reshape(content_ar)
        bidi_text = get_display(reshaped_text)
        
        # Wrapping Arabic text manually since textwrap doesn't understand Bidi order well
        # We wrap the ORIGINAL text first, then process each line
        ar_lines = textwrap.wrap(content_ar, width=35)
        processed_ar_lines = []
        for line in ar_lines:
            processed_ar_lines.append(get_display(arabic_reshaper.reshape(line)))
        
        ar_display_text = "\n".join(processed_ar_lines)
        
        draw.multiline_text((width/2, current_y), ar_display_text, font=font_ar, fill=(0, 0, 0), anchor="ma", align="center", spacing=25)
        
        # Calculate height taken by Arabic text
        current_y += (len(processed_ar_lines) * 95) + 60

    # 5. Draw Indonesian Content
    if content_id:
        id_wrapped = textwrap.fill(content_id, width=50)
        draw.multiline_text((width/2, current_y), id_wrapped, font=font_id, fill=(60, 60, 60), anchor="ma", align="center", spacing=15)

    # 6. Draw Branding
    if show_branding:
        draw.rectangle([(0, height-150), (width, height)], fill=(245, 245, 245))
        draw.text((width/2, height - 75), "Ditemukan via al-Huda", font=font_brand, fill=(0, 103, 91), anchor="mm")

    # 7. Export to Bytes
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()
