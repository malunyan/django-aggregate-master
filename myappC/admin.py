from django.contrib import admin

from import_export.resources import ModelResource
from import_export.admin import ImportMixin,ImportExportMixin,ImportExportActionModelAdmin
from import_export.formats import base_formats
from import_export import resources, widgets, fields
from import_export.fields import Field
from import_export.widgets import *
from .models import  OrderItemDetail3, Order3
from ec_site.models import *
from import_export.results import RowResult

# Register your models here.

#=========================OrderItemDetail.ModelAdmin=====================================#
class OrderItemDetail3Resource(resources.ModelResource):
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
        model = OrderItemDetail3
        fields = ('key')
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
class OrderItemDetail3Admin(ImportExportActionModelAdmin, admin.ModelAdmin):
    to_encoding= 'cp932'
    list_display=('code', 'price')
    search_fields = ['code__code']
    resource_class = OrderItemDetail3Resource
    def settlement(self, obj):
        return obj.settlement.name
    settlement.short_description = 'カテゴリ名'
    settlement.admin_order_field = 'product__category'
#========================================================================================#


#==============================Order.ModelAdmin===========================================#
class Order3Resource(resources.ModelResource):
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
    date = Field(attribute='date', column_name='purchase-date')
    code = Field(attribute='code', column_name='order-id', widget=ForeignKeyWidget(Earnings, 'order_number'))
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
        model = Order3
        import_order = ('date', 'code', 'orderer')
        import_id_fields = ['code']
    def before_import_row(self, row, row_number=None, **kwargs):
        row['order-id'] = row['order-id'].replace('     ', '')
        row['purchase-date'] = row['purchase-date'].replace('/', '-')
        row['purchase-date'] = row['purchase-date'].split('T')[0]
        row['purchase-date'] = "".join([s for s in row['purchase-date'].splitlines(True) if s.strip("\r\n")])
class Order3Admin(ImportExportMixin,admin.ModelAdmin):
    list_display=('code','orderer', 'amount')
    resource_class = Order3Resource
#========================================================================================#

admin.site.register(Order3, Order3Admin)
admin.site.register(OrderItemDetail3, OrderItemDetail3Admin)
