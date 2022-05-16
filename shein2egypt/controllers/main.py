from odoo import http
from odoo.http import request


class shein2egypt(http.Controller):

    @http.route('/Shein2egypt', website=True, auth='public')
    def web_scrapper(self, **kw):
        return request.render("shein2egypt.Shein_page", {})
        #return "hello world"
