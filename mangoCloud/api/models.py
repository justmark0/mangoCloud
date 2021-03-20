from django.db import models


class File(models.Model):
    file_id = models.CharField(max_length=256, unique=True)  # File is unique name of file
    user_id = models.ForeignKey("backend.User", on_delete=models.CASCADE)  # User_id that uploaded this file
    is_shared = models.BooleanField(default=False)  # Is user sharing this file to other users. Can be
    # extended by adding table of sharing and storing share_id
    file_name = models.CharField(max_length=512)  # Name of the file how user call it
    is_folder = models.BooleanField(default=False)  # Is this file a folder
    size = models.BigIntegerField()  # Size of the file in bytes
    parent = models.ForeignKey("File", on_delete=models.SET_NULL, null=True)
    is_trash = models.BooleanField(default=False)
    date_of_creation = models.DateTimeField(auto_now_add=True)
    trash_date = models.DateTimeField(null=True, default=None)

    class Meta:
        indexes = [
            models.Index(fields=['file_id']),
            models.Index(fields=['user_id']),
            models.Index(fields=['file_name']),
        ]


class Access(models.Model):
    file_id = models.ForeignKey("File", on_delete=models.CASCADE)
    owner_id = models.ForeignKey("backend.User", on_delete=models.CASCADE, related_name="owner")
    share_uid = models.ForeignKey("backend.User", on_delete=models.CASCADE, related_name="share")
    can_edit = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['file_id']),
            models.Index(fields=['owner_id']),
            models.Index(fields=['share_uid']),
        ]
