from PIL import Image, ImageDraw, ImageFont
import io
import textwrap

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
    
    # 2. Setup Fonts (Standard Fallbacks)
    try:
        # Mencoba menggunakan font sistem
        font_title = ImageFont.truetype("arial.ttf", 40)
        font_ar = ImageFont.truetype("arial.ttf", 60) # Note: Idealnya font khusus Naskh
        font_id = ImageFont.truetype("arial.ttf", 45)
        font_brand = ImageFont.truetype("arial.ttf", 30)
    except:
        font_title = ImageFont.load_default()
        font_ar = ImageFont.load_default()
        font_id = ImageFont.load_default()
        font_brand = ImageFont.load_default()

    # 3. Draw Header (Title)
    draw.text((width/2, 100), title, font=font_title, fill=(100, 100, 100), anchor="mm")
    
    current_y = 250
    
    # 4. Draw Arabic Content
    if content_ar:
        # Sederhana wrapping untuk Arab (Reverse order normally needed for RTL, 
        # but Pillow handling depends on version/OS)
        ar_wrapped = textwrap.fill(content_ar, width=40)
        draw.multiline_text((width/2, current_y), ar_wrapped, font=font_ar, fill=(0, 0, 0), anchor="ma", align="center")
        current_y += (len(ar_wrapped.split('\n')) * 80) + 50

    # 5. Draw Indonesian Content
    if content_id:
        id_wrapped = textwrap.fill(content_id, width=45)
        draw.multiline_text((width/2, current_y), id_wrapped, font=font_id, fill=(50, 50, 50), anchor="ma", align="center")

    # 6. Draw Branding
    if show_branding:
        draw.text((width/2, height - 80), "tanyaquran.id", font=font_brand, fill=(0, 103, 91), anchor="mm")

    # 7. Export to Bytes
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()
