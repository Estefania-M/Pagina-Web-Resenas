# Generated by Django 4.2 on 2023-06-14 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bannos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ubicacion',
            name='edificio',
            field=models.CharField(choices=[('Escuela', 'Escuela'), ('Física', 'Física'), ('Minas', 'Minas'), ('Justicia Espada', 'Justicia Espada'), ('Eléctrica', 'Eléctrica'), ('Geología', 'Geología'), ('Civil', 'Civil'), ('Norte', 'Norte'), ('Oriente', 'Oriente'), ('Poniente', 'Poniente'), ('Subterraneo', 'Subterraneo')], max_length=250),
        ),
    ]