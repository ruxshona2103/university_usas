import json
from django.http import JsonResponse


def translate_view(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    try:
        from deep_translator import GoogleTranslator
        body = json.loads(request.body)
        text = (body.get('text') or '').strip()
        if not text:
            return JsonResponse({'ru': '', 'en': ''})
        ru = GoogleTranslator(source='uz', target='ru').translate(text) or ''
        en = GoogleTranslator(source='uz', target='en').translate(text) or ''
        return JsonResponse({'ru': ru, 'en': en})
    except Exception as exc:
        return JsonResponse({'error': str(exc)}, status=500)
