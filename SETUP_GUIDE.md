# YouTube SEO AGI Tool - Setup Guide

Bu kılavuz, YouTube SEO AGI Tool'u kurmak, yapılandırmak ve kullanmak için adım adım talimatlar içerir.

## 📋 İçindekiler

1. [Kurulum](#kurulum)
2. [API Anahtarları Yapılandırması](#api-anahtarları-yapılandırması)
   - [Ücretsiz API Kullanımı](#ücretsiz-api-kullanım-durumu) ⭐
3. [Continuous Learning Başlatma](#continuous-learning-başlatma)
4. [Gerçek Veri ile Test](#gerçek-veri-ile-test)
5. [Performans Optimizasyonu](#performans-optimizasyonu)

> 💡 **Not:** Tüm tool **tamamen ücretsiz** API'lerle çalışır! Detaylar için [FREE_API_GUIDE.md](FREE_API_GUIDE.md) dosyasına bakın.

---

## 🚀 Kurulum

### 1. Bağımlılıkları Yükle

```bash
pip install -r requirements.txt
```

### 2. Ortam Değişkenlerini Ayarla

`.env` dosyasını oluşturun (`.env.example` dosyasını kopyalayarak):

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

---

## 🔑 API Anahtarları Yapılandırması

### Otomatik Yapılandırma

En kolay yol, interaktif setup scriptini kullanmaktır:

```bash
python setup_api_keys.py
```

Bu script size tüm API anahtarlarını soracak ve `.env` dosyasını otomatik olarak yapılandıracak.

### Manuel Yapılandırma

`.env` dosyasını düzenleyerek manuel olarak da yapılandırabilirsiniz:

```env
# YouTube API (ZORUNLU)
YOUTUBE_API_KEY=your_youtube_api_key_here

# Reddit API (Opsiyonel)
# Reddit API (Optional - Public API works without credentials)
# OAuth API için (daha fazla özellik için):
REDDIT_CLIENT_ID=your_reddit_client_id_here
REDDIT_CLIENT_SECRET=your_reddit_client_secret_here

# Twitter API (Optional - Very limited free tier, not recommended)
# Twitter olmadan da tool çalışır, sadece Twitter trend verisi olmaz
TWITTER_BEARER_TOKEN=your_twitter_bearer_token_here
```

### API Ücretsiz Kullanım Durumu

**✅ Tüm API'ler ÜCRETSİZ kullanılabilir!**

| API | Ücretsiz Durum | Limitler |
|-----|----------------|----------|
| **YouTube Data API v3** | ✅ Tamamen Ücretsiz | Günlük 10,000 quota birimi |
| **Google Trends (pytrends)** | ✅ Tamamen Ücretsiz | API key gerekmez, rate limiting var |
| **Reddit API** | ✅ Ücretsiz (2 seçenek) | Public API: Sınırsız (rate limit var)<br>OAuth API: Dakikada 100 sorgu |
| **Twitter/X API** | ⚠️ Sınırlı Ücretsiz | Free tier: Çok sınırlı (önerilmez)<br>Alternatif: Public web scraping |

### API Anahtarlarını Nereden Alabilirim?

#### YouTube Data API v3 (✅ ÜCRETSİZ - ZORUNLU)
**Ücretsiz Kotası:** Günlük 10,000 quota birimi (yeterli)

1. [Google Cloud Console](https://console.cloud.google.com) giriş yapın
2. Yeni proje oluşturun veya mevcut projeyi seçin
3. "APIs & Services" > "Library" bölümüne gidin
4. "YouTube Data API v3" arayın ve etkinleştirin
5. "Credentials" > "Create Credentials" > "API Key"
6. API anahtarınızı kopyalayın

**Not:** Ücretsiz kotası çoğu kullanım için yeterlidir. Quota yönetimi için cache kullanıyoruz.

#### Google Trends (✅ ÜCRETSİZ - API KEY GEREKMEZ)
**Durum:** Tamamen ücretsiz, API key gerekmez

`pytrends` kütüphanesi Google Trends web sitesini kullanır, resmi API değildir:
```bash
pip install pytrends
```

**Not:** Rate limiting var, çok fazla istek gönderirseniz geçici olarak engellenebilirsiniz.

#### Reddit API (✅ ÜCRETSİZ - 2 SEÇENEK)

**Seçenek 1: Public API (Önerilen - API Key Gerekmez)**
- Reddit'in public JSON endpoint'lerini kullanır
- Ücretsiz ve sınırsız (rate limiting var)
- Kimlik doğrulama gerekmez
- Kodumuz zaten bu yöntemi kullanıyor

**Seçenek 2: OAuth API (Opsiyonel - Daha Fazla Özellik)**
1. [Reddit Apps](https://www.reddit.com/prefs/apps) sayfasına gidin
2. "create another app..." butonuna tıklayın
3. Uygulama adı, tip (script) ve redirect URI girin
4. Client ID ve Client Secret'ı kopyalayın

**Limit:** Dakikada 100 sorgu (çoğu kullanım için yeterli)

#### Twitter/X API (⚠️ SINIRLI ÜCRETSİZ - OPSİYONEL)

**Durum:** Twitter'ın ücretsiz planı çok sınırlıdır. İki seçenek:

**Seçenek 1: Twitter Free Tier (Çok Sınırlı)**
1. [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard) giriş yapın
2. "Free" planı seçin
3. Use case formunu doldurun (yukarıdaki örnek metni kullanın)
4. Onaylandıktan sonra API Key'leri alın

**Limit:** Çok düşük (aylık ~1,500 tweet okuma)

**Seçenek 2: Twitter API Kullanmama (Önerilen)**
- Twitter API ücretsiz planı çok sınırlı olduğu için, tool Twitter olmadan da çalışır
- Google Trends ve Reddit yeterli trend verisi sağlar
- Twitter entegrasyonu opsiyoneldir

**Not:** Kodumuz Twitter API olmadan da çalışır, sadece Twitter verisi olmaz.

### API Bağlantılarını Test Et

Tüm API bağlantılarını test etmek için:

```bash
python test_api_connections.py
```

Bu script şunları test eder:
- ✅ YouTube API bağlantısı (ücretsiz)
- ✅ Google Trends (pytrends - ücretsiz, API key gerekmez)
- ✅ Reddit API (public API - ücretsiz, kimlik doğrulama gerekmez)
- ⚠️ Twitter/X API (opsiyonel, çok sınırlı ücretsiz plan)

---

## 🔄 Continuous Learning Başlatma

### Dashboard Üzerinden

1. Dashboard'u başlatın:
   ```bash
   streamlit run dashboard.py
   ```

2. "🔄 Continuous Learning" sayfasına gidin

3. "▶️ Start Learning Loop" butonuna tıklayın

### Komut Satırından

24/7 öğrenme döngüsünü başlatmak için:

```bash
python start_continuous_learning.py
```

Bu script:
- Tüm modülleri başlatır
- Continuous learning loop'u başlatır
- Her saatte bir otomatik öğrenme iterasyonu yapar
- Günlük raporlar oluşturur (09:00'da)

Durdurmak için `Ctrl+C` tuşlarına basın.

### Continuous Learning Ne Yapar?

- ✅ Her saat performans snapshot'ı alır
- ✅ Yeni trendleri keşfeder
- ✅ Knowledge graph'ı günceller
- ✅ A/B test önerileri üretir
- ✅ Günlük/haftalık raporlar oluşturur

---

## 🧪 Gerçek Veri ile Test

### Test Senaryoları

Gerçek kanal verileriyle test yapmak için:

```bash
python test_real_data.py
```

Bu script şunları test eder:
1. **Channel Analysis** - Kanal analizi
2. **Keyword Research** - Anahtar kelime araştırması
3. **Performance Tracking** - Performans takibi
4. **Multi-Source Integration** - Çoklu kaynak entegrasyonu
5. **Safety & Ethics** - Güvenlik ve etik kontrolü

### Test Sonuçları

Test scripti her modül için:
- ✅ Başarılı testler
- ❌ Başarısız testler
- ⚠️ Uyarılar

gösterir.

---

## ⚡ Performans Optimizasyonu

### Otomatik Optimizasyon

Performans optimizasyonu için:

```bash
python optimize_performance.py
```

Bu script:
- JSON dosyalarını optimize eder (eski girişleri temizler)
- Cache performansını kontrol eder
- Optimizasyon önerileri sunar
- `performance_config.json` oluşturur

### Manuel Optimizasyon

#### Cache Temizleme

```bash
# Windows PowerShell
Get-ChildItem -Path .cache -Recurse -File | Where-Object {$_.LastWriteTime -lt (Get-Date).AddDays(-7)} | Remove-Item

# Linux/Mac
find .cache -type f -mtime +7 -delete
```

#### Veri Dosyalarını Temizleme

Eski veri girişlerini temizlemek için `optimize_performance.py` scriptini düzenli olarak çalıştırın.

### Performans Ayarları

`performance_config.json` dosyasını düzenleyerek performans ayarlarını özelleştirebilirsiniz:

```json
{
  "cache": {
    "enabled": true,
    "ttl_seconds": 3600,
    "max_size_mb": 100
  },
  "api": {
    "rate_limit_per_minute": 60,
    "batch_size": 10
  }
}
```

---

## 📊 Dashboard Kullanımı

### Dashboard'u Başlatma

```bash
streamlit run dashboard.py
```

Tarayıcınızda `http://localhost:8501` adresine gidin.

### Özellikler

Dashboard'da şu sayfalar mevcuttur:

- **📊 Dashboard** - Genel bakış
- **📈 Channel Analysis** - Kanal analizi
- **🔍 Keyword Research** - Anahtar kelime araştırması
- **⚔️ Competitor Analysis** - Rakip analizi
- **✏️ Title Optimizer** - Başlık optimizasyonu
- **📝 Description Generator** - Açıklama üretici
- **🏷️ Tag Suggester** - Etiket önerileri
- **📅 Trend Predictor** - Trend tahmini
- **💡 Proactive Advisor** - Proaktif öneriler
- **📊 Performance Tracking** - Performans takibi
- **🎯 Milestone Tracker** - Milestone takibi
- **🧠 Feedback Learning** - Geri bildirim öğrenme
- **🔥 Viral Predictor** - Viral içerik tahmini
- **📊 Competitor Benchmark** - Rakip kıyaslama
- **🌐 Multi-Source Data** - Çoklu kaynak verileri
- **🧠 Knowledge Graph** - Bilgi grafiği
- **🔄 Continuous Learning** - Sürekli öğrenme
- **💻 Code Self-Improvement** - Kod kendini iyileştirme
- **🛡️ Safety & Ethics** - Güvenlik ve etik

---

## 🔧 Sorun Giderme

### "No module named 'diskcache'" Hatası

```bash
pip install diskcache
```

### "YouTube API key not found" Hatası

`.env` dosyasında `YOUTUBE_API_KEY` değişkeninin doğru ayarlandığından emin olun.

### API Quota Hatası

YouTube API günlük 10,000 quota birimi limiti vardır. Cache kullanımını artırın veya API çağrılarını azaltın.

### Cache Sorunları

Cache'i temizlemek için:

```python
from src.utils.youtube_client import create_client
client = create_client()
client.clear_cache()
```

---

## 📝 Sonraki Adımlar

1. ✅ API anahtarlarını yapılandırın
2. ✅ API bağlantılarını test edin
3. ✅ Gerçek veri ile test yapın
4. ✅ Continuous learning'i başlatın
5. ✅ Performans optimizasyonu yapın
6. ✅ Dashboard'u kullanmaya başlayın

---

## 🆘 Yardım

Sorun yaşıyorsanız:
1. `TEST_REPORT.md` dosyasını kontrol edin
2. Test scriptlerini çalıştırın
3. Log dosyalarını inceleyin
4. GitHub Issues'da sorun bildirin

---

**Başarılar! 🚀**

