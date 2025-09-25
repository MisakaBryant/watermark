import unittest
import os
from PIL import Image
from watermark.watermark_util import add_watermark

class TestTextEffects(unittest.TestCase):
    def setUp(self):
        self.img_path = 'tests/text_effects_base.jpg'
        img = Image.new('RGB', (300, 100), color='gray')
        img.save(self.img_path)

    def tearDown(self):
        if os.path.exists(self.img_path):
            os.remove(self.img_path)
        for f in [
            'tests/wm_shadow_outline.jpg',
            'tests/wm_bold_italic.jpg',
            'tests/wm_color.jpg'
        ]:
            if os.path.exists(f):
                os.remove(f)

    def test_shadow_and_outline(self):
        out_img = add_watermark(
            self.img_path, "阴影描边测试", font_size=32, color="#FF0000", position="center", opacity=90
        )
        out_img.save('tests/wm_shadow_outline.jpg')
        self.assertTrue(os.path.exists('tests/wm_shadow_outline.jpg'))

    def test_bold_italic(self):
        out_img = add_watermark(
            self.img_path, "Bold Italic", font="Arial", font_size=32, bold=True, italic=True, color="#00FF00", position="top_center", opacity=80
        )
        out_img.save('tests/wm_bold_italic.jpg')
        self.assertTrue(os.path.exists('tests/wm_bold_italic.jpg'))

    def test_color(self):
        out_img = add_watermark(
            self.img_path, "彩色水印", font_size=32, color="#0000FF", position="bottom_center", opacity=70
        )
        out_img.save('tests/wm_color.jpg')
        self.assertTrue(os.path.exists('tests/wm_color.jpg'))

if __name__ == '__main__':
    unittest.main()
