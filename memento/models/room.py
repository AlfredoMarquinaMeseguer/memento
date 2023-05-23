# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _


class Room(models.Model):
    """Velatory room

    :ivar _name: Name of the table in the database
    :vartype _name: str    
    :ivar _description: Description of the table in the database
    :vartype _description: str
    :ivar name: Name of the room
    :vartype name: odoo.fields.Char
    :ivar room_number: Number of the room
    :vartype room_number: odoo.fields.Integer
    :ivar state: State of the room
    :vartype state: odoo.fields.Selection
    :ivar booking: List of clients who have booked the room
    :vartype booking: odoo.fields.One2many
    """
    _name = 'memento.room'
    _description = 'Room Booking'

    # A la próxima importo enum
    FREE = 'free'
    """
    State value for when the room is free
    
    :type: str 
    """
    BOOKED = 'booked'
    """
    State value for when the room is booked
    
    :type: str 
    """
    OCCUPIED = 'occupied'
    """
    State value for when the room is occupied
    
    :type: str 
    """
    DIRTY = 'dirty'
    """
    State value for when the room is dirty
    
    :type: str 
    """
    MAINTENANCE = 'maintenance'
    """
    State value for when the room is under maintenance
    
    :type: str 
    """

    name = fields.Char(required=True, string="Name")
    room_number = fields.Integer('Room number')
    state = fields.Selection(
        [(FREE, 'Free'),
         (BOOKED, 'Booked'),
         (DIRTY, 'Dirty'),
         (OCCUPIED, 'Occupied'),
         (MAINTENANCE, 'Maintenance')],
        'State',
        default=FREE
    )
    booking = fields.One2many(
        'memento.client.info',
        'room_id',
        string='Bookings'
    )

    @api.model
    def is_allowed_transition(self, old_state: str, new_state: str) -> bool:
        """Changes the current state of self to a new_state

        If allowed reassings the state of the room to the new state. If not allowed raises an UserError
        :raises UserError: illegal transition 
        """
        
        allowed = [(Room.FREE, Room.BOOKED),
                   (Room.FREE, Room.OCCUPIED),
                   (Room.FREE, Room.MAINTENANCE),
                   (Room.BOOKED, Room.FREE),
                   (Room.BOOKED, Room.OCCUPIED),
                   (Room.BOOKED, Room.MAINTENANCE),
                   (Room.OCCUPIED, Room.DIRTY),
                   (Room.OCCUPIED, Room.MAINTENANCE),
                   (Room.OCCUPIED, Room.MAINTENANCE),
                   (Room.DIRTY, Room.FREE),
                   (Room.DIRTY, Room.MAINTENANCE),
                   (Room.MAINTENANCE, Room.FREE)]
        return (old_state, new_state) in allowed

    def change_state(self, new_state: str):        
        """Changes the current state of the room to new_state

        If allowed reassings the state of the client to the new state. 
        If not allowed raises an UserError
        :param new_state: State that wants to be transitioned to
        :type new_state: str
        :raises UserError: illegal transition 
        """
        
        for room in self:
            if room.is_allowed_transition(room.state, new_state):
                room.state = new_state
            else:
                message = _('Transitioning from %s to %s is not allowd') % (
                    room.state, new_state)
                raise UserError(message)

    def make_free(self):
        """Changes the state of the room to FREE"""
        
        self.change_state(Room.FREE)

    def make_booked(self):
        """Changes the state of the room to BOOKED"""
        
        self.change_state(Room.BOOKED)

    def make_occupied(self):
        """Changes the state of the room to OCCUPIED"""
        
        self.change_state(Room.OCCUPIED)

    def make_dirty(self):
        """Changes the state of the room to DIRTY"""
        
        self.change_state(Room.DIRTY)

    def make_maintenance(self):
        """Changes the state of the room to MAINTENANCE"""
        
        self.change_state(Room.MAINTENANCE)
