import base64
import urllib
import requests
from selenium.webdriver.chrome.options import Options
from dataclasses import dataclass
from odoo import http
from odoo.http import request
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import math
from tkinter import *
import tkinter as tk
from tkinter import ttk


# https://www.odoo.com/documentation/master/developer/reference/backend/http.html

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
    size7: str = None
    size8: str = None
    size9: str = None
    size10: str = None
    size11: str = None
    size12: str = None
    size13: str = None
    size14: str = None
    size15: str = None
    size16: str = None
    size17: str = None
    size18: str = None
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


def get_product(url):
    counter = 0
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get(url)
    name = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div/div[1]/div/div[2]/div[2]/div/div[1]/h1').text
    try:
        price = driver.find_element_by_xpath(
            '/html/body/div[1]/div[1]/div/div[1]/div/div[2]/div[2]/div/div[1]/div[2]/div/div/span').text
    except:
        price = driver.find_element_by_xpath(
            '/html/body/div[1]/div[1]/div/div[1]/div/div[2]/div[2]/div/div[1]/div[3]/div/div/span').text
    try:
        color = driver.find_element_by_xpath(
            '/html/body/div[1]/div[1]/div/div[1]/div/div[2]/div[2]/div/div[2]/div[1]/div[1]/span/span').text
    except:
        color = 'Fixed'
    link = url
    try:
        image = driver.find_element_by_xpath(
            '/html/body/div[1]/div[1]/div/div[1]/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/div[2]/img').get_attribute(
            'src')
    except:
        image = driver.find_element_by_xpath(
            '/html/body/div[1]/div[1]/div/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/div[1]/div[1]/img[1]').get_attribute(
            'src')
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
    print(image)
    return Product(name=name, price=price, color=color, link=link, image=image, size1=size1, size2=size2, size3=size3,
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


def upload_image(link):
    if 'https:' in link:
        get = urllib.request.urlopen(link)
    else:
        get = urllib.request.urlopen(
            'https:' + str(link))

    img = get.read()
    files = {'files[]': ('image.png', img)}
    post = requests.post('https://angelo666.pythonanywhere.com/upload', files=files)
    return post.content.decode('utf-8')


def get_img(code):
    return requests.get(f'https://angelo666.pythonanywhere.com/img/{code}/').content


def put_colour_in_name(name, colour):
    if "Fixed" in colour:
        colour_name = name
    else:
        colour_name = name + " color:" + colour
    return colour_name


class shein2egypt(http.Controller):

    @http.route('/Shein2egypt', website=True, auth='user')
    def web_scrapper(self, **kw):
        if kw:

            Attribute = request.env['product.attribute'].sudo().search([('name', '=', 'Size')])

            Link_of_product = kw["Url"]

            # checking if its shein url only or not and not a homepage
            if 'https' in Link_of_product and 'shein' in Link_of_product and ".html" in Link_of_product:

                # check for parent products in database
                checkLink = request.env['product.template'].search(
                    [('product_description', 'like', Link_of_product[11:120]),
                     ('description', '=', '<p>first item</p>')])
                print(checkLink)

                if checkLink:

                    name_C = checkLink.name
                    Description_C = checkLink.product_description
                    price_C = checkLink.list_price
                    image_C = checkLink.image_1920
                    # put child category
                    category_implementation = request.env['product.public.category'].sudo().search(
                        [('id', '=', '14',)])

                    C_product = request.env['product.template'].sudo().create({'name': name_C,
                                                                               'list_price': price_C,
                                                                               'product_description': Description_C,
                                                                               'is_published': True,
                                                                               'image_1920': image_C,
                                                                               'public_categ_ids': [
                                                                                   (6, 0, [category_implementation.id])]
                                                                               })

                    copy_attributes = request.env['product.template.attribute.line'].sudo().search(
                        [('id', '=', checkLink.attribute_line_ids.id)])

                    Sizes_C = copy_attributes.value_ids

                    Write_sizes(Sizes_C.ids, Attribute, C_product)

                    return request.redirect("/shop/category/personal-shop-15")
                # Copying ends here and it endsss in 0.5 - 2 seconds

                else:
                    # if we dont have it in parents products
                    start = time.time()

                    product = get_product(Link_of_product)

                    code = upload_image(product.image)
                    # translation didnt work here so we added by id
                    # not name since it was translated inside so it couldn't find the name

                    category_implementation = request.env['product.public.category'].sudo().search(
                        [('id', '=', '8',)])

                    product_name = put_colour_in_name(product.name, product.color)

                    _product = request.env['product.template'].sudo().create({'name': product_name,
                                                                              'list_price': get_raw_price(
                                                                                  product.price),
                                                                              'standard_price': get_raw_price(
                                                                                  product.price),
                                                                              'product_description': product.link,
                                                                              'is_published': True,
                                                                              'image_1920': base64.b64encode(
                                                                                  get_img(code)),
                                                                              'public_categ_ids': [
                                                                                  (6, 0, [category_implementation.id])],
                                                                              'description': 'first item',

                                                                              })
                    print(_product.id)

                    counter = int(product.counterT)
                    check_avilable_sizes(product.size1, product.size2, product.size3, product.size4, product.size5,
                                         product.size6)

                    Define_sizes(counter, product.size1, product.size2, product.size3, product.size4, product.size5,
                                 product.size6, _product)

                    end = time.time()
                    print(f"image loading Not in database {end - start}")

                    return request.redirect("/shop/category/personal-shop-15")

            else:

                return request.redirect("/Shein2egypt")

        return request.render('shein2egypt.Shein_page')
