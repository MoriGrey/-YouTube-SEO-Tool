# 🍎 Mac için Hızlı Başlangıç

Bu kılavuz Mac kullanıcıları için özel olarak hazırlanmıştır.

## 📋 Gereksinimler

- Python 3.8 veya üzeri
- pip (Python paket yöneticisi)
- Terminal erişimi

## 🚀 Kurulum Adımları

### 1. Python Versiyonunu Kontrol Et

```bash
python3 --version
```

Eğer Python yüklü değilse:

```bash
# Homebrew ile (önerilen)
brew install python3

# veya python.org'dan indirin
```

### 2. Projeyi İndir

**Git ile (önerilen):**

```bash
git clone [REPOSITORY_URL]
cd YouTube-SEO-AGI-Tool
```

**ZIP ile:**

```bash
# ZIP dosyasını indirin ve açın
unzip YouTube-SEO-AGI-Tool.zip
cd YouTube-SEO-AGI-Tool
```

### 3. Virtual Environment Oluştur

```bash
python3 -m venv venv
```

### 4. Virtual Environment'ı Aktif Et

```bash
source venv/bin/activate
```

**Not:** Terminal penceresini her açtığınızda bu komutu çalıştırmanız gerekir.

### 5. Bağımlılıkları Yükle

```bash
pip install -r requirements.txt
```

Bu işlem birkaç dakika sürebilir.

### 6. .env Dosyasını Oluştur

```bash
cp .env.example .env
```

Sonra `.env` dosyasını düzenleyin ve API anahtarlarınızı ekleyin:

```bash
nano .env
# veya
open -e .env
```

### 7. Dashboard'u Başlat

```bash
streamlit run dashboard.py
```

Tarayıcınızda otomatik olarak `http://localhost:8501` açılacaktır.

## ⚙️ Yapılandırma

### API Anahtarları

`.env` dosyasında şu anahtarları ayarlayın:

```env
YOUTUBE_API_KEY=your_youtube_api_key
GOOGLE_TRENDS_API_KEY=optional
REDDIT_CLIENT_ID=optional
REDDIT_CLIENT_SECRET=optional
TWITTER_API_KEY=optional
```

**Not:** Sadece YouTube API anahtarı zorunludur. Diğerleri opsiyoneldir.

### Port Değiştirme

Eğer 8501 portu kullanılıyorsa:

```bash
streamlit run dashboard.py --server.port 8502
```

## 🛠️ Sorun Giderme

### "command not found: streamlit"

```bash
# Virtual environment aktif mi?
source venv/bin/activate

# Streamlit yüklü mü?
pip list | grep streamlit

# Yoksa yükleyin
pip install streamlit
```

### "Permission denied"

```bash
chmod +x *.py
```

### Python Versiyonu Uyumsuz

```bash
# Python 3.8+ gerekli
python3 --version

# Eğer eski versiyon varsa, Homebrew ile güncelleyin
brew upgrade python3
```

### Port Zaten Kullanılıyor

```bash
# Kullanılan portu bul
lsof -i :8501

# Process'i sonlandır
kill -9 [PID]

# veya farklı port kullan
streamlit run dashboard.py --server.port 8502
```

## 📱 Sürekli Öğrenme

Sürekli öğrenme döngüsünü başlatmak için:

```bash
# Virtual environment aktif olmalı
source venv/bin/activate

# Sürekli öğrenme script'ini çalıştır
python start_continuous_learning.py
```

## 🎯 İlk Kullanım

1. Dashboard açıldığında sidebar'dan dil seçin (Türkçe/İngilizce)
2. "Target Channel" ve "Niche" bilgilerini girin
3. İstediğiniz sayfaya gidin ve analiz yapın

## 💡 İpuçları

- Virtual environment'ı her zaman aktif tutun
- `.env` dosyasını asla Git'e commit etmeyin
- Dashboard'u kapatmak için Terminal'de `Ctrl+C` basın
- Sürekli öğrenme ayrı bir Terminal penceresinde çalışır

## 📞 Yardım

Sorun yaşarsanız:

1. Python versiyonunu kontrol edin: `python3 --version`
2. Virtual environment aktif mi: `which python` (venv/bin/python göstermeli)
3. Tüm paketler yüklü mü: `pip list`
4. Hata mesajını tam olarak kopyalayın

**İyi kullanımlar! 🚀**

