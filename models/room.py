# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools.translate import _


class Room(models.Model):
    _name = 'memento.room'
    _description = 'Room Booking'

    # _parent_store = True
    # _parent_name = "parent_id"  # optional if field is 'parent_id'

    FREE = 'free'
    BOOKED = 'booked'
    OCCUPIED = 'occupied'
    DIRTY = 'dirty'
    MAINTENANCE = 'maintenance'

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
    def is_allowed_transition(self, old_state, new_state):
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

    def change_state(self, new_state):
        for room in self:
            if room.is_allowed_transition(room.state, new_state):
                room.state = new_state
            else:
                message = _('Transitioning from %s to %s is not allowd') % (
                    room.state, new_state)
                raise UserError(message)

    def make_free(self):
        self.change_state(Room.FREE)

    def make_booked(self):
        self.change_state(Room.BOOKED)

    def make_occupied(self):
        self.change_state(Room.OCCUPIED)

    def make_dirty(self):
        self.change_state(Room.DIRTY)

    def make_maintenance(self):
        self.change_state(Room.MAINTENANCE)
