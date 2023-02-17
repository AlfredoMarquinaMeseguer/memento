# -*- coding: utf-8 -*-
{
    'name': "Memento Mori",  # Module title
    'summary': "Manage bodies easily",  # Module subtitle phrase
    'description': """
        Manage cadavers easily        
        Description related to thanatory.
    """,  # Supports reStructuredText(RST) format
    'author': "Alfredo",
    'website': "http://www.mementomori.urlinventa'.com",
    'category': 'Tools',
    'version': '14.0.1',
    'depends': ['base'],

    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/client.xml'
        #'views/library_book_categ.xml'
    ],
    # This demo data files will be loaded if db initialize with demo data (commented becaues file is not added in this example)
    # 'demo': [
    #     'demo.xml'
    # ],
}
