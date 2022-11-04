from django.contrib import admin
from import_export.resources import ModelResource
from import_export.admin import ImportMixin,ImportExportMixin,ImportExportActionModelAdmin
from import_export.formats import base_formats
from import_export import resources, widgets, fields
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget,DateTimeWidget
from .models import Product, User, OrderItem, OrderItemDetail, Order, Earnings
from import_export.results import RowResult

""" Django 管理サイト名変更 """
admin.site.site_header = 'J.A.R.V.I.S.'

""" サイト管理名変更 """
admin.site.index_title = 'ビアハウス入金消込システム'


#=================================Product.ModelAdmin====================================#
class ProductAdmin(admin.ModelAdmin):
    list_display=('pk','name')
#=======================================================================================#



#================================InvoiceDetailInline=====================================#
class InvoiceDetailInline(admin.TabularInline):
    model = OrderItemDetail
    show_change_link = True
    extra = 0
#========================================================================================#


#=========================OrderItemDetail.ModelAdmin=====================================#
class OrderItemDetailResource(resources.ModelResource):
    def get_field_names(self):
        names = []
        for field in self.get_fields():
            names.append(self.get_field_name(field))
        return names
    def import_row(self, row, instance_loader, **kwargs):
        # overriding import_row to ignore errors and skip rows that fail to import
        # without failing the entire import
        import_result = super(ModelResource, self).import_row(
            row, instance_loader, **kwargs
        )
        if import_result.import_type == RowResult.IMPORT_TYPE_ERROR:
            import_result.diff = [
                row.get(name, '') for name in self.get_field_names()
            ]
            # Add a column with the error message
            import_result.diff.append(
                "Errors: {}".format(
                    [err.error for err in import_result.errors]
                )
            )
            # clear errors and mark the record to skip
            import_result.errors = []
            import_result.import_type = RowResult.IMPORT_TYPE_SKIP
        return import_result
    code = fields.Field(attribute='code', column_name='order_number',widget=ForeignKeyWidget(Earnings,'order_number'))
    #code = fields.Field(attribute='code', column_name='order_number',widget=ForeignKeyWidget(Code,'code'))
    name = Field(attribute='name', column_name='user_name')
    price = Field(attribute='price', column_name='item_price')
    payment_code = Field(attribute='payment_code', column_name='payment_code')
    process_code = Field(attribute='process_code', column_name='process_code')
    state = Field(attribute='state', column_name='state')
    card_type = Field(attribute='card_type', column_name='credit_card_type')
    class Meta:
        model = OrderItemDetail
        fields = ('key__items__name','key__name','key__price','code__total_tax_included',
        'code__order_number__amount','code__order_number__postage','code__order_number__point',
        'code__order_number__tax','code__order_number__correction_amount')
        import_order = ('code', 'name')
        import_id_fields = ['code']
    def before_import_row(self, row, row_number=None, **kwargs):
        row['credit_card_type'] = row['credit_card_type'].replace('0', '未確定')
        row['credit_card_type'] = row['credit_card_type'].replace('1', 'VISA')
        row['credit_card_type'] = row['credit_card_type'].replace('2', 'MASTER')
        row['credit_card_type'] = row['credit_card_type'].replace('3', 'DINERS')
        row['credit_card_type'] = row['credit_card_type'].replace('4', 'JCB')
        row['credit_card_type'] = row['credit_card_type'].replace('5', 'AMEX')
        row['credit_card_type'] = row['credit_card_type'].replace('9', 'その他')

        row['process_code'] = row['process_code'].replace('1', '初回課金')
        row['process_code'] = row['process_code'].replace('2', '登録済み課金')
        row['process_code'] = row['process_code'].replace('3', '登録のみ')
        row['process_code'] = row['process_code'].replace('4', '登録変更')
        row['process_code'] = row['process_code'].replace('7', '退会取消')
        row['process_code'] = row['process_code'].replace('8', '月次課金解除')
        row['process_code'] = row['process_code'].replace('9', '退会')

        row['state'] = row['state'].replace('1', '課金済')
        row['state'] = row['state'].replace('0', '未課金')
        row['state'] = row['state'].replace('4', '審査中')
        row['state'] = row['state'].replace('5', '仮売上')
        row['state'] = row['state'].replace('6', '出荷登録中')
        row['state'] = row['state'].replace('9', 'キャンセル')
        row['state'] = row['state'].replace('11', '審査NG')
