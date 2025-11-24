# Ücretsiz API Kullanım Kılavuzu

Bu kılavuz, YouTube SEO AGI Tool'u **tamamen ücretsiz** API'lerle kullanmak için gereken bilgileri içerir.

## ✅ Ücretsiz API'ler

### 1. YouTube Data API v3
**Durum:** ✅ Tamamen Ücretsiz  
**Kota:** Günlük 10,000 quota birimi  
**Gerekli:** Evet (zorunlu)

**Nasıl Alınır:**
1. [Google Cloud Console](https://console.cloud.google.com) → Yeni Proje
2. "APIs & Services" → "Library"
3. "YouTube Data API v3" → Enable
4. "Credentials" → "Create Credentials" → "API Key"

**Kota Yönetimi:**
- Tool otomatik olarak cache kullanır
- Aynı veriler tekrar çekilmez
- Günlük 10,000 birim çoğu kullanım için yeterlidir

---

### 2. Google Trends (pytrends)
**Durum:** ✅ Tamamen Ücretsiz  
**API Key:** Gerekmez  
**Gerekli:** Hayır (opsiyonel ama önerilir)

**Kurulum:**
```bash
pip install pytrends
```

**Nasıl Çalışır:**
- `pytrends` kütüphanesi Google Trends web sitesini kullanır
- Resmi API değildir, web scraping yapar
- Tamamen ücretsizdir

**Limitler:**
- Rate limiting var (çok fazla istek gönderirseniz geçici engelleme)
- Günde birkaç yüz sorgu güvenlidir

---

### 3. Reddit API
**Durum:** ✅ Ücretsiz (2 seçenek)  
**Gerekli:** Hayır (opsiyonel)

#### Seçenek 1: Public API (Önerilen - API Key Gerekmez)
- Reddit'in public JSON endpoint'lerini kullanır
- Ücretsiz ve sınırsız
- Kimlik doğrulama gerekmez
- **Tool zaten bu yöntemi kullanıyor!**

**Kullanım:**
```python
# Otomatik olarak çalışır, hiçbir şey yapmanıza gerek yok
```

#### Seçenek 2: OAuth API (Daha Fazla Özellik İçin)
**Limit:** Dakikada 100 sorgu

**Nasıl Alınır:**
1. [Reddit Apps](https://www.reddit.com/prefs/apps) → "create another app"
2. App adı, tip (script), redirect URI
3. Client ID ve Secret'ı kopyalayın

**Not:** Public API çoğu kullanım için yeterlidir, OAuth gerekmez.

---

### 4. Twitter/X API
**Durum:** ⚠️ Çok Sınırlı Ücretsiz Plan  
**Gerekli:** Hayır (önerilmez)

**Durum:**
- Twitter'ın ücretsiz planı çok sınırlıdır (aylık ~1,500 tweet)
- Tool Twitter olmadan da mükemmel çalışır
- Google Trends ve Reddit yeterli trend verisi sağlar

**Öneri:** Twitter API'yi kullanmayın, tool zaten yeterli veri kaynağına sahip.

---

## 🎯 Minimum Kurulum (Sadece Ücretsiz)

### Gerekli (Sadece 1 API Key):
1. ✅ **YouTube Data API v3** - Ücretsiz, günlük 10,000 kota

### Opsiyonel (API Key Gerekmez):
2. ✅ **Google Trends (pytrends)** - Ücretsiz, API key gerekmez
3. ✅ **Reddit Public API** - Ücretsiz, API key gerekmez

### Gerekmez:
4. ❌ **Twitter API** - Çok sınırlı, önerilmez

---

## 📝 Kurulum Adımları

### 1. YouTube API Key Alın (Zorunlu)
```bash
# Google Cloud Console'dan API key alın
# .env dosyasına ekleyin:
YOUTUBE_API_KEY=your_key_here
```

### 2. pytrends Kurun (Opsiyonel ama Önerilir)
```bash
pip install pytrends
```

### 3. Reddit API (Hiçbir Şey Yapmanıza Gerek Yok)
- Public API otomatik çalışır
- OAuth API istiyorsanız (opsiyonel):
  ```bash
  # .env dosyasına ekleyin:
  REDDIT_CLIENT_ID=your_id_here
  REDDIT_CLIENT_SECRET=your_secret_here
  ```

### 4. Twitter API (Kullanmayın)
- Tool Twitter olmadan da çalışır
- Gerekmez

---

## 💰 Maliyet Özeti

| API | Maliyet | Kota |
|-----|---------|------|
| YouTube Data API v3 | **$0** | Günlük 10,000 |
| Google Trends (pytrends) | **$0** | Rate limit var |
| Reddit Public API | **$0** | Rate limit var |
| Twitter API | **$0** (ama çok sınırlı) | Aylık ~1,500 |

**Toplam Maliyet: $0** 🎉

---

## ✅ Test Etme

Tüm ücretsiz API'leri test etmek için:

```bash
python test_api_connections.py
```

Bu script:
- ✅ YouTube API'yi test eder (ücretsiz)
- ✅ Google Trends'i test eder (ücretsiz, API key gerekmez)
- ✅ Reddit Public API'yi test eder (ücretsiz, API key gerekmez)
- ⚠️ Twitter API'yi test eder (opsiyonel, önerilmez)

---

## 🚀 Hemen Başlayın

1. **Sadece YouTube API Key alın** (5 dakika)
2. **pytrends kurun:** `pip install pytrends`
3. **Tool'u çalıştırın:** `streamlit run dashboard.py`

**Hepsi bu kadar!** Reddit ve Google Trends otomatik çalışır, hiçbir şey yapmanıza gerek yok.

---

## 📊 Veri Kaynakları Karşılaştırması

| Özellik | YouTube API | Google Trends | Reddit | Twitter |
|---------|-------------|---------------|--------|---------|
| Ücretsiz | ✅ | ✅ | ✅ | ⚠️ Sınırlı |
| API Key Gerekli | ✅ | ❌ | ❌ (Public) | ✅ |
| Trend Analizi | ✅ | ✅ | ✅ | ✅ |
| Viral Tespit | ✅ | ✅ | ✅ | ✅ |
| Kota Limit | Yüksek | Orta | Yüksek | Çok Düşük |
| Önerilen | ✅ Zorunlu | ✅ Önerilir | ✅ Önerilir | ❌ Gerekmez |

**Sonuç:** YouTube + Google Trends + Reddit yeterli! Twitter gerekmez.

---

## ❓ Sık Sorulan Sorular

**S: Twitter API olmadan tool çalışır mı?**  
A: Evet! Tool Twitter olmadan da mükemmel çalışır. Google Trends ve Reddit yeterli trend verisi sağlar.

**S: Reddit için API key gerekir mi?**  
A: Hayır! Public API otomatik çalışır, hiçbir şey yapmanıza gerek yok.

**S: Google Trends için API key gerekir mi?**  
A: Hayır! `pytrends` kütüphanesi API key gerektirmez.

**S: YouTube API ücretsiz mi?**  
A: Evet! Günlük 10,000 quota birimi tamamen ücretsizdir.

**S: Kota limiti aşarsam ne olur?**  
A: YouTube API günlük limiti aşarsanız, ertesi gün sıfırlanır. Cache kullanımı limiti aşmayı önler.

---

**Başarılar! Tüm tool ücretsiz API'lerle çalışır! 🎉**

