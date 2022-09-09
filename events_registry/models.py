from django.db import models
from django.contrib.postgres.fields import ArrayField

from users.models import Member

class Event(models.Model):
    name = models.CharField(max_length=24, blank=False)
    start_date = models.DateField(blank=False)
    start_time = models.TimeField(blank=False)
    end_date = models.DateField(blank=False)
    end_time = models.TimeField(blank=False)
    max_number_of_participants = models.IntegerField(blank=False)
    attenders = ArrayField(base_field=models.IntegerField(blank=True),blank=True,null=None,default=list)
    arrivals = ArrayField(base_field=models.IntegerField(blank=True),blank=True,null=True,default=list)
    seats = models.JSONField(default=dict, blank=True, null=True)

    @property
    def count_attenders(self):
        return len(self.attenders)

    @property
    def count_arrivals(self):
        return len(self.arrivals)

    @property
    def get_attenders(self):
        attenders = Member.objects.filter(pk__in=self.attenders)
        return attenders

    @property
    def get_max_attenders_number(self):
        return self.max_number_of_participants

    def add_attender(self, member_id):
        if member_id in self.attenders:
            pass
        else:
            self.attenders.append(member_id)

    def remove_attender(self, member_id):
        self.attenders.remove(member_id)
 
    def has_attender(self, member_id):
        if member_id in self.attenders:
            return True
        else:
            return False
    
    def add_arrival(self, member_id):
        self.arrivals.append(member_id)

    def remove_arrival(self, member_id):
        self.arrivals.remove(member_id)
 
    def has_arrival(self, member_id):
        if member_id in self.arrivals:
            return True
        else:
            return False

    def clean_up_attenders(self):
        clean_up_counter = 0
        for attender_id in set(self.attenders):
            if attender_id not in self.arrivals:
                self.attenders.remove(attender_id)
                clean_up_counter += 1
                        
        return clean_up_counter

    
    def give_seat(self, member_id):
        # For old created events with no seats
        dict(self.seats)
        try:
            for seat_number in range(1, self.count_arrivals+1):
                if seat_number not in self.seats.values():
                    self.seats[str(member_id)] = seat_number
                    break
        except:
            raise Exception(f"An error accourd while giving a member with {member_id} a seat")

    def remove_seat(self, member_id):
        try:
            self.seats.pop(str(member_id))
        except:
            raise Exception(f"Can't remove seat for member {member_id}")


    def get_seat(self, member_id):
        try:
            return self.seats.get(str(member_id))

        except:
            raise Exception(f"Can't get the seat number for member {member_id}")

    @property
    def get_seats(self):
        return self.seats


    @property
    def is_fully_booked(self):
        if self.count_attenders == self.get_max_attenders_number:
            return True
        else:
            return False



    def __str__(self):
        return self.name

     

    