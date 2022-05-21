import base64
import urllib
import requests
import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from dataclasses import dataclass
from odoo import http
from odoo.http import request


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

    @http.route('/Shein2egypt', website=True, auth='user')
    def web_scrapper(self, **kw):
        if kw:
            if 'https' in kw["Url"]:
                Link_of_product = kw["Url"]
                checkLink = request.env['product.template'].search(
                    [('product_description', '=', Link_of_product,)])

                if checkLink:
                    # if there is a product with same link we remove it from category so it doesn't show in
                    # ALl search history part
                    product = get_product(kw["Url"])
                    code = upload_image(product.image)
                    userid = request.env.user.id

                    request.env['product.template'].sudo().create({'name': product.name,
                                                                   'list_price': get_raw_price(product.price),
                                                                   'product_description': product.link,
                                                                   'is_published': True,
                                                                   'image_1920': base64.b64encode(get_img(code)),
                                                                   'description': userid
                                                                   })
                    return request.redirect("/shop/category/your-search-history-8")

                else:
                    product = get_product(kw["Url"])
                    code = upload_image(product.image)
                    x = request.env['product.public.category'].sudo().search(
                        [('name', '=', 'Your Search History',)])
                    userid = request.env.user.id

                    request.env['product.template'].sudo().create({'name': product.name,
                                                                   'list_price': get_raw_price(product.price),
                                                                   'product_description': product.link,
                                                                   'is_published': True,
                                                                   'image_1920': base64.b64encode(get_img(code)),
                                                                   'public_categ_ids': [(6, 0, [x.id])],
                                                                   'description': userid

                                                                   })
                    return request.redirect("/shop/category/your-search-history-8")
            else:

                return request.redirect("/Shein2egypt")

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
