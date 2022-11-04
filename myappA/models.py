from django.db import models
from ec_site.models import *
from django.core.validators import FileExtensionValidator
# Create your models here.
#=========================入金項目モデル====================================#
class Product2(models.Model):
    class Meta:
        verbose_name = '入金項目'
        verbose_name_plural = "入金項目"

    name = models.CharField(verbose_name = '入金者',max_length=100)

    def __str__(self):
        return str(self.name)
#===========================================================================#


#=========================口座情報モデル====================================#
class OrderItem2(models.Model):
    class Meta:
        verbose_name = '口座情報'
        verbose_name_plural = '口座情報'

    user = models.ForeignKey(User,verbose_name = '入力者',on_delete = models.CASCADE, null=True,related_name='user')
    name = models.DateField(verbose_name="入金日", null=True, blank=True)
    items = models.ForeignKey(Product2, verbose_name = '入金項目',on_delete = models.CASCADE,related_name='order', blank=True)
    price = models.DecimalField(verbose_name="入金金額",max_digits=7, decimal_places=0, null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)
    pdf_file = models.FileField(upload_to='uploads/%Y/%m/%d/',verbose_name='PDFファイル',validators=[FileExtensionValidator(['pdf', ])],)

    def __str__(self):
        return str(self.name)
        #f'作成日: {self.created_date.strftime("%Y年%m月%d日%I:%M %p")}'
#===========================================================================#



#=========================注文情報モデル====================================#
class Order2(models.Model):
    class Meta:
        verbose_name = '注文情報(ﾋﾞｱﾊｳｽｵﾝﾗｲﾝｼｮｯﾌﾟ)'
        verbose_name_plural = "注文情報(ﾋﾞｱﾊｳｽｵﾝﾗｲﾝｼｮｯﾌﾟ)"

    code = models.CharField(verbose_name ="注文番号",max_length=30, primary_key=True)
    date = models.DateField(verbose_name ="日付", null=True, blank=True)
    orderer = models.CharField(verbose_name ="注文者",max_length=30,primary_key=False)
    amount = models.IntegerField(verbose_name = '注文金額')
    postage = models.IntegerField(verbose_name = '送料')
    delivery_fee = models.IntegerField(verbose_name = '代金引換手数料')
    point = models.IntegerField(verbose_name = '利用ポイント')
    tax = models.IntegerField(verbose_name = '消費税')
    method = models.CharField(verbose_name ="決済方法",max_length=30)
    slip = models.CharField(verbose_name ="伝票番号",max_length=30)
    coupon = models.CharField(verbose_name = 'クーポン割引額',max_length=30)
    correction_amount = models.IntegerField(verbose_name = '修正額')
    group = models.CharField(verbose_name ="グループ名",max_length=30)

    def __str__(self):
        return str(self.code)
#===========================================================================#

#=========================決済情報モデル====================================#
class OrderItemDetail2(models.Model):
    class Meta:
        verbose_name = '決済情報(GMOｲﾌﾟｼﾛﾝ)'
        verbose_name_plural = '決済情報(GMOｲﾌﾟｼﾛﾝ)'
    code = models.ForeignKey(Earnings, verbose_name ="注文番号", on_delete=models.CASCADE)
    name = models.CharField(verbose_name ="決済者",max_length=30)
    price = models.DecimalField(verbose_name="決済金額",max_digits=7, decimal_places=0)
    payment_code = models.CharField(verbose_name ="決済方法",max_length=3, null=True, blank=True)
    process_code = models.CharField(verbose_name ="処理区分",max_length=10, null=True, blank=True)
    state = models.CharField(verbose_name ="決済結果",max_length=10, null=True, blank=True)
    card_type = models.CharField(verbose_name ="ｶｰﾄﾞﾀｲﾌﾟ",max_length=10, null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)
    key = models.ForeignKey(OrderItem2,verbose_name = '口座情報',on_delete = models.CASCADE, null=True, blank=True, related_name="order_payment")
    def __str__(self):
        return str(self.code)
#===========================================================================#
