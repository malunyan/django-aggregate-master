from django.contrib import admin
from import_export.resources import ModelResource
from import_export.admin import ImportMixin,ImportExportMixin,ImportExportActionModelAdmin
from import_export.formats import base_formats
from import_export import resources, widgets, fields
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget,DateTimeWidget
from .models import Product2,OrderItem2, OrderItemDetail2, Order2
from ec_site.models import *
from import_export.results import RowResult

# Register your models here.
#=================================Product.ModelAdmin====================================#
class Product2Admin(admin.ModelAdmin):
    list_display=('pk','name')
#=======================================================================================#



#================================InvoiceDetailInline=====================================#
class InvoiceDetail2Inline(admin.TabularInline):
    model = OrderItemDetail2
    show_change_link = True
    extra = 0
#========================================================================================#


#=========================OrderItemDetail.ModelAdmin=====================================#
class OrderItemDetail2Resource(resources.ModelResource):
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
        model = OrderItemDetail2
        fields = ('key__items__name','key__name','key__price','code__total_tax_included','code__order_number__amount')
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
class OrderItemDetail2Admin(ImportExportActionModelAdmin, admin.ModelAdmin):
    to_encoding= 'cp932'
    list_display=('code', 'name', 'price')
    search_fields = ['code__code']
    resource_class = OrderItemDetail2Resource
    def settlement(self, obj):
        return obj.settlement.name
    settlement.short_description = 'カテゴリ名'
    settlement.admin_order_field = 'product__category'
#========================================================================================#


#==============================Order.ModelAdmin===========================================#
class Order2Resource(resources.ModelResource):
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
    date = Field(attribute='date', column_name='日付')
    code = Field(attribute='code', column_name='注文番号')
    orderer = Field(attribute='orderer', column_name='注文者')
    amount = Field(attribute='amount', column_name='注文金額')
    postage = Field(attribute='postage', column_name='送料')
    delivery_fee = Field(attribute='delivery_fee', column_name='代金引換手数料')
    point = Field(attribute='point', column_name='利用ポイント')
    tax = Field(attribute='tax', column_name='消費税')
    method = Field(attribute='method', column_name='決済方法')
    slip = Field(attribute='slip', column_name='伝票番号')
    coupon = Field(attribute='coupon', column_name='クーポン割引額')
    correction_amount = Field(attribute='correction_amount', column_name='修正額')
    group = Field(attribute='group', column_name='グループ名')
    class Meta:
        model = Order2
        import_order = ('date', 'code', 'orderer')
        import_id_fields = ['code']
    def before_import_row(self, row, row_number=None, **kwargs):
        row['日付'] = row['日付'].replace('/', '-')

class Order2Admin(ImportExportMixin,admin.ModelAdmin):
    list_display=('code','orderer', 'amount')
    resource_class = Order2Resource
#========================================================================================#


#==============================OrderItem.ModelAdmin======================================#
class OrderItem2Resource(ModelResource):
    class Meta:
        model = OrderItem2
        import_order = ('pk', 'name', 'items','price')
        import_id_fields = ['pk']

class OrderItem2Admin(ImportExportMixin, admin.ModelAdmin):
    resource_class = OrderItem2Resource
    list_display=('pk', 'name', 'items','price','pdf_file')
    inlines = [InvoiceDetail2Inline]
#========================================================================================#


#================================Settlement.ModelAdmin===================================#
class Settlement2Admin(admin.ModelAdmin):
    list_display=('pk', 'name', 'amount')
#========================================================================================#



admin.site.register(Product2, Product2Admin)
admin.site.register(Order2, Order2Admin)
admin.site.register(OrderItem2, OrderItem2Admin)
admin.site.register(OrderItemDetail2, OrderItemDetail2Admin)
