"""
カスタマイズユーザーモデルを定義
"""

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from base.models import create_id

# ユーザーモデル
class UserManager(BaseUserManager):

    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            username,
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    id = models.CharField(default=create_id, primary_key=True, max_length=22)
    username = models.CharField(
        max_length=50, unique=True, blank=True, default='匿名')
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email', ]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

# ユーザーのプロフィール情報
class Profile(models.Model):
    user = models.OneToOneField(
        User, primary_key=True, on_delete=models.CASCADE)
    # OneToOneField：1対1の関係性、ユーザーAに対してプロフィールA

    # 送付先の名前(ユーザーネームを使う仕様にしてもOK)
    name = models.CharField(default='', blank=True, max_length=50)
    # 郵便番号
    zipcode = models.CharField(default='', blank=True, max_length=8)
    # 都道府県
    prefecture = models.CharField(default='', blank=True, max_length=50)
    # 市町村
    city = models.CharField(default='', blank=True, max_length=50)
    # それ以降の住所
    address1 = models.CharField(default='', blank=True, max_length=50)
    address2 = models.CharField(default='', blank=True, max_length=50)
    # 電話番号
    tel = models.CharField(default='', blank=True, max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# OneToOneField を同時に作成　ユーザーモデルが作成されたらプロフィールが作成される仕様
# @：デコレーター　関数が実行される前に ＠～ の処理を実行する
@receiver(post_save, sender=User)         # ユーザーモデルが作成された時点で
def create_onetoone(sender, **kwargs):    # プロフィールを作成する
    if kwargs['created']:
        Profile.objects.create(user=kwargs['instance'])