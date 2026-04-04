import os
import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from django.utils import timezone

from .models import ProductSet

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

        if not phone or not qty_info or not delivery:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': 'Телефон, топтом жана алуу ыкмасын толтуруңуз!'})
            messages.error(request, "Керектүү талааларды толтуруңуз!")
            return redirect('home')

        if delivery in ['Жеткирүү', 'Доставка'] and not address:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': 'Доставка тандасаңыз, дарек жазыңыз!'})
            messages.error(request, "Доставка үчүн дарек милдеттүү!")
            return redirect('home')

        send_telegram_order(name, phone, qty_info, delivery, address, payment, comment)

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'ok', 
                'message': 'Заказыңыз ийгиликтүү кабыл алынды! ✨'
            })

        messages.success(request, "Заказыңыз ийгиликтүү кабыл алынды! Жакында байланышабыз.")
        return redirect('home')

    return render(request, 'shop/index.html')


# ====================== 3. DEEPSEEK AI ЧАТ (ЖАҢЫЛАНДЫ) ======================
def strawberry_chat(request):
    user_message = request.GET.get('message', '').strip()
    
    if not user_message:
        return JsonResponse({'reply': 'Салам! Кандай жардам бере алам? 🍓'})

    # Сиздин DeepSeek API ачкычыңыз
    DEEPSEEK_API_KEY = "sk-d9c90c4d4b0f4e1bb8f7a0f8f38adf99"
    url = "https://api.deepseek.com/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }

    data = {
        "model": "deepseek-chat", # Бул DeepSeek-V3 модели
        "messages": [
            {
                "role": "system", 
                "content": (
                    "Сен SSMOD дүкөнүнүн сылык жана жардамчысысың. "
                    "Биз премиум шоколаддагы кулпунай сатабыз. "
                    "Баалар: 10шт - 800с, 14шт - 1200с, 18шт - 1400с, 20шт - 1600с. "
                    "Жоопторуңду кыска, сылык, премиум люкс стилде жана кыргыз тилинде гана бер."
                )
            },
            {"role": "user", "content": user_message}
        ],
        "stream": False,
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=20)
        
        if response.status_code == 200:
            result = response.json()
            reply = result['choices'][0]['message']['content']
        else:
            print(f"DeepSeek API Status Error: {response.status_code}")
            reply = "Кечиресиз, учурда AI жардамчы бир аз ойлонуп жатат. Менеджер сизге жакында жооп берет! 🍓"

    except Exception as e:
        print(f"--- DeepSeek AI Connection Error: {e} ---")
        reply = "Тармакта ката кетти. Бизге Ватсап аркылуу жазсаңыз болот! 🍓"

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