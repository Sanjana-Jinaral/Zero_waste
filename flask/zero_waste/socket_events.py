from flask_socketio import emit, join_room, leave_room
from flask_login import current_user
from extensions import socketio

def init_socket(socketio):
    @socketio.on('join_ngo')
    def handle_join_ngo(data):
        """NGO dashboard joins its private room to receive volunteer updates."""
        ngo_id = data.get('ngo_id')
        if ngo_id:
            room = f'ngo_{ngo_id}'
            join_room(room)
            print(f'NGO {ngo_id} joined room {room}')
            emit('joined_room', {'room': room})

    @socketio.on('volunteer_location')
    def handle_volunteer_location(data):
        """
        Payload from a volunteer client:
        {
            volunteer_id: int,
            lat: float,
            lng: float,
            delivery_id: int,
            ngo_id: int
        }
        """
        ngo_id = data.get('ngo_id')
        if not ngo_id:
            return

        room = f'ngo_{ngo_id}'
        # Forward the update to the NGO's private room
        emit('volunteer_location_update', data, room=room)
