# university_usas

## Local ishga tushirish (venv)

1) Venv yaratish + dependency o'rnatish:
- `bash scripts/setup_venv.sh`

2) `.env` yaratish:
- `cp .env.example .env`

3) Migratsiya va server:
- `source .venv/bin/activate`
- `python manage.py migrate`
- `python manage.py runserver`

## Production (Koyeb)

- `.env`da `DJANGO_SETTINGS_MODULE=config.settings.prod` qo'ying
- `DATABASE_URL` va ImageKit (`IMAGEKIT_PUBLIC_KEY/PRIVATE_KEY/URL_ENDPOINT`) majburiy
