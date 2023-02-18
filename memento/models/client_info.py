# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _

""" 
This file contains the following classes:

:class ClientInfo: Information of the client, specific to the funerary-thanatory
:class ResPartner: Inheritance from res.partner, representative of the client
:class Document: Documents need by the client_info
"""

class ClientInfo(models.Model):
    """
    This class contains several attributes related to the processes 
    the body undergoes during the its time in the funerary-thanatory
    :ivar _name: Name of the table in the database
    :vartype _name: str    
    :ivar _description: Description of the table in the database
    :vartype _description: str
    :ivar name: Name of the client
    :vartype name: odoo.fields.Char    
    :ivar thantopraxy_notes: Specifications for the thanatopraxor
    :vartype name: odoo.fields.Char    
    :ivar category: Plan which the client has hired
    :vartype category: odoo.fields.Selection    
    :ivar state: Stage of the funerary cicle
    :vartype state: odoo.fields.Selection    
    :ivar hired_services: Services hired by the client
    :vartype hired_services: odoo.fields.Many2many    
    :ivar representative_id: Living representative(s) of the client
    :vartype representative_id: odoo.fields.Many2many        
    :ivar required_documents: Documents required by the client in order 
                              to be buried and others
    :vartype required_documents: odoo.fields.One2Many    
    :ivar room_id: Room where the velatory will be held
    :vartype room_id: odoo.fields.Many2one    
    :ivar start_booking: Moment when the client will enter the velatory 
                         room
    :vartype start_booking: odoo.fields.DateTime    
    :ivar end_booking: Moment when the client will leave the velatory 
                       roomName of the client
    :vartype end_booking: odoo.fields.DateTime     
    
    :raises UserError: when trying an illegal transition of state 
    """

    _name = 'memento.client.info'
    _description = 'Client Info'

    COLLECT = 'to_collect'
    """
    State value for when the client hasn't been retive from the morgue yet.
    
    :type: str 
    """
    PRE_THANATOS = 'pre_thanatos'
    """
    State value for when the client hasn't enter thanatropraxy yet.
    
    :type: str 
    """
    IN_THANATOS = 'in_thanatos'
    """
    State value for when the client is in thanatopraxy at the moment.
    
    :type: str 
    """
    NO_ROOM = 'no_room'
    """
    State value for when the client has finnished thantopraxy but hasn't been
    assigned a room yet.
    
    :type: str 
    """
    IN_ROOM = 'in_room'
    """
    State value for when the client is in a velatory room at the moment.
    
    :type: str 
    """
    TO_SHIP = 'to_ship'
    """
    State value for when the client has finnished the velatory but hasn't 
    leave the funerary-thanatory yet.
    
    :type: str 
    """
    SHIPPED = 'shipped'
    """
    State value for when the client has left the funerary-thanatory yet.
    
    :type: str 
    """

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
        :rtype: bool
        """
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
        """Changes the current state of self to a new_state

        If allowed reassings the state of the client to the new state. If not allowed raises an UserError
        :raises UserError: illegal transition 
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
    """Client Representative

    The client representative is the living person the funerary-thanatory can contact to arragements notify of the state of the client.
    The client representative is technically the real client.
    :ivar _inherit: Name of the table it inherits from
    :vartype _inherit: str
    :ivar represented_client: Clientes representados
    :vartype represented_client: odoo.fields.Many2many
    :param models: class that allows this class to become a table in the postgress database
    :type models: object
    """
    _inherit = 'res.partner'
    represented_client = fields.Many2many(
        'memento.client.info',
        string='Represented Client'
    )


class Document(models.Model):
    """Document
    
    Documents needed by the client needs in order to: be able to be buried, allow the heirs to have the inheritance,
    transport the body between states, provinces or even countries, etc.
    :ivar _name: Name of the table in the database
    :vartype _name: str    
    :ivar _description: Description of the table in the database
    :vartype _description: str
    :param models: class that allows this class to become a table in the postgress database
    :type models: object
    :ivar name: Name of the document being presented
    :vartype name: odoo.fields.Char
    :ivar client: Client which the document belogns to
    :vartype client: odoo.fields.Many2one
    :ivar description: Description of the content of the document
    :vartype description: odoo.fields.Text
    :ivar route: /path/to/document
    :vartype route: odoo.fields.Text
    """
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
