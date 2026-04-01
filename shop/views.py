import os
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
import requests
from .models import ProductSet

# ЖАҢЫ Gemini китепканасы
from google import genai

# Gemini'ни жөндөө
client = genai.Client(api_key=settings.GEMINI_API_KEY)

# 1. Телеграмга заказ жөнөтүү
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
    if delivery == "Жеткирүү":
        text += f"📍 *Дарек:* {address}\n"
        
    text += (
        f"💰 *Төлөм:* {payment}\n"
        f"💬 *Комментарий:* {comment if comment else 'Жок'}\n"
        f"------------------------------"
    )
    
    payload = {'chat_id': chat_id, 'text': text, 'parse_mode': 'Markdown'}
    try:
        requests.post(url, data=payload, timeout=10)
    except Exception as e:
        print(f"Telegram Error: {e}")

# 2. Башкы бет
def home(request):
    if request.method == "POST":
        name = request.POST.get('userName', 'Көрсөтүлгөн эмес')
        phone = request.POST.get('userPhone')
        qty_info = request.POST.get('orderQty')
        delivery = request.POST.get('deliveryMethod')
        address = request.POST.get('userAddress', 'Көрсөтүлгөн эмес')
        payment = request.POST.get('paymentMethod')
        comment = request.POST.get('userMsg')

        if phone and qty_info:
            send_telegram_order(name, phone, qty_info, delivery, address, payment, comment)
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'ok'})
            messages.success(request, "Заказыңыз кабыл алынды!")
            return redirect('home')
    return render(request, 'shop/index.html')

# 3. Жаңыланган Акылдуу Чат (Gemini)
def strawberry_chat(request):
    user_message = request.GET.get('message', '')
    if user_message:
        try:
            prompt = (
                "Сен 'SSMOD' дүкөнүнүн жардамчысысың. Биз шоколаддагы кулпунайларды сатабыз. "
                "Баалар: 10шт-1200с, 14шт-1600с, 18шт-2000с, 20шт-2200с. "
                "Кыска жана сылык кыргызча жооп бер. "
                f"Кардардын суроосу: {user_message}"
            )
            
            # Жаңы китепкананын форматы (моделдин атын gemini-2.0-flash же gemini-1.5-flash кылып көр)
            response = client.models.generate_content(
                model="gemini-1.5-flash", 
                contents=prompt
            )
            reply = response.text
        except Exception as e:
            print(f"--- AI ERROR: {e} ---")
            # Эгер модель табылбаса (404), анда менеджерге багыттайбыз
            reply = "Кечиресиз, учурда байланыш үзүлдү. Менеджер жакында жооп берет! 🍓"
    else:
        reply = "Салам! Кандай жардам бере алам?"
    
    return JsonResponse({'reply': reply})
# 4. Башка баракчалар (БУЛ ЖЕР МААНИЛҮҮ)
def about(request):
    return render(request, 'shop/about.html')

def price(request):
    sets = ProductSet.objects.all()
    return render(request, 'shop/price.html', {'sets': sets})

def contact(request):
    return render(request, 'shop/contact.html')

def reviews(request):
    return render(request, 'shop/reviews.html')