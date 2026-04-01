from django.db import models

class ProductSet(models.Model):
    title = models.CharField(
        max_length=200, 
        verbose_name="Топтомдун аталышы",
        help_text="Мисалы: Кулпунай классик"
    )
    pieces = models.PositiveIntegerField(
        verbose_name="Даана саны",
        help_text="Топтомдо канча даана бар?"
    )
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=0, 
        verbose_name="Баасы (сом)"
    )
    
    # Даяр болуу убактысы
    ready_time = models.CharField(
        max_length=100, 
        verbose_name="Даяр болуу убактысы", 
        help_text="Мисалы: 2-3 саат же 1 күн",
        default="2 саат"
    )
    
    # Сүрөт (Видеонун ордуна же видео жүктөлгөнгө чейин көрсөтүлөт)
    image = models.ImageField(
        upload_to='sets/images/', 
        verbose_name="Сүрөтү (Превью)",
        null=True,
        blank=True
    )

    # ЖАҢЫ: Видео талаасы
    video = models.FileField(
        upload_to='sets/videos/', 
        verbose_name="Видео (MP4 формат сунушталат)",
        null=True, 
        blank=True,
        help_text="Эгер видео жүктөлсө, сайтта сүрөттүн ордуна видео ойноп турат."
    )
    
    # Топтом жөнүндө маалымат
    description = models.TextField(
        verbose_name="Кошумча маалымат",
        help_text="Топтомдун курамы же өзгөчөлүгү жөнүндө",
        blank=True,
        null=True
    )

    # WhatsApp билдирүүсү
    whatsapp_msg = models.TextField(
        verbose_name="WhatsApp билдирүүсү", 
        help_text="Кардар 'Заказ берүү' баскычын басканда сизге келе турган текст",
        blank=True
    )

    # Модель сакталып жатканда автоматтык түрдө WhatsApp текстин даярдоо
    def save(self, *args, **kwargs):
        if not self.whatsapp_msg:
            self.whatsapp_msg = f"Саламатсызбы! Мен SSMOD сайтынан заказ берейин дегем: {self.title} ({self.pieces} шт). Баасы: {self.price} сом."
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.pieces} шт) - {self.price} сом"

    class Meta:
        verbose_name = "Топтом"
        verbose_name_plural = "Топтомдор"
        ordering = ['-id']