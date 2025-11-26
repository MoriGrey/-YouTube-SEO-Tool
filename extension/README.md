# YouTube SEO AGI Tool - Browser Extension

Chrome/Firefox extension that enhances YouTube pages with SEO scores, keyword suggestions, and **automatic form filling** in YouTube Studio.

## ✨ Özellikler

- **SEO Score Overlay**: YouTube videolarında gerçek zamanlı SEO skoru
- **Keyword Suggestions**: İlgili anahtar kelime önerileri
- **Auto-Fill Form**: YouTube Studio'da otomatik form doldurma
  - Title otomatik doldurulur
  - Description otomatik doldurulur
  - Tags otomatik eklenir
- **Quick Tips**: Hızlı optimizasyon önerileri
- **Dashboard Link**: Hızlı erişim için dashboard linki

## 🚀 Kurulum

### Chrome

1. `chrome://extensions/` adresine gidin
2. "Developer mode" (Geliştirici modu) açın
3. "Load unpacked" (Paketlenmemiş yükle) tıklayın
4. `extension` klasörünü seçin

### Firefox

1. `about:debugging` adresine gidin
2. "This Firefox" seçin
3. "Load Temporary Add-on" tıklayın
4. `extension/manifest.json` dosyasını seçin

## ⚙️ Yapılandırma

### API URL'lerini Güncelleme

Extension'ı kullanmadan önce API URL'lerini güncellemeniz gerekir:

**1. background.js** (satır ~8):
```javascript
const API_BASE_URL = 'https://your-app-name.streamlit.app/api';
```

**2. content.js** (satır ~8):
```javascript
apiBaseUrl: 'https://your-app-name.streamlit.app/api',
```

**3. popup.js** (satır ~50):
```javascript
chrome.tabs.create({ url: 'https://your-app-name.streamlit.app' });
```

### API Key

Extension, dashboard'daki API key'i kullanır. Dashboard'a giriş yapıp API key'inizi girmeniz yeterlidir.

## 🎯 Kullanım

### YouTube Watch Sayfasında

1. Herhangi bir YouTube videosunu açın
2. Extension otomatik olarak SEO analizi yapar
3. Video bilgilerinin yanında SEO skoru görünür
4. **"✨ Auto-Fill Form"** butonuna tıklayarak YouTube Studio'ya yönlendirilirsiniz

### YouTube Studio'da Otomatik Doldurma

1. YouTube Studio'ya gidin: `https://studio.youtube.com/video/VIDEO_ID/edit`
2. Extension otomatik olarak analiz yapar
3. **"✨ Auto-Fill Form"** butonuna tıklayın
4. Form alanları otomatik doldurulur:
   - ✅ Title
   - ✅ Description  
   - ✅ Tags

### Manuel Auto-Fill

Eğer otomatik doldurma çalışmazsa:

1. Extension popup'ını açın (toolbar icon)
2. "🔍 Analyze Current Video" tıklayın
3. Sonuçları görüntüleyin
4. "✨ Auto-Fill Form" butonunu kullanın

## 📁 Dosya Yapısı

```
extension/
├── manifest.json       # Extension yapılandırması
├── background.js       # Service worker (API iletişimi)
├── content.js         # YouTube sayfalarına enjekte edilen script
├── popup.html         # Extension popup arayüzü
├── popup.js           # Popup script
├── styles.css         # Extension stilleri
├── icons/             # Extension iconları (16x16, 48x48, 128x128)
├── README.md          # Bu dosya
├── INSTALLATION.md    # Detaylı kurulum kılavuzu
└── QUICK_START.md     # Hızlı başlangıç kılavuzu
```

## 🔧 Geliştirme

### Test Etme

1. Extension'ı yükleyin
2. YouTube'da bir video açın
3. Console'u açın (F12) → Logları kontrol edin
4. Extension popup'ını açın → Durumu kontrol edin

### Debugging

**Chrome:**
- `chrome://extensions/` → Extension → "Inspect views: service worker"
- Console'da hataları kontrol edin

**Firefox:**
- `about:debugging` → Extension → "Inspect"
- Console'da hataları kontrol edin

## 🐛 Sorun Giderme

### Extension Görünmüyor
- Extension'ın aktif olduğundan emin olun
- Sayfayı yenileyin (F5)

### SEO Skoru Görünmüyor
- Console'u kontrol edin (F12)
- API URL'lerinin doğru olduğundan emin olun
- API key'in dashboard'da yapılandırıldığından emin olun

### Auto-Fill Çalışmıyor
- YouTube Studio'da olduğunuzdan emin olun
- Sayfanın tamamen yüklendiğinden emin olun
- Form alanlarının boş olduğundan emin olun
- Console'da hata var mı kontrol edin

## 📝 Notlar

- Extension sadece **https** üzerinden çalışır
- YouTube Studio'da auto-fill için sayfanın tamamen yüklenmesi gerekir
- Extension, YouTube'un SPA yapısına uyumludur
- Her video değiştiğinde otomatik olarak yeniden analiz yapar

## 🔄 Güncelleme

Extension'ı güncellemek için:

1. Yeni dosyaları `extension` klasörüne kopyalayın
2. Chrome'da `chrome://extensions/` sayfasına gidin
3. Extension'ın yanındaki **"Reload"** (Yeniden yükle) butonuna tıklayın

## 📞 Destek

Sorun yaşıyorsanız:
- `INSTALLATION.md` dosyasına bakın
- Console loglarını kontrol edin
- API URL'lerinin doğru olduğundan emin olun
