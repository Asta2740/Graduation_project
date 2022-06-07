import requests

from odoo import fields, models, api
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from dataclasses import dataclass
import math

from odoo.http import request


class RealTimeCurrencyConverter():
    def __init__(self, url):
        self.data = requests.get(url).json()
        self.currencies = self.data['rates']

    def convert(self, from_currency, to_currency, amount):
        initial_amount = amount
        # first convert it into USD if it is not in USD.
        # because our base currency is USD
        if from_currency != 'USD':
            amount = amount / self.currencies[from_currency]

            # limiting the precision to 4 decimal places
        amount = round(amount * self.currencies[to_currency], 4)
        return amount


@dataclass
class Product:
    name: str = None
    color: str = None
    price: str = None
    link: str = None
    image: str = None
    is_featured: bool = False
    size1: str = None
    size2: str = None
    size3: str = None
    size4: str = None
    size5: str = None
    size6: str = None
    counterT: str = None


def Define_sizes(counter, productS1, productS2, productS3, productS4, productS5, productS6, _product):
    if counter:
        Attribute = request.env['product.attribute'].sudo().search([('name', '=', 'Size')])
        sizesList = [productS1, productS2, productS3, productS4,
                     productS5, productS6, ]
        _product = _product
        # for rotation in sizesList:
        #     if 'Nothing' in sizesList:
        #         sizesList.remove('Nothing')
        print(sizesList)
        sizing = set_avilable_sizes(sizesList)

        Write_sizes(sizing, Attribute, _product)


def set_avilable_sizes(sizesList):
    sizesList2 = []
    for x in sizesList:
        val = request.env['product.attribute.value'].sudo().search([('name', '=', x,)])

        if val:
            sizesList2.append(val)

    return sizesList2


def check_avilable_sizes(productS1, productS2, productS3, productS4, productS5, productS6, ):
    Attribute = request.env['product.attribute'].sudo().search([('name', '=', 'Size')])
    sizesList = [productS1, productS2, productS3, productS4,
                 productS5, productS6, ]
    for rotation in sizesList:
        if 'Nothing' in sizesList:
            sizesList.remove('Nothing')

    for x in sizesList:
        if 'Nothing' in x or '-' in x:
            continue
        else:
            val = request.env['product.attribute.value'].sudo().search([('name', '=', x,)])
            if not val:
                request.env['product.attribute.value'].sudo().create({'name': x,
                                                                      'attribute_id': Attribute.id})


def Write_sizes(sizes_id_separte_odoo_form, Attribute, _product, ):
    # check is it copying or new item
    if all([isinstance(item, int) for item in sizes_id_separte_odoo_form]):
        # copy
        sizes_id_int_form = sizes_id_separte_odoo_form
    else:
        # new
        sizes_id_separte_odoo_form = sizes_id_separte_odoo_form
        print(sizes_id_separte_odoo_form)

        sizes_id_int_form = []

        for adding_ids in sizes_id_separte_odoo_form:
            x = adding_ids.id
            if x:
                sizes_id_int_form.append(adding_ids.id)
        print(sizes_id_int_form)

    ptal = request.env['product.template.attribute.line'].sudo().create({
        'attribute_id': Attribute.id if Attribute else False,
        'product_tmpl_id': _product.id,
        'value_ids': [(6, 0, sizes_id_int_form)],
    })
    _product.sudo().write({'attribute_line_ids': [(6, 0, [ptal.id])]})


