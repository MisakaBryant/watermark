import unittest
import os
from watermark.main import scan_images

class TestScanImages(unittest.TestCase):
    def test_scan_images_file(self):
        # 假设有一张图片 test.jpg
        with open('tests/test.jpg', 'wb') as f:
            f.write(b'\x00')
        files = scan_images('tests/test.jpg')
        self.assertEqual(len(files), 1)
        os.remove('tests/test.jpg')

    def test_scan_images_dir(self):
        os.makedirs('tests/tmp', exist_ok=True)
        with open('tests/tmp/a.jpg', 'wb') as f:
            f.write(b'\x00')
        with open('tests/tmp/b.txt', 'w') as f:
            f.write('not image')
        files = scan_images('tests/tmp')
        self.assertEqual(len(files), 1)
        os.remove('tests/tmp/a.jpg')
        os.remove('tests/tmp/b.txt')
        os.rmdir('tests/tmp')

if __name__ == '__main__':
    unittest.main()
