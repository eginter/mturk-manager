# Generated by Django 2.0 on 2019-01-11 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0046_template_worker_template_hit'),
    ]

    operations = [
        migrations.AddField(
            model_name='message_reject',
            name='message_lowercase',
            field=models.CharField(default='t', max_length=1024, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='message_reject',
            name='message',
            field=models.CharField(max_length=1024),
        ),
    ]
