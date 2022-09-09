# Django modules
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages as dj_messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import JsonResponse
from datetime import datetime

# project moduels
from .models import Event
from .forms import EventForm
from users.models import Member


def index(request):
    return render(request,"index.html")

@login_required
def events(request):
    if request.method != "POST":
        events = Event.objects.filter(start_date__gte = datetime.today()).order_by('-start_date','start_time')

        context = {'events':events}
        return render(request, 'events.html',context=context)


@login_required
def event(request, event_id):

    event = get_object_or_404(Event,id=event_id)
    member = get_object_or_404(Member,id=request.user.id)

    # Check if member is attending the event
    if request.user.is_authenticated:
        attending = event.has_attender(member.id)

    context = {'event':event,'attending':attending}
    return render(request,"event.html",context=context)

# Register member in event
@login_required
def register(request, event_id):
    event = get_object_or_404(Event,id=event_id)
    member = get_object_or_404(Member,id=request.user.id)

    if request.method == "POST":    
        #Member is not registered in the event with places avaliable in the event
        if event.is_fully_booked == False and event.has_attender(member.id) == False:
            event.add_attender(member.id)
            event.save()
            return JsonResponse(
                {'status':'r',
                'attenders_count':event.count_attenders,
                'button_text':'Unregister',
                'button_id':'u-' + str(event_id),
                'button_class':'primary-outline-button',
                'message':'You were successfully registered in the event',
                'message_class':'alert alert-success'}
                ,status= 200)

        #If member is already registered in the event
        elif event.has_attender(member.id) == True:
            return JsonResponse(
                {'status':'r-in',
                'attenders_count':event.count_attenders,
                'button_id':'u-' + str(event_id),
                'button_class':'primary-outline-button',
                'button_text':'Unregister',
                'message':'You are already registered in this event!','message_class':'alert alert-warning'},
                status= 400)

        #if event is fully booked
        elif event.is_fully_booked == True:
            return JsonResponse(
                {'status':'r-full',
                'attenders_count':event.count_attenders,
                'button_id':'r-' + str(event_id),
                'button_class':'primary-outline-button disabled',
                'button_text':'Full',
                'message':'Registering failed, the event is fully booked!','message_class':'alert alert-danger'},
                status= 400)

# Unregister member from event
@login_required
def unregister(request, event_id):
    event = get_object_or_404(Event,id=event_id)
    member = get_object_or_404(Member,id=request.user.id)

    if request.method == "POST":
        # Member is registered in the event
        if event.has_attender(member.id) == True:
            # If member has checked in
            if event.has_arrival(member.id):
                seat_number = event.get_seat(member_id=member.id)
                return JsonResponse(
                {'status':'u',
                'attenders_count':event.count_attenders,
                'button_id':'r-' + str(event_id),
                'button_class':'btn btn-outline-danger disabled',
                'button_text':f'{seat_number}',
                'message':"You can't unregister after you have been checked in",'message_class':'alert alert-danger'},
                status= 400)

            else:
                event.remove_attender(member.id)
                event.save()
                return JsonResponse(
                    {'status':'u',
                    'attenders_count':event.count_attenders,
                    'button_id':'r-' + str(event_id),
                    'button_class':'primary-outline-button',
                    'button_text':'Regsiter',
                    'message':'You were successfully unregistered from the event','message_class':'alert alert-success'},
                    status= 200)

        # Member is not registered in the event
        else:
            return JsonResponse(
                {'status':'u',
                'attenders_count':event.count_attenders,
                'button_id':'r-' + str(event_id),
                'button_class':'primary-outline-button',
                'button_text':'Regsiter',
                'message':'You are not registered in this event!','message_class':'alert alert-warning'},
                status= 400)


#Check in members in event
@login_required
@permission_required('events_registry.change_event',raise_exception=True)
def check_in(request, event_id):
    if request.method == "POST":
        event = get_object_or_404(Event,id=event_id)
        arrival_id = int(request.POST.get('arrival_id'))

        # Member is registered in the event
        if event.has_attender(arrival_id):

            # Member is already checked in 
            if event.has_arrival(arrival_id):
                return JsonResponse(
                {'status':'c-in',
                'attenders_count':event.count_attenders,
                'arrivals_count':event.count_arrivals,
                'message':'Member is already checked in!','message_class':'alert alert-warning'},
                status= 400)

            # Member is not chekced in yet
            else:
                event.add_arrival(arrival_id)
                event.give_seat(arrival_id)
                event.save() 
                seat_number = event.get_seat(arrival_id)
                return JsonResponse(
                {'status':'c-in',
                'attenders_count':event.count_attenders,
                'arrivals_count':event.count_arrivals,
                'seat_number':seat_number,
                'message':'',
                'message_class':'alert alert-success'},
                status= 200)
                
        # Member is not registered in the event
        else:
            return JsonResponse(
            {'status':'n-r',
            'attenders_count':event.count_attenders,
            'arrivals_count':event.count_arrivals,
            'message':f' Member with ID {arrival_id} is not registered in this event!','message_class':'alert alert-warning','message_class':'alert alert-warning'},
            status= 400)


