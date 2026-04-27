#!/usr/bin/env bash
# =============================================================================
#  deploy.sh  —  O'ZDSA backend deployment skripti
#  Ishlatish:
#    chmod +x deploy.sh
#    ./deploy.sh           # migrate + seed (birinchi deploy)
#    ./deploy.sh --no-seed # faqat migrate (keyingi deploylar)
#    ./deploy.sh --clear   # migrate + barcha seedlarni tozalab qayta yozadi
# =============================================================================

set -euo pipefail

SETTINGS="config.settings.prod"
PYTHON="${PYTHON:-python}"          # venv ichida python bo'lsa shu ishlaydi
MANAGE="$PYTHON manage.py"

RUN_SEED=true
CLEAR_FLAG=""

# ── Argumentlarni parse qilish ─────────────────────────────────────────────
for arg in "$@"; do
  case $arg in
    --no-seed) RUN_SEED=false ;;
    --clear)   CLEAR_FLAG="--clear" ;;
    *) echo "Noma'lum argument: $arg"; exit 1 ;;
  esac
done

echo ""
echo "============================================"
echo "  O'ZDSA DEPLOY — settings: $SETTINGS"
echo "============================================"

# ── 1. Statik fayllar ─────────────────────────────────────────────────────
echo ""
echo "[1/4] collectstatic..."
$MANAGE collectstatic --noinput --settings=$SETTINGS

# ── 2. Migratsiyalar ──────────────────────────────────────────────────────
echo ""
echo "[2/4] migrate..."
$MANAGE migrate --settings=$SETTINGS

# ── 3. Superuser (faqat mavjud bo'lmasa) ─────────────────────────────────
echo ""
echo "[3/4] Superuser tekshirilmoqda..."
$MANAGE shell --settings=$SETTINGS -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    import os
    User.objects.create_superuser(
        username=os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin'),
        password=os.getenv('DJANGO_SUPERUSER_PASSWORD', 'admin1234'),
        email=os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@usas.uz'),
    )
    print('  Superuser yaratildi.')
else:
    print('  Superuser mavjud, o\\'tilib ketildi.')
"

# ── 4. Seed ───────────────────────────────────────────────────────────────
if [ "$RUN_SEED" = true ]; then
  echo ""
  echo "[4/4] seed_all $CLEAR_FLAG ..."
  $MANAGE seed_all $CLEAR_FLAG --settings=$SETTINGS
else
  echo ""
  echo "[4/4] seed o'tkazib yuborildi (--no-seed)."
fi

echo ""
echo "============================================"
echo "  DEPLOY MUVAFFAQIYATLI YAKUNLANDI"
echo "============================================"
echo ""
