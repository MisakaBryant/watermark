import unittest
import os
from PIL import Image
import piexif
from watermark.exif_util import get_exif_date

class TestExifUtil(unittest.TestCase):
    def setUp(self):
        # 创建带有exif的测试图片
        self.img_path = 'tests/exif_test.jpg'
        img = Image.new('RGB', (10, 10), color='red')
        exif_dict = {"Exif": {piexif.ExifIFD.DateTimeOriginal: b"2022:09:18 12:34:56"}}
        exif_bytes = piexif.dump(exif_dict)
        img.save(self.img_path, exif=exif_bytes)

    def tearDown(self):
        if os.path.exists(self.img_path):
            os.remove(self.img_path)

    def test_get_exif_date(self):
        date = get_exif_date(self.img_path)
        self.assertEqual(date, "2022-09-18")

if __name__ == '__main__':
    unittest.main()
