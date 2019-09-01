# -*- coding: utf-8 -*-
{
    'name': "bloopark_sales_exchage",

    'summary': """Sales Delivery Exchange Custom Process
        """,

    'description': """
        The module provide a delivery exchange process, allowing the customer to exchange an already delivered and paid product.
        """,
    'author': "Bloopark",
    'website': "www.bloopark.de",
    'category': 'Ecommerce',
    'version': '0.1.1',
    'depends': ['base', 'web', 'website', 'website_sale'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/assets.xml',
        'views/views.xml',
        'views/portal_templates.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}
