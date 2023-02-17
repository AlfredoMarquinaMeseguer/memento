# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ClientInfo(models.Model):
    _name = 'memento.thanatory.room'
    _description = 'Thanatory Room'


    _parent_store = True
    _parent_name = "parent_id"  # optional if field is 'parent_id'

    room_number = fields.Integer(required = True, )

    especifications = fields.Text()
    category =fields.Selection([('gold', 'Gold Plan'),
                              ('silver', 'Silver Plan'),
                              ('base', 'Base Plan'),
                              ('insurance','Insurance Plan')],
                               'plan', default='base') 
    
    state = fields.Selection([('free', 'Free'),
                              ('reserved', 'Awaiting Thanatopraxy'),
                              ('ocupied', 'Ocupied'),
                              ('cleaning', 'Room to be Asigned'),
                              ('maintenance', 'In Room')],
                               'state', default='free')
	
    current_client = fields.One2many(
        'memento.client.info', 
        string='client'
        ondelete='restrict',
        index=True
    )
    
   
    parent_path = fields.Char(index=True)

    @api.constrains('parent_id')
    def _check_hierarchy(self):
        if not self._check_recursion():
            raise models.ValidationError('Error! You cannot create recursive categories.')