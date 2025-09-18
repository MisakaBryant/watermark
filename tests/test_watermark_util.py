import unittest
import os
from PIL import Image
from watermark.watermark_util import add_watermark

class TestWatermarkUtil(unittest.TestCase):
    def setUp(self):
        self.img_path = 'tests/wm_test.jpg'
        img = Image.new('RGB', (100, 100), color='blue')
        img.save(self.img_path)

    def tearDown(self):
        if os.path.exists(self.img_path):
            os.remove(self.img_path)
        if os.path.exists('tests/wm_out.jpg'):
            os.remove('tests/wm_out.jpg')

    def test_add_watermark(self):
        out_img = add_watermark(self.img_path, "2025-09-18", font_size=20, color="#FF0000", position="center")
        out_img.save('tests/wm_out.jpg')
        self.assertTrue(os.path.exists('tests/wm_out.jpg'))

if __name__ == '__main__':
    unittest.main()
