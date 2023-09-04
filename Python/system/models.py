'''
FilePath: models.py
Author: yun.huang <1594909346@qq.com>
Date: 2023-08-23 21:58:35
LastEditors: yun.huang <1594909346@qq.com>
LastEditTime: 2023-09-04 14:41:25
Version: 1.0.1
Copyright: 2023 YunYou Innovation Technology Co., Ltd. All Rights Reserved.
Descripttion: 愿你开心每一天~
'''
from django.contrib.auth.models import AbstractUser
from django.db import models

from utils.models import CoreModel, table_prefix

class Users(AbstractUser):
    TYPE_CHOICES = (
        ('ADMIN', 'ADMIN'),
        ('USER', 'USER'),
    )
    user_id = models.BigAutoField(primary_key=True, verbose_name='主键')
    open_id = models.CharField(max_length=180, blank=True, null=True, verbose_name='微信用户标识')
    avatar = models.CharField(max_length=200, blank=True, null=True, verbose_name='用户头像')
    user_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='用户微信昵称')
    email = models.EmailField(max_length=100, blank=True, null=True, verbose_name='邮箱')
    password = models.CharField(max_length=255, blank=True, null=True, verbose_name='用户密码')
    type = models.CharField(max_length=5, choices=TYPE_CHOICES, default='USER', null=False)
    frequency = models.BigIntegerField(default=0, verbose_name='Ai币')
    is_sign_in = models.BooleanField(default=False, verbose_name='是否签到')
    detection_counts = models.BigIntegerField(default=0, blank=True, null=True, verbose_name="违禁次数", help_text="违禁次数")
    is_disable = models.BooleanField(default=0, blank=True, null=True, verbose_name="是否封禁", help_text="是否封禁")
    update_time = models.DateTimeField(
        auto_now=True, null=True, blank=True, help_text="修改时间", verbose_name="修改时间")
    created_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="创建时间",
                                           verbose_name="创建时间")

    # 没用的一些字段,暂时不去掉
    is_superuser = models.BooleanField(default=False, null=True)
    username = models.CharField(max_length=30, default="功能暂未接入", unique=True, null=True)
    first_name = models.CharField(max_length=30, default="功能暂未接入", null=True)
    last_name = models.CharField(max_length=30, default="功能暂未接入", null=True)
    is_staff = models.BooleanField(default=False, null=True)
    is_active = models.BooleanField(default=1, null=True)
    date_joined = models.DateTimeField(null=True)

    class Meta:
        indexes = [
            models.Index(fields=['created_time'], name='user_idx_created_time'),
            models.Index(fields=['frequency'], name='user_idx_frequency'),
            models.Index(fields=['open_id'], name='idx_open_id'),
            models.Index(fields=['update_time'], name='user_idx_update_time'),
            models.Index(fields=['email', 'password'], name='user_email_password_index')
        ]
        db_table = "user"
        verbose_name = '用户表'
        verbose_name_plural = verbose_name
        ordering = ('user_id',)

class Drawing(models.Model):
    drawing_id = models.BigAutoField(primary_key=True, verbose_name='绘图ID')
    user_id = models.BigIntegerField(verbose_name='所属用户')
    prompt = models.TextField(verbose_name='提示词')
    negative_prompt = models.TextField(blank=True, null=True, verbose_name='反向提示词')
    original_url = models.CharField(max_length=200, blank=True, null=True, verbose_name='上传图')
    generate_url = models.CharField(max_length=200, blank=True, null=True, verbose_name='生成图')
    is_public = models.BooleanField(default=False, blank=True, null=True, verbose_name='是否公开')
    update_time = models.DateTimeField(
        auto_now=True, null=True, blank=True, help_text="修改时间", verbose_name="修改时间")
    created_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="创建时间",
                                           verbose_name="创建时间")

    class Meta:
        indexes = [
            models.Index(fields=['generate_url'], name='drawing_generate_url_index'),
            models.Index(fields=['created_time'], name='drawing_idx_created_time'),
            models.Index(fields=['is_public'], name='idx_is_public'),
            models.Index(fields=['update_time'], name='drawing_idx_update_time'),
            models.Index(fields=['user_id'], name='drawing_idx_user_id')
        ]
        db_table = "drawing"
        verbose_name = '绘图表'
        verbose_name_plural = verbose_name
        ordering = ('drawing_id',)

