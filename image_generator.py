from PIL import Image, ImageDraw, ImageFont
import io
import textwrap
import os

def get_font(size, is_arabic=False):
    # Common font paths inside Debian/Ubuntu containers
    font_paths = [
        "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "arial.ttf"
    ]
    
    if is_arabic:
        # Prioritize Noto Sans Arabic for Arabic text
        font_paths = [
            "/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf",
            "/usr/share/fonts/truetype/noto/NotoNaskhArabic-Regular.ttf",
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
    font_title = get_font(45)
    font_ar = get_font(70, is_arabic=True)
    font_id = get_font(50)
    font_brand = get_font(35)

    # 3. Draw Header (Title)
    draw.text((width/2, 80), title, font=font_title, fill=(80, 80, 80), anchor="mm")
    
    # Draw a divider line
    draw.line([(width*0.1, 150), (width*0.9, 150)], fill=(220, 220, 220), width=2)
    
    current_y = 220
    padding = 80
    max_text_width = width - (padding * 2)
    
    # 4. Draw Arabic Content
    if content_ar:
        # Better wrapping calculation based on font size
        # Approx chars per line for size 70 is about 25-30
        ar_wrapped = textwrap.fill(content_ar, width=30)
        draw.multiline_text((width/2, current_y), ar_wrapped, font=font_ar, fill=(0, 0, 0), anchor="ma", align="center", spacing=20)
        
        # Calculate height taken by Arabic text
        lines = ar_wrapped.split('\n')
        current_y += (len(lines) * 100) + 60

    # 5. Draw Indonesian Content
    if content_id:
        # Approx chars per line for size 50 is about 45-50
        id_wrapped = textwrap.fill(content_id, width=45)
        draw.multiline_text((width/2, current_y), id_wrapped, font=font_id, fill=(60, 60, 60), anchor="ma", align="center", spacing=12)

    # 6. Draw Branding
    if show_branding:
        # Draw bottom footer
        draw.rectangle([(0, height-150), (width, height)], fill=(245, 245, 245))
        draw.text((width/2, height - 75), "Ditemukan via al-Huda", font=font_brand, fill=(0, 103, 91), anchor="mm")

    # 7. Export to Bytes
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()
