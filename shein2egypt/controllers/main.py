import base64
import urllib
import requests
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from dataclasses import dataclass
from odoo import http
from odoo.http import request
import time


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



def get_product(url):
    start = time.time()


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

    try:
        size1 = driver.find_element_by_xpath(
            '/html/body/div[1]/div[1]/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div[1]/span/div/div').text
    except:
        size1 = driver.find_element_by_xpath(
            '/html/body/div[1]/div[1]/div/div[1]/div/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/div[2]/span/div/div').text

    driver.quit()
    print(Product(name=name, price=price, color=color, link=link, image=image, size1=size1)

          )

    end = time.time()
    print(f"scrapper {end - start}")

    return Product(name=name, price=price, color=color, link=link, image=image)


def get_raw_price(string):
    if '€' in string:
        convert_price = 19.10
    elif "$" in string:
        convert_price = 18.26
    else:
        convert_price = 4.87

    new_str = ''
    for each in string:
        if each in "1234567890.,":
            new_str += each
    if ',' in new_str:
        new_str = new_str.replace(',', '.')
    price = round(float(new_str) * convert_price)
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


class shein2egypt(http.Controller):

    @http.route('/Shein2egypt', website=True, auth='user' )
    def web_scrapper(self, **kw):
        if kw:
            product = get_product(kw["Url"])
            return product.size
            # if 'https' in kw["Url"]:
            #     #checking if its shein url
            #     Link_of_product = kw["Url"]
            #
            #     checkLink = request.env['product.template'].search(
            #         [('product_description', '=', Link_of_product,)])
            #
            #     if checkLink:
            #         # if there is a product with same link we remove it from category so it doesn't show in
            #         # ALl search history part
            #         product = get_product(kw["Url"])
            #         start = time.time()
            #         code = upload_image(product.image)
            #         userid = request.env.user.id
            #         end = time.time()
            #         print(f"image loading in DB  {end - start}")
            #         start = time.time()
            #
            #         request.env['product.template'].sudo().create({'name': product.name,
            #                                                        'list_price': get_raw_price(product.price),
            #                                                        'product_description': product.link,
            #                                                        'is_published': True,
            #                                                        'image_1920': base64.b64encode(get_img(code)),
            #                                                        'description': userid
            #                                                        })
            #         end = time.time()
            #         print(f"adding to database in DB {end - start}")
            #
            #         return request.redirect("/shop/category/your-search-history-8")
            #
            #
            #     else:
            #
            #
            #         product = get_product(kw["Url"])
            #         start = time.time()
            #         code = upload_image(product.image)
            #         x = request.env['product.public.category'].sudo().search(
            #             [('name', '=', 'Your Search History',)])
            #
            #         Attribute = request.env['product.attribute'].sudo().search([('name', '=', 'SIze')])
            #
            #
            #
            #         end = time.time()
            #         print(f"image loading Not in database {end - start}")
            #
            #         userid = request.env.user.id
            #         start = time.time()
            #         product_name = product.name
            #         product_price = get_raw_price(product.price)
            #         product_link = product.link
            #         Product_image = base64.b64encode(get_img(code))
            #
            #         _product = request.env['product.template'].sudo().create({'name': product_name,
            #                                                        'list_price':product_price,
            #                                                        'product_description': product_link,
            #                                                        'is_published': True,
            #                                                        'image_1920': Product_image,
            #                                                        'public_categ_ids': [(6, 0, [x.id])],
            #                                                        'description': userid,
            #
            #
            #                                                        })
            #
            #
            #         val = request.env['product.attribute.value'].sudo().search([('name', '=', "S")])
            #
            #
            #         ptal = request.env['product.template.attribute.line'].sudo().create({
            #             'attribute_id': Attribute.id if Attribute else False,
            #             'product_tmpl_id': _product.id,
            #             'value_ids': [(6, 0, [val.id])],
            #         })
            #         _product.sudo().write({
            #             'attribute_line_ids': [(6, 0, [ptal.id])]})
            #
            #
            #
            #         end = time.time()
            #         print(f"adding to database not in database {end - start}")
            #
            #         return request.redirect("/shop/category/your-search-history-8")
            # else:
            #
            #     return request.redirect("/Shein2egypt")

        return request.render('shein2egypt.Shein_page')





class pos_website_sale(http.Controller):
    @http.route(['/shop/clear_cart'], type='json', auth="public", website=True)
    def clear_cart(self):
        order = request.website.sale_get_order()
        if order:
            for line in order.website_order_line:
                line.unlink()

# class popcat(http.Controller):
#
#     @http.route('/popcat', website=True, auth='user')
#     def popcat(self, **kw):
#         return request.render('shein2egypt.Pop_cat')

# @http.route('/payment/status', type='http', auth='public', website=True, sitemap=False)
#     def display_status(self, **kwargs):
#         """ Display the payment status page.
#
#         :param dict kwargs: Optional data. This parameter is not used here
#         :return: The rendered status page
#         :rtype: str
#         """
#         return request.render('payment.payment_status')
