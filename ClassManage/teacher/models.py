import random
import base64
import hashlib

from django.db import models


def random_account():
    """
    获取随机用户名
    :return: 随机用户名
    """
    word = '1234567890qwertyuiopasdfghjklzxcvbnm'
    account = ''.join(random.sample(word, 8))
    while TeacherInfo.objects.filter(account=account).first():
        random_account()
    return account


# Create your models here.
class TeacherInfo(models.Model):
    name = models.CharField(verbose_name='老师姓名', max_length=50)
    gender = models.BooleanField(verbose_name='性别', default=False)
    account = models.CharField(verbose_name='账号', max_length=50, default=random_account)
    password = models.CharField(verbose_name='密码', max_length=40, default='fd3d69aafa0d649b44d7d6cdf4c6159937cadac5')

    def __str__(self):
        return self.name

    def show_gender(self):
        if self.gender:
            return '男'
        else:
            return '女'

    @staticmethod
    def encrypt_password(password):
        """
        加密密码
        :param password: 明文密码
        :return: 加密后的密码
        """
        m = hashlib.md5(password.encode()).hexdigest()
        b = base64.b64encode(m.encode())
        return hashlib.sha1(b).hexdigest()

    def check_account(self, account):
        """
        检查是否有重复账号
        :param account: 账号
        :return: boolean
        """
        pass

    class Meta:
        verbose_name = '老师信息'
        verbose_name_plural = verbose_name
