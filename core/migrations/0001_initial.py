# Generated by Django 2.0.7 on 2018-07-06 12:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bitacora',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cuando', models.DateTimeField()),
                ('mensaje', models.TextField()),
                ('hecho_por', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Boleta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField()),
                ('fecha', models.DateField(auto_now_add=True)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='BoletaDetalle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('unitario', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('pertenece_a_boleta', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.Boleta')),
            ],
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mensaje', models.TextField()),
                ('cuando', models.DateTimeField()),
                ('hecho_por', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombres', models.CharField(max_length=100)),
                ('apellidos', models.CharField(max_length=100)),
                ('pais', models.CharField(max_length=100)),
                ('documento', models.CharField(max_length=50)),
                ('activo', models.BooleanField(default=True)),
                ('ingreso_pais', models.DateField()),
                ('ingreso', models.DateField()),
                ('salida', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comanda',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField()),
                ('fecha', models.DateField(auto_now_add=True)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='ComandaDetalle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('unitario', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('pertenece_a_comanda', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.Comanda')),
            ],
        ),
        migrations.CreateModel(
            name='Consumo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField()),
                ('fecha', models.DateField(auto_now_add=True)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='ConsumoDetalle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('unitario', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('pertenece_a_consumo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.Consumo')),
            ],
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.IntegerField()),
                ('fecha', models.DateField(auto_now_add=True)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='FacturaDetalle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('unitario', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('pertenece_a_factura', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.Factura')),
            ],
        ),
        migrations.CreateModel(
            name='Habitacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Habitaciones',
            },
        ),
        migrations.CreateModel(
            name='Local',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
                ('direccion', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Locales',
            },
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cuando', models.DateTimeField()),
                ('estado', models.CharField(choices=[('R', 'Recibido'), ('A', 'Atendido'), ('I', 'Impreso'), ('P', 'Pagado')], default='R', max_length=1)),
                ('notas', models.TextField()),
                ('hecho_por', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('para', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.Cliente')),
            ],
        ),
        migrations.CreateModel(
            name='PedidoDetalle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('pertenece_al_pedido', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.Pedido')),
            ],
        ),
        migrations.CreateModel(
            name='Plato',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('foto', models.FileField(default='default.jpg', upload_to='fotos')),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='PrecioPlato',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('anio', models.IntegerField(verbose_name='Año')),
                ('precio_de', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.Plato')),
            ],
            options={
                'verbose_name': 'Precio',
                'verbose_name_plural': 'Precios',
            },
        ),
        migrations.CreateModel(
            name='Punto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
                ('pertenece_a', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.Local')),
            ],
        ),
        migrations.CreateModel(
            name='Tipo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('recibo', models.CharField(choices=[('C', 'Comanda'), ('D', 'Detalle de Consumo')], default='D', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Visitante',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombres', models.CharField(max_length=200)),
                ('local', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.Local')),
                ('pedido', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='core.Pedido')),
            ],
        ),
        migrations.AddField(
            model_name='plato',
            name='de_venta_en',
            field=models.ManyToManyField(to='core.Punto'),
        ),
        migrations.AddField(
            model_name='plato',
            name='tipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.Tipo'),
        ),
        migrations.AddField(
            model_name='pedidodetalle',
            name='plato',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.Plato'),
        ),
        migrations.AddField(
            model_name='pedido',
            name='punto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.Punto'),
        ),
        migrations.AddField(
            model_name='habitacion',
            name='pertenece_a',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.Local'),
        ),
        migrations.AddField(
            model_name='facturadetalle',
            name='plato',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.Plato'),
        ),
        migrations.AddField(
            model_name='factura',
            name='local',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.Local'),
        ),
        migrations.AddField(
            model_name='factura',
            name='pedido',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='core.Pedido'),
        ),
        migrations.AddField(
            model_name='consumodetalle',
            name='plato',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.Plato'),
        ),
        migrations.AddField(
            model_name='consumo',
            name='local',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.Local'),
        ),
        migrations.AddField(
            model_name='consumo',
            name='pedido',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='core.Pedido'),
        ),
        migrations.AddField(
            model_name='comandadetalle',
            name='plato',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.Plato'),
        ),
        migrations.AddField(
            model_name='comanda',
            name='local',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.Local'),
        ),
        migrations.AddField(
            model_name='comanda',
            name='pedido',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='core.Pedido'),
        ),
        migrations.AddField(
            model_name='cliente',
            name='hospedado_en',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.Habitacion'),
        ),
        migrations.AddField(
            model_name='boletadetalle',
            name='plato',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.Plato'),
        ),
        migrations.AddField(
            model_name='boleta',
            name='local',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.Local'),
        ),
        migrations.AddField(
            model_name='boleta',
            name='pedido',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='core.Pedido'),
        ),
        migrations.AddField(
            model_name='bitacora',
            name='local',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='core.Local'),
        ),
    ]
