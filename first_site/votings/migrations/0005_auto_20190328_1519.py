# Generated by Django 2.1.7 on 2019-03-28 09:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('votings', '0004_auto_20190328_1054'),
    ]

    operations = [
        migrations.CreateModel(
            name='Styles',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('style', models.CharField(max_length=150)),
            ],
        ),
        migrations.RemoveField(
            model_name='document',
            name='coordinates',
        ),
        migrations.AlterField(
            model_name='document',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='styles',
            name='roomId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='votings.Document'),
        ),
    ]
