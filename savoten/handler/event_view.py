from flask import Blueprint, render_template

event_view = Blueprint('view',
                       __name__,
                       template_folder='templates',
                       static_folder='static')


@event_view.route('/events', methods=['GET'])
def get_events_page():
    return render_template('get_events.html')


@event_view.route('/create_event', methods=['GET'])
def create_event_page():
    return render_template('create_event.html')
