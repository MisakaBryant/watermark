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
    opacity: int = 60,
    rotate: int = 0,
    img_watermark_path: str = None,
    imgwm_opacity: int = 60,
    imgwm_scale: int = 100
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
    # 先计算文本尺寸
    text_bbox = draw.textbbox((0,0), text, font=font_obj)
    w, h = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
    # 增加padding，防止阴影/描边/旋转裁剪
    padding = 20
    w_pad, h_pad = w + 2*padding, h + 2*padding
    # 若旋转，需计算旋转后尺寸
    if rotate:
        import math
        rad = math.radians(rotate)
        cosv, sinv = abs(math.cos(rad)), abs(math.sin(rad))
        w_rot = int(w_pad * cosv + h_pad * sinv)
        h_rot = int(w_pad * sinv + h_pad * cosv)
        w_img, h_img = w_rot, h_rot
    else:
        w_img, h_img = w_pad, h_pad
    # 九宫格九点布局
    margin = 10
    if position == "left_top":
        xy = (margin, margin)
    elif position == "top_center":
        xy = ((img.width - w_img)//2, margin)
    elif position == "right_top":
        xy = (img.width - w_img - margin, margin)
    elif position == "left_center":
        xy = (margin, (img.height - h_img)//2)
    elif position == "center":
        xy = ((img.width - w_img)//2, (img.height - h_img)//2)
    elif position == "right_center":
        xy = (img.width - w_img - margin, (img.height - h_img)//2)
    elif position == "left_bottom":
        xy = (margin, img.height - h_img - margin)
    elif position == "bottom_center":
        xy = ((img.width - w_img)//2, img.height - h_img - margin)
    else:  # right_bottom
        xy = (img.width - w_img - margin, img.height - h_img - margin)
    # 透明度处理
    if color.startswith("#") and len(color) == 7:
        rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
    else:
        rgb = (255,255,255)
    fill = rgb + (int(255 * opacity / 100),)
    # 阴影和描边参数
    shadow_offset = 2
    outline_width = 2
    # 先在独立图层绘制文本（便于旋转）
    text_img = Image.new("RGBA", (w_pad, h_pad), (255,255,255,0))
    text_draw = ImageDraw.Draw(text_img)
    # 阴影（黑色半透明）
    shadow_fill = (0, 0, 0, int(255 * opacity / 100 * 0.6))
    text_draw.text((padding+shadow_offset, padding+shadow_offset), text, font=font_obj, fill=shadow_fill)
    # 描边（白色/黑色，自动判断）
    outline_color = (0, 0, 0, int(255 * opacity / 100)) if sum(fill[:3]) > 400 else (255, 255, 255, int(255 * opacity / 100))
    for dx in range(-outline_width, outline_width+1):
        for dy in range(-outline_width, outline_width+1):
            if dx == 0 and dy == 0:
                continue
            text_draw.text((padding+shadow_offset+dx, padding+shadow_offset+dy), text, font=font_obj, fill=outline_color)
    # 正文
    text_draw.text((padding, padding), text, font=font_obj, fill=fill)
    # 旋转
    if rotate:
        text_img = text_img.rotate(rotate, expand=1, resample=Image.BICUBIC)
    # 粘贴到 txt_layer
    txt_layer.alpha_composite(text_img, dest=xy)

    # 图片水印
    if img_watermark_path and os.path.isfile(img_watermark_path):
        try:
            wm_img = Image.open(img_watermark_path).convert("RGBA")
            # 缩放
            if imgwm_scale != 100:
                w = int(wm_img.width * imgwm_scale / 100)
                h = int(wm_img.height * imgwm_scale / 100)
                wm_img = wm_img.resize((w, h), Image.LANCZOS)
            # 透明度
            if imgwm_opacity < 100:
                alpha = wm_img.split()[-1].point(lambda p: int(p * imgwm_opacity / 100))
                wm_img.putalpha(alpha)
            # 位置与文本水印一致
            wm_xy = xy
            # 粘贴
            txt_layer.alpha_composite(wm_img, dest=wm_xy)
        except Exception:
            pass

    watermarked = Image.alpha_composite(img, txt_layer)
    return watermarked.convert("RGB")
