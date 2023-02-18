# sas_memento_mori
Basic Odoo module for the Memento Mori thanatory-funerary

Modelo Relacional:
- memento_client_info(***generated* memento_client_info_id**, *representative_id*, *room_id*, name, thantopraxy_notes, category, state, hired_services, required_documents, start_booking, end_booking)
  - Client Info
- res_partner(***inherited* res.partner**,represented_client)
  - Client representatives inherited from res_partner
- memento_document(***generated* memento_document_id**, name, *client*, description, route)
  - Documents needed by the client
- memento_room(***generated* memento_room_id**, name, room_number, state, *booking*)
  - Velatory room
