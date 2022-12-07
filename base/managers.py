from django.contrib.auth.base_user import BaseUserManager


class MemberManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, username, password, **extra_fields):

        """
        Create and save a User with the given email and password.
        """
        if not username:
            raise ValueError(_('The username must be set.'))
        if not password:
            raise ValueError(_('The password must be set.'))

        print('Username: %s, Password: %s' % (username, password))
        for key in extra_fields.keys():
            print('%s = %s' % (key, extra_fields[key]))

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    # def natural_key(self):
    #     return self.username

    def create_superuser(self, username, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(username, password, **extra_fields)
