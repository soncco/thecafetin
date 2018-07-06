from django.db import models
from django.contrib.auth.models import User


#Ubicacion
class Local(models.Model):
    nombre = models.CharField(max_length = 20)
    direccion = models.CharField(max_length = 100)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Locales"

class Habitacion(models.Model):
    nombre = models.CharField(max_length = 50)
    pertenece_a = models.ForeignKey(Local, on_delete=models.PROTECT)

    def __str__(self):
        return "%s: %s" % (self.pertenece_a, self.nombre)

    class Meta:
        verbose_name_plural = "Habitaciones"

class Punto(models.Model):
    nombre = models.CharField(max_length = 20)
    pertenece_a  = models.ForeignKey(Local, on_delete=models.PROTECT)

    def __str__(self):
        return "%s: %s" % (self.pertenece_a, self.nombre)

class Cliente(models.Model):
    nombres = models.CharField(max_length = 100)
    apellidos = models.CharField(max_length = 100)
    hospedado_en = models.ForeignKey(Habitacion, on_delete=models.PROTECT)
    pais = models.CharField(max_length = 100)
    documento = models.CharField(max_length = 50)
    activo = models.BooleanField(default = True)
    ingreso_pais = models.DateField()
    ingreso = models.DateField()
    salida = models.DateField(null = True, blank = True)

    def __str__(self):
        return "%s %s" % (self.nombres, self.apellidos)

    def my_habitacion(self):
        return "%s: %s" % (self.hospedado_en.pertenece_a, self.hospedado_en.nombre)
    my_habitacion.short_description = 'Donde está hospedado'

    habitacion = property(my_habitacion)

# Cocina.
class Tipo(models.Model):
    RECIBOS = (
        ('C', 'Comanda'),
        ('D', 'Detalle de Consumo'),
    )
    nombre = models.CharField(max_length = 100)
    recibo = models.CharField(max_length = 1, choices = RECIBOS, default = 'D')

    def __str__(self):
        return self.nombre

class PlatoManager(models.Manager):
    def get_by_natural_key(self, nombre, precio):
        return self.get(nombre = nombre, precio = precio)

class Plato(models.Model):
    objects = PlatoManager()
    nombre = models.CharField(max_length = 255)
    tipo = models.ForeignKey(Tipo, on_delete=models.PROTECT)
    de_venta_en = models.ManyToManyField(Punto)
    foto = models.FileField(upload_to = 'fotos', default = 'default.jpg')
    activo = models.BooleanField(default = True)

    def __str__(self):
        return self.nombre

class PrecioPlato(models.Model):
    precio_de = models.ForeignKey(Plato, on_delete=models.PROTECT)
    precio = models.DecimalField(max_digits = 5, decimal_places = 2, default = 0)
    anio = models.IntegerField(verbose_name = 'Año')

    class Meta:
        verbose_name = "Precio"
        verbose_name_plural = "Precios"

    def __str__(self):
        return str(self.precio)

# Pedidos
class Pedido(models.Model):
    ESTADOS = (
        ('R', 'Recibido'),
        ('A', 'Atendido'),
        ('I', 'Impreso'),
        ('P', 'Pagado'),
    )
    hecho_por = models.ForeignKey(User, on_delete=models.PROTECT)
    para = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    cuando = models.DateTimeField()
    estado = models.CharField(max_length = 1, choices = ESTADOS, default = 'R')
    punto = models.ForeignKey(Punto, on_delete=models.PROTECT)
    notas = models.TextField()

class PedidoDetalle(models.Model):
    pertenece_al_pedido = models.ForeignKey(Pedido, on_delete=models.PROTECT)
    plato = models.ForeignKey(Plato, on_delete=models.PROTECT)
    cantidad = models.IntegerField()

class Visitante(models.Model):
    nombres = models.CharField(max_length = 200)
    local = models.ForeignKey(Local, on_delete=models.PROTECT)
    pedido = models.OneToOneField(Pedido, on_delete=models.PROTECT)

    def __str__(self):
        return self.nombres

