from django.db import models
from ec_site.models import *
from myappB.models import *
# Create your models here.

#=========================注文情報モデル====================================#
class Order3(models.Model):
    class Meta:
        verbose_name = '注文情報(Amazon)'
        verbose_name_plural = "注文情報(Amazon)"

    code = models.ForeignKey(Earnings, to_field = 'order_number', verbose_name ="注文番号", on_delete=models.CASCADE,primary_key=True)
    date = models.DateField(verbose_name ="日付", null=True, blank=True)
    orderer = models.CharField(verbose_name ="注文者",max_length=30,primary_key=False)
    amount = models.IntegerField(verbose_name = '注文金額')
    postage = models.IntegerField(verbose_name = '送料', null=True, blank=True)
    postage_tax = models.IntegerField(verbose_name = '消費税(送料)', null=True, blank=True)
    #delivery_fee = models.IntegerField(verbose_name = '代金引換手数料')
    #point = models.IntegerField(verbose_name = '利用ポイント')
    tax = models.IntegerField(verbose_name = '消費税')
    #method = models.CharField(verbose_name ="決済方法",max_length=30)
    #slip = models.CharField(verbose_name ="伝票番号",max_length=30)
    coupon = models.CharField(verbose_name = 'クーポン割引額',max_length=30)
    coupon_code = models.CharField(verbose_name = 'クーポンコード',max_length=30)
    #correction_amount = models.IntegerField(verbose_name = '修正額')
    #group = models.CharField(verbose_name ="グループ名",max_length=30)

    def __str__(self):
        return str(self.code)
#===========================================================================#

#=========================決済情報モデル====================================#
class OrderItemDetail3(models.Model):
    class Meta:
        verbose_name = '決済情報(Amazonﾍﾟｲﾒﾝﾄ)'
        verbose_name_plural = '決済情報(Amazonﾍﾟｲﾒﾝﾄ)'
    code = models.ForeignKey(Earnings, verbose_name ="注文番号", on_delete=models.CASCADE)
    #name = models.CharField(verbose_name ="決済者",max_length=30)
    price = models.DecimalField(verbose_name="決済金額",max_digits=7, decimal_places=0)
    #payment_code = models.CharField(verbose_name ="決済方法",max_length=3, null=True, blank=True)
    process_code = models.CharField(verbose_name ="処理区分",max_length=10, null=True, blank=True)
    state = models.CharField(verbose_name ="決済結果",max_length=10, null=True, blank=True)
    card_type = models.CharField(verbose_name ="ｶｰﾄﾞﾀｲﾌﾟ",max_length=10, null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)
    key = models.ForeignKey(Earnings,verbose_name = '口座情報',on_delete = models.CASCADE, null=True, blank=True, related_name="order_payment")
    def __str__(self):
        return str(self.code)
#===========================================================================#
