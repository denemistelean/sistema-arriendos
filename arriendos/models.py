from django.db import models


# Create your models here.
class Arriendo(models.Model):
    nombre = models.CharField(max_length=100)
    capital = models.IntegerField()
    porcentaje = models.JSONField()
    mto_interes = models.JSONField()
    fecha = models.DateField()
    estado = models.CharField(max_length=1, choices=[('A', 'Activo'), ('I', 'Inactivo')], default='A')
    fecha_sist = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Pago(models.Model):
    TIPO_PAGO_CHOICES = [
        ('Yape', 'Yape'),
        ('Plin', 'Plin'),
        ('Transferencia', 'Transferencia'),
        ('Efectivo', 'Efectivo'),
        ('Otro', 'Otro'),
    ]

    arriendo = models.ForeignKey(Arriendo, on_delete=models.CASCADE, related_name='pagos')
    fecha = models.DateField()
    ano = models.CharField(max_length=4)
    mes = models.CharField(max_length=20)
    tipo_pago = models.CharField(max_length=50, choices=TIPO_PAGO_CHOICES)
    fecha_sist = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Pago {self.mes}/{self.ano} - {self.arriendo.nombre}'