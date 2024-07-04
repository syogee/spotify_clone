from django.db import models

# Create your models here.
class Albums(models.Model):
    album = models.CharField(max_length=300, unique=True, null=False)
    actors = models.CharField(max_length=500)
    directed_by = models.CharField(max_length=100)
    produced_by = models.CharField(max_length=100)
    music_directors = models.CharField(max_length=300)
    language = models.CharField(max_length=20)
    release_date = models.CharField(max_length=50)
    image_url = models.CharField(max_length=500, unique=True, null=False)
    def __str__(self):
        return self.album

class Songs(models.Model):
    album = models.ForeignKey(Albums, on_delete=models.CASCADE, to_field='album')
    song_name = models.CharField(max_length=300)
    singers = models.CharField(max_length=300)
    durations = models.CharField(max_length=300)
    song_url = models.CharField(max_length=300)
    def __str__(self):
        return self.song_name