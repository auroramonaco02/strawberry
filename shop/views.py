import os
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from django.utils import timezone   # ← Бул импортту коштук!

import requests
from .models import ProductSet

# Google Gemini
from google import genai
from google.genai.types import GenerateContentConfig  # кошумча (милдеттүү эмес, бирок жакшы)

# Gemini Client (бир жолу гана түзөбүз)
client = genai.Client(api_key=settings.GEMINI_API_KEY)


# ====================== 1. ТЕЛЕГРАМГА ЗАКАЗ ЖӨНӨТҮҮ ======================
def send_telegram_order(name, phone, qty_info, delivery, address, payment, comment):
    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    text = (
        f"🍓 *ЖАҢЫ ЗАКАЗ (SSMOD)* 🍓\n\n"
        f"👤 *Кардар:* {name}\n"
        f"📞 *Телефон:* {phone}\n"
        f"📦 *Топтом:* {qty_info}\n"
        f"🚚 *Алуу ыкмасы:* {delivery}\n"
    )
    
    if delivery in ["Жеткирүү", "Доставка"]:
        if address and address.strip():
            text += f"📍 *Дарек:* {address.strip()}\n"
        else:
            text += f"📍 *Дарек:* (жазылган эмес!)\n"
    
    text += (
        f"💰 *Төлөм:* {payment}\n"
        f"💬 *Комментарий:* {comment if comment else 'Жок'}\n"
        f"────────────────────────────\n"
        f"⏰ {timezone.now().strftime('%d.%m.%Y %H:%M')}"
    )
    
    payload = {
        'chat_id': chat_id, 
        'text': text, 
        'parse_mode': 'Markdown'
    }
    
    try:
        requests.post(url, data=payload, timeout=15)
    except Exception as e:
        print(f"Telegram Error: {e}")


# ====================== 2. БАШКЫ БЕТ (home) ======================
def home(request):
    if request.method == "POST":
        name = request.POST.get('userName', 'Көрсөтүлгөн эмес')
        phone = request.POST.get('userPhone', '').strip()
        qty_info = request.POST.get('orderQty', '').strip()
        delivery = request.POST.get('deliveryMethod', '').strip()
        address = request.POST.get('userAddress', '').strip()
        payment = request.POST.get('paymentMethod', '').strip()
        comment = request.POST.get('userMsg', '').strip()

        # Негизги текшерүү
        if not phone or not qty_info or not delivery:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': 'Телефон, топтом жана алуу ыкмасын толтуруңуз!'})
            messages.error(request, "Керектүү талааларды толтуруңуз!")
            return redirect('home')

        # Доставка болсо адрес милдеттүү
        if delivery in ['Жеткирүү', 'Доставка'] and not address:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': 'Доставка тандасаңыз, дарек жазыңыз!'})
            messages.error(request, "Доставка үчүн дарек милдеттүү!")
            return redirect('home')

        # Телеграмга жөнөтүү
        send_telegram_order(name, phone, qty_info, delivery, address, payment, comment)

        # AJAX суроо болсо
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'ok', 
                'message': 'Заказыңыз ийгиликтүү кабыл алынды! ✨'
            })

        messages.success(request, "Заказыңыз ийгиликтүү кабыл алынды! Жакында байланышабыз.")
        return redirect('home')

    return render(request, 'shop/index.html')


# ====================== 3. GEMINI ЧАТ (ОҢДОЛГОН) ======================
def strawberry_chat(request):
    user_message = request.GET.get('message', '').strip()
    
    if not user_message:
        return JsonResponse({'reply': 'Салам! Кандай жардам бере алам? 🍓'})

    try:
        # Туура жол (2025-2026 версия)
        response = client.models.generate_content(
            model="gemini-1.5-flash",   # же "gemini-2.0-flash-exp" сынап көр
            contents=user_message,
            config=GenerateContentConfig(
                temperature=0.7,
                max_output_tokens=300,
                system_instruction=(
                    "Сен SSMOD дүкөнүнүн сылык жана жардамчысысың. "
                    "Биз премиум шоколаддагы кулпунай сатабыз. "
                    "Баалар: 10шт - 800с, 14шт - 1200с, 18шт - 1400с, 20шт - 1600с. "
                    "Кыска, достук жана кыргызча жооп бер."
                )
            )
        )
        
        reply = response.text if hasattr(response, 'text') else str(response)

    except Exception as e:
        print(f"--- Gemini AI Error: {e} ---")
        reply = "Кечиресиз, учурда AI жардамчы иштебей турат. Менеджер жакында сиз менен байланышабыз! 🍓"

    return JsonResponse({'reply': reply})


# ====================== 4. БАШКА БЕТТЕР ======================
def about(request):
    return render(request, 'shop/about.html')

def price(request):
    sets = ProductSet.objects.all()
    return render(request, 'shop/price.html', {'sets': sets})

def contact(request):
    return render(request, 'shop/contact.html')

def reviews(request):
    return render(request, 'shop/reviews.html')