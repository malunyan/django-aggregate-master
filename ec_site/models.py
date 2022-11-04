from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

#=========================入金項目モデル====================================#
class Product(models.Model):
    class Meta:
        verbose_name = '入金項目'
        verbose_name_plural = "入金項目"

    name = models.CharField(verbose_name = '入金者',max_length=100)

    def __str__(self):
        return str(self.name)
#===========================================================================#


#=========================口座情報モデル====================================#
class OrderItem(models.Model):
    class Meta:
        verbose_name = '口座情報'
        verbose_name_plural = '口座情報'

    user = models.ForeignKey(User,verbose_name = '入力者',on_delete = models.CASCADE, null=True)
    name = models.DateField(verbose_name="入金日", null=True, blank=True)
    items = models.ForeignKey(Product, verbose_name = '入金項目',on_delete = models.CASCADE,related_name='order', blank=True)
    price = models.DecimalField(verbose_name="入金金額",max_digits=7, decimal_places=0, null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)


    def __str__(self):
        return f'作成日: {self.created_date.strftime("%Y年%m月%d日%I:%M %p")}'
#===========================================================================#



#=========================注文情報モデル====================================#
class Order(models.Model):
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




#=========================売上情報モデル====================================#
class Earnings(models.Model):
    class Meta:
        verbose_name = '楽商売上明細データ'
        verbose_name_plural = '楽商売上明細データ'

    delivery_number = models.IntegerField(verbose_name ="納品no")
    line_number = models.IntegerField(verbose_name ="行no")
    sales_date = models.DateField(verbose_name="売上日", null=True, blank=True)
    customer_code = models.CharField(verbose_name ="得意先コード",max_length=6)
    customer_name = models.CharField(verbose_name ="得意先名",max_length=30)
    delivery_code = models.CharField(verbose_name ="納品先コード",max_length=10)
    delivery_name = models.CharField(verbose_name ="納品先名",max_length=50)
    post_code = models.CharField(verbose_name ="郵便番号",max_length=8, null=True, blank=True)
    address1 = models.CharField(verbose_name ="住所1",max_length=50, null=True, blank=True)
    address2 = models.CharField(verbose_name ="住所2",max_length=50, null=True, blank=True)
    phone_number = models.CharField(verbose_name ="ＴＥＬ",max_length=15, null=True, blank=True)
    overview = models.CharField(verbose_name ="摘要",max_length=30, null=True, blank=True)
    slip_number = models.CharField(verbose_name ="伝票番号",max_length=10)
    order_number = models.OneToOneField(Order, verbose_name ="注文番号", on_delete=models.CASCADE,primary_key=True)
    total_tax_excluded_amount = models.IntegerField(verbose_name ="合計税抜金額", null=True, blank=True)
    total_tax_amount = models.IntegerField(verbose_name ="合計消費税", null=True, blank=True)
    total_tax_included = models.IntegerField(verbose_name ="合計税込金額", null=True, blank=True)
    transaction_classification = models.CharField(verbose_name ="取引区分",max_length=3)
    transaction_classification_name = models.CharField(verbose_name ="取引区分名",max_length=5)
    product_code = models.CharField(verbose_name ="商品コード",max_length=6)
    product_name = models.CharField(verbose_name ="商品名",max_length=30)
    warehouse_code = models.CharField(verbose_name ="倉庫コード",max_length=5)
    warehouse_name = models.CharField(verbose_name ="倉庫名",max_length=10)
    quantity = models.IntegerField(verbose_name ="総数量", null=True, blank=True)
    tax_excluded_amount = models.IntegerField(verbose_name ="税抜金額", null=True, blank=True)
    tax_amount = models.IntegerField(verbose_name ="消費税額", null=True, blank=True)
    tax_included = models.IntegerField(verbose_name ="税込金額", null=True, blank=True)
    line_overview = models.CharField(verbose_name ="行摘要",max_length=30)
    input_date = models.DateTimeField(verbose_name="入力日")
    correction_date = models.DateTimeField(verbose_name="訂正日", null=True, blank=True)
    delete_date = models.DateTimeField(verbose_name="削除日", null=True, blank=True)
    billing_code = models.CharField(verbose_name ="請求先コード",max_length=6)
    billing_name = models.CharField(verbose_name ="請求先名",max_length=10)
    customer_category_3 = models.CharField(verbose_name ="得意先区分3",max_length=3, null=True, blank=True)
    customer_category_name_3 = models.CharField(verbose_name ="得意先区分名3",max_length=10, null=True, blank=True)
    shipping_code = models.CharField(verbose_name ="運送コード",max_length=3)
    consumption_tax_classification = models.CharField(verbose_name ="消費税区分",max_length=3, null=True, blank=True)
    time_specification_code = models.CharField(verbose_name ="時間指定コード",max_length=3, null=True, blank=True)
    time_designation_division_name = models.CharField(verbose_name ="時間指定区分名",max_length=15, null=True, blank=True)
    specify_time = models.CharField(verbose_name ="時間指定",max_length=10, null=True, blank=True)
    shipping_description_1 = models.CharField(verbose_name ="出荷摘要１",max_length=20, null=True, blank=True)
    shipping_description_2 = models.CharField(verbose_name ="出荷摘要２",max_length=20, null=True, blank=True)
    invoice_number = models.CharField(verbose_name ="送り状№",max_length=20, null=True, blank=True)

    def __str__(self):
        return str(self.order_number)
