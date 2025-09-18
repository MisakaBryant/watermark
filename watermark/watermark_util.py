from PIL import Image, ImageDraw, ImageFont
import os
from typing import Tuple

def add_watermark(
    image_path: str,
    text: str,
    font_size: int = 32,
    color: str = "#FFFFFF",
    position: str = "right_bottom"
) -> Image.Image:
    img = Image.open(image_path).convert("RGBA")
    txt_layer = Image.new("RGBA", img.size, (255,255,255,0))
    draw = ImageDraw.Draw(txt_layer)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except Exception:
        font = ImageFont.load_default()
    text_size = draw.textbbox((0,0), text, font=font)
    w, h = text_size[2] - text_size[0], text_size[3] - text_size[1]
    # 位置计算
    if position == "left_top":
        xy = (10, 10)
    elif position == "center":
        xy = ((img.width - w)//2, (img.height - h)//2)
    else:  # right_bottom
        xy = (img.width - w - 10, img.height - h - 10)
    draw.text(xy, text, font=font, fill=color)
    watermarked = Image.alpha_composite(img, txt_layer)
    return watermarked.convert("RGB")
