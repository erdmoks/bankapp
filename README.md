# MiniBank MVC

Flask ve SQLite ile hazırlanmış, temel bankacılık müşteri paneli örneğidir.

## Özellikler

- Müşteri kaydı ve güvenli giriş
- `customer` tablosunda benzersiz `customer_id`
- Werkzeug ile hash'lenmiş şifre saklama
- Basit müşteri dashboard'u
- Mevcut şifre doğrulamalı şifre değiştirme

## Kurulum

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Tarayıcıdan `http://127.0.0.1:5000` adresine gidin. Uygulama ilk açılışta aynı klasörde `banking.db` dosyasını oluşturur.

> Gerçek projede `SECRET_KEY` ortam değişkeni olarak tanımlanmalı; demo uygulamada geliştirme için varsayılan bir değer kullanılmıştır.
