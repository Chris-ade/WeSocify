# Generated by Django 4.1.4 on 2023-02-01 20:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import feed.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feed', '0012_remove_feed_is_reposted'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to=feed.models.get_comment_image_filename, verbose_name='comment_images')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RenameModel(
            old_name='FeedImages',
            new_name='FeedMedia',
        ),
        migrations.RenameModel(
            old_name='FeedComments',
            new_name='Comments',
        ),
        migrations.DeleteModel(
            name='FeedCommentImages',
        ),
        migrations.AddField(
            model_name='commentmedia',
            name='comment',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='comment_image', to='feed.comments'),
        ),
        migrations.AddField(
            model_name='commentmedia',
            name='feed',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='comment_image', to='feed.feed'),
        ),
    ]
