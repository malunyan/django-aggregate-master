from django.db import models

# Create your models here.
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
    order_number = models.CharField(verbose_name ="注文番号",max_length=10,unique=True)
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
