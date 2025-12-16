# Contributing Guide

ESP32-CAM Davomat Tizimiga hissa qo'shish uchun qo'llanma.

## Development Setup

1. Repository ni fork qiling
2. Clone qiling: `git clone your-fork-url`
3. Setup script ishga tushiring: `./setup.sh` (Linux/Mac) yoki `.\setup.ps1` (Windows)
4. Branch yarating: `git checkout -b feature/your-feature`

## Code Style

### Python (Backend)
- PEP 8 standartiga rioya qiling
- Type hints ishlating
- Docstrings yozing (Google style)
- Black formatter ishlating: `black .`

### TypeScript (Frontend)
- ESLint va Prettier ishlating
- Functional components ishlating
- TypeScript strict mode

### Arduino (ESP32)
- Izohlar yozing
- Magic numbers uchun constants ishlating

## Commit Messages

```
feat: yangi funksiya qo'shish
fix: xatolikni tuzatish
docs: dokumentatsiya yangilash
style: kod formatlash
refactor: kod refactoring
test: test qo'shish
chore: build yoki tool o'zgarishlari
```

## Pull Request

1. Testlarni yozing
2. Dokumentatsiyani yangilang
3. CHANGELOG.md ga qo'shing
4. PR yarating va tavsifini yozing

## Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## Questions?

GitHub Issues da savol bering.
