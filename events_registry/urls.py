from django.urls import path, include
from . import views


app_name = "events_registry"

urlpatterns = [
    path('', views.index,name="index"),
    path('events/',views.events,name='events'),
    path('new_event',views.new_event,name='new_event'),
    # path('event/<int:event_id>/', views.event,name="event"),
    path('edit_event/<int:event_id>/',views.edit_event,name="edit_event"),
    path('event/<int:event_id>/register/',views.register,name="register"),
    path('event/<int:event_id>/unregister/',views.unregister,name="unregister"),
    path('event/<int:event_id>/monitor/',views.monitor,name='monitor'),
    path('event/<int:event_id>/check_in/',views.check_in,name="check_in"),
    path('event/<int:event_id>/check_out/',views.check_out,name="check_out"),
    path('event/<int:event_id>/clean_up_attenders/',views.clean_up_attenders,name="clean_up_attenders"),

]
