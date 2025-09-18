import argparse
import os
from typing import List

def parse_args():
    parser = argparse.ArgumentParser(description="批量为图片添加拍摄日期水印")
    parser.add_argument("path", help="图片文件或目录路径")
    parser.add_argument("--font-size", type=int, default=32, help="字体大小，默认32")
    parser.add_argument("--color", type=str, default="#FFFFFF", help="水印颜色，默认白色")
    parser.add_argument("--position", type=str, default="right_bottom", choices=["left_top", "center", "right_bottom"], help="水印位置")
    return parser.parse_args()

def scan_images(path: str) -> List[str]:
    exts = {".jpg", ".jpeg", ".png", ".bmp", ".tiff"}
    files = []
    if os.path.isfile(path):
        if os.path.splitext(path)[1].lower() in exts:
            files.append(path)
    else:
        for root, _, filenames in os.walk(path):
            for f in filenames:
                if os.path.splitext(f)[1].lower() in exts:
                    files.append(os.path.join(root, f))
    return files

from watermark.exif_util import get_exif_date
from watermark.watermark_util import add_watermark

def save_watermarked_image(src_path: str, img, out_dir: str):
    # 直接用原图文件名，或可选：保持原目录结构
    out_path = os.path.join(out_dir, os.path.basename(src_path))
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    img.save(out_path)
    return out_path

def main():
    args = parse_args()
    images = scan_images(args.path)
    print(f"共找到 {len(images)} 张图片：")
    if not images:
        print("未找到图片文件。")
        return
    # 输出目录
    if os.path.isfile(args.path):
        base_dir = os.path.dirname(args.path)
    else:
        base_dir = args.path
    out_dir = base_dir.rstrip(os.sep) + "_watermark"
    os.makedirs(out_dir, exist_ok=True)
    for img_path in images:
        date = get_exif_date(img_path)
        if not date:
            print(f"跳过无exif日期的图片: {img_path}")
            continue
        watermarked = add_watermark(
            img_path, date,
            font_size=args.font_size,
            color=args.color,
            position=args.position
        )
        out_path = save_watermarked_image(img_path, watermarked, out_dir)
        print(f"已保存: {out_path}")

if __name__ == "__main__":
    main()
