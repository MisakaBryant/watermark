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

def main():
    args = parse_args()
    images = scan_images(args.path)
    print(f"共找到 {len(images)} 张图片：")
    for img in images:
        print(img)

if __name__ == "__main__":
    main()
