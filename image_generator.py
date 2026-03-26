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
    
    # 2. Dynamic Sizing Logic
    total_chars = len(content_ar) + len(content_id)
    
    # Base sizes for short text
    size_ar = 65
    size_id = 45
    wrap_ar = 30
    wrap_id = 50
    
    # Shrink if text is long
    if total_chars > 1000:
        size_ar, size_id = 35, 28
        wrap_ar, wrap_id = 50, 75
    elif total_chars > 500:
        size_ar, size_id = 45, 35
        wrap_ar, wrap_id = 40, 60
        
    font_title = get_font(35)
    font_ar = get_font(size_ar, is_arabic=True)
    font_id = get_font(size_id)
    font_brand = get_font(30)

    # 3. Draw Header
    draw.text((width/2, 60), title, font=font_title, fill=(120, 120, 120), anchor="mm")
    draw.line([(width*0.1, 110), (width*0.9, 110)], fill=(230, 230, 230), width=2)
    
    current_y = 160
    
    # 4. Draw Arabic Content
    if content_ar:
        ar_lines = textwrap.wrap(content_ar, width=wrap_ar)
        processed_ar_lines = []
        for line in ar_lines:
            processed_ar_lines.append(get_display(arabic_reshaper.reshape(line)))
        
        ar_display_text = "\n".join(processed_ar_lines)
        draw.multiline_text((width/2, current_y), ar_display_text, font=font_ar, fill=(0, 0, 0), anchor="ma", align="center", spacing=15)
        
        # Calculate dynamic height
        current_y += (len(processed_ar_lines) * (size_ar + 15)) + 40

    # 5. Draw Indonesian Content
    if content_id:
        id_wrapped = textwrap.fill(content_id, width=wrap_id)
        # Check if still fits, if not, truncate with ellipsis
        max_id_height = (height - 180) - current_y
        id_lines = id_wrapped.split('\n')
        
        # If too many lines for remaining space, we might need to truncate
        estimated_height = len(id_lines) * (size_id + 10)
        if estimated_height > max_id_height:
            allowed_lines = int(max_id_height / (size_id + 10)) - 1
            id_wrapped = "\n".join(id_lines[:allowed_lines]) + "..."

        draw.multiline_text((width/2, current_y), id_wrapped, font=font_id, fill=(60, 60, 60), anchor="ma", align="center", spacing=10)

    # 6. Draw Branding
    if show_branding:
        draw.rectangle([(0, height-120), (width, height)], fill=(248, 249, 250))
        draw.text((width/2, height - 60), "Ditemukan via al-Huda (al-huda.masmuf.cloud)", font=font_brand, fill=(0, 103, 91), anchor="mm")

    # 7. Export to Bytes
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()
