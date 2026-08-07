# 🚀 Dev & System Cache Cleaner (Windows & macOS & Linux)

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.6+-green.svg)
![OS](https://img.shields.io/badge/OS-Windows%20%7C%20macOS%20%7C%20Linux-orange.svg)

Çapraz platform (Cross-Platform) geliştirici önbelleği ve sistem geçici dosya temizleme aracı. 
Windows, macOS ve Linux işletim sistemlerini otomatik tespit eder; Xcode, Flutter, CocoaPods, Gradle, NPM, Pip ve sistem Temp klasörlerindeki gereksiz GB'larca önbelleği güvenle temizler.

---

## 🔒 Güvenlik Notu (Ne Silinir, Ne Silinmez?)

> **Çok Önemli:** Çalıştırılan komutlarla bilgisayarınızda **kişisel hiçbir dosya, kod veya proje SİLİNMEZ!**

Silinenlerin tamamı sistemin ve geliştirici araçlarının ihtiyaç duyduğunda tekrar otomatik oluşturabileceği geçici önbellek (cache) ve artık dosyalardır:

### 🍏 macOS İçin Temizlenen Başlıca Yerler:
1. **Xcode DerivedData (`~/Library/Developer/Xcode/DerivedData`)**: Xcode ile derleme yaparken oluşan geçici indeksler ve binary'ler. *(Bir sonraki derlemede sıfırdan oluşturulur, kodlarınıza zarar vermez).*
2. **Xcode Archives (`~/Library/Developer/Xcode/Archives`)**: Eski derleme arşiv kalıntıları.
3. **CocoaPods Cache (`~/Library/Caches/CocoaPods`)**: İndirilen iOS pod paketlerinin önbellek kopyaları.
4. **iOS Simülatör Kalıntıları (`xcrun simctl delete unavailable`)**: Artık kullanılmayan / silinmiş eski hayalet simülatörlerin kalıntıları.
5. **Flutter & Pub Cache (`~/.pub-cache`)**: İndirilen Dart/Flutter paket önbellekleri.
6. **Gradle & Android SDK Temp (`~/.gradle/caches`)**: Android derleme ve bağımlılık önbellekleri.
7. **Homebrew, NPM, Yarn, Pip, VS Code Caches**: İndirilen paket ve uygulama önbellekleri.

### 🪟 Windows İçin Temizlenen Başlıca Yerler:
1. **User Temp (%TEMP%)**: Uygulamaların bıraktığı geçici sistem dosyaları.
2. **Gradle Cache (`%USERPROFILE%\.gradle\caches`)**: Android / Java bağımlılık önbellekleri.
3. **NPM & Yarn Cache (`AppData\Local\npm-cache`)**: Node.js paket önbellekleri.
4. **Flutter / Pub Cache (`AppData\Local\Pub\Cache`)**: Flutter paket önbellekleri.
5. **Pip & NuGet Caches**: Python ve .NET paket önbellekleri.
6. **VS Code Caches**: VS Code önbellek ve render artıkları.

---

## 💻 Kullanım / Usage

### 🪟 Windows'ta Kullanım:
- `clean.bat` dosyasına çift tıklayabilirsiniz.
- Veya PowerShell / CMD üzerinden:
```cmd
python clean.py
```

### 🍏 Mac'te Kullanım:
- `clean.command` dosyasına çift tıklayarak Terminal'de açabilirsiniz.
- Veya Mac Terminal'den:
```bash
python3 clean.py
```

---

## ⚙️ Parametreler

- `--force` veya `-y`: Onay sormadan doğrudan temizliği başlatır.
  ```bash
  python clean.py --force
  ```

---

## 📜 Lisans / License

MIT License. Özgürce kullanabilir ve geliştirebilirsiniz.
