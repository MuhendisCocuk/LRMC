# 🐧 Linux Resolve Media Converter (LRMC) / Linux Resolve Medya Dönüştürücü

## İngilizce Versiyon

### 📜 Description

Linux Resolve Media Converter (LRMC) is a simple, cross-platform Python tool designed to convert video files into DaVinci Resolve compatible formats. It supports single video conversion as well as batch processing for entire folders. It ensures:

```
Video conversion to MPEG-4

Audio conversion to 24-bit LPCM

User-friendly GUI with PyQt6

Options to overwrite or save a copy

Batch conversion with progress bar and error logging

```

This tool is ideal for content creators and editors who want to quickly prepare their videos for DaVinci Resolve on Linux.

### ✨ Features

```
Single video or folder conversion

Batch processing with progress bar

LPCM 24-bit audio for maximum compatibility

Copy or overwrite option

Simple GUI using PyQt6

```

### 🛠️ Installation

Clone the repository:

```
git clone https://github.com/MuhendisCocuk/LRMC.git
cd LRMC
```

Create and activate a virtual environment:

<aside>

python3 -m venv venv
source venv/bin/activate

</aside>

Install required Python packages:

<aside>

pip install PyQt6

</aside>

Ensure ffmpeg is installed on your system:

Debian/Ubuntu:

```
sudo apt install ffmpeg
```

Manjaro/Arch:

```
sudo pacman -S ffmpeg
```

### 🚀 Usage

```
Run the application:

python ResolveConverter.py

Use the GUI to select a single video or an entire folder.

Choose “Save” to overwrite or “Save as Copy” to create copies.

```

Optional: You can create a global command alias to run it from anywhere:

<aside>

alias lrmc='cd /path/to/LRMC && source venv/bin/activate && python [ResolveConverter.py](http://resolveconverter.py/)'

</aside>

## Türkçe Sürüm

### 📝 Açıklama

Linux Resolve Medya Dönüştürücü (LRMC), videoları DaVinci Resolve uyumlu formatlara dönüştürmek için geliştirilmiş basit bir Python aracıdır. Tek bir video veya tüm klasörler için toplu işlem desteği sunar. Özellikler:

```
Video: MPEG-4 

Ses: 24-bit LPCM

PyQt6 tabanlı kullanıcı dostu GUI

Dosya üzerine yazma veya kopya kaydetme seçenekleri

Toplu dönüştürmede ilerleme çubuğu ve hata kaydı

```

Linux üzerinde içerik üreticileri ve editörler için hızlı ve güvenilir bir çözüm sunar.

### ✨ Özellikler

```
Tek video veya klasör dönüştürme

Toplu işlem ve progress bar

Maksimum uyumluluk için 24-bit LPCM ses

Kopya veya üzerine yazma seçenekleri

PyQt6 ile basit GUI

```

### 🛠️ Kurulum

Depoyu klonla:

```
git clone https://github.com/MuhendisCocuk/LRMC.git
cd LRMC
```

Sanal ortam oluştur ve aktif et:

<aside>

python3 -m venv venv
source venv/bin/activate

</aside>

Python paketlerini yükle:

<aside>

pip install PyQt6

</aside>

ffmpeg kurulu olmalı:

Debian/Ubuntu:

```
sudo apt install ffmpeg
```

Manjaro/Arch:

```
sudo pacman -S ffmpeg
```

### 🚀 Kullanım

Uygulamayı çalıştır:

```
python ResolveConverter.py
```

GUI üzerinden tek video veya klasör seç.

“Kaydet” ile dosyanın üzerine yaz veya “Kopya olarak kaydet” ile yeni dosya oluştur.

İsteğe bağlı: Terminalden her yerden çalıştırmak için alias oluşturabilirsin:

<aside>

alias lrmc='cd /path/to/LRMC && source venv/bin/activate && python [ResolveConverter.py](http://resolveconverter.py/)'

</aside>

### ⚖️ Lisans ve Yazar

```
Lisans: MIT / Açık kaynak

Yazar: Mühendis Çocuk

```
