from odoo import fields,models,api


class ProductsTemplate(models.Model):
    _inherit = "product.template"
    #so now we inherted the product table and giviin it a new filed
    product_description = fields.Char(string="product description")
    #you will see scrapper name in gui as label name , if you dont give any name it will be name
