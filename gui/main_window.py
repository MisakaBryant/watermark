import sys

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QListWidget, QListWidgetItem, QFileDialog, QLabel, QAbstractItemView,
    QLineEdit, QSlider, QComboBox, QFormLayout, QGroupBox, QRadioButton, QButtonGroup, QMessageBox
    , QFontComboBox, QColorDialog, QSpinBox, QCheckBox
)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
import os
from PIL import Image

class WatermarkMainWindow(QMainWindow):
    # ...existing code...
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

        # 拖拽相关
        self.custom_pos = None  # (x, y) 归一化坐标
        self.dragging = False

        # ...existing code...

        # 右侧：预览区 + 水印参数设置
        right_layout = QVBoxLayout()
        self.preview_label = QLabel("预览区")
        self.preview_label.setAlignment(Qt.AlignCenter)
        # 拖拽事件绑定
        self.preview_label.mousePressEvent = self.on_preview_mouse_press
        self.preview_label.mouseMoveEvent = self.on_preview_mouse_move
        self.preview_label.mouseReleaseEvent = self.on_preview_mouse_release
        right_layout.addWidget(self.preview_label)
    def on_preview_mouse_press(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self._drag_start = event.pos()

    def on_preview_mouse_move(self, event):
        if self.dragging:
            pos = event.pos()
            # 计算归一化坐标
            x = pos.x() / self.preview_label.width()
            y = pos.y() / self.preview_label.height()
            self.custom_pos = (x, y)
            # 切换为“自定义”位置
            if self.position_combo.findText("自定义") == -1:
                self.position_combo.addItem("自定义")
            self.position_combo.setCurrentText("自定义")
            self.update_preview()

    def on_preview_mouse_release(self, event):
        self.dragging = False
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
        param_layout = QFormLayout()
        # 文本内容
        self.text_input = QLineEdit("Watermark")
        self.text_input.textChanged.connect(self.update_preview)
        param_layout.addRow("水印文本：", self.text_input)
        # 字体
        self.font_combo = QFontComboBox()
        self.font_combo.currentFontChanged.connect(self.update_preview)
        param_layout.addRow("字体：", self.font_combo)
        # 字号
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 128)
        self.font_size_spin.setValue(32)
        self.font_size_spin.valueChanged.connect(self.update_preview)
        param_layout.addRow("字号：", self.font_size_spin)
        # 粗体
        self.bold_check = QCheckBox("粗体")
        self.bold_check.stateChanged.connect(self.update_preview)
        param_layout.addRow(self.bold_check)
        # 斜体
        self.italic_check = QCheckBox("斜体")
        self.italic_check.stateChanged.connect(self.update_preview)
        param_layout.addRow(self.italic_check)
        # 颜色
        self.color_btn = QPushButton("选择颜色")
        self.color_btn.clicked.connect(self.choose_text_color)
        self.text_color = "#FFFFFF"
        param_layout.addRow("字体颜色：", self.color_btn)
        # 透明度
        self.opacity_slider = QSlider(Qt.Horizontal)
        self.opacity_slider.setRange(0, 100)
        self.opacity_slider.setValue(60)
        self.opacity_slider.valueChanged.connect(self.update_preview)
        param_layout.addRow("透明度：", self.opacity_slider)
        # 位置
        self.position_combo = QComboBox()
        self.position_combo.addItems([
            "左上", "上中", "右上",
            "左中", "居中", "右中",
            "左下", "下中", "右下"
        ])
        self.position_combo.currentIndexChanged.connect(self.on_position_changed)
        param_layout.addRow("位置：", self.position_combo)

    def on_position_changed(self):
        # 切换九宫格时清除自定义坐标
        if self.position_combo.currentText() != "自定义":
            self.custom_pos = None
        self.update_preview()
        right_layout.addLayout(param_layout)

    def choose_text_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.text_color = color.name()
            self.update_preview()

        # 图片水印设置区
        imgwm_group = QGroupBox("图片水印（可选）")
        imgwm_layout = QFormLayout()
        self.imgwm_path = QLineEdit()
        btn_choose_imgwm = QPushButton("选择图片")
        btn_choose_imgwm.clicked.connect(self.choose_imgwm)
        imgwm_path_layout = QHBoxLayout()
        imgwm_path_layout.addWidget(self.imgwm_path)
        imgwm_path_layout.addWidget(btn_choose_imgwm)
        imgwm_layout.addRow("水印图片：", imgwm_path_layout)
        self.imgwm_opacity = QSlider(Qt.Horizontal)
        self.imgwm_opacity.setRange(0, 100)
        self.imgwm_opacity.setValue(60)
        self.imgwm_opacity.valueChanged.connect(self.update_preview)
        imgwm_layout.addRow("图片透明度：", self.imgwm_opacity)
        self.imgwm_scale = QSlider(Qt.Horizontal)
        self.imgwm_scale.setRange(10, 200)
        self.imgwm_scale.setValue(100)
        self.imgwm_scale.valueChanged.connect(self.update_preview)
        imgwm_layout.addRow("缩放(%)：", self.imgwm_scale)
        imgwm_group.setLayout(imgwm_layout)
        right_layout.addWidget(imgwm_group)

        # 导出设置区
        export_group = QGroupBox("导出设置")
        export_layout = QFormLayout()
        # 输出文件夹
        self.output_dir_edit = QLineEdit()
        btn_choose_dir = QPushButton("选择...")
        btn_choose_dir.clicked.connect(self.choose_output_dir)
        dir_layout = QHBoxLayout()
        dir_layout.addWidget(self.output_dir_edit)
        dir_layout.addWidget(btn_choose_dir)
        export_layout.addRow("输出文件夹：", dir_layout)
        # 命名规则
        self.naming_prefix = QLineEdit("wm_")
        self.naming_suffix = QLineEdit("")
        export_layout.addRow("前缀：", self.naming_prefix)
        export_layout.addRow("后缀：", self.naming_suffix)
        # 输出格式
        self.format_group = QButtonGroup()
        radio_jpg = QRadioButton("JPEG")
        radio_png = QRadioButton("PNG")
        self.format_group.addButton(radio_jpg, 0)
        self.format_group.addButton(radio_png, 1)
        radio_jpg.setChecked(True)
        fmt_layout = QHBoxLayout()
        fmt_layout.addWidget(radio_jpg)
        fmt_layout.addWidget(radio_png)
        export_layout.addRow("输出格式：", fmt_layout)

        # JPEG 质量调节
        self.quality_slider = QSlider(Qt.Horizontal)
        self.quality_slider.setRange(10, 100)
        self.quality_slider.setValue(90)
        self.quality_slider.setTickInterval(10)
        self.quality_slider.setTickPosition(QSlider.TicksBelow)
        export_layout.addRow("JPEG质量：", self.quality_slider)

        # 尺寸缩放设置
        self.resize_mode_combo = QComboBox()
        self.resize_mode_combo.addItems(["不缩放", "按宽度", "按高度", "按百分比"])
        self.resize_value = QLineEdit()
        self.resize_value.setPlaceholderText("数值，如800 或 50")
        resize_layout = QHBoxLayout()
        resize_layout.addWidget(self.resize_mode_combo)
        resize_layout.addWidget(self.resize_value)
        export_layout.addRow("尺寸调整：", resize_layout)
        export_group.setLayout(export_layout)
        right_layout.addWidget(export_group)

        # 导出按钮
        btn_export = QPushButton("批量导出水印图片")
        btn_export.clicked.connect(self.export_images)
        right_layout.addWidget(btn_export)

        # 模板管理区
        template_group = QGroupBox("水印模板管理")
        template_layout = QHBoxLayout()
        self.template_combo = QComboBox()
        self.load_templates()
        btn_save_tpl = QPushButton("保存模板")
        btn_save_tpl.clicked.connect(self.save_template)
        btn_load_tpl = QPushButton("加载模板")
        btn_load_tpl.clicked.connect(self.load_selected_template)
        btn_del_tpl = QPushButton("删除模板")
        btn_del_tpl.clicked.connect(self.delete_selected_template)
        template_layout.addWidget(self.template_combo)
        template_layout.addWidget(btn_save_tpl)
        template_layout.addWidget(btn_load_tpl)
        template_layout.addWidget(btn_del_tpl)
        template_group.setLayout(template_layout)
        right_layout.addWidget(template_group)

        # 自动加载上次设置
        self.load_last_template()

        main_layout.addLayout(right_layout, 5)

    def choose_imgwm(self):
        path, _ = QFileDialog.getOpenFileName(self, "选择水印图片", "", "图片文件 (*.png *.jpg *.jpeg *.bmp *.tiff)")
        if path:
            self.imgwm_path.setText(path)
            self.update_preview()

    def get_template_path(self):
        import os
        return os.path.join(os.path.expanduser("~"), ".watermark_templates.json")

    def load_templates(self):
        import json
        self.templates = {}
        path = self.get_template_path()
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                self.templates = json.load(f)
        self.template_combo.clear()
        self.template_combo.addItems(self.templates.keys())

    def save_template(self):
        import json
        name, ok = QFileDialog.getSaveFileName(self, "模板名", "", "*.tpl")
        if not ok or not name:
            return
        tpl = {
            "text": self.text_input.text(),
            "opacity": self.opacity_slider.value(),
            "position": self.position_combo.currentIndex(),
            "prefix": self.naming_prefix.text(),
            "suffix": self.naming_suffix.text(),
            "format": self.format_group.checkedId()
        }
        self.templates[os.path.basename(name)] = tpl
        with open(self.get_template_path(), "w", encoding="utf-8") as f:
            json.dump(self.templates, f, ensure_ascii=False, indent=2)
        self.load_templates()

    def load_selected_template(self):
        name = self.template_combo.currentText()
        if not name or name not in self.templates:
            return
        tpl = self.templates[name]
        self.text_input.setText(tpl.get("text", ""))
        self.opacity_slider.setValue(tpl.get("opacity", 60))
        self.position_combo.setCurrentIndex(tpl.get("position", 2))
        self.naming_prefix.setText(tpl.get("prefix", "wm_"))
        self.naming_suffix.setText(tpl.get("suffix", ""))
        fmt = tpl.get("format", 0)
        self.format_group.button(fmt).setChecked(True)
        self.update_preview()

    def delete_selected_template(self):
        name = self.template_combo.currentText()
        if not name or name not in self.templates:
            return
        del self.templates[name]
        with open(self.get_template_path(), "w", encoding="utf-8") as f:
            import json
            json.dump(self.templates, f, ensure_ascii=False, indent=2)
        self.load_templates()

    def load_last_template(self):
        # 启动时自动加载第一个模板
        if hasattr(self, "templates") and self.templates:
            self.template_combo.setCurrentIndex(0)
            self.load_selected_template()

    def choose_output_dir(self):
        dir_ = QFileDialog.getExistingDirectory(self, "选择输出文件夹")
        if dir_:
            self.output_dir_edit.setText(dir_)

    def export_images(self):
        if not self.image_list:
            QMessageBox.warning(self, "提示", "请先导入图片！")
            return
        out_dir = self.output_dir_edit.text().strip()
        if not out_dir or not os.path.isdir(out_dir):
            QMessageBox.warning(self, "提示", "请先选择有效的输出文件夹！")
            return
        prefix = self.naming_prefix.text()
        suffix = self.naming_suffix.text()
        fmt = "JPEG" if self.format_group.checkedId() == 0 else "PNG"
        quality = self.quality_slider.value() if fmt == "JPEG" else None
        resize_mode = self.resize_mode_combo.currentIndex()
        resize_value = self.resize_value.text().strip()
        from watermark.watermark_util import add_watermark
        import traceback
        for path in self.image_list:
            try:
                base = os.path.basename(path)
                name, ext = os.path.splitext(base)
                out_name = f"{prefix}{name}{suffix}.{fmt.lower()}"
                out_path = os.path.join(out_dir, out_name)
                # 获取水印参数
                text, opacity, position, imgwm, imgwm_opacity, imgwm_scale = self.get_current_watermark_params()
                img = add_watermark(
                    path, text, opacity=opacity, position=position,
                    img_watermark_path=imgwm if imgwm else None,
                    imgwm_opacity=imgwm_opacity, imgwm_scale=imgwm_scale
                )
                # 尺寸缩放
                if resize_mode > 0 and resize_value:
                    try:
                        if resize_mode == 1:  # 按宽度
                            w = int(resize_value)
                            h = int(img.height * w / img.width)
                            img = img.resize((w, int(h)), Image.LANCZOS)
                        elif resize_mode == 2:  # 按高度
                            h = int(resize_value)
                            w = int(img.width * h / img.height)
                            img = img.resize((int(w), h), Image.LANCZOS)
                        elif resize_mode == 3:  # 按百分比
                            scale = float(resize_value) / 100.0
                            w = int(img.width * scale)
                            h = int(img.height * scale)
                            img = img.resize((w, h), Image.LANCZOS)
                    except Exception:
                        pass
                # 保存
                save_kwargs = {}
                if fmt == "JPEG":
                    save_kwargs["quality"] = quality
                    save_kwargs["subsampling"] = 0
                img.save(out_path, fmt, **save_kwargs)
            except Exception as e:
                print(f"导出失败: {path}\n{traceback.format_exc()}")
        QMessageBox.information(self, "完成", "批量导出完成！")

    # ...existing code...
    def get_current_watermark_params(self):
        text = self.text_input.text()
        font = self.font_combo.currentFont().family()
        font_size = self.font_size_spin.value()
        bold = self.bold_check.isChecked()
        italic = self.italic_check.isChecked()
        color = self.text_color
        opacity = self.opacity_slider.value()
        pos_map = {
            0: "left_top", 1: "top_center", 2: "right_top",
            3: "left_center", 4: "center", 5: "right_center",
            6: "left_bottom", 7: "bottom_center", 8: "right_bottom"
        }
        if self.position_combo.currentText() == "自定义" and self.custom_pos:
            position = ("custom", self.custom_pos)
        else:
            position = pos_map.get(self.position_combo.currentIndex(), "right_bottom")
        imgwm = self.imgwm_path.text().strip()
        imgwm_opacity = self.imgwm_opacity.value()
        imgwm_scale = self.imgwm_scale.value()
        return text, font, font_size, bold, italic, color, opacity, position, imgwm, imgwm_opacity, imgwm_scale

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
        (
            text, font, font_size, bold, italic, color, opacity, position,
            imgwm, imgwm_opacity, imgwm_scale
        ) = self.get_current_watermark_params()
        try:
            watermarked = add_watermark(
                img_path, text,
                font=font, font_size=font_size, bold=bold, italic=italic, color=color,
                opacity=opacity, position=position,
                img_watermark_path=imgwm if imgwm else None,
                imgwm_opacity=imgwm_opacity, imgwm_scale=imgwm_scale
            )
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
        def export_images(self):
            if not self.image_list:
                QMessageBox.warning(self, "提示", "请先导入图片！")
                return
            out_dir = self.output_dir_edit.text().strip()
            if not out_dir or not os.path.isdir(out_dir):
                QMessageBox.warning(self, "提示", "请先选择有效的输出文件夹！")
                return
            prefix = self.naming_prefix.text()
            suffix = self.naming_suffix.text()
            fmt = "JPEG" if self.format_group.checkedId() == 0 else "PNG"
            quality = self.quality_slider.value() if fmt == "JPEG" else None
            resize_mode = self.resize_mode_combo.currentIndex()
            resize_value = self.resize_value.text().strip()
            from watermark.watermark_util import add_watermark
            import traceback
            for path in self.image_list:
                try:
                    base = os.path.basename(path)
                    name, ext = os.path.splitext(base)
                    out_name = f"{prefix}{name}{suffix}.{fmt.lower()}"
                    out_path = os.path.join(out_dir, out_name)
                    # 获取水印参数
                    (
                        text, font, font_size, bold, italic, color, opacity, position,
                        imgwm, imgwm_opacity, imgwm_scale
                    ) = self.get_current_watermark_params()
                    img = add_watermark(
                        path, text,
                        font=font, font_size=font_size, bold=bold, italic=italic, color=color,
                        opacity=opacity, position=position,
                        img_watermark_path=imgwm if imgwm else None,
                        imgwm_opacity=imgwm_opacity, imgwm_scale=imgwm_scale
                    )
                    # 尺寸缩放
                    if resize_mode > 0 and resize_value:
                        try:
                            if resize_mode == 1:  # 按宽度
                                w = int(resize_value)
                                h = int(img.height * w / img.width)
                                img = img.resize((w, int(h)), Image.LANCZOS)
                            elif resize_mode == 2:  # 按高度
                                h = int(resize_value)
                                w = int(img.width * h / img.height)
                                img = img.resize((int(w), h), Image.LANCZOS)
                            elif resize_mode == 3:  # 按百分比
                                scale = float(resize_value) / 100.0
                                w = int(img.width * scale)
                                h = int(img.height * scale)
                                img = img.resize((w, h), Image.LANCZOS)
                        except Exception:
                            pass
                    # 保存
                    save_kwargs = {}
                    if fmt == "JPEG":
                        save_kwargs["quality"] = quality
                        save_kwargs["subsampling"] = 0
                    img.save(out_path, fmt, **save_kwargs)
                except Exception as e:
                    print(f"导出失败: {path}\n{traceback.format_exc()}")
            QMessageBox.information(self, "完成", "批量导出完成！")
        self.add_images(files)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = WatermarkMainWindow()
    win.show()
    sys.exit(app.exec_())
