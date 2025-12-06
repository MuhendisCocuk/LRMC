import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QFileDialog, QVBoxLayout, QMessageBox, QProgressBar
import subprocess

VIDEO_EXTENSIONS = ('.mp4', '.mov', '.mkv', '.avi')

class LRMC(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Linux Resolve Media Converter (LRMC)")
        self.setGeometry(200, 200, 500, 300)

        self.video_path = None
        self.folder_path = None

        layout = QVBoxLayout()

        self.label = QLabel("Video veya klasör seçilmedi")
        layout.addWidget(self.label)

        select_video_button = QPushButton("Tek Video Seç")
        select_video_button.clicked.connect(self.select_video)
        layout.addWidget(select_video_button)

        select_folder_button = QPushButton("Klasör Seç")
        select_folder_button.clicked.connect(self.select_folder)
        layout.addWidget(select_folder_button)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)

        save_button = QPushButton("Üzerine Yaz")
        save_button.clicked.connect(lambda: self.convert(copy=False))
        layout.addWidget(save_button)

        copy_button = QPushButton("Kopya Olarak Kaydet")
        copy_button.clicked.connect(lambda: self.convert(copy=True))
        layout.addWidget(copy_button)

        self.setLayout(layout)

    def select_video(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Video Dosyası Seç", "", "Video Dosyaları (*.mp4 *.mov *.mkv *.avi)"
        )
        if file_path:
            self.video_path = file_path
            self.folder_path = None
            self.label.setText(f"Seçilen Video: {os.path.basename(file_path)}")

    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Klasör Seç")
        if folder_path:
            self.folder_path = folder_path
            self.video_path = None
            self.label.setText(f"Seçilen Klasör: {folder_path}")

    def convert(self, copy=False):
        files_to_convert = []

        if self.video_path:
            files_to_convert = [self.video_path]
        elif self.folder_path:
            for root, _, files in os.walk(self.folder_path):
                for file in files:
                    if file.lower().endswith(VIDEO_EXTENSIONS):
                        files_to_convert.append(os.path.join(root, file))
        else:
            QMessageBox.warning(self, "Hata", "Önce bir video veya klasör seçmelisiniz!")
            return

        if not files_to_convert:
            QMessageBox.warning(self, "Hata", "Dönüştürülecek video bulunamadı!")
            return

        self.progress_bar.setValue(0)
        total_files = len(files_to_convert)
        failed_files = []

        for i, video_file in enumerate(files_to_convert, start=1):
            folder = os.path.dirname(video_file)
            base_name = os.path.splitext(os.path.basename(video_file))[0]

            if copy:
                output_path = os.path.join(folder, f"{base_name}_copy.mov")
            else:
                output_path = os.path.join(folder, f"{base_name}.mov")

            ffmpeg_cmd = [
                "ffmpeg",
                "-i", video_file,
                "-c:v", "mpeg4",
                "-qscale:v", "2",
                "-c:a", "pcm_s24le",
                "-y",
                output_path
            ]

            try:
                subprocess.run(ffmpeg_cmd, check=True)
            except subprocess.CalledProcessError:
                failed_files.append(video_file)

            # Progress bar güncelle
            self.progress_bar.setValue(int(i / total_files * 100))

        success_count = total_files - len(failed_files)
        message = f"{success_count}/{total_files} video başarıyla dönüştürüldü."
        if failed_files:
            message += "\nHata alan dosyalar:\n" + "\n".join([os.path.basename(f) for f in failed_files])

        QMessageBox.information(self, "İşlem Tamamlandı", message)
        self.progress_bar.setValue(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LRMC()
    window.show()
    sys.exit(app.exec())
