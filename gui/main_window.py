import sys

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QListWidget, QListWidgetItem, QFileDialog, QLabel, QAbstractItemView
)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
import os
from PIL import Image

class WatermarkMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Watermark 批量水印工具")
        self.setGeometry(200, 200, 1000, 700)

        self.image_list = []  # 存储图片路径

        # 主布局
        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)


        # 左侧：图片列表
        left_layout = QVBoxLayout()
        self.list_widget = QListWidget()
        self.list_widget.setIconSize(Qt.QSize(100, 100))
        self.list_widget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.list_widget.itemSelectionChanged.connect(self.on_image_selected)
        left_layout.addWidget(QLabel("已导入图片："))
        left_layout.addWidget(self.list_widget)

        btn_layout = QHBoxLayout()
        btn_import = QPushButton("导入图片")
        btn_import.clicked.connect(self.import_images)
        btn_folder = QPushButton("导入文件夹")
        btn_folder.clicked.connect(self.import_folder)
        btn_delete = QPushButton("删除选中")
        btn_delete.clicked.connect(self.delete_selected)
        btn_layout.addWidget(btn_import)
        btn_layout.addWidget(btn_folder)
        btn_layout.addWidget(btn_delete)
        left_layout.addLayout(btn_layout)

        main_layout.addLayout(left_layout, 2)


    # 右侧：预览区 + 水印参数设置
    right_layout = QVBoxLayout()
    self.preview_label = QLabel("预览区")
    self.preview_label.setAlignment(Qt.AlignCenter)
    right_layout.addWidget(self.preview_label)

    # 水印参数设置区
    from PyQt5.QtWidgets import QLineEdit, QSlider, QComboBox, QFormLayout
    param_layout = QFormLayout()
    # 文本内容
    self.text_input = QLineEdit("Watermark")
    self.text_input.textChanged.connect(self.update_preview)
    param_layout.addRow("水印文本：", self.text_input)
    # 透明度
    self.opacity_slider = QSlider(Qt.Horizontal)
    self.opacity_slider.setRange(0, 100)
    self.opacity_slider.setValue(60)
    self.opacity_slider.valueChanged.connect(self.update_preview)
    param_layout.addRow("透明度：", self.opacity_slider)
    # 位置
    self.position_combo = QComboBox()
    self.position_combo.addItems(["左上", "居中", "右下"])
    self.position_combo.currentIndexChanged.connect(self.update_preview)
    param_layout.addRow("位置：", self.position_combo)

    right_layout.addLayout(param_layout)
    main_layout.addLayout(right_layout, 5)
    def get_current_watermark_params(self):
        text = self.text_input.text()
        opacity = self.opacity_slider.value()
        pos_map = {0: "left_top", 1: "center", 2: "right_bottom"}
        position = pos_map.get(self.position_combo.currentIndex(), "right_bottom")
        return text, opacity, position

    def update_preview(self):
        selected = self.list_widget.selectedItems()
        if not selected:
            self.preview_label.clear()
            self.preview_label.setText("预览区")
            return
        item = selected[0]
        img_path = item.data(Qt.UserRole)
        if not img_path or not os.path.isfile(img_path):
            self.preview_label.setText("预览区")
            return
        # 应用水印
        from watermark.watermark_util import add_watermark
        text, opacity, position = self.get_current_watermark_params()
        try:
            watermarked = add_watermark(img_path, text, opacity=opacity, position=position)
            # 转 QPixmap
            import io
            buf = io.BytesIO()
            watermarked.save(buf, format="PNG")
            buf.seek(0)
            qimg = QPixmap()
            qimg.loadFromData(buf.read())
            scaled = qimg.scaled(600, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.preview_label.setPixmap(scaled)
        except Exception as e:
            self.preview_label.setText(f"预览失败: {e}")

        # 支持拖拽导入
        self.setAcceptDrops(True)

    def import_images(self):
        files, _ = QFileDialog.getOpenFileNames(self, "选择图片", "", "图片文件 (*.jpg *.jpeg *.png *.bmp *.tiff)")
        self.add_images(files)

    def import_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "选择文件夹")
        if folder:
            exts = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
            files = [os.path.join(folder, f) for f in os.listdir(folder)
                     if f.lower().endswith(exts)]
            self.add_images(files)

    def add_images(self, files):
        exts = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
        for f in files:
            if not f.lower().endswith(exts):
                continue
            if f not in self.image_list and os.path.isfile(f):
                self.image_list.append(f)
                item = QListWidgetItem(os.path.basename(f))
                item.setData(Qt.UserRole, f)
                thumb = self.make_thumbnail(f)
                if thumb:
                    item.setIcon(QIcon(thumb))
                self.list_widget.addItem(item)

    def make_thumbnail(self, path):
        try:
            img = Image.open(path)
            img.thumbnail((100, 100))
            thumb_path = path + ".thumb.jpg"
            img.save(thumb_path, "JPEG")
            return thumb_path
        except Exception:
            return None

    def on_image_selected(self):
        self.update_preview()

    def delete_selected(self):
        selected = self.list_widget.selectedItems()
        for item in selected:
            row = self.list_widget.row(item)
            img_path = item.data(Qt.UserRole)
            if img_path in self.image_list:
                self.image_list.remove(img_path)
            self.list_widget.takeItem(row)
        self.on_image_selected()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        files = []
        for url in event.mimeData().urls():
            f = url.toLocalFile()
            if os.path.isdir(f):
                exts = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
                files += [os.path.join(f, x) for x in os.listdir(f) if x.lower().endswith(exts)]
            elif os.path.isfile(f):
                files.append(f)
        self.add_images(files)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = WatermarkMainWindow()
    win.show()
    sys.exit(app.exec_())
