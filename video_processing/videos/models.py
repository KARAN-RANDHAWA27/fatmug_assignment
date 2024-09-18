from django.db import models

# Create your models here.

class Video(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='videos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'videos_video'  # Specify the database table name
        verbose_name = 'Video'  # Singular name for the model
        verbose_name_plural = 'Videos'  # Plural name for the model
        ordering = ['-uploaded_at']  # Default ordering by uploaded_at descending

    def __str__(self):
        return self.title


class Subtitle(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='subtitles')
    language = models.CharField(max_length=10)
    content = models.TextField()
    timestamp = models.DurationField()  # Store the timestamp as a DurationField

    class Meta:
        db_table = 'videos_subtitle'  # Specify the database table name
        verbose_name = 'Subtitle'  # Singular name for the model
        verbose_name_plural = 'Subtitles'  # Plural name for the model
        ordering = ['language']  # Default ordering by language

    def __str__(self):
        return f"{self.language} subtitles for {self.video.title}"