class OrderItemDetailAdmin(ImportExportActionModelAdmin, admin.ModelAdmin):
    to_encoding= 'cp932'
    list_display=('code', 'name', 'price')
    search_fields = ['code__code']
    resource_class = OrderItemDetailResource
    def settlement(self, obj):
        return obj.settlement.name
    settlement.short_description = 'カテゴリ名'
    settlement.admin_order_field = 'product__category'
#========================================================================================#


#==============================Earnings.ModelAdmin===========================================#
class EarningsResource(resources.ModelResource):
    def get_field_names(self):
        names = []
        for field in self.get_fields():
            names.append(self.get_field_name(field))
        return names
    def import_row(self, row, instance_loader, **kwargs):
        # overriding import_row to ignore errors and skip rows that fail to import
        # without failing the entire import
        import_result = super(ModelResource, self).import_row(
            row, instance_loader, **kwargs
        )
        if import_result.import_type == RowResult.IMPORT_TYPE_ERROR:
            import_result.diff = [
                row.get(name, '') for name in self.get_field_names()
            ]
            # Add a column with the error message
            import_result.diff.append(
                "Errors: {}".format(
                    [err.error for err in import_result.errors]
                )
            )
            # clear errors and mark the record to skip
            import_result.errors = []
            import_result.import_type = RowResult.IMPORT_TYPE_SKIP
        return import_result
    delivery_number = Field(attribute='delivery_number', column_name='納品no')
    line_number = Field(attribute='line_number', column_name='行no')
    sales_date = Field(attribute='sales_date', column_name='売上日')
    customer_code = Field(attribute='customer_code', column_name='得意先コード')
    customer_name = Field(attribute='customer_name', column_name='得意先名')
    delivery_code = Field(attribute='delivery_code', column_name='納品先コード')
    delivery_name = Field(attribute='delivery_name', column_name='納品先名')
    post_code = Field(attribute='post_code', column_name='郵便番号')
    address1 = Field(attribute='address1', column_name='住所1')
    address2 = Field(attribute='address2', column_name='住所2')
    phone_number = Field(attribute='phone_number', column_name='ＴＥＬ')
    overview = Field(attribute='overview', column_name='摘要')
    slip_number = Field(attribute='slip_number', column_name='項目1')
    order_number = fields.Field(attribute='order_number', column_name='項目2',widget=ForeignKeyWidget(Order,'code'))
    total_tax_excluded_amount = Field(attribute='total_tax_excluded_amount', column_name='合計税抜金額')
    total_tax_amount = Field(attribute='total_tax_amount', column_name='合計消費税')
    total_tax_included = Field(attribute='total_tax_included', column_name='合計税込金額')
    transaction_classification = Field(attribute='transaction_classification', column_name='取引区分')
    transaction_classification_name = Field(attribute='transaction_classification_name', column_name='取引区分名')
    product_code = Field(attribute='product_code', column_name='商品コード')
    product_name = Field(attribute='product_name', column_name='商品名')
    warehouse_code = Field(attribute='warehouse_code', column_name='倉庫コード')
    warehouse_name = Field(attribute='warehouse_name', column_name='倉庫名')
    quantity = Field(attribute='quantity', column_name='総数量')
    tax_excluded_amount = Field(attribute='tax_excluded_amount', column_name='税抜金額')
    tax_amount = Field(attribute='tax_amount', column_name='消費税額')
    tax_included = Field(attribute='tax_included', column_name='税込金額')
    line_overview = Field(attribute='line_overview', column_name='行摘要')
    input_date = fields.Field(attribute='input_date', column_name='入力日',widget=widgets.DateTimeWidget(format="%Y-%m-%d %H:%M:%S"))
    correction_date = fields.Field(attribute='correction_date', column_name='訂正日',widget=widgets.DateTimeWidget(format="%Y-%m-%d %H:%M:%S"))
    delete_date = fields.Field(attribute='delete_date', column_name='削除日',widget=widgets.DateTimeWidget(format="%Y-%m-%d %H:%M:%S"))
    billing_code = Field(attribute='billing_code', column_name='請求先コード')
    billing_name = Field(attribute='billing_name', column_name='請求先名')
    customer_category_3 = Field(attribute='customer_category_3', column_name='得意先区分3')
    customer_category_name_3 = Field(attribute='customer_category_name_3', column_name='得意先区分名3')
    shipping_code = Field(attribute='shipping_code', column_name='運送コード')
    consumption_tax_classification = Field(attribute='consumption_tax_classification', column_name='消費税区分')
    time_specification_code = Field(attribute='time_specification_code', column_name='時間指定コード')
    time_designation_division_name = Field(attribute='time_designation_division_name', column_name='時間指定区分名')
    specify_time = Field(attribute='specify_time', column_name='時間指定')
    shipping_description_1 = Field(attribute='shipping_description_1', column_name='出荷摘要１')
    shipping_description_2 = Field(attribute='shipping_description_2', column_name='出荷摘要２')
    invoice_number = Field(attribute='invoice_number', column_name='送り状№')
    class Meta:
        model = Earnings
        import_order = ('delivery_number','sales_date', 'delivery_name','order_number')
        import_id_fields = ['delivery_number','order_number']
    def before_import_row(self, row, row_number=None, **kwargs):
        row['売上日'] = row['売上日'].replace('/', '-')
        row['入力日'] = row['入力日'].replace('/', '-')
        row['訂正日'] = row['訂正日'].replace('/', '-')
        row['削除日'] = row['削除日'].replace('/', '-')
