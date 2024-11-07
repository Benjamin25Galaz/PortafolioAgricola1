from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



# Create your models here.

class Tema(models.Model):
    author= models.ForeignKey(User, on_delete=models.CASCADE)  # El campo autor debe existir
    titulo = models.CharField(max_length=200)
    content = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.titulo
    
class Comment(models.Model):
    tema = models.ForeignKey(Tema, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.tema}'
    
class Donacion(models.Model):
    OPCIONES = [
        ('Planta un Árbol', 'Planta un Árbol'),
        ('Herramientas', 'Herramientas'),
        ('Desechos', 'Desechos'),
    ]

    COMUNAS = [
        ('Alhué', 'Alhué'),
        ('Buin', 'Buin'),
        ('Cerrillos', 'Cerrillos'),
        ('Cerro Navia', 'Cerro Navia'),
        ('Colina', 'Colina'),
        ('El Bosque', 'El Bosque'),
        ('Estación Central', 'Estación Central'),
        ('Huechuraba', 'Huechuraba'),
        ('Independencia', 'Independencia'),
        ('La Florida', 'La Florida'),
        ('La Granja', 'La Granja'),
        ('La Pintana', 'La Pintana'),
        ('La Reina', 'La Reina'),
        ('Las Condes', 'Las Condes'),
        ('Lo Barnechea', 'Lo Barnechea'),
        ('Lo Espejo', 'Lo Espejo'),
        ('Maipú', 'Maipú'),
        ('Ñuñoa', 'Ñuñoa'),
        ('Pedro Aguirre Cerda', 'Pedro Aguirre Cerda'),
        ('Peñalolén', 'Peñalolén'),
        ('Providencia', 'Providencia'),
        ('Pudahuel', 'Pudahuel'),
        ('Quilicura', 'Quilicura'),
        ('Quinta Normal', 'Quinta Normal'),
        ('Recoleta', 'Recoleta'),
        ('Renca', 'Renca'),
        ('San Bernardo', 'San Bernardo'),
        ('San Joaquín', 'San Joaquín'),
        ('San Miguel', 'San Miguel'),
        ('San Ramón', 'San Ramón'),
        ('Santiago', 'Santiago'),
        ('Vitacura', 'Vitacura'),
    ]
    
    TIPOS_ARBOL = [
        ('Roble', 'Roble'),
        ('Árbol de Neem', 'Árbol de Neem'),
        ('Cedro', 'Cedro'),
    ]

    PRECIO_ARBOL = {
        'Roble': 5000,
        'Árbol de Neem': 8000,
        'Cedro': 12000,
    }

    opcion = models.CharField(max_length=100, choices=OPCIONES)
    comuna = models.CharField(max_length=100, choices=COMUNAS)
    tipo_arbol = models.CharField(max_length=100, choices=TIPOS_ARBOL)
    cantidad = models.IntegerField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    valor_total = models.PositiveIntegerField(default=0)

    class Meta:
        managed = True
        db_table = 'donacion'
        constraints = [
            models.UniqueConstraint(fields=['opcion', 'comuna', 'tipo_arbol', 'cantidad'], name='unique_donation')
        ]

    def save(self, *args, **kwargs):
        if self.tipo_arbol in self.PRECIO_ARBOL:
            self.valor_total = self.cantidad * self.PRECIO_ARBOL[self.tipo_arbol]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.opcion} - {self.cantidad} semillas"

class Solicitud(models.Model):
    RETIRO_AGUAS = 'retiro_aguas_piscina'
    RETIRO_ARBOLES = 'retiro_arboles'

    COMUNAS = [
        ('Alhué', 'Alhué'),
        ('Buin', 'Buin'),
        ('Cerrillos', 'Cerrillos'),
        ('Cerro Navia', 'Cerro Navia'),
        ('Colina', 'Colina'),
        ('El Bosque', 'El Bosque'),
        ('Estación Central', 'Estación Central'),
        ('Huechuraba', 'Huechuraba'),
        ('Independencia', 'Independencia'),
        ('La Florida', 'La Florida'),
        ('La Granja', 'La Granja'),
        ('La Pintana', 'La Pintana'),
        ('La Reina', 'La Reina'),
        ('Las Condes', 'Las Condes'),
        ('Lo Barnechea', 'Lo Barnechea'),
        ('Lo Espejo', 'Lo Espejo'),
        ('Maipú', 'Maipú'),
        ('Ñuñoa', 'Ñuñoa'),
        ('Pedro Aguirre Cerda', 'Pedro Aguirre Cerda'),
        ('Peñalolén', 'Peñalolén'),
        ('Providencia', 'Providencia'),
        ('Pudahuel', 'Pudahuel'),
        ('Quilicura', 'Quilicura'),
        ('Quinta Normal', 'Quinta Normal'),
        ('Recoleta', 'Recoleta'),
        ('Renca', 'Renca'),
        ('San Bernardo', 'San Bernardo'),
        ('San Joaquín', 'San Joaquín'),
        ('San Miguel', 'San Miguel'),
        ('San Ramón', 'San Ramón'),
        ('Santiago', 'Santiago'),
        ('Vitacura', 'Vitacura'),
    ]

    TIPO_SOLICITUD_CHOICES = [
        (RETIRO_AGUAS, 'Retiro de aguas de piscinas'),
        (RETIRO_ARBOLES, 'Retiro de árboles'),
    ]

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    tipo_solicitud = models.CharField(max_length=50, choices=TIPO_SOLICITUD_CHOICES)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField()
    direccion = models.CharField(max_length=200)
    comuna = models.CharField(max_length=100, choices=COMUNAS)
    fecha_retiro = models.DateField()
    cantidad_arboles = models.IntegerField(null=True, blank=True)
    cantidad_litros = models.IntegerField(null=True, blank=True)
    comentarios = models.TextField(null=True, blank=True)

    def __str__(self):
        
        return f'{self.nombre} {self.apellido}'



class Register(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo_electronico = models.EmailField(max_length=100)
    contrasena = models.CharField(max_length=100)
    confirmar_contrasena = models.CharField(max_length=100)

    def str(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    imagen = models.ImageField(upload_to='productos/')
    stock = models.PositiveIntegerField()

    def __str__(self):
        return self.nombre

    def verificar_y_reponer_stock(self):
        if self.stock == 0:
            self.stock = 5
            self.save()

class Pago(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField()
    telefono = models.CharField(max_length=15)
    total = models.PositiveIntegerField()

    def __str__(self):
        return f"Pago de {self.nombre} {self.apellido} - {self.total} CLP"
    


class Compra(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)

class CompraProducto(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

