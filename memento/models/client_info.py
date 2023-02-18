# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _


class ClientInfo(models.Model):
    
    """Client Info

    :raises UserError: when trying an illegal transition of state 
    """    
    _name = 'memento.client.info'
    _description = 'Client Info'

    COLLECT = 'to_collect'
    PRE_THANATOS = 'pre_thanatos'
    IN_THANATOS = 'in_thanatos'
    NO_ROOM = 'no_room'
    IN_ROOM = 'in_room'
    TO_SHIP = 'to_ship'
    SHIPPED = 'shipped'
    
    
    name = fields.Char(required=True, string="Name")

    thantopraxy_notes = fields.Text('Information for the thanatopraxor')
    category = fields.Selection(
        [('gold', 'Gold Plan'),
         ('silver', 'Silver Plan'),
         ('base', 'Base Plan'),
         ('insurance', 'Insurance Plan')],
        'plan',
        default='base'
    )
    state = fields.Selection(
        [(COLLECT, 'To Collect'),
         (PRE_THANATOS, 'Awaiting Thanatopraxy'),
         (IN_THANATOS, 'In Thanatopraxy'),
         (NO_ROOM, 'Room to be Asigned'),
         (IN_ROOM, 'In Room'),
         (TO_SHIP, 'Awaiting Shipment'),
         (SHIPPED, 'Shipped')],
        'state',
        default=COLLECT
    )
    hired_services = fields.Many2many(
        'product.product',
        string='services',
        ondelete='restrict',
        index=True
    )
    representative_id = fields.Many2many(
        'res.partner',
        string='Representative'
    )
    room_id = fields.Many2one(
        'memento.room',
        string='Room',
        ondelete='restrict',
        index=True
    )
    required_documents = fields.One2many(
        'memento.document',
        'client',
        string='Required Documents',
        ondelete='restrict',
        index=True
    )
    start_booking = fields.Datetime('Beginning of the Booking')
    end_booking = fields.Datetime('End of the Booking')

    @api.model
    def is_allowed_transition(self, current_state: str, new_state: str) -> bool:
        """Establishes the allowed transitons between states

        :param current_state: state to transition from
        :type current_satate: str
        :param new_state: state to transition to
        :type new_state: str

        :returns: whether the transition is allowed or not
        :rtype: bool"""
        # List of allowed transitions
        allowed = [(ClientInfo.COLLECT, ClientInfo.PRE_THANATOS),
                   (ClientInfo.COLLECT, ClientInfo.IN_THANATOS),
                   (ClientInfo.PRE_THANATOS, ClientInfo.IN_THANATOS),
                   (ClientInfo.IN_THANATOS, ClientInfo.NO_ROOM),
                   (ClientInfo.IN_THANATOS, ClientInfo.IN_ROOM),
                   (ClientInfo.NO_ROOM, ClientInfo.IN_ROOM),
                   (ClientInfo.IN_ROOM, ClientInfo.TO_SHIP),
                   (ClientInfo.IN_ROOM, ClientInfo.SHIPPED),
                   (ClientInfo.TO_SHIP, ClientInfo.SHIPPED)]
        return (current_state, new_state) in allowed

    def change_state(self, new_state):
        """Changes the current state of self to a new_state if allowed

        :raises UserError: if transition illegal
        """
        for body in self:
            if body.is_allowed_transition(body.state, new_state):
                body.state = new_state
            else:
                message = _('Moving from %s to %s is not allowd') % (
                    body.state, new_state)
                raise UserError(message)

    def collect(self):        
        """Changes the state of the client to PRE_THANATOS

        Used when the body has already arrived to the thanatory-funerary.
        """
        self.change_state(ClientInfo.PRE_THANATOS)

    def start_thanatos(self):
        """Changes the state of the client to IN_THANATOS

        Used when the body can start the thanatopraxy.
        """
        self.change_state(ClientInfo.IN_THANATOS)

    def finish_thanatos(self):
        """Changes the state of the client to NO_ROOM

        Used when the body finishes the thanatopraxy and has no room assigned yet.
        """
        self.change_state(ClientInfo.NO_ROOM)

    def assign_room(self):
        """Changes the state of the client to IN_ROOM

        Used when the body is assigned a room.
        """
        self.change_state(ClientInfo.IN_ROOM)

    def finish_velatory(self):
        """Changes the state of the client to TO_SHIP

        Used when the velatory is finished and the body is scheduled to 
        """
        self.change_state(ClientInfo.TO_SHIP)

    def ship(self):
        """Changes the state of the client to SHIPPED        

        Used when the body has left the thanatory
        """
        self.change_state(ClientInfo.SHIPPED)


class ResPartner(models.Model):
    """_summary_

    :param models: _description_
    :type models: _type_
    """
      
    """_summary_
    """      
    _inherit = 'res.partner'
    """_summary_
    """
    represented_client = fields.Many2many(
        'memento.client.info',
        string='Represented Client'
    )


class Document(models.Model):

    _name = 'memento.document'
    _description = 'Documents related'

    name = fields.Char('Document Name', required=True)
    client = fields.Many2one(
        'memento.client.info',
        string='Required Documents',
        ondelete='restrict',
        index=True
    )
    description = fields.Text('Document Description')
    route = fields.Text('Route To Document File')
