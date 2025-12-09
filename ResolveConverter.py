import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QFileDialog, QVBoxLayout, QMessageBox, QProgressBar
import subprocess

VIDEO_EXTENSIONS = ('.mp4', '.mov', '.mkv', '.avi')
AUDIO_EXTENSIONS = ('.mp3', '.wav', '.flac', '.aac', '.ogg')

class LRMC(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Linux Resolve Media Converter (LRMC)")
        self.setGeometry(200, 200, 500, 350)

        self.video_path = None
        self.audio_path = None
        self.folder_path = None

        layout = QVBoxLayout()

        self.label = QLabel("Dosya veya klasör seçilmedi")
        layout.addWidget(self.label)

        select_video_button = QPushButton("Tek Video Seç")
        select_video_button.clicked.connect(self.select_video)
        layout.addWidget(select_video_button)

        select_audio_button = QPushButton("Tek Ses Dosyası Seç")
        select_audio_button.clicked.connect(self.select_audio)
        layout.addWidget(select_audio_button)

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
            self.audio_path = None
            self.folder_path = None
            self.label.setText(f"Seçilen Video: {os.path.basename(file_path)}")

    def select_audio(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Ses Dosyası Seç", "", "Ses Dosyaları (*.mp3 *.wav *.flac *.aac *.ogg)"
        )
        if file_path:
            self.audio_path = file_path
            self.video_path = None
            self.folder_path = None
            self.label.setText(f"Seçilen Ses: {os.path.basename(file_path)}")

    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Klasör Seç")
        if folder_path:
            self.folder_path = folder_path
            self.video_path = None
            self.audio_path = None
            self.label.setText(f"Seçilen Klasör: {folder_path}")

    def convert(self, copy=False):
        files_to_convert = []

        if self.video_path:
            files_to_convert = [self.video_path]
            extensions = VIDEO_EXTENSIONS
        elif self.audio_path:
            files_to_convert = [self.audio_path]
            extensions = AUDIO_EXTENSIONS
        elif self.folder_path:
            extensions = VIDEO_EXTENSIONS + AUDIO_EXTENSIONS
            for root, _, files in os.walk(self.folder_path):
                for file in files:
                    if file.lower().endswith(extensions):
                        files_to_convert.append(os.path.join(root, file))
        else:
            QMessageBox.warning(self, "Hata", "Önce bir dosya veya klasör seçmelisiniz!")
            return

        if not files_to_convert:
            QMessageBox.warning(self, "Hata", "Dönüştürülecek dosya bulunamadı!")
            return

        self.progress_bar.setValue(0)
        total_files = len(files_to_convert)
        failed_files = []

        for i, file in enumerate(files_to_convert, start=1):
            folder = os.path.dirname(file)
            base_name = os.path.splitext(os.path.basename(file))[0]
            ext = os.path.splitext(file)[1].lower()

            if ext in VIDEO_EXTENSIONS:
                if copy:
                    output_path = os.path.join(folder, f"{base_name}_copy.mov")
                else:
                    output_path = os.path.join(folder, f"{base_name}.mov")
                ffmpeg_cmd = [
                    "ffmpeg",
                    "-i", file,
                    "-c:v", "mpeg4",
                    "-qscale:v", "2",
                    "-c:a", "pcm_s24le",
                    "-y",
                    output_path
                ]
            else:  # Audio files
                if copy:
                    output_path = os.path.join(folder, f"{base_name}_copy.wav")
                else:
                    output_path = os.path.join(folder, f"{base_name}.wav")
                ffmpeg_cmd = [
                    "ffmpeg",
                    "-i", file,
                    "-c:a", "pcm_s24le",
                    "-y",
                    output_path
                ]

            try:
                subprocess.run(ffmpeg_cmd, check=True)
            except subprocess.CalledProcessError:
                failed_files.append(file)

            self.progress_bar.setValue(int(i / total_files * 100))

        success_count = total_files - len(failed_files)
        message = f"{success_count}/{total_files} dosya başarıyla dönüştürüldü."
        if failed_files:
            message += "\nHata alan dosyalar:\n" + "\n".join([os.path.basename(f) for f in failed_files])

        QMessageBox.information(self, "İşlem Tamamlandı", message)
        self.progress_bar.setValue(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LRMC()
    window.show()
    sys.exit(app.exec())
