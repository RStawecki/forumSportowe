# Generated by Django 3.1.5 on 2021-02-02 15:40

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
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('desc', models.TextField()),
                ('image', models.ImageField(blank=True, upload_to='images/')),
                ('createDate', models.DateTimeField(auto_now_add=True)),
                ('category', models.CharField(choices=[('ft', 'Football'), ('bs', 'Basketball'), ('sj', 'Ski Jumping'), ('hb', 'Handball'), ('bx', 'Boxing'), ('vb', 'Volleyball')], default='fb', max_length=2)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
