from django.contrib import admin

from .models import ContactMessage, Donation, LiveRoom, Review, Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'active')
    list_filter = ('active',)
    search_fields = ('name', 'description')


@admin.register(LiveRoom)
class LiveRoomAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'room_type', 'host_name', 'scheduled_at', 'is_open')
    list_filter = ('room_type', 'is_open', 'subject')
    search_fields = ('title', 'host_name', 'description')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'rating', 'subject', 'created_at')
    list_filter = ('rating',)
    search_fields = ('author_name', 'subject', 'message')


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'amount', 'created_at')
    search_fields = ('name', 'email', 'message')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')

