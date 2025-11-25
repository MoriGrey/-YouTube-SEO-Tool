# Authentication Setup Guide

## 🔐 İlk Kurulum

### 1. Default Kullanıcı

İlk kurulumda otomatik olarak bir admin kullanıcısı oluşturulur:

- **Username:** `admin`
- **Password:** `admin123`
- **Email:** `admin@example.com`

**⚠️ ÖNEMLİ:** İlk girişten sonra şifreyi değiştirin!

### 2. Manuel Kurulum

Eğer farklı kullanıcı oluşturmak isterseniz:

```bash
python setup_auth.py
```

Bu script size kullanıcı bilgilerini soracak ve `config/auth_config.yaml` dosyasını oluşturacak.

### 3. Yeni Kullanıcı Ekleme

`config/auth_config.yaml` dosyasını düzenleyerek yeni kullanıcı ekleyebilirsiniz:

```yaml
credentials:
  usernames:
    admin:
      email: admin@example.com
      failed_login_attempts: 0
      logged_in: false
      name: Admin User
      password: $2b$12$...  # bcrypt hash
    newuser:
      email: user@example.com
      failed_login_attempts: 0
      logged_in: false
      name: New User
      password: $2b$12$...  # bcrypt hash
```

**Password Hash Oluşturma:**

```python
import streamlit_authenticator as stauth
hashed_password = stauth.Hasher(['your_password']).generate()[0]
print(hashed_password)
```

## 🔒 Güvenlik

### Production İçin

1. **Cookie Key Değiştirin:**
   - `config/auth_config.yaml` dosyasındaki `cookie.key` değerini değiştirin
   - Veya `AUTH_COOKIE_KEY` environment variable'ı kullanın

2. **Default Şifreyi Değiştirin:**
   - İlk girişten sonra mutlaka şifreyi değiştirin
   - Güçlü şifre kullanın (en az 12 karakter)

3. **Config Dosyasını Güvenli Tutun:**
   - `config/auth_config.yaml` dosyasını Git'e commit etmeyin
   - `.gitignore` dosyasına eklendi ✅

## 📝 Kullanım

### Login

1. Dashboard açıldığında login ekranı görünür
2. Username ve password girin
3. "Login" butonuna tıklayın

### Logout

1. Sidebar'dan "🚪 Logout" butonuna tıklayın
2. Session sonlanır ve login ekranına dönersiniz

### Session Yönetimi

- Cookie-based session (30 gün geçerli)
- Session state'te kullanıcı bilgileri saklanır
- Logout ile session temizlenir

## 🔍 Troubleshooting

### "ModuleNotFoundError: No module named 'streamlit_authenticator'"

**Çözüm:**
```bash
pip install streamlit-authenticator PyYAML bcrypt
```

### "Config file not found"

**Çözüm:**
```bash
python setup_auth.py
```

### Login çalışmıyor

**Kontrol:**
1. `config/auth_config.yaml` dosyasının var olduğundan emin olun
2. Password hash'in doğru olduğundan emin olun
3. Cookie key'in doğru olduğundan emin olun

---

**Not:** Authentication aktif olduğunda, tüm kullanıcılar login olmadan dashboard'a erişemez.

