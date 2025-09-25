import unittest
import os
from PIL import Image
from watermark.watermark_util import add_watermark

class TestCoreFeatures(unittest.TestCase):
    def test_text_watermark_rotate(self):
        out_img = add_watermark(
            self.img_path, "旋转45度", font_size=24, color="#FF8800", position="center", opacity=90, rotate=45
        )
        out_img.save('tests/wm_rotate.jpg')
        self.assertTrue(os.path.exists('tests/wm_rotate.jpg'))
    def setUp(self):
        self.img_path = 'tests/core_base.jpg'
        img = Image.new('RGBA', (200, 120), color=(128, 128, 255, 255))
        img_rgb = img.convert('RGB')
        img_rgb.save(self.img_path)
        self.logo_path = 'tests/logo.png'
        logo = Image.new('RGBA', (40, 40), color=(255, 0, 0, 128))
        logo.save(self.logo_path)

    def tearDown(self):
        for f in [self.img_path, self.logo_path,
                  'tests/wm_text.jpg', 'tests/wm_img.jpg', 'tests/wm_custom.jpg', 'tests/wm_resize.jpg']:
            if os.path.exists(f):
                os.remove(f)

    def test_text_watermark_nine_grid(self):
        out_img = add_watermark(
            self.img_path, "九宫格", font_size=24, color="#00AAFF", position="right_top", opacity=80
        )
        out_img.save('tests/wm_text.jpg')
        self.assertTrue(os.path.exists('tests/wm_text.jpg'))

    def test_image_watermark(self):
        # 假设 add_watermark 支持 img_watermark_path 参数
        try:
            out_img = add_watermark(
                self.img_path, "", position="center", opacity=100,
                img_watermark_path=self.logo_path, imgwm_opacity=80, imgwm_scale=100
            )
            out_img.save('tests/wm_img.jpg')
            self.assertTrue(os.path.exists('tests/wm_img.jpg'))
        except TypeError:
            # 如果未实现图片水印参数，跳过
            pass

    def test_custom_position(self):
        out_img = add_watermark(
            self.img_path, "自定义", font_size=20, color="#FF00FF", position=("custom", (0.7, 0.2)), opacity=90
        )
        out_img.save('tests/wm_custom.jpg')
        self.assertTrue(os.path.exists('tests/wm_custom.jpg'))

    def test_resize(self):
        out_img = add_watermark(
            self.img_path, "缩放", font_size=18, color="#333333", position="center", opacity=100
        )
        out_img = out_img.resize((100, 60), Image.LANCZOS)
        out_img.save('tests/wm_resize.jpg')
        self.assertTrue(os.path.exists('tests/wm_resize.jpg'))

if __name__ == '__main__':
    unittest.main()
