# 🚀 Quick API Test Guide

## ❌ Sorun: "Failed to fetch" Hatası

`file://` protokolü ile açılan HTML dosyaları CORS hatası verir. Bu normal bir browser güvenlik kısıtlamasıdır.

## ✅ Çözüm: Direkt Browser Test

### Yöntem 1: Direkt Link Test (EN KOLAY)

Aşağıdaki linki **yeni sekmede** açın:

**Health Check:**
```
https://youtoubeseo.streamlit.app?_api=true&action=health
```

**Beklenen Sonuç:**
```json
{
  "status": "ok",
  "service": "YouTube SEO AGI Tool API",
  "version": "1.0.0"
}
```

Eğer bu JSON'u görüyorsanız → ✅ **API ÇALIŞIYOR!**

---

### Yöntem 2: Browser Console Test

1. **Herhangi bir web sayfasında** F12 tuşuna basın
2. **Console** sekmesine gidin
3. Aşağıdaki kodu yapıştırın ve Enter'a basın:

```javascript
fetch('https://youtoubeseo.streamlit.app?_api=true&action=health')
  .then(r => r.text())
  .then(text => {
    console.log('Raw response:', text);
    // Try to parse JSON
    try {
      const json = JSON.parse(text);
      console.log('✅ Success! JSON:', json);
    } catch(e) {
      // Try to extract from HTML
      const match = text.match(/<pre[^>]*id=["']json-response["'][^>]*>([\s\S]*?)<\/pre>/);
      if (match) {
        const json = JSON.parse(match[1]);
        console.log('✅ Success! Extracted JSON:', json);
      } else {
        console.log('⚠️ Response is HTML, check the page');
      }
    }
  })
  .catch(err => console.error('❌ Error:', err));
```

**Beklenen Sonuç:**
- Console'da `✅ Success! JSON: {status: "ok", ...}` görünmeli

---

### Yöntem 3: Extension Test (ÖNERİLEN)

Extension'lar CORS'tan etkilenmez, bu yüzden en güvenilir test yöntemi:

1. **Chrome'da extension'ı yükle/reload et:**
   - `chrome://extensions/` → Extension'ı bul → "Reload"

2. **YouTube'da bir video aç:**
   - Herhangi bir YouTube videosu

3. **Extension'ı test et:**
   - Extension popup'ını aç
   - Video analizini başlat
   - Console'da (F12) hata var mı kontrol et

4. **Console loglarını kontrol et:**
   - F12 → Console
   - Extension loglarını görürsünüz
   - "Testing API connection" mesajını arayın

---

### Yöntem 4: Python Test (Terminal)

Eğer Python yüklüyse:

```bash
python -c "import requests; r = requests.get('https://youtoubeseo.streamlit.app?_api=true&action=health'); print('Status:', r.status_code); print('Response:', r.text)"
```

**Beklenen Sonuç:**
```
Status: 200
Response: {"status": "ok", "service": "YouTube SEO AGI Tool API", "version": "1.0.0"}
```

---

## 🔍 Sorun Giderme

### Eğer direkt link çalışmıyorsa:

1. **App'in çalışıp çalışmadığını kontrol edin:**
   - https://youtoubeseo.streamlit.app adresini açın
   - App açılıyorsa → App çalışıyor ✅
   - App açılmıyorsa → App down, Streamlit Cloud'u kontrol edin

2. **Network hatası:**
   - İnternet bağlantınızı kontrol edin
   - Firewall/proxy ayarlarını kontrol edin

3. **CORS hatası (sadece file:// için):**
   - Normal! `file://` protokolü CORS'a izin vermez
   - Yukarıdaki yöntemleri kullanın (direkt link, console, extension)

---

## ✅ Başarı Kriterleri

API çalışıyorsa:
- ✅ Direkt link JSON döndürür
- ✅ Browser console'da fetch başarılı olur
- ✅ Extension API çağrıları çalışır
- ✅ Python/curl test başarılı olur

---

## 📝 Notlar

- **Extension'lar CORS'tan etkilenmez** → En güvenilir test yöntemi
- **file:// protokolü CORS'a izin vermez** → Normal browser davranışı
- **Streamlit Cloud CORS aktif** → `.streamlit/config.toml`'de `enableCORS = true`

---

**Son Güncelleme:** 2025-01-26

