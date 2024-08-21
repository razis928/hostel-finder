from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class HostelOwner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='owner_pics/', blank=True, null=True)
    
    def __str__(self):
        return f'{self.user.username} - {self.phone_number}'

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to='customer_pics/', blank=True, null=True)
    
    def __str__(self):
        return self.user.username

class Hostel(models.Model):
    owner = models.ForeignKey(HostelOwner, on_delete=models.CASCADE, related_name='hostels')
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    area = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='hostel_images/', blank=True, null=True)
    image_1 = models.ImageField(upload_to='hostel_images/', blank=True, null=True)
    image_2 = models.ImageField(upload_to='hostel_images/', blank=True, null=True)
    image_3 = models.ImageField(upload_to='hostel_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Room(models.Model):
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, related_name='rooms')
    room_type = models.CharField(max_length=100, choices=[('Single', 'Single'), ('Double', 'Double'), ('Dorm', 'Dorm')])
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=True)
    capacity = models.IntegerField(help_text="Number of people the room can accommodate")
    room_image = models.ImageField(upload_to='room_images/', blank=True, null=True)

    def __str__(self):
        return f'{self.room_type} - {self.hostel.name}'

class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='bookings')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bookings')
    check_in = models.DateField()
    check_out = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False)
    expired = models.BooleanField(default=False)

    class Meta:
        unique_together = ('room', 'check_in', 'check_out')

    def calculate_total_price(self):
        duration = (self.check_out - self.check_in).days
        return self.room.price_per_night * duration
    
    def save(self, *args, **kwargs):
        self.total_price = self.calculate_total_price()
        self.expired = self.check_out < timezone.now().date()
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        return self.check_out < timezone.now().date()
    
    def __str__(self):
        return f'Booking by {self.customer.user.username} for {self.room.hostel.name} from {self.check_in} to {self.check_out}'

class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.subject
