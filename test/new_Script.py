import sys
import os
import subprocess
from multiprocessing import Pool, cpu_count
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, 
                             QVBoxLayout, QMessageBox, QProgressBar)
from PyQt6.QtCore import Qt, QThread, pyqtSignal

# --- AYARLAR ---
INPUT_DIR = os.path.expanduser("~/Videos/Input")
OUTPUT_DIR = os.path.expanduser("~/Videos/Output")
VIDEO_EXT = ('.mp4', '.mov', '.mkv', '.avi', '.ts')
AUDIO_EXT = ('.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a')

def get_ffmpeg_cmd(input_path, output_path):
    ext = os.path.splitext(input_path)[1].lower()

    if ext in VIDEO_EXT:
        # MJPEG: DaVinci Resolve Free (Linux) ile uyumlu, küçük boyut, minimum kalite kaybı
        return [
            "ffmpeg", "-i", input_path,
            "-c:v", "mjpeg",
            "-q:v", "8",
            "-pix_fmt", "yuvj422p",
            "-c:a", "pcm_s16le",
            "-y", output_path
        ]
    else:
        return [
            "ffmpeg", "-i", input_path,
            "-c:a", "pcm_s16le",
            "-y", output_path
        ]

def worker(file_info):
    """Her bir çekirdek için çalışan işlem birimi"""
    input_path, output_path = file_info
    try:
        cmd = get_ffmpeg_cmd(input_path, output_path)
        result = subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE  # Hata mesajını yakala
        )
        os.remove(input_path)  # Başarılı dönüşüm sonrası orijinali sil
        return True, os.path.basename(input_path)
    except subprocess.CalledProcessError as e:
        # Hata durumunda dosyayı silme
        return False, os.path.basename(input_path)
    except Exception:
        return False, os.path.basename(input_path)

class ConversionThread(QThread):
    progress = pyqtSignal(int)
    status_update = pyqtSignal(str)
    finished = pyqtSignal(int, int, list)

    def run(self):
        if not os.path.exists(INPUT_DIR):
            os.makedirs(INPUT_DIR)
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)

        tasks = []
        for root, _, files in os.walk(INPUT_DIR):
            for file in files:
                if file.lower().endswith(VIDEO_EXT + AUDIO_EXT):
                    in_p = os.path.join(root, file)
                    out_p = os.path.join(OUTPUT_DIR, os.path.splitext(file)[0] + ".mov")
                    tasks.append((in_p, out_p))

        if not tasks:
            self.finished.emit(0, 0, [])
            return

        total = len(tasks)
        success = 0
        failed_files = []

        self.status_update.emit(f"{total} dosya bulundu, işleniyor...")

        with Pool(processes=cpu_count()) as pool:
            for i, (result, filename) in enumerate(pool.imap_unordered(worker, tasks), 1):
                if result:
                    success += 1
                else:
                    failed_files.append(filename)
                self.progress.emit(int((i / total) * 100))
                self.status_update.emit(f"{i}/{total} tamamlandı: {filename}")

        self.finished.emit(success, total, failed_files)


class LRMC(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("LRMC Pro - DaVinci Linux Optimizer (MJPEG)")
        self.setFixedSize(520, 300)
        self.setStyleSheet("background-color: #1e1e1e; color: white; font-family: sans-serif;")

        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        # Başlık
        title = QLabel("LRMC Pro — DaVinci Resolve Linux Optimizer")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 13px; font-weight: bold; color: #f39c12; margin-bottom: 5px;")
        layout.addWidget(title)

        # Codec bilgisi
        codec_info = QLabel("Codec: MJPEG q:8  |  Ses: PCM 16-bit  |  DaVinci Free Linux uyumlu")
        codec_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        codec_info.setStyleSheet("color: #2ecc71; font-size: 10px;")
        layout.addWidget(codec_info)

        # Dizin bilgisi
        self.info_label = QLabel(f"Girdi:  {INPUT_DIR}\nÇıktı: {OUTPUT_DIR}")
        self.info_label.setStyleSheet("color: #888; font-size: 10px; margin-top: 5px;")
        layout.addWidget(self.info_label)

        # Durum etiketi
        self.status_label = QLabel("Hazır — Input klasörüne dosyaları yerleştir")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("font-size: 12px; color: #3498db; margin-top: 5px;")
        layout.addWidget(self.status_label)

        # İlerleme çubuğu
        self.p_bar = QProgressBar()
        self.p_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #444;
                border-radius: 5px;
                text-align: center;
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: #2ecc71;
                border-radius: 4px;
            }
        """)
        layout.addWidget(self.p_bar)

        # Başlat butonu
        self.btn_start = QPushButton("OTOMATİK DÖNÜŞTÜRÜCÜYÜ BAŞLAT")
        self.btn_start.setStyleSheet("""
            QPushButton {
                background-color: #e67e22;
                color: white;
                padding: 15px;
                font-weight: bold;
                font-size: 13px;
                border-radius: 5px;
            }
            QPushButton:hover { background-color: #d35400; }
            QPushButton:disabled { background-color: #555; color: #999; }
        """)
        self.btn_start.clicked.connect(self.start_process)
        layout.addWidget(self.btn_start)

        self.setLayout(layout)

    def start_process(self):
        self.btn_start.setEnabled(False)
        self.p_bar.setValue(0)
        self.status_label.setText("İşleniyor... Tüm çekirdekler aktif!")
        self.thread = ConversionThread()
        self.thread.progress.connect(self.p_bar.setValue)
        self.thread.status_update.connect(self.status_label.setText)
        self.thread.finished.connect(self.on_finished)
        self.thread.start()

    def on_finished(self, success, total, failed_files):
        self.btn_start.setEnabled(True)
        self.p_bar.setValue(0)

        if total == 0:
            QMessageBox.information(self, "Bilgi", 
                f"Input klasöründe desteklenen dosya bulunamadı.\n\nKlasör: {INPUT_DIR}")
            self.status_label.setText("Hazır — Input klasörüne dosyaları yerleştir")
        else:
            self.status_label.setText("İşlem Tamamlandı!")
            msg = f"✅ {success}/{total} dosya başarıyla dönüştürüldü."
            if failed_files:
                msg += f"\n\n❌ Başarısız ({len(failed_files)} dosya):\n" + "\n".join(failed_files)
            QMessageBox.information(self, "Tamamlandı", msg)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LRMC()
    window.show()
    sys.exit(app.exec())