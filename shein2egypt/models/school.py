from odoo import fields,models


class ScrapperProfile(models.Model):
    _name = "scrapper.profile"

    name = fields.Char(string="scrapper namez") #you will see scrapper name in gui as label name , if you dont give any name it will be name
    email =fields.Char(string="email")
    phone =fields.Char(String="phone")