def product_update(Url):
    counter = 0
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = uc.Chrome(options=options)
    driver.get(Url)
    try:
        price = driver.find_element_by_xpath(
            '/html/body/div[1]/div[1]/div/div[1]/div/div[2]/div[2]/div/div[1]/div[2]/div/div/span').text
    except:
        price = driver.find_element_by_xpath(
            '/html/body/div[1]/div[1]/div/div[1]/div/div[2]/div[2]/div/div[1]/div[3]/div/div/span').text
    try:
        counter = counter + 1

        check_if_sold_out = driver.find_element_by_xpath(
            '/html/body/div[1]/div[1]/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div[1]/span/div').get_attribute(
            "class")
        if 'radio_soldout' in check_if_sold_out:
            size1 = 'Nothing'

        else:

            size1 = driver.find_element_by_xpath(
                '/html/body/div[1]/div[1]/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div[1]/span/div/div').text

            if 'XS - L' in size1:
                check_if_sold_out = driver.find_element_by_xpath(
                    '/html/body/div[1]/div[1]/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/span/div').get_attribute(
                    "class")
                if 'radio_soldout' in check_if_sold_out:
                    size1 = 'Nothing'
                else:
                    size1 = driver.find_element_by_xpath(
                        '/html/body/div[1]/div[1]/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/span/div/div').text

    except:
        size1 = 'Nothing'
        counter = counter - 1

    # if 'Nothing' in size1:
    #     size2 = 'Nothing'
    #     size3 = 'Nothing'
    #     size4 = 'Nothing'
    #     size5 = 'Nothing'
    #     size6 = 'Nothing'
    # else:
    try:
        counter = counter + 1
        check_if_sold_out = driver.find_element_by_xpath(
            '/html/body/div[1]/div[1]/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/span/div').get_attribute(
            "class")
        if 'radio_soldout' in check_if_sold_out:
            size2 = 'Nothing'

        else:

            size2 = driver.find_element_by_xpath(
                '/html/body/div[1]/div[1]/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/span/div/div').text
            if size1 in size2 and size1 != 'L' and size2 != 'XL' and size1 != 'XL' and size2 != 'XXL':
                check_if_sold_out = driver.find_element_by_xpath(
                    '/html/body/div[1]/div[1]/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div[3]/span/div').get_attribute(
                    "class")
                if 'radio_soldout' in check_if_sold_out:
                    size2 = 'Nothing'
                else:
                    size2 = driver.find_element_by_xpath(
                        '/html/body/div[1]/div[1]/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div[3]/span/div/div').text
    except:
        size2 = 'Nothing'
        counter = counter - 1

    try:
        counter = counter + 1
        check_if_sold_out = driver.find_element_by_xpath(
            '/html/body/div[1]/div[1]/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div[3]/span/div').get_attribute(
            "class")
        if 'radio_soldout' in check_if_sold_out:
            size3 = 'Nothing'

        else:
            size3 = driver.find_element_by_xpath(
                '/html/body/div[1]/div[1]/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div[3]/span/div/div').text
            if size2 in size3 and size2 != 'L' and size3 != 'XL' and size2 != 'XL' and size3 != 'XXL':
                check_if_sold_out = driver.find_element_by_xpath(
                    '/html/body/div[1]/div[1]/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div[4]/span/div').get_attribute(
                    "class")
                if 'radio_soldout' in check_if_sold_out:
                    size3 = 'Nothing'

                else:
                    size3 = driver.find_element_by_xpath(
                        '/html/body/div[1]/div[1]/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div[4]/span/div/div').text
    except:
        size3 = 'Nothing'
        counter = counter - 1

    try:
        counter = counter + 1
        check_if_sold_out = driver.find_element_by_xpath(
            '/html/body/div[1]/div[1]/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div[4]/span/div').get_attribute(
            "class")
        if 'radio_soldout' in check_if_sold_out:
            size4 = 'Nothing'

        else:
            size4 = driver.find_element_by_xpath(
                '/html/body/div[1]/div[1]/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div[4]/span/div/div').text
            if size3 in size4 and size3 != 'L' and size4 != 'XL':
                check_if_sold_out = driver.find_element_by_xpath(
                    '/html/body/div[1]/div[1]/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div[5]/span/div').get_attribute(
                    "class")
                if 'radio_soldout' in check_if_sold_out:
                    size4 = 'Nothing'

                else:
                    size4 = driver.find_element_by_xpath(
                        '/html/body/div[1]/div[1]/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div[5]/span/div/div').text
    except:
        counter = counter - 1
        size4 = 'Nothing'

    try:
        counter = counter + 1
        check_if_sold_out = driver.find_element_by_xpath(
            '/html/body/div[1]/div[1]/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div[5]/span/div').get_attribute(
            "class")
        if 'radio_soldout' in check_if_sold_out:
            size5 = 'Nothing'

        else:
            size5 = driver.find_element_by_xpath(
                '/html/body/div[1]/div[1]/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div[5]/span/div/div').text
            if size4 in size5 and size4 != 'L' and size5 != 'XL' and size4 != 'XL' and size5 != 'XXL':
                check_if_sold_out = driver.find_element_by_xpath(
                    '/html/body/div[1]/div[1]/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div[6]/span/div').get_attribute(
                    "class")
                if 'radio_soldout' in check_if_sold_out:
                    size5 = 'Nothing'

                else:
                    size5 = driver.find_element_by_xpath(
                        '/html/body/div[1]/div[1]/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div[6]/span/div/div').text
    except:
        counter = counter - 1
        size5 = 'Nothing'

    try:
        counter = counter + 1
        check_if_sold_out = driver.find_element_by_xpath(
            '/html/body/div[1]/div[1]/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div[6]/span/div').get_attribute(
            "class")
        if 'radio_soldout' in check_if_sold_out:
            size6 = 'Nothing'

        else:
            size6 = driver.find_element_by_xpath(
                '/html/body/div[1]/div[1]/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div[6]/span/div/div').text
            if size5 in size6 and size5 != 'L' and size6 != 'XL' and size5 != 'XL' and size6 != 'XXL':
                check_if_sold_out = driver.find_element_by_xpath(
                    '/html/body/div[1]/div[1]/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div[7]/span/div').get_attribute(
                    "class")
                if 'radio_soldout' in check_if_sold_out:
                    size6 = 'Nothing'

                else:
                    size6 = driver.find_element_by_xpath(
                        '/html/body/div[1]/div[1]/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div[7]/span/div/div').text
    except:
        counter = counter - 1
        size6 = 'Nothing'
    counterT = str(counter)

    driver.quit()

    return Product(price=price, size1=size1, size2=size2, size3=size3,
                   size4=size4, size5=size5, size6=size6, counterT=counter)


