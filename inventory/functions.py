from filer.models.imagemodels import Image
from filer.models.foldermodels import Folder
from django.contrib.auth.models import User
from inventory.models import ItemImage


def upload_and_attach(files, user, item=None):
    superuser = User.objects.get(username='admin_img')
    folder, created = Folder.objects.get_or_create(
        name='ItemImageUploads')
    images = []
    for f in files:
        img, created = Image.objects.get_or_create(
            owner=superuser,
            original_filename=f.name,
            file=f,
            folder=folder,
            author="%s" % str(user.username))
        img.save()
        images += [img]
        if item:
            new_link = ItemImage(item=item, filer_image=img)
            new_link.save()
    return images
