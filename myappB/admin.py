from django.contrib import admin
from import_export.resources import ModelResource
from import_export.admin import ImportMixin,ImportExportMixin,ImportExportActionModelAdmin
from import_export.formats import base_formats
from import_export import resources, widgets, fields
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget,DateTimeWidget
from .models import Earnings
from import_export.results import RowResult

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
    order_number = Field(attribute='order_number', column_name='項目2')
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

admin.site.register(Earnings, EarningsAdmin)
