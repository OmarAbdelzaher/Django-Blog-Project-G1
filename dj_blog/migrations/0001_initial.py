# Generated by Django 3.2.12 on 2022-02-17 18:35

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
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat_name', models.CharField(max_length=100)),
                ('user', models.ManyToManyField(related_name='categories', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_body', models.CharField(max_length=100)),
                ('comment_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='dj_blog.comment')),
            ],
        ),
        migrations.CreateModel(
            name='ForbiddenWords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('forbidden_word', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='PostTags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reply_body', models.CharField(max_length=100)),
                ('reply_time', models.TimeField(null=True)),
                ('comment_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dj_blog.comment')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('picture', models.ImageField(null=True, upload_to='images/')),
                ('content', models.CharField(max_length=255)),
                ('date_of_publish', models.DateTimeField(auto_now_add=True, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dj_blog.category')),
                ('dislikes', models.ManyToManyField(blank=True, related_name='dislikes', to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(blank=True, related_name='likes', to=settings.AUTH_USER_MODEL)),
                ('tag', models.ManyToManyField(blank=True, to='dj_blog.PostTags')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='post_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='dj_blog.post'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(null=True, upload_to='dj_blog/static/img/Users Images/')),
                ('is_locked', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