#Check out members from events
@login_required
@permission_required('events_registry.change_event',raise_exception=True)
def check_out(request, event_id):
    if request.method == "POST":
        event = get_object_or_404(Event,id=event_id)
        arrival_id = int(request.POST.get('arrival_id'))

        # Member is registered in the event
        if event.has_attender(arrival_id):

            # Member is checked in
            if event.has_arrival(arrival_id):
                event.remove_arrival(arrival_id)
                event.remove_seat(arrival_id)
                event.save()
                return JsonResponse(
                {'status':'c-out',
                'attenders_count':event.count_attenders,
                'arrivals_count':event.count_arrivals,
                'seat_number':'',
                'message':'',
                'message_class':'alert alert-success'},
                status= 200)

            # Member is already checked out
            else:
                return JsonResponse(
                {'status':'c-out',
                'attenders_count':event.count_attenders,
                'arrivals_count':event.count_arrivals,
                'message':f' Member with ID {arrival_id} is already checked out!','message_class':'alert alert-warning'},
                status= 400)

        else:
            return JsonResponse(
            {'status':'n-r',
            'attenders_count':event.count_attenders,
            'arrivals_count':event.count_arrivals,
            'message':f' Member with ID {arrival_id} is not registered in this event!','message_class':'alert alert-warning'},
            status= 400)

# Monitor an event
@login_required
@permission_required('events_registry.change_event',raise_exception=True)
def monitor(request, event_id):
    event = get_object_or_404(Event,id=event_id)
    context = {'event':event}
    return render(request, "monitor.html",context=context)
            
# Add new event
@login_required
@permission_required('events_registry.add_event',raise_exception=True)
def new_event(request):
    if request.method == 'GET':
        form = EventForm()

    elif request.method == "POST":
        form = EventForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('events_registry:events')

        else:
            dj_messages.add_message(request, dj_messages.ERROR, 'Adding a new event failed',extra_tags='danger')

    context = {'form':form}
    return render(request, 'new_event.html',context=context)


# Edit event
@login_required
@permission_required('events_registry.change_event','events_registry.delete_event')
def edit_event(request, event_id):
    event = get_object_or_404(Event,id=event_id)

    if request.method == 'GET':
        form = EventForm(instance=event)

    elif request.method == "POST":
        if request.POST.get('update-event') == 'delete':
            event.delete()
            return redirect('events_registry:events')
            
        elif request.POST.get('update-event') == 'apply':
            form = EventForm(instance=event,data=request.POST)
            if form.is_valid():
                form.save()
                return redirect('events_registry:events')

        else:
            dj_messages.add_message(request, dj_messages.ERROR, 'Adding a new event failed',extra_tags='danger')

    context = {'form':form,'event':event}
    return render(request, 'edit_event.html',context=context)

# Clean up events from attenders who didn't check in before the selected end date and time of the event
@login_required
@permission_required('events_registry.change_event',raise_exception=True)
def clean_up_attenders(request, event_id):
    if request.method ==  'POST':
        event = get_object_or_404(Event,id=event_id)

        if (event.end_date == datetime.date(datetime.today())) and (
            event.end_time <= datetime.time(datetime.now())) :

            cleaned_up_counter = event.clean_up_attenders()
            event.save()
            if cleaned_up_counter:
                return JsonResponse(
                    {'status':'cp-up',
                    'attenders_count':event.count_attenders,
                    'arrivals_count':event.count_arrivals,
                    'message':f' {cleaned_up_counter} attender/s were removed. The page will now refresh to load the new list!',
                    'message_class':'alert alert-success'},
                    status= 200)

            # All attenders have checked in, or no attenders are in the event
            else:
                return JsonResponse(
                    {'status':'cp-nup',
                    'attenders_count':event.count_attenders,
                    'arrivals_count':event.count_arrivals,
                    'message':'Clean up was successful, but no attendees were removed.',
                    'message_class':'alert alert-warning'},
                    status= 200)

        #  The allowed time and date for cleaning up the event has not come yet
        else:
            return JsonResponse(
            {'status':'cl-f',
            'attenders_count':event.count_attenders,
            'arrivals_count':event.count_arrivals,
            'message':f"You need to wait until {event.start_date} at {event.end_time.strftime('%H:%M')} to perform this task",
            'message_class':'alert alert-danger'},
            status= 400)
