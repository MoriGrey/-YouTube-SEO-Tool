# Dashboard Test Kılavuzu

## 🚀 Dashboard'u Başlatma

### Yöntem 1: Terminal'den
```bash
streamlit run dashboard.py
```

### Yöntem 2: Python'dan
```bash
python -m streamlit run dashboard.py
```

## 📍 Erişim

Dashboard otomatik olarak şu adreste açılır:
- **URL:** http://localhost:8501
- **Port:** 8501 (varsayılan)

Eğer port 8501 kullanılıyorsa, Streamlit otomatik olarak bir sonraki boş portu kullanır (8502, 8503, vb.)

## 🔐 Giriş Bilgileri

**Varsayılan Kullanıcı:**
- **Username:** `admin`
- **Password:** `admin123`

⚠️ **Önemli:** İlk girişten sonra şifreyi değiştirin!

## 🔑 API Key Yapılandırması

1. Dashboard açıldıktan sonra sidebar'da "API Key" bölümüne gidin
2. YouTube Data API v3 key'inizi girin
3. "Save API Key" butonuna tıklayın

**API Key Nasıl Alınır:**
1. [Google Cloud Console](https://console.cloud.google.com) → Yeni Proje
2. "APIs & Services" → "Library"
3. "YouTube Data API v3" → Enable
4. "Credentials" → "Create Credentials" → "API Key"
5. API key'inizi kopyalayın

## ✅ Test Edilecek Yeni Özellikler

### 1. 🔍 Video SEO Audit
- Sidebar'dan "🔍 Video SEO Audit" sayfasını seçin
- Bir video ID veya URL girin
- "Audit Video" butonuna tıklayın
- **Beklenen:** SEO skoru, detaylı analiz, öneriler

### 2. 📝 Caption Optimizer
- Sidebar'dan "📝 Caption Optimizer" sayfasını seçin
- Bir video ID veya URL girin
- 3 tab var:
  - **Analyze Captions:** Caption analizi
  - **Optimize:** Optimizasyon önerileri
  - **Multilingual Support:** Çoklu dil desteği kontrolü

### 3. 🎯 Engagement Booster
- Sidebar'dan "🎯 Engagement Booster" sayfasını seçin
- Bir video ID veya URL girin
- "Get Engagement Suggestions" butonuna tıklayın
- **Beklenen:** Polls, Cards, End Screens önerileri

### 4. 🖼️ Thumbnail Enhancer
- Sidebar'dan "🖼️ Thumbnail Enhancer" sayfasını seçin
- Bir video ID veya URL girin
- 3 tab var:
  - **Analyze:** Thumbnail analizi ve CTR tahmini
  - **Improvements:** İyileştirme önerileri
  - **A/B Tests:** A/B test önerileri

## 🧪 Test Senaryoları

### Senaryo 1: Video SEO Audit
1. Video SEO Audit sayfasına gidin
2. Video ID girin: `dQw4w9WgXcQ` (test için)
3. Audit butonuna tıklayın
4. **Kontrol:**
   - SEO skoru görünüyor mu? (0-100)
   - Title, Description, Tags, Thumbnail analizi var mı?
   - Öneriler listeleniyor mu?

### Senaryo 2: Caption Optimizer
1. Caption Optimizer sayfasına gidin
2. Video ID girin
3. "Analyze Captions" tab'ında analiz yapın
4. **Kontrol:**
   - SEO skoru görünüyor mu?
   - Keyword analizi var mı?
   - Öneriler listeleniyor mu?

### Senaryo 3: Engagement Booster
1. Engagement Booster sayfasına gidin
2. Video ID girin
3. Engagement önerilerini alın
4. **Kontrol:**
   - Polls önerileri var mı?
   - Cards önerileri var mı?
   - End Screens önerileri var mı?

### Senaryo 4: Thumbnail Enhancer
1. Thumbnail Enhancer sayfasına gidin
2. Video ID girin
3. Thumbnail analizi yapın
4. **Kontrol:**
   - CTR skoru görünüyor mu?
   - Thumbnail görseli gösteriliyor mu?
   - İyileştirme önerileri var mı?

## 🐛 Bilinen Sorunlar

1. **API Key Gerekli:** Tüm özellikler için YouTube API key gereklidir
2. **Video ID Formatı:** Video ID veya tam URL kabul edilir
3. **Captions:** Bazı videolarda captions olmayabilir (normal)

## 📊 Beklenen Sonuçlar

- ✅ Tüm sayfalar açılıyor
- ✅ Video analizi çalışıyor
- ✅ Sonuçlar görüntüleniyor
- ✅ Öneriler listeleniyor
- ✅ Hata mesajları anlaşılır

## 🔄 Dashboard'u Durdurma

Terminal'de `Ctrl+C` tuşlarına basın.

## 📝 Notlar

- İlk açılışta modüller initialize edilir (birkaç saniye sürebilir)
- API key şifreli olarak saklanır
- Rate limiting aktif (çok fazla istek gönderirseniz uyarı alırsınız)