class Bitacora(models.Model):
    hecho_por = models.ForeignKey(User, on_delete=models.PROTECT)
    local = models.ForeignKey(Local, on_delete=models.PROTECT)
    cuando = models.DateTimeField()
    mensaje = models.TextField()

class Chat(models.Model):
    hecho_por = models.ForeignKey(User, on_delete=models.PROTECT)
    mensaje = models.TextField()
    cuando = models.DateTimeField()

# Documentos
class Comanda(models.Model):
    numero = models.IntegerField()
    fecha = models.DateField(auto_now_add = True)
    local = models.ForeignKey(Local, on_delete=models.PROTECT)
    pedido = models.OneToOneField(Pedido, on_delete=models.PROTECT)
    total = models.DecimalField(max_digits = 5, decimal_places = 2, default = 0)

    def save(self):
        if self.numero == None:
            total = Comanda.objects.filter(local = self.local).count()
            self.numero = total + 1
        super(Comanda, self).save()

class ComandaDetalle(models.Model):
    pertenece_a_comanda = models.ForeignKey(Comanda, on_delete=models.PROTECT)
    plato = models.ForeignKey(Plato, on_delete=models.PROTECT)
    cantidad = models.IntegerField()
    unitario = models.DecimalField(max_digits = 5, decimal_places = 2, default = 0)
    subtotal = models.DecimalField(max_digits = 5, decimal_places = 2, default = 0)

class Consumo(models.Model):
    numero = models.IntegerField()
    fecha = models.DateField(auto_now_add = True)
    local = models.ForeignKey(Local, on_delete=models.PROTECT)
    pedido = models.OneToOneField(Pedido, on_delete=models.PROTECT)
    total = models.DecimalField(max_digits = 5, decimal_places = 2, default = 0)

    def save(self):
        if self.numero == None:
            total = Consumo.objects.filter(local = self.local).count()
            self.numero = total + 1
        super(Consumo, self).save()

class ConsumoDetalle(models.Model):
    pertenece_a_consumo = models.ForeignKey(Consumo, on_delete=models.PROTECT)
    plato = models.ForeignKey(Plato, on_delete=models.PROTECT)
    cantidad = models.IntegerField()
    unitario = models.DecimalField(max_digits = 5, decimal_places = 2, default = 0)
    subtotal = models.DecimalField(max_digits = 5, decimal_places = 2, default = 0)

class Boleta(models.Model):
    numero = models.IntegerField()
    fecha = models.DateField(auto_now_add = True)
    local = models.ForeignKey(Local, on_delete=models.PROTECT)
    pedido = models.OneToOneField(Pedido, on_delete=models.PROTECT)
    total = models.DecimalField(max_digits = 5, decimal_places = 2, default = 0)

class BoletaDetalle(models.Model):
    pertenece_a_boleta = models.ForeignKey(Boleta, on_delete=models.PROTECT)
    plato = models.ForeignKey(Plato, on_delete=models.PROTECT)
    cantidad = models.IntegerField()
    unitario = models.DecimalField(max_digits = 5, decimal_places = 2, default = 0)
    subtotal = models.DecimalField(max_digits = 5, decimal_places = 2, default = 0)

class Factura(models.Model):
    numero = models.IntegerField()
    fecha = models.DateField(auto_now_add = True)
    local = models.ForeignKey(Local, on_delete=models.PROTECT)
    pedido = models.OneToOneField(Pedido, on_delete=models.PROTECT)
    total = models.DecimalField(max_digits = 5, decimal_places = 2, default = 0)

class FacturaDetalle(models.Model):
    pertenece_a_factura = models.ForeignKey(Factura, on_delete=models.PROTECT)
    plato = models.ForeignKey(Plato, on_delete=models.PROTECT)
    cantidad = models.IntegerField()
    unitario = models.DecimalField(max_digits = 5, decimal_places = 2, default = 0)
    subtotal = models.DecimalField(max_digits = 5, decimal_places = 2, default = 0)