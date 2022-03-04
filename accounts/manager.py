from django.contrib.auth.models import BaseUserManager

class UserAccountManager(BaseUserManager):
    def create_superuser(self, email, first_name , last_name , password):
        user = self.create_user(email , first_name, last_name, password)
        user.is_staff = True
        user.is_accepted = True
        user.is_superuser=True
        user.save(using=self.db)
        return user

    def create_user(self,email,first_name,last_name,password=None):
        if not email :
            raise ValueError(("Users must have and email address"))
        if not first_name :
            raise ValueError(("Users must have a first name"))
        if not last_name :
            raise ValueError(("Users must have a last name"))

        email = self.normalize_email(email)
        user = self.model(email=email , first_name=first_name, last_name=last_name)
        user.set_password(password)
        return user