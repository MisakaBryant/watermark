from PIL import Image, ImageDraw, ImageFont
import os
from typing import Tuple

def add_watermark(
    image_path: str,
    text: str,
    font: str = "Arial",
    font_size: int = 32,
    bold: bool = False,
    italic: bool = False,
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
    # 字体文件查找
    font_path = None
    import platform
    sys_plat = platform.system()
    font_name = font if font else "Arial"
    if sys_plat == "Windows":
        base = os.environ.get("WINDIR", "C:\\Windows") + "\\Fonts\\"
        # 常见字体映射
        font_candidates = [
            f"{font_name}.ttf", f"{font_name}.TTF", f"{font_name}.otf", f"{font_name}.OTF",
            f"{font_name} Bold.ttf", f"{font_name} Italic.ttf", f"{font_name} Bold Italic.ttf"
        ]
        for cand in font_candidates:
            p = os.path.join(base, cand)
            if os.path.exists(p):
                font_path = p
                break
    elif sys_plat == "Darwin":
        base = "/Library/Fonts/"
        font_candidates = [f"{font_name}.ttf", f"{font_name}.otf"]
        for cand in font_candidates:
            p = os.path.join(base, cand)
            if os.path.exists(p):
                font_path = p
                break
    # Linux/其它
    if not font_path:
        font_path = None
    # 字体样式
    try:
        if font_path:
            font_obj = ImageFont.truetype(font_path, font_size)
        else:
            font_obj = ImageFont.truetype(font_name, font_size)
    except Exception:
        font_obj = ImageFont.load_default()
    # PIL 不直接支持粗体/斜体，部分字体可用
    text_size = draw.textbbox((0,0), text, font=font_obj)
    w, h = text_size[2] - text_size[0], text_size[3] - text_size[1]
    # 九宫格九点布局
    margin = 10
    if position == "left_top":
        xy = (margin, margin)
    elif position == "top_center":
        xy = ((img.width - w)//2, margin)
    elif position == "right_top":
        xy = (img.width - w - margin, margin)
    elif position == "left_center":
        xy = (margin, (img.height - h)//2)
    elif position == "center":
        xy = ((img.width - w)//2, (img.height - h)//2)
    elif position == "right_center":
        xy = (img.width - w - margin, (img.height - h)//2)
    elif position == "left_bottom":
        xy = (margin, img.height - h - margin)
    elif position == "bottom_center":
        xy = ((img.width - w)//2, img.height - h - margin)
    else:  # right_bottom
        xy = (img.width - w - margin, img.height - h - margin)
    # 透明度处理
    if color.startswith("#") and len(color) == 7:
        rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
    else:
        rgb = (255,255,255)
    fill = rgb + (int(255 * opacity / 100),)
    draw.text(xy, text, font=font_obj, fill=fill)
    watermarked = Image.alpha_composite(img, txt_layer)
    return watermarked.convert("RGB")
