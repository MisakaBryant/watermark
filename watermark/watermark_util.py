from PIL import Image, ImageDraw, ImageFont
import os
from typing import Tuple

def add_watermark(
    image_path: str,
    text: str,
    font_size: int = 32,
    color: str = "#FFFFFF",
    position: str = "right_bottom",
    opacity: int = 60
) -> Image.Image:
    """
    opacity: 0-100, 100为不透明
    """
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
    # 透明度处理
    if color.startswith("#") and len(color) == 7:
        rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
    else:
        rgb = (255,255,255)
    fill = rgb + (int(255 * opacity / 100),)
    draw.text(xy, text, font=font, fill=fill)
    watermarked = Image.alpha_composite(img, txt_layer)
    return watermarked.convert("RGB")
