import os
import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import login

from .models import ProductSet
from .forms import RegistrationForm   # ← Бул сапты ачык калтырыңыз!


# ====================== 1. ТЕЛЕГРАМГА ЗАКАЗ ЖӨНӨТҮҮ ======================
def send_telegram_order(name, phone, qty_info, delivery, address, payment, comment, qr_note=""):
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
        text += f"📍 *Дарек:* {address if address else '(жазылган эмес!)'}\n"
    
    text += f"💰 *Төлөм:* {payment}\n"
    
    # МБанк болсо кошумча билдирүү кошобуз
    if qr_note and ("МБанк" in payment or "Которуу" in payment):
        text += f"📸 *QR Чек:* {qr_note}\n"
    
    text += (
        f"💬 *Комментарий:* {comment if comment else 'Жок'}\n"
        f"────────────────────────────\n"
        f"⏰ {timezone.now().strftime('%d.%m.%Y %H:%M')}"
    )
    
    payload = {'chat_id': chat_id, 'text': text, 'parse_mode': 'Markdown'}
    
    try:
        requests.post(url, data=payload, timeout=15)
    except Exception as e:
        print(f"Telegram Error: {e}")
# ====================== 2. РЕГИСТРАЦИЯ ======================
def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Аккаунтыңыз ийгиликтүү түзүлдү! 🎉")
            return redirect('home')
        else:
            messages.error(request, "Ката кетти. Маалыматтарды текшериңиз.")
    else:
        form = RegistrationForm()

    return render(request, 'shop/register.html', {'form': form})


# ====================== 3. БАШКЫ БЕТ ======================
def home(request):
    if request.method == "POST":
        name = request.POST.get('userName', 'Көрсөтүлгөн эмес')
        phone = request.POST.get('userPhone', '').strip()
        qty_info = request.POST.get('orderQty', '').strip()
        delivery = request.POST.get('deliveryMethod', '').strip()
        address = request.POST.get('userAddress', '').strip()
        payment = request.POST.get('paymentMethod', '').strip()
        comment = request.POST.get('userMsg', '').strip()
        qr_note = request.POST.get('qrNote', '').strip()

        # ==================== ВАЛИДАЦИЯ ====================
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

        # ==================== TELEGRAM ====================
        send_telegram_order(name, phone, qty_info, delivery, address, payment, comment, qr_note)

        # ==================== WHATSAPP ====================
        whatsapp_text = (
            f"🍓 *ЖАҊЫ ЗАКАЗ (SSMOD)* 🍓\n\n"
            f"👤 Кардар: {name}\n"
            f"📞 Телефон: {phone}\n"
            f"📦 Топтом: {qty_info}\n"
            f"🚚 Алуу ыкмасы: {delivery}\n"
        )
        
        if delivery in ["Жеткирүү", "Доставка"] and address:
            whatsapp_text += f"📍 Дарек: {address}\n"
        
        whatsapp_text += f"💰 Төлөм: {payment}\n"
        
        if qr_note:
            whatsapp_text += f"📸 QR Чек: {qr_note}\n"
        
        whatsapp_text += f"💬 Комментарий: {comment if comment else 'Жок'}\n"

        # WhatsApp link
        import urllib.parse
        encoded_text = urllib.parse.quote(whatsapp_text)
        whatsapp_url = f"https://wa.me/996704034209?text={encoded_text}"

        # ==================== ЖООП ====================
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'ok', 
                'message': 'Заказыңыз ийгиликтүү кабыл алынды! ✨',
                'whatsapp_url': whatsapp_url
            })

        messages.success(request, "Заказыңыз ийгиликтүү кабыл алынды! Жакында байланышабыз.")
        return redirect('home')

    return render(request, 'shop/index.html')

# ====================== DEEPSEEK AI ЧАТ ======================
def strawberry_chat(request):
    user_message = request.GET.get('message', '').strip()
    
    if not user_message:
        return JsonResponse({'reply': 'Салам! Кандай жардам бере алам? 🍓'})

    DEEPSEEK_API_KEY = "sk-d9c90c4d4b0f4e1bb8f7a0f8f38adf99"   # Сиздин ачкычыңыз
    
    url = "https://api.deepseek.com/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }

    data = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "system",
                "content": "Сен SSMOD дүкөнүнүн сылык жардамчысысың. Премиум шоколаддагы кулпунай сатабыз..."
            },
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=20)
        if response.status_code == 200:
            result = response.json()
            reply = result['choices'][0]['message']['content']
        else:
            reply = "Кечиресиз, учурда AI бир аз ойлонуп жатат 🍓"
    except Exception:
        reply = "Тармакта ката кетти. Ватсап аркылуу жазыңыз! 🍓"

    return JsonResponse({'reply': reply})


# ====================== ЖЕТИШПЕГЕН БЕТТЕР (View'лар) ======================

def about(request):
    return render(request, 'shop/about.html')

def price(request):
    sets = ProductSet.objects.all()
    return render(request, 'shop/price.html', {'sets': sets})

def contact(request):
    return render(request, 'shop/contact.html')

def reviews(request):
    return render(request, 'shop/reviews.html')

def fresh_view(request):
    return render(request, 'shop/fresh.html')

def callebaut_view(request):
    return render(request, 'shop/callebaut.html')

def handmade_view(request):
    return render(request, 'shop/handmade.html')

def elite_view(request):
    return render(request, 'shop/elite.html')
# Калган view'лар (about, price, contact ж.б.) өзгөрүүсүз калды...