# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

Agar xavfsizlik muammosini topsangiz:

1. **Ommaviy bo'lmagan xabar yuboring**: GitHub Issues da emas!
2. Email: security@example.com (yoki repository owner)
3. Quyidagilarni kiriting:
   - Muammo tavsifi
   - Qayta yaratish qadamlari
   - Potensial ta'sir
   - Tavsiya etilgan yechim (agar bor bo'lsa)

## Security Best Practices

### API Keys
- ✅ API keylarni environment variables da saqlang
- ✅ API keylarni hech qachon commit qilmang
- ✅ Production uchun kuchli keylar ishlating
- ✅ Keylarni muntazam rotate qiling

### Database
- ✅ Kuchli parollar ishlating
- ✅ Database backuplarni shifrlang
- ✅ Minimal privileges principle

### Network
- ✅ HTTPS ishlating (production)
- ✅ CORS to'g'ri sozlang
- ✅ Rate limiting qo'shing

### Face Data
- ✅ Embeddings shifrlangan holda saqlang
- ✅ GDPR/privacy qonunlariga rioya qiling
- ✅ User consent oling

## Known Issues

Hozircha ma'lum xavfsizlik muammolari yo'q.

## Updates

Security yangilanishlar CHANGELOG.md da e'lon qilinadi.
