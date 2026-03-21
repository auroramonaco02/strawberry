from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ProductSet
import requests
from django.conf import settings

# Төмөндөгү функция Телеграмга билдирүү жөнөтөт (Backend аркылуу)
def send_telegram_message(name, phone, message):
    token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    text = (
        f"🍰 *Жаңы заказ (SSMOD)*\n\n"
        f"👤 *Аты:* {name}\n"
        f"📞 *Тел:* {phone}\n"
        f"💬 *Билдирүү:* {message if message else 'Жок'}"
    )
    
    payload = {'chat_id': chat_id, 'text': text, 'parse_mode': 'Markdown'}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Telegram Error: {e}")

def home(request):
    # Эгер формадан (POST) маалымат келсе:
    if request.method == "POST":
        user_name = request.POST.get('userName')
        user_phone = request.POST.get('userPhone')
        user_msg = request.POST.get('userMsg')
        
        # Телеграмга жөнөтүү функциясын чакырабыз
        send_telegram_message(user_name, user_phone, user_msg)
        
        # Колдонуучуга билдирүү көрсөтүп, кайра башкы бетке багыттайбыз
        messages.success(request, "Заказыңыз кабыл алынды!")
        return redirect('home')

    # Башкы бет үчүн маалыматтар (өзгөрүүсүз калды)
    products = ProductSet.objects.all()
    return render(request, 'shop/index.html', {'products': products})

def about(request):
    return render(request, 'shop/about.html')

def price(request):
    sets = ProductSet.objects.all()
    return render(request, 'shop/price.html', {'sets': sets})

def reviews(request):
    return render(request, 'shop/reviews.html')

def contact(request):
    return render(request, 'shop/contact.html')