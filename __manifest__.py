# -*- coding: utf-8 -*-
{
    'name': "Memento Mori",  # Module title
    'summary': "Manage bodies easily",  # Module subtitle phrase
    'description': """
Manage Library
==============
Description related to library.
    """,  # Supports reStructuredText(RST) format
    'author': "Alfredo",
    'website': "http://www.example.com",
    'category': 'App',
    'version': '14.0.1',
    'depends': ['base'],

    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/library_book.xml',
        'views/library_book_categ.xml'
    ],
    # This demo data files will be loaded if db initialize with demo data (commented becaues file is not added in this example)
    # 'demo': [
    #     'demo.xml'
    # ],
}
