from django.contrib import admin
from .models import ProductSet

@admin.register(ProductSet)
class ProductSetAdmin(admin.ModelAdmin):
    # Админканын башкы тизмесинде көрүнө турган колонкалар
    list_display = ('title', 'price', 'pieces', 'ready_time')
    
    # Ичине киргенде көрүнө турган жана өзгөртө турган талаалар
    # Бул жерге 'video' талаасын коштук, ошондо админкадан видео жүктөй аласыз
    fields = (
        'title', 
        'pieces', 
        'price', 
        'ready_time', 
        'image', 
        'video',  # Видео талаасы ушул жерде
        'description', 
        'whatsapp_msg'
    )
    
    # WhatsApp билдирүүсүн автоматтык толтуруу үчүн readonly кылсаңыз да болот
    # readonly_fields = ('whatsapp_msg',)