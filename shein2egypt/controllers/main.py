from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from dataclasses import dataclass


@dataclass
class Product:
    name: str = None
    color: str = None
    price: str = None
    link: str = None
    image: str = None
    is_featured: bool = False


def get_product(url):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = uc.Chrome(options=options)
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
    driver.quit()
    print(Product(name=name, price=price, color=color, link=link, image=image)
          )
    return Product(name=name, price=price, color=color, link=link, image=image)


def get_raw_price(string):
    new_str = ''
    for each in string:
        if each in "1234567890.":
            new_str += each
    return float(new_str)


class shein2egypt(http.Controller):

    @http.route('/Shein2egypt', website=True, auth='public')
    def web_scrapper(self, **kw):
        if kw:
            product = get_product(kw["Url"])

            request.env['product.template'].sudo().create({'name': product.name,
                                                           'list_price': get_raw_price(product.price),
                                                           'product_description': product.link,
                                                           })
            # 'responsible_id':
            #'image_1920': product.image

            print(product.image)
            return str(product)

        return request.render('shein2egypt.Shein_page')
        # return "hello world"
