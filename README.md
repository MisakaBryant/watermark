# Watermark CLI Tool

本项目是一个命令行工具，可批量为图片添加拍摄日期水印。

## 功能
- 递归扫描指定目录下所有图片文件
- 读取图片 EXIF 拍摄时间，提取年月日作为水印
- 支持自定义字体大小、颜色和水印位置（左上、居中、右下）
- 处理后图片保存到原目录名_watermark 子目录

## 安装依赖
```bash
pip install pillow piexif
```

## 使用方法
```bash
python -m watermark.main <图片或目录路径> [--font-size 32] [--color "#FFFFFF"] [--position right_bottom]
```

- `--font-size`：字体大小，默认32
- `--color`：水印颜色，默认白色
- `--position`：水印位置，可选 left_top/center/right_bottom，默认 right_bottom

## 示例
```bash
python -m watermark.main ./photos --font-size 40 --color "#FF0000" --position center
```

## 测试
```bash
python -m unittest discover tests
```

---

