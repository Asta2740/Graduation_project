from odoo import http
from odoo.http import request


class shein2egypt(http.Controller):

    @http.route('/Shein2egypt', website=True, auth='public')
    def web_scrapper(self, **kw):
        return "hello world"