class EarningsAdmin(ImportExportMixin,admin.ModelAdmin):
    list_display=('delivery_number','sales_date', 'delivery_name','order_number')
    search_fields = ['order_number']
    resource_class = EarningsResource
#========================================================================================#


#==============================Order.ModelAdmin===========================================#
class OrderResource(resources.ModelResource):
    def get_field_names(self):
        names = []
        for field in self.get_fields():
            names.append(self.get_field_name(field))
        return names
    def import_row(self, row, instance_loader, **kwargs):
        # overriding import_row to ignore errors and skip rows that fail to import
        # without failing the entire import
        import_result = super(ModelResource, self).import_row(
            row, instance_loader, **kwargs
        )
        if import_result.import_type == RowResult.IMPORT_TYPE_ERROR:
            import_result.diff = [
                row.get(name, '') for name in self.get_field_names()
            ]
            # Add a column with the error message
            import_result.diff.append(
                "Errors: {}".format(
                    [err.error for err in import_result.errors]
                )
            )
            # clear errors and mark the record to skip
            import_result.errors = []
            import_result.import_type = RowResult.IMPORT_TYPE_SKIP
        return import_result
    date = fields.Field(attribute='date', column_name='日付')
    code = fields.Field(attribute='code', column_name='注文番号')
    orderer = fields.Field(attribute='orderer', column_name='注文者')
    amount = fields.Field(attribute='amount', column_name='注文金額')
    postage = fields.Field(attribute='postage', column_name='送料')
    delivery_fee = fields.Field(attribute='delivery_fee', column_name='代金引換手数料')
    point = fields.Field(attribute='point', column_name='利用ポイント')
    tax = fields.Field(attribute='tax', column_name='消費税')
    method = fields.Field(attribute='method', column_name='決済方法')
    slip = fields.Field(attribute='slip', column_name='伝票番号')
    coupon = fields.Field(attribute='coupon', column_name='クーポン割引額')
    correction_amount = fields.Field(attribute='correction_amount', column_name='修正額')
    group = fields.Field(attribute='group', column_name='グループ名')
    class Meta:
        model = Order
        import_order = ('date', 'code', 'orderer')
        import_id_fields = ['code']
    def before_import_row(self, row, row_number=None, **kwargs):
        row['日付'] = row['日付'].replace('/', '-')

class OrderAdmin(ImportExportMixin,admin.ModelAdmin):
    list_display=('code','orderer', 'amount')
    resource_class = OrderResource
#========================================================================================#


#==============================OrderItem.ModelAdmin======================================#
class OrderItemResource(ModelResource):
    class Meta:
        model = OrderItem
        import_order = ('pk', 'name', 'items','price')
        import_id_fields = ['pk']

class OrderItemAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = OrderItemResource
    list_display=('pk', 'name', 'items','price')
    inlines = [InvoiceDetailInline]
#========================================================================================#


#================================Settlement.ModelAdmin===================================#
class SettlementAdmin(admin.ModelAdmin):
    list_display=('pk', 'name', 'amount')
#========================================================================================#



admin.site.register(Product, ProductAdmin)
admin.site.register(Earnings, EarningsAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(OrderItemDetail, OrderItemDetailAdmin)
