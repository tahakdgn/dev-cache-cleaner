# Dev & System Cache Cleaner (GUI & CLI)

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.6+-green.svg)
![OS](https://img.shields.io/badge/OS-Windows%20%7C%20macOS%20%7C%20Linux-orange.svg)
![Interface](https://img.shields.io/badge/Interface-GUI%20%7C%20CLI-purple.svg)

Capraz platform (Cross-Platform) gelistirici onbellegi ve sistem gecici dosya temizleme araci. 
Grafik Masaustu Arayuzu (GUI) veya Terminal (CLI) secenegiyle, Windows, macOS ve Linux uzerinde tek tikla gigabaytlarca onbellegi guvenle temizler.

---

## Proje Klasor Yapisi (Repository Architecture)

```
dev-cache-cleaner/
├── core/                       # Ana motor dosyaları (Python clean & gui)
│   ├── clean.py                # Çapraz platform tarama ve CLI motoru
│   └── gui.py                  # Koyu temalı grafik masaüstü arayüzü
├── windows/                    # Windows özel başlatıcıları
│   ├── DevCacheCleaner.vbs     # Çift tıkla sessiz masaüstü arayüzü
│   ├── run_gui.bat             # Batch GUI başlatıcısı
│   └── clean.bat               # Batch CLI başlatıcısı
├── macos/                      # macOS özel başlatıcıları
│   ├── DevCacheCleaner.command # macOS tek tıkla arayüz başlatıcı
│   └── clean.command           # macOS terminal temizleme başlatıcı
├── linux/                      # Linux başlatıcıları
│   └── clean.sh                # Linux shell başlatıcısı
├── README.md                   # Dokümantasyon
├── LICENSE                     # MIT Lisansı
└── .gitignore
```

---

## Projeyi Baslatma ve Kurulum (Quick Start & Setup)

### 1. Repoyu Klonlayin veya Indirin
Terminal / Komut Satiri uzerinden projeyi bilgisayariniza indirin:
```bash
git clone https://github.com/tahakdgn/dev-cache-cleaner.git
cd dev-cache-cleaner
```

### 2. Uygulamayi Calistirma Yontemleri

#### Windows uzerinde:
- **Masaustu Arayuzu (GUI):** `windows/DevCacheCleaner.vbs` dosyasina cift tiklayin.
- **Terminal (CLI):** `windows/clean.bat` dosyasina cift tiklayin veya:
  ```cmd
  python core/clean.py
  ```

#### macOS uzerinde:
- **Masaustu Arayuzu (GUI / Terminal):** `macos/DevCacheCleaner.command` dosyasina cift tiklayin.
- **Terminal (CLI):** `macos/clean.command` dosyasina cift tiklayin veya:
  ```bash
  python3 core/clean.py
  ```

#### Linux uzerinde:
- **Terminal / GUI:** `linux/clean.sh` dosyasini calistirin veya:
  ```bash
  python3 core/gui.py
  ```

---

## Sorun Giderme ve Sikca Sorulan Sorular (Troubleshooting & FAQ)

### 1. macOS: "Uygun erisim ayricaliklarina sahip olmadiginiz icin calistirilamadi" Hatasi
macOS uzerinde `.command` ve `.sh` dosyalarinin calistirma izni varsayilan olarak kapali gelebilir.
**Cozum:** Proje dizini icindeyken terminale su komutu yazarak izin verin:
```bash
cd ~/Desktop/dev-cache-cleaner
chmod +x macos/*.command linux/*.sh
```

### 2. macOS Uzerinde Pencere Arayuzu (GUI) Yerine Renkli Terminal Arayuzunun Acilmasi
macOS'in varsayilan Python kurulumunda grafik pencere kutuphanesi (`tkinter`) kapali gelebilir. Script akilli yedekleme sistemi sayesinde hata verip kapanmak yerine otomatik olarak zengin renkli Terminal arayuzunu (`clean.py`) baslatir.
**Grafik Pencere Arayuzunu Açmak Icin Cozum:**
Python.org üzerinden güncel Python 3 kurabilir veya Homebrew kullanarak Tkinter kütüphanesini yükleyebilirsiniz:
```bash
brew install python-tk
```

---

## Kendi Ozel Hedeflerinizi Ekleme (Proje Ozellestirme)

Kendi projenize veya bilgisayariniza ozel yeni bir onbellek klasorunu temizlemek isterseniz, `core/clean.py` ve `core/gui.py` dosyalarindaki `get_target_directories` fonksiyonuna tek bir satir eklemeniz yeterlidir:

```python
# Örnek ekleme biçimi:
("Kendi Ozel Onbelleginiz", Path("C:/Hedef/Klasor/Yolu"), "Dev", "Aciklama metni")
```

---

## Guvenlik Notu (Ne Silinir, Ne Silinmez?)

> **Onemli:** Calistirilan komutlarla bilgisayarinizda **kisisel hicbir dosya, kod veya proje SILINMEZ.**

Silinenlerin tamami sistemin ve gelistirici araclarinin ihtiyac duydugunda tekrar otomatik olusturabilecegi gecici onbellek (cache) ve artik dosyalardir.

---

## Lisans (License)

MIT License. Ozgurce kullanabilir ve gelistirebilirsiniz.
