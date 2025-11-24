# Projeyi Paylaşma Kılavuzu

Bu kılavuz, YouTube SEO AGI Tool projesini başkalarıyla paylaşmak için adım adım talimatlar içerir.

## 🚀 Yöntem 1: Git ile Paylaşım (Önerilen)

### Windows'ta (Siz)

#### 1. Git Repository Oluştur

```bash
# Proje klasörüne gidin
cd C:\Users\morig\Desktop\YouTube-SEO-AGI-Tool

# Git repository başlat
git init

# Tüm dosyaları ekle
git add .

# İlk commit
git commit -m "Initial commit: YouTube SEO AGI Tool with Turkish localization"
```

#### 2. GitHub/GitLab'a Yükle

**GitHub kullanıyorsanız:**

```bash
# GitHub'da yeni repository oluşturun (github.com)
# Sonra şu komutları çalıştırın:

git remote add origin https://github.com/KULLANICI_ADI/YouTube-SEO-AGI-Tool.git
git branch -M main
git push -u origin main
```

**GitLab kullanıyorsanız:**

```bash
git remote add origin https://gitlab.com/KULLANICI_ADI/YouTube-SEO-AGI-Tool.git
git branch -M main
git push -u origin main
```

### Mac'te (Arkadaşınız)

#### 1. Repository'yi Klonla

```bash
# GitHub için
git clone https://github.com/KULLANICI_ADI/YouTube-SEO-AGI-Tool.git

# GitLab için
git clone https://gitlab.com/KULLANICI_ADI/YouTube-SEO-AGI-Tool.git

# Proje klasörüne girin
cd YouTube-SEO-AGI-Tool
```

#### 2. Virtual Environment Oluştur

```bash
# Python 3.8+ gerekli
python3 --version

# Virtual environment oluştur
python3 -m venv venv

# Aktif et
source venv/bin/activate
```

#### 3. Bağımlılıkları Yükle

```bash
pip install -r requirements.txt
```

#### 4. .env Dosyasını Oluştur

```bash
# .env.example dosyasını kopyala
cp .env.example .env

# .env dosyasını düzenle (API anahtarlarını ekle)
nano .env
# veya
open -e .env
```

#### 5. Dashboard'u Başlat

```bash
streamlit run dashboard.py
```

---

## 📦 Yöntem 2: ZIP Dosyası ile Paylaşım

### Windows'ta (Siz)

#### 1. Gereksiz Dosyaları Temizle

```bash
# venv klasörünü sil (arkadaşınız kendi oluşturacak)
# .env dosyasını sil (güvenlik için)
# __pycache__ klasörlerini sil
```

#### 2. ZIP Oluştur

**PowerShell ile:**

```powershell
# Proje klasörüne gidin
cd C:\Users\morig\Desktop

# ZIP oluştur (venv hariç)
Compress-Archive -Path YouTube-SEO-AGI-Tool -DestinationPath YouTube-SEO-AGI-Tool.zip -Force
```

**Manuel olarak:**
- Proje klasörüne sağ tıklayın
- "Send to" > "Compressed (zipped) folder" seçin
- `venv` klasörünü ZIP'ten çıkarın (çok büyük)

### Mac'te (Arkadaşınız)

#### 1. ZIP'i Aç

```bash
# ZIP dosyasını indirin ve açın
unzip YouTube-SEO-AGI-Tool.zip

# Proje klasörüne gidin
cd YouTube-SEO-AGI-Tool
```

#### 2. Virtual Environment Oluştur

```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Bağımlılıkları Yükle

```bash
pip install -r requirements.txt
```

#### 4. .env Dosyasını Oluştur

```bash
cp .env.example .env
nano .env  # API anahtarlarını ekle
```

#### 5. Dashboard'u Başlat

```bash
streamlit run dashboard.py
```

---

## 🍎 Mac için Özel Notlar

### Python Kurulumu

Mac'te Python genellikle önceden yüklüdür, ancak güncel versiyon için:

```bash
# Homebrew ile (önerilen)
brew install python3

# veya python.org'dan indirin
```

### Virtual Environment Sorunları

Eğer `python3 -m venv venv` çalışmazsa:

```bash
# pip3 kullanın
pip3 install virtualenv
virtualenv venv
source venv/bin/activate
```

### Streamlit Port Sorunu

Mac'te port 8501 kullanılıyorsa:

```bash
# Farklı port kullan
streamlit run dashboard.py --server.port 8502
```

### İzin Sorunları

Eğer "Permission denied" hatası alırsa:

```bash
# Script'lere çalıştırma izni ver
chmod +x start_continuous_learning.py
```

---

## 🔒 Güvenlik Notları

### Paylaşmadan Önce Kontrol Edin:

- ✅ `.env` dosyasını silin veya `.gitignore`'a ekleyin
- ✅ API anahtarlarını paylaşmayın
- ✅ `venv/` klasörünü paylaşmayın
- ✅ `__pycache__/` klasörlerini paylaşmayın
- ✅ `.DS_Store` (Mac) ve `Thumbs.db` (Windows) dosyalarını paylaşmayın

### .gitignore Kontrolü

`.gitignore` dosyası şunları içermeli:

```
.env
venv/
.venv/
__pycache__/
*.pyc
.DS_Store
Thumbs.db
data/*.json
```

---

## 📋 Paylaşım Checklist

### Windows'ta (Siz)

- [ ] Git repository oluşturuldu (veya ZIP hazırlandı)
- [ ] `.env` dosyası paylaşılmadı
- [ ] `venv/` klasörü paylaşılmadı
- [ ] Tüm değişiklikler commit edildi
- [ ] README.md güncel
- [ ] SETUP_GUIDE.md mevcut

### Mac'te (Arkadaşınız)

- [ ] Python 3.8+ yüklü
- [ ] Repository klonlandı (veya ZIP açıldı)
- [ ] Virtual environment oluşturuldu
- [ ] Bağımlılıklar yüklendi (`pip install -r requirements.txt`)
- [ ] `.env` dosyası oluşturuldu ve API anahtarları eklendi
- [ ] Dashboard başlatıldı (`streamlit run dashboard.py`)

---

## 🆘 Sorun Giderme

### Mac'te "command not found: streamlit"

```bash
# Virtual environment aktif mi kontrol edin
source venv/bin/activate

# Streamlit yüklü mü kontrol edin
pip list | grep streamlit

# Yoksa yükleyin
pip install streamlit
```

### Mac'te "Permission denied"

```bash
# Script'lere izin ver
chmod +x *.py
```

### Port Zaten Kullanılıyor

```bash
# Farklı port kullan
streamlit run dashboard.py --server.port 8502
```

### Python Versiyonu Uyumsuz

```bash
# Python versiyonunu kontrol et
python3 --version

# Python 3.8+ gerekli
# macOS'ta genellikle Python 3.9+ yüklüdür
```

---

## 📞 İletişim

Sorun yaşarsanız:
1. Hata mesajını tam olarak kopyalayın
2. Python versiyonunu kontrol edin: `python3 --version`
3. Virtual environment aktif mi kontrol edin: `which python`
4. `requirements.txt`'deki tüm paketler yüklü mü kontrol edin: `pip list`

---

## 🎉 Başarılı Kurulum Sonrası

Kurulum başarılı olduğunda:

1. Dashboard açılır: `http://localhost:8501`
2. Sidebar'dan dil seçimi yapılabilir (Türkçe/İngilizce)
3. API anahtarları `.env` dosyasından okunur
4. Tüm modüller çalışır durumda

**İyi kullanımlar! 🚀**

