import string, random
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth import get_user_model
from django.utils.text import slugify



# UserManager
class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(
            self, email, password, **kwargs):
        email = self.normalize_email(email)
        is_staff = kwargs.pop('is_staff', False)
        is_superuser = kwargs.pop(
            'is_superuser', False)
        user = self.model(
            email=email,
            is_active=True,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
            self, email, password=None,
            **extra_fields):
        return self._create_user(
            email, password, **extra_fields)

    def create_superuser(
            self, email, password,
            **extra_fields):
        return self._create_user(
            email, password,
            is_staff=True, is_superuser=True,
            **extra_fields)

    def update_pw_user(self, email, password):
        email = self.normalize_email(email)
        user = get_user_model().objects.get(email=email)
        user.set_password(password)
        user.save()
        return user
# random string generator
def random_string_generator(size = 4, chars = string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# slug generator
def unique_slug_generator(instance, name_attr, new_slug = None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(getattr(instance,name_attr))
    Klass = instance.__class__
    max_length = Klass._meta.get_field('slug').max_length
    slug = slug[:max_length]
    qs_exists = Klass.objects.filter(slug = slug).exists()
        
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug = slug[:max_length-5], randstr = random_string_generator(size = 4))
                
        return unique_slug_generator(instance, "company_name", new_slug = new_slug)
    return slug