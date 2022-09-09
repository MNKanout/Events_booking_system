from events_registry.views import event
from django import template
from ..models import Event
from django.shortcuts import get_object_or_404

register = template.Library()


@register.filter(name='get_seat')
def get_seat_number(member_id, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if event.seats.get(member_id):
        return event.seats.get(member_id)


