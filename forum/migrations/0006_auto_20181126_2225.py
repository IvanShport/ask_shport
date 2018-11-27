# Generated by Django 2.1.2 on 2018-11-26 19:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0005_auto_20181126_2200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likecomment',
            name='comment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='forum.Comment'),
        ),
        migrations.AlterField(
            model_name='likecomment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='authorization.Profile'),
        ),
        migrations.AlterField(
            model_name='likepost',
            name='post',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='forum.Post'),
        ),
        migrations.AlterField(
            model_name='likepost',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='authorization.Profile'),
        ),
    ]
