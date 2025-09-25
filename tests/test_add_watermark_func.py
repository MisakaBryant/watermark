from watermark.watermark_util import add_watermark
from PIL import Image
import os

def test_add_watermark():
    # 测试图片路径
    img_path = os.path.join(os.path.dirname(__file__), '../photos/test.jpg')
    out_path = os.path.join(os.path.dirname(__file__), '../photos_watermark/test_watermark.jpg')
    # 基本参数
    text = 'Watermark'
    font = '宋体'
    font_size = 32
    bold = True
    italic = False
    color = '#FFFFFF'
    opacity = 80
    rotate = 0
    position = 'right_top'
    imgwm = None
    imgwm_opacity = 60
    imgwm_scale = 100
    # 调用
    img = add_watermark(
        img_path, text,
        font=font, font_size=font_size, bold=bold, italic=italic, color=color,
        opacity=opacity, rotate=rotate, position=position,
        img_watermark_path=imgwm,
        imgwm_opacity=imgwm_opacity, imgwm_scale=imgwm_scale
    )
    img.save(out_path)
    print(f'水印图片已保存到: {out_path}')

def test_add_watermark_visible():
    # 明显可见的水印测试
    img_path = os.path.join(os.path.dirname(__file__), '../photos/test.jpg')
    out_path = os.path.join(os.path.dirname(__file__), '../photos_watermark/test_watermark_visible.jpg')
    text = 'VISIBLE WATERMARK'
    font = 'Arial'
    font_size = 80
    bold = False
    italic = False
    color = '#00FF00'  # 绿色
    opacity = 100
    rotate = 0
    position = 'center'
    imgwm = None
    imgwm_opacity = 100
    imgwm_scale = 100
    img = add_watermark(
        img_path, text,
        font=font, font_size=font_size, bold=bold, italic=italic, color=color,
        opacity=opacity, rotate=rotate, position=position,
        img_watermark_path=imgwm,
        imgwm_opacity=imgwm_opacity, imgwm_scale=imgwm_scale
    )
    img.save(out_path)
    print(f'可见水印图片已保存到: {out_path}')

if __name__ == '__main__':
    test_add_watermark()
    test_add_watermark_visible()
