{
    'name': 'WebScrapper',
    'version': '1.0',
    'author': 'youssef',
    'summary': 'Links to products',
    'sequence': 10,
    'sequence': '1',
    'description': "we will begin our journy now",
    'category': 'Sales/Sales',
    'website': 'sheesh',
    'depends': ['product', 'website', 'website_sale','website.assets'],
    'data': [
        'security/ir.model.access.csv',
        'views/template.xml',
        'views/products.xml',
        'security/security.xml',

    ],

    'installable': True,
    'application': True,
}
# a short idea of what is the module about
