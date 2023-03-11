from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self,phone_number,first_name=None,last_name=None,email=None,username=None, password=None):

        if not phone_number:
            raise ValueError("phone number is needed")

        user=self.model(phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,email=self.normalize_email(email),
            username=username
        )

        filtred=self.filter(phone_number=phone_number)
        if not filtred.exists():
            
            user.set_password(password)
            user.save(using=self._db)
            return user
        else:
            raise ValueError("phone number is exisit")


    def create_superuser(self,phone_number,
                                email,
                                password,
                                first_name=None,
                                last_name=None,
                                username=None ):


        a=int(input("enter number"))
        if a==888:

            user=self.create_user(
                phone_number=phone_number,
                first_name=first_name,
                last_name=last_name,email=self.normalize_email(email),
                username=username,
                password=password
        )
            user.is_admin=True
            user.is_staff=True
            user.is_active=True
            user.is_superadmin=True
            user.save(using=self._db)
            return user
        else:
            raise ValueError("not valid secret key")
        

class User(AbstractUser):

    first_name=models.CharField(max_length=200,null=True,blank=True)
    last_name=models.CharField(max_length=200,null=True,blank=True)
    username=models.CharField(max_length=200,null=True,blank=True)
    email=models.EmailField(max_length=200,null=True,blank=True)
    phone_number=models.CharField(max_length=200,unique=True)
    date_joined=models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now=True)
    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=False)
    is_superadmin=models.BooleanField(default=False)


    USERNAME_FIELD="phone_number"
    # REQUIRED_FIELDS=["phone_number"]   

    objects=UserManager()


    def __str__(self) -> str:

        return str(self.phone_number)

    def has_perm(self,perm,obj=None):

        return self.is_admin
    
    def has_module_perms(self,add_label):

        return True