# Generated by Django 5.0.4 on 2024-04-29 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0003_reviews'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attachments',
            name='Image',
        ),
        migrations.AddField(
            model_name='attachments',
            name='File',
            field=models.FileField(default='/attachments/def.png', upload_to='attachments/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='attachments',
            name='Type',
            field=models.CharField(default='', max_length=100),
        ),
    ]
