from django.db import models


class File(models.Model):
    file_id = models.CharField(max_length=256, unique=True)  # File is unique name of file
    user_id = models.ForeignKey("backend.User", on_delete=models.CASCADE)  # User_id that uploaded this file
    is_shared = models.BooleanField(default=False)  # Is user sharing this file to other users. Can be
    # extended by adding table of sharing and storing share_id
    file_name = models.CharField(max_length=512)  # Name of the file how user call it
    is_folder = models.BooleanField(default=False)  # Is this file a folder

    class Meta:
        indexes = [
            models.Index(fields=['file_id']),
        ]


class Access(models.Model):
    file_id = models.ForeignKey("File", on_delete=models.CASCADE)
    owner_id = models.ForeignKey("backend.User", on_delete=models.CASCADE, related_name="owner")
    share_uid = models.ForeignKey("backend.User", on_delete=models.CASCADE, related_name="share")
    can_edit = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['file_id']),
        ]


class Folder(models.Model):
    folder = models.ForeignKey("File", on_delete=models.CASCADE, related_name="folder")
    file = models.ForeignKey("File", on_delete=models.CASCADE, related_name="file")

    class Meta:
        indexes = [
            models.Index(fields=['folder']),
            models.Index(fields=['file']),
        ]