def get_raw_price(string):
    new_str = ''
    for each in string:
        if each in "1234567890.,":
            new_str += each
    if ',' in new_str:
        new_str = new_str.replace(',', '.')
    if '€' in string:
        url = 'https://api.exchangerate-api.com/v4/latest/EUR'
        converter = RealTimeCurrencyConverter(url)
        price = math.ceil(converter.convert('EUR', 'EGP', float(new_str)))
    elif "$" in string:
        url = 'https://api.exchangerate-api.com/v4/latest/USD'
        converter = RealTimeCurrencyConverter(url)
        price = math.ceil(converter.convert('USD', 'EGP', float(new_str)))
    else:
        url = 'https://api.exchangerate-api.com/v4/latest/SAR'
        converter = RealTimeCurrencyConverter(url)
        price = math.ceil(converter.convert('SAR', 'EGP', float(new_str)))

    return price


class ProductsTemplate(models.Model):
    _inherit = "product.template"
    # so now we inherted the product table and giviin it a new filed
    product_description = fields.Char(string="product description")
    if_sales = fields.Boolean(string="Has Sale or not")

    Counter = fields.Char(string="Counter")

    # you will see scrapper name in gui as label name , if you dont give any name it will be name
    def Archived_update(self):
        intId = self.ids
        category_implementation = request.env['product.public.category'].sudo().search(
            [('id', '=', '14',)])

        Products_List = request.env['product.template']
        for count in intId:
            counter = request.env['product.template'].sudo().search([("id", "=", count)])
            Products_List = Products_List + counter

        for x in Products_List:
            x.sudo().write({'public_categ_ids': [(6, 0, [category_implementation.id])]})

    def Update_products(self):
        intId = self.ids
        category_implementation = request.env['product.public.category'].sudo().search(
            [('id', '=', '14',)])

        Products_List = request.env['product.template']
        for count in intId:
            counter = request.env['product.template'].sudo().search([("id", "=", count)])
            Products_List = Products_List + counter

        print(Products_List)

        y = str

        for x in Products_List:
            if y == x.name:
                continue
            Products_idz = x.product_description
            print(x.name)
            if Products_idz:

                product = product_update(Products_idz)

                x.sudo().write({'list_price': get_raw_price(product.price)})

                name = x.name

                Updating_Child_products = request.env['product.template'].sudo().search(
                    [('name', '=', name)])
                # good till here

                Define_sizes(counter, product.size1, product.size2, product.size3, product.size4, product.size5,
                             product.size6, x)

                for xy in Updating_Child_products:
                    xy.sudo().write({'list_price': get_raw_price(product.price)})
                    x.sudo().write({'public_categ_ids': [(6, 0, [category_implementation.id])]})

                    Define_sizes(counter, product.size1, product.size2, product.size3, product.size4,
                                 product.size5,
                                 product.size6, xy)

                y = x.name

        # request.redirect("/shop/category/update-12")
