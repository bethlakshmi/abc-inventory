from django.contrib.auth.models import User
from filer.models.imagemodels import Image
from django.core.files import File


def login_as(user, testcase):
    user.set_password('foo')
    user.save()
    testcase.client.login(username=user.username,
                          email=user.email,
                          password='foo')


def set_image(itemimage):
    superuser = User.objects.create_superuser(
        'superuser_for_%d' % itemimage.pk,
        'admin@importimage.com',
        'secret')
    path = "inventory/tests/made_up_filename.png"
    current_img = Image.objects.create(
        owner=superuser,
        original_filename="made_up_filename.png",
        file=File(open(path, 'rb')))
    current_img.save()
    itemimage.filer_image_id = current_img.pk
    itemimage.save()


def assert_option_state(response, value, text, selected=False):
    selected_state = ""
    if selected:
        selected_state = " selected"
    option_state = (
        '<option value="%s"%s>%s</option>' % (
                    value, selected_state, text))
    assert bytes(option_state, 'utf-8') in response.content
