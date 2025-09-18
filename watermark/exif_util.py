from PIL import Image
import piexif
from datetime import datetime

def get_exif_date(image_path: str) -> str:
    try:
        exif_dict = piexif.load(image_path)
        date_str = exif_dict['Exif'].get(piexif.ExifIFD.DateTimeOriginal)
        if date_str:
            # exif 字节转字符串
            date_str = date_str.decode('utf-8')
            # 只取年月日
            dt = datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
            return dt.strftime("%Y-%m-%d")
    except Exception:
        pass
    return None