#===========================================================================#



#=========================決済情報モデル====================================#
class OrderItemDetail(models.Model):
    class Meta:
        verbose_name = '決済情報(GMOｲﾌﾟｼﾛﾝ)'
        verbose_name_plural = '決済情報(GMOｲﾌﾟｼﾛﾝ)'
    code = models.ForeignKey(Earnings, verbose_name ="注文番号", on_delete=models.CASCADE,related_name='number')
    name = models.CharField(verbose_name ="決済者",max_length=30)
    price = models.DecimalField(verbose_name="決済金額",max_digits=7, decimal_places=0)
    payment_code = models.CharField(verbose_name ="決済方法",max_length=3, null=True, blank=True)
    process_code = models.CharField(verbose_name ="処理区分",max_length=10, null=True, blank=True)
    state = models.CharField(verbose_name ="決済結果",max_length=10, null=True, blank=True)
    card_type = models.CharField(verbose_name ="ｶｰﾄﾞﾀｲﾌﾟ",max_length=10)
    created_date = models.DateField(auto_now_add=True)
    key = models.ForeignKey(OrderItem,verbose_name = '口座情報',on_delete = models.CASCADE, null=True, blank=True, related_name="order_payment")
    def __str__(self):
        return str(self.code)
#===========================================================================#

#=========================決済情報モデル(Eコレクト)====================================#
class OrderItemDetailEcollect(models.Model):
    class Meta:
        verbose_name = '決済情報(Eコレクト)'
        verbose_name_plural = '決済情報(Eコレクト)'
    tranfer_date_year = models.CharField(verbose_name ="振込日付（年）",max_length=4)
    tranfer_date_month = models.CharField(verbose_name ="振込日付（月）",max_length=2)
    tranfer_date_day = models.CharField(verbose_name="振込日付（日）",max_length=2)
    shipmentday = models.CharField(verbose_name ="発送日",max_length=8, null=True, blank=True)
    shipping_number = models.ForeignKey(Order, verbose_name ="お問い合せNo.",on_delete = models.CASCADE, null=True, blank=True)
    cod_amount = models.IntegerField(verbose_name ="代引金",null=True, blank=True)
    cod_charge = models.IntegerField(verbose_name ="代引手数料",null=True, blank=True)
    cod_card_charge = models.IntegerField(verbose_name ="カード決済事務手数料",null=True, blank=True)
    revenue_stamp_fee = models.IntegerField(verbose_name = '収入印紙代相当額',null=True, blank=True)
    type = models.CharField(verbose_name ="種類",max_length=10)
    sales_office = models.CharField(verbose_name ="回収営業所",max_length=10,null=True, blank=True)
    correction_information = models.CharField(verbose_name ="訂正情報",max_length=10,null=True, blank=True)
    correction_transfer_date_month = models.CharField(verbose_name ="訂正振込日（月）",max_length=2,null=True, blank=True)
    correction_transfer_date_day = models.CharField(verbose_name ="訂正振込日（日）",max_length=2,null=True, blank=True)
    transfer_target_class = models.CharField(verbose_name ="振込対象区分",max_length=10,null=True, blank=True)
    cod_fee_payment_method = models.CharField(verbose_name ="代引手数料支払方法",max_length=10,null=True, blank=True)
    def __str__(self):
        return str(self.shipping_number)
#===========================================================================#
