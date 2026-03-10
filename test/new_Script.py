import sys
import os
import subprocess
import shutil
from multiprocessing import Pool, cpu_count
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, 
                             QVBoxLayout, QMessageBox, QProgressBar, QHBoxLayout)
from PyQt6.QtCore import Qt, QThread, pyqtSignal

# --- AYARLAR ---
INPUT_DIR = os.path.expanduser("~/Videos/Input")
OUTPUT_DIR = os.path.expanduser("~/Videos/Output")
VIDEO_EXT = ('.mp4', '.mov', '.mkv', '.avi', '.ts')
AUDIO_EXT = ('.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a')

def get_ffmpeg_cmd(input_path, output_path):
    ext = os.path.splitext(input_path)[1].lower()
    if ext in VIDEO_EXT:
        # Profesyonel Kurgu Standartı: ProRes 422 + PCM Ses
        return [
            "ffmpeg", "-i", input_path,
            "-c:v", "prores_ks", "-profile:v", "3", # ProRes HQ
            "-vendor", "apl0", "-bits_per_mb", "8000",
            "-pix_fmt", "yuv422p10le",             # 10-bit Renk
            "-c:a", "pcm_s24le",                   # Linux Resolve dostu ses
            "-y", output_path
        ]
    else:
        return [
            "ffmpeg", "-i", input_path,
            "-c:a", "pcm_s24le", "-y", output_path
        ]

def worker(file_info):
    """Her bir çekirdek için çalışan işlem birimi"""
    input_path, output_path = file_info
    try:
        subprocess.run(get_ffmpeg_cmd(input_path, output_path), 
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        os.remove(input_path) # İşlem bitince Input'takini sil
        return True
    except:
        return False

class ConversionThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(int, int)

    def run(self):
        if not os.path.exists(INPUT_DIR): os.makedirs(INPUT_DIR)
        if not os.path.exists(OUTPUT_DIR): os.makedirs(OUTPUT_DIR)

        tasks = []
        for root, _, files in os.walk(INPUT_DIR):
            for file in files:
                if file.lower().endswith(VIDEO_EXT + AUDIO_EXT):
                    in_p = os.path.join(root, file)
                    out_p = os.path.join(OUTPUT_DIR, os.path.splitext(file)[0] + ".mov")
                    tasks.append((in_p, out_p))

        if not tasks:
            self.finished.emit(0, 0)
            return

        total = len(tasks)
        success = 0
        
        # Çoklu Çekirdek Kullanımı (Pool)
        with Pool(processes=cpu_count()) as pool:
            for i, result in enumerate(pool.imap_unordered(worker, tasks), 1):
                if result: success += 1
                self.progress.emit(int((i / total) * 100))
        
        self.finished.emit(success, total)

class LRMC(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("LRMC Pro - DaVinci Linux Optimizer")
        self.setFixedSize(500, 250)
        self.setStyleSheet("background-color: #1e1e1e; color: white; font-family: sans-serif;")

        layout = QVBoxLayout()
        
        self.status_label = QLabel("Hazır (Input klasörünü kontrol et)")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("font-size: 14px; margin-top: 20px; color: #3498db;")
        layout.addWidget(self.status_label)

        self.info_label = QLabel(f"Girdi: {INPUT_DIR}\nÇıktı: {OUTPUT_DIR}")
        self.info_label.setStyleSheet("color: #888; font-size: 10px;")
        layout.addWidget(self.info_label)

        self.p_bar = QProgressBar()
        self.p_bar.setStyleSheet("""
            QProgressBar { border: 1px solid #444; border-radius: 5px; text-align: center; }
            QProgressBar::chunk { background-color: #2ecc71; }
        """)
        layout.addWidget(self.p_bar)

        self.btn_start = QPushButton("OTOMATİK DÖNÜŞTÜRÜCÜYÜ BAŞLAT")
        self.btn_start.setStyleSheet("""
            QPushButton { background-color: #e67e22; color: white; padding: 15px; font-weight: bold; border-radius: 5px; }
            QPushButton:hover { background-color: #d35400; }
        """)
        self.btn_start.clicked.connect(self.start_process)
        layout.addWidget(self.btn_start)

        self.setLayout(layout)

    def start_process(self):
        self.btn_start.setEnabled(False)
        self.status_label.setText("İşleniyor... Tüm çekirdekler aktif!")
        self.thread = ConversionThread()
        self.thread.progress.connect(self.p_bar.setValue)
        self.thread.finished.connect(self.on_finished)
        self.thread.start()

    def on_finished(self, success, total):
        self.btn_start.setEnabled(True)
        self.p_bar.setValue(0)
        if total == 0:
            QMessageBox.information(self, "Bilgi", "Input klasöründe dosya bulunamadı.")
        else:
            self.status_label.setText("İşlem Tamamlandı!")
            QMessageBox.information(self, "Bitti", f"{success}/{total} dosya taşındı ve dönüştürüldü.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LRMC()
    window.show()
    sys.exit(app.exec())