class Exchange(models.Model):
    exchange_id = models.BigAutoField(primary_key=True, verbose_name='兑换码ID')
    exchange_code = models.CharField(max_length=8, unique=True, blank=True, null=True, verbose_name='兑换码')
    frequency = models.BigIntegerField(blank=True, null=True, verbose_name='兑换码所含Ai币')
    update_time = models.DateTimeField(
        auto_now=True, null=True, blank=True, help_text="修改时间", verbose_name="修改时间")
    created_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="创建时间",
                                           verbose_name="创建时间")

    class Meta:
        indexes = [
            models.Index(fields=['created_time'], name='exchange_idx_created_time'),
            models.Index(fields=['exchange_code'], name='idx_exchange_code'),
            models.Index(fields=['frequency'], name='exchange_idx_frequency'),
            models.Index(fields=['update_time'], name='exchange_idx_update_time')
        ]
        db_table = "exchange"
        verbose_name = '兑换表'
        verbose_name_plural = verbose_name
        ordering = ('exchange_id',)

class Orders(models.Model):
    orders_id = models.CharField(max_length=100, primary_key=True)
    user_id = models.BigIntegerField(blank=True, null=True)
    product_id = models.BigIntegerField(blank=True, null=True)
    product_name = models.CharField(max_length=50, blank=True, null=True)
    product_price = models.FloatField(blank=True, null=True)
    state = models.SmallIntegerField(blank=True, null=True)
    frequency = models.BigIntegerField(blank=True, null=True)
    reason_failure = models.CharField(max_length=50, blank=True, null=True)
    pay_time = models.DateTimeField(null=True, blank=True)
    update_time = models.DateTimeField(
        auto_now=True, null=True, blank=True, help_text="修改时间", verbose_name="修改时间")
    created_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="创建时间",
                                           verbose_name="创建时间")

    class Meta:
        indexes = [
            models.Index(fields=['product_id'], name='orders_product_id_index'),
            models.Index(fields=['state'], name='orders_state_index'),
            models.Index(fields=['user_id'], name='orders_user_id_index')
        ]
        db_table = "orders"
        verbose_name = '命令表'
        verbose_name_plural = verbose_name
        ordering = ('orders_id',)

class Product(models.Model):
    product_id = models.BigAutoField(primary_key=True)
    product_name = models.CharField(max_length=100, blank=True, null=True)
    frequency = models.BigIntegerField(blank=True, null=True,)
    product_price = models.FloatField(blank=True, null=True,)
    update_time = models.DateTimeField(
        auto_now=True, null=True, blank=True, help_text="修改时间", verbose_name="修改时间")
    created_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="创建时间",
                                           verbose_name="创建时间")

    class Meta:
        indexes = [
            models.Index(fields=['product_name'], name='product_product_name_index')
        ]
        db_table = "product"
        verbose_name = '产品表'
        verbose_name_plural = verbose_name
        ordering = ('product_id',)

class Star(models.Model):
    star_id = models.BigAutoField(primary_key=True, verbose_name='主键')
    user_id = models.BigIntegerField(blank=True, null=True, verbose_name='所属用户')
    issue = models.TextField(blank=True, null=True, verbose_name='问题')
    answer = models.TextField(blank=True, null=True, verbose_name='答案')
    update_time = models.DateTimeField(
        auto_now=True, null=True, blank=True, help_text="修改时间", verbose_name="修改时间")
    created_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="创建时间",
                                           verbose_name="创建时间")

    class Meta:
        indexes = [
            models.Index(fields=['created_time'], name='star_idx_created_time'),
            models.Index(fields=['update_time'], name='star_idx_update_time'),
            models.Index(fields=['user_id'], name='star_idx_user_id')
        ]
        db_table = "star"
        verbose_name = '问答表'
        verbose_name_plural = verbose_name
        ordering = ('star_id',)

class TextDetection(models.Model):
    id = models.BigAutoField(primary_key=True, help_text="主键")
    account = models.CharField(max_length=128, verbose_name="违禁账号", help_text="违禁账号")
    account_ip = models.CharField(max_length=15, verbose_name="违禁IP", help_text="违禁IP")
    text_value = models.CharField(max_length=255, null=True, blank=True, verbose_name="文本内容", help_text="文本内容")
    text_keyword = models.CharField(max_length=255, null=True, blank=True, verbose_name="关键词", help_text="关键词")
    update_time = models.DateTimeField(
        auto_now=True, null=True, blank=True, help_text="修改时间", verbose_name="修改时间")
    created_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="创建时间",
                                           verbose_name="创建时间")

    class Meta:
        indexes = [
            models.Index(fields=['created_time'], name='text_idx_created_time'),
            models.Index(fields=['update_time'], name='text_idx_update_time'),
            models.Index(fields=['id'], name='text_idx_id')
        ]
        db_table = table_prefix + 'text_detection'
        verbose_name = '违禁词表'
        verbose_name_plural = verbose_name
        ordering = ('id',)

class StableDiffusionConfig(models.Model):
    sd_id = models.BigAutoField(primary_key=True, help_text="主键")
    model_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='模型名称')
    text_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='展示名称')
    is_selected = models.BooleanField(default=0, blank=True, null=True, verbose_name="是否默认")
    update_time = models.DateTimeField(
        auto_now=True, null=True, blank=True, help_text="修改时间", verbose_name="修改时间")
    created_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, help_text="创建时间",
                                           verbose_name="创建时间")

    class Meta:
        indexes = [
            models.Index(fields=['created_time'], name='sd_idx_created_time'),
            models.Index(fields=['update_time'], name='sd_idx_update_time'),
            models.Index(fields=['sd_id'], name='sd_idx_id'),
            models.Index(fields=['text_name'], name='sd_idx_text_name')
        ]
        db_table = table_prefix + 'sd_config'
        verbose_name = 'sd绘图表'
        verbose_name_plural = verbose_name
        ordering = ('sd_id',)

class OperationLog(CoreModel):
    request_modular = models.CharField(max_length=64, verbose_name="请求模块", null=True, blank=True, help_text="请求模块")
    request_path = models.TextField(verbose_name="请求地址", null=True, blank=True, help_text="请求地址")
    request_body = models.TextField(verbose_name="请求参数", null=True, blank=True, help_text="请求参数")
    request_method = models.CharField(max_length=8, verbose_name="请求方式", null=True, blank=True, help_text="请求方式")
    request_msg = models.TextField(verbose_name="操作说明", null=True, blank=True, help_text="操作说明")
    request_ip = models.CharField(max_length=32, verbose_name="请求ip地址", null=True, blank=True, help_text="请求ip地址")
    request_browser = models.CharField(max_length=64, verbose_name="请求浏览器", null=True, blank=True, help_text="请求浏览器")
    response_code = models.CharField(max_length=32, verbose_name="响应状态码", null=True, blank=True, help_text="响应状态码")
    request_os = models.CharField(max_length=64, verbose_name="操作系统", null=True, blank=True, help_text="操作系统")
    json_result = models.TextField(verbose_name="返回信息", null=True, blank=True, help_text="返回信息")
    status = models.BooleanField(default=False, verbose_name="响应状态", help_text="响应状态")

    class Meta:
        db_table = table_prefix + 'operation_log'
        verbose_name = '操作日志'
        verbose_name_plural = verbose_name
        ordering = ('-created_time',)

class LoginLog(CoreModel):
    LOGIN_TYPE_CHOICES = (
        (1, '后台登录'),
        (2, '前台登录')
    )
    username = models.CharField(max_length=32, verbose_name="登录用户名", null=True, blank=True, help_text="登录用户名")
    ip = models.CharField(max_length=32, verbose_name="登录ip", null=True, blank=True, help_text="登录ip")
    agent = models.CharField(max_length=1500,verbose_name="agent信息", null=True, blank=True, help_text="agent信息")
    browser = models.CharField(max_length=200, verbose_name="浏览器名", null=True, blank=True, help_text="浏览器名")
    os = models.CharField(max_length=150, verbose_name="操作系统", null=True, blank=True, help_text="操作系统")
    login_type = models.IntegerField(default=1, choices=LOGIN_TYPE_CHOICES, verbose_name="登录类型", help_text="登录类型")

    class Meta:
        db_table = table_prefix + 'login_log'
        verbose_name = '登录日志'
        verbose_name_plural = verbose_name
        ordering = ('-created_time',)
