🐧 Linux Resolve Media Converter (LRMC) / Linux Resolve Medya Dönüştürücü
İngilizce Versiyon
📜 Description

Linux Resolve Media Converter (LRMC) is a simple, cross-platform Python tool designed to convert video files into DaVinci Resolve compatible formats. It supports single video conversion as well as batch processing for entire folders. It ensures:

    Video conversion to MPEG-4 (classic, not H.264)

    Audio conversion to 24-bit LPCM

    User-friendly GUI with PyQt6

    Options to overwrite or save a copy

    Batch conversion with progress bar and error logging

This tool is ideal for content creators and editors who want to quickly prepare their videos for DaVinci Resolve on Linux.
✨ Features

    Single video or folder conversion

    Batch processing with progress bar

    LPCM 24-bit audio for maximum compatibility

    Copy or overwrite option

    Simple GUI using PyQt6

🛠️ Installation

    Clone the repository:
    Bash

git clone https://github.com/yourusername/LRMC.git
cd LRMC

Create and activate a virtual environment:
Bash

python3 -m venv venv
source venv/bin/activate

Install required Python packages:
Bash

pip install PyQt6

Ensure ffmpeg is installed on your system:

    Debian/Ubuntu:
    Bash

sudo apt install ffmpeg

Manjaro/Arch:
Bash

        sudo pacman -S ffmpeg

🚀 Usage

    Run the application:
    Bash

    python ResolveConverter.py

    Use the GUI to select a single video or an entire folder.

    Choose “Save” to overwrite or “Save as Copy” to create copies.

Optional: You can create a global command alias to run it from anywhere:
Bash

alias lrmc='cd /path/to/LRMC && source venv/bin/activate && python ResolveConverter.py'

Türkçe Sürüm
📝 Açıklama

Linux Resolve Medya Dönüştürücü (LRMC), videoları DaVinci Resolve uyumlu formatlara dönüştürmek için geliştirilmiş basit bir Python aracıdır. Tek bir video veya tüm klasörler için toplu işlem desteği sunar. Özellikler:

    Video: MPEG-4 (klasik, H.264 değil)

    Ses: 24-bit LPCM

    PyQt6 tabanlı kullanıcı dostu GUI

    Dosya üzerine yazma veya kopya kaydetme seçenekleri

    Toplu dönüştürmede ilerleme çubuğu ve hata kaydı

Linux üzerinde içerik üreticileri ve editörler için hızlı ve güvenilir bir çözüm sunar.
✨ Özellikler

    Tek video veya klasör dönüştürme

    Toplu işlem ve progress bar

    Maksimum uyumluluk için 24-bit LPCM ses

    Kopya veya üzerine yazma seçenekleri

    PyQt6 ile basit GUI

🛠️ Kurulum

    Depoyu klonla:
    Bash

git clone https://github.com/yourusername/LRMC.git
cd LRMC

Sanal ortam oluştur ve aktif et:
Bash

python3 -m venv venv
source venv/bin/activate

Python paketlerini yükle:
Bash

pip install PyQt6

ffmpeg kurulu olmalı:

    Debian/Ubuntu:
    Bash

sudo apt install ffmpeg

Manjaro/Arch:
Bash

        sudo pacman -S ffmpeg

🚀 Kullanım

    Uygulamayı çalıştır:
    Bash

    python ResolveConverter.py

    GUI üzerinden tek video veya klasör seç.

    “Kaydet” ile dosyanın üzerine yaz veya “Kopya olarak kaydet” ile yeni dosya oluştur.

İsteğe bağlı: Terminalden her yerden çalıştırmak için alias oluşturabilirsin:
Bash

alias lrmc='cd /path/to/LRMC && source venv/bin/activate && python ResolveConverter.py'

⚖️ Lisans ve Yazar

    Lisans: MIT / Açık kaynak

    Yazar: Kaptan Pengu
