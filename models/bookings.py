# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class RoomBooking(models.Model):
    _name = 'memento.room.booking'
    _description = 'Room Booking'


    _parent_store = True
    _parent_name = "parent_id"  # optional if field is 'parent_id'

    room_number = fields.Integer(required = True, )

    
    client = fields.One2many(
        'memento.client.info', 
        string='client'
        ondelete='restrict',
        index=True
    )
    
    room = fields.One2many(
        'memento.'
    )  
    parent_path = fields.Char(index=True)

    @api.constrains('parent_id')
    def _check_hierarchy(self):
        if not self._check_recursion():
            raise models.ValidationError('Error! You cannot create recursive categories.')