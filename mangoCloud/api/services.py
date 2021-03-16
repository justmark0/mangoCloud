from django.conf import settings


def get_or_none(classname, **kwargs):
    try:
        return classname.objects.get(**kwargs)
    except classname.DoesNotExist:
        return None


def absolute_path_from_filename(name: str):
    path = (settings.FILES_FOLDER / name)
    if not path.exists():
        return None
    return str(path)
