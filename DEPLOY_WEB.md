# Web Tabanlı Deploy Kılavuzu

Bu kılavuz, YouTube SEO AGI Tool'u web tabanlı olarak deploy etmek için adım adım talimatlar içerir. Böylece hem siz hem arkadaşınız aynı anda kullanabilirsiniz.

## 🌐 Deploy Seçenekleri

### 1. Streamlit Cloud (Önerilen - En Kolay) ⭐

**Avantajlar:**
- ✅ Tamamen ücretsiz
- ✅ Otomatik deploy (GitHub ile)
- ✅ Her kullanıcı kendi API key'ini girer
- ✅ Kolay güncelleme
- ✅ HTTPS desteği

**Adımlar:**

1. **GitHub'a Push Edin**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/KULLANICI_ADI/YouTube-SEO-AGI-Tool.git
   git push -u origin main
   ```

2. **Streamlit Cloud'a Giriş Yapın**
   - [streamlit.io](https://streamlit.io) adresine gidin
   - "Sign up" ile GitHub hesabınızla giriş yapın
   - "New app" butonuna tıklayın

3. **App Ayarları**
   - **Repository:** GitHub repo'nuzu seçin
   - **Branch:** `main` veya `master`
   - **Main file path:** `dashboard.py`
   - **App URL:** İstediğiniz URL'i seçin (örn: `youtube-seo-agi-tool`)

4. **Deploy**
   - "Deploy!" butonuna tıklayın
   - İlk deploy 2-3 dakika sürebilir
   - Deploy tamamlandıktan sonra URL'iniz hazır!

5. **Kullanım**
   - Her kullanıcı kendi YouTube API key'ini sidebar'dan girer
   - API key'ler session state'te saklanır (güvenli)
   - Her kullanıcı kendi verilerini görür

**Not:** Streamlit Cloud ücretsiz planında:
- Sınırsız public app
- Her app için ayrı URL
- Otomatik HTTPS
- GitHub ile otomatik sync

---

### 2. Heroku (Alternatif)

**Avantajlar:**
- ✅ Ücretsiz tier mevcut (sınırlı)
- ✅ Özel domain desteği
- ✅ Daha fazla kontrol

**Adımlar:**

1. **Heroku CLI Kurulumu**
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku
   
   # Windows
   # https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Heroku'ya Giriş**
   ```bash
   heroku login
   ```

3. **Procfile Oluşturun**
   ```
   web: streamlit run dashboard.py --server.port=$PORT --server.address=0.0.0.0
   ```

4. **Deploy**
   ```bash
   heroku create youtube-seo-agi-tool
   git push heroku main
   ```

5. **Açın**
   ```bash
   heroku open
   ```

**Not:** Heroku free tier 2022'de sona erdi. Artık ücretli plan gerekli.

---

### 3. Railway (Önerilen Alternatif) ⭐

**Avantajlar:**
- ✅ Ücretsiz tier (sınırlı)
- ✅ Kolay deploy
- ✅ GitHub ile otomatik sync

**Adımlar:**

1. [Railway.app](https://railway.app) adresine gidin
2. GitHub ile giriş yapın
3. "New Project" > "Deploy from GitHub repo"
4. Repo'nuzu seçin
5. Railway otomatik olarak Streamlit'i algılar
6. Deploy tamamlandıktan sonra URL'iniz hazır!

---

### 4. Render (Alternatif)

**Avantajlar:**
- ✅ Ücretsiz tier mevcut
- ✅ Kolay deploy

**Adımlar:**

1. [Render.com](https://render.com) adresine gidin
2. GitHub ile giriş yapın
3. "New Web Service" seçin
4. Repo'nuzu bağlayın
5. Ayarlar:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run dashboard.py --server.port=$PORT --server.address=0.0.0.0`
6. "Create Web Service" butonuna tıklayın

---

## 🔑 API Key Yönetimi

### Web Tabanlı Kullanımda:

- ✅ **Her kullanıcı kendi API key'ini girer** (sidebar'dan)
- ✅ **API key'ler session state'te saklanır** (güvenli, geçici)
- ✅ **Her kullanıcı kendi verilerini görür**
- ✅ **API key'ler birbirine karışmaz**

### Güvenlik:

- API key'ler **asla** database'e kaydedilmez
- API key'ler **sadece** session state'te tutulur
- Her kullanıcı session'ı kapanınca API key silinir
- API key'ler **asla** log'lara yazılmaz

---

## 📋 Deploy Öncesi Kontrol Listesi

- [ ] `requirements.txt` dosyası güncel
- [ ] `.streamlit/config.toml` dosyası mevcut
- [ ] `dashboard.py` multi-user API key desteği var
- [ ] GitHub'a push edildi
- [ ] Test edildi (local'de çalışıyor)

---

## 🚀 Hızlı Deploy (Streamlit Cloud)

1. **GitHub'a Push:**
   ```bash
   git add .
   git commit -m "Ready for web deployment"
   git push
   ```

2. **Streamlit Cloud:**
   - [share.streamlit.io](https://share.streamlit.io) giriş yapın
   - "New app" > Repo seçin > `dashboard.py` > Deploy

3. **Hazır!** 🎉

---

## 🔧 Sorun Giderme

### "ModuleNotFoundError"

**Çözüm:** `requirements.txt` dosyasını kontrol edin, eksik paketleri ekleyin.

### "API key not found"

**Çözüm:** Kullanıcılar sidebar'dan API key'lerini girmeli. Bu normal bir durum.

### "Port already in use"

**Çözüm:** Cloud platformlar otomatik port yönetimi yapar. Bu hatayı görmezsiniz.

### Deploy başarısız

**Çözüm:**
1. Log'ları kontrol edin
2. `requirements.txt` dosyasını kontrol edin
3. Python versiyonunu kontrol edin (3.9+ gerekli)

---

## 📝 Notlar

- **Streamlit Cloud** en kolay ve ücretsiz seçenek
- Her kullanıcı kendi API key'ini girer (güvenli)
- API key'ler session bazlıdır (geçici)
- Deploy sonrası URL'inizi paylaşabilirsiniz
- Güncellemeler otomatik deploy olur (GitHub push sonrası)

---

**Başarılar! 🚀**

