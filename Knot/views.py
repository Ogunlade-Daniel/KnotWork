from django.contrib import messages
from django.shortcuts import redirect, render

from .models import ContactMessage, Donation, LiveRoom, Review, Subject


def home(request):
    subjects = Subject.objects.filter(active=True)[:6]
    featured_rooms = LiveRoom.objects.filter(is_open=True).order_by('-scheduled_at')[:4]
    reviews = Review.objects.all()[:4]
    return render(request, 'Knot/index.html', {
        'subjects': subjects,
        'featured_rooms': featured_rooms,
        'reviews': reviews,
    })


def about(request):
    return render(request, 'Knot/about.html')


def contact(request):
    if request.method == 'POST':
        ContactMessage.objects.create(
            name=request.POST.get('name', '').strip(),
            email=request.POST.get('email', '').strip(),
            subject=request.POST.get('subject', '').strip(),
            message=request.POST.get('message', '').strip(),
        )
        messages.success(request, 'Thanks for reaching out! We received your message.')
        return redirect('contact')

    return render(request, 'Knot/contact.html')


def live_rooms(request):
    rooms = LiveRoom.objects.filter(is_open=True).order_by('-scheduled_at')
    return render(request, 'Knot/live_rooms.html', {'rooms': rooms})


def donations(request):
    if request.method == 'POST':
        amount_value = request.POST.get('amount', '0').strip()
        try:
            amount = float(amount_value)
            if amount <= 0:
                raise ValueError('Donation amount must be greater than zero.')
        except (ValueError, TypeError):
            messages.error(request, 'Please enter a valid donation amount.')
            return redirect('donations')

        Donation.objects.create(
            name=request.POST.get('name', '').strip(),
            email=request.POST.get('email', '').strip(),
            amount=amount,
            message=request.POST.get('message', '').strip(),
        )
        messages.success(request, 'Thank you for supporting Knotwork!')
        return redirect('donations')

    return render(request, 'Knot/donations.html')


def reviews(request):
    if request.method == 'POST':
        rating_value = request.POST.get('rating', '5').strip()
        try:
            rating = min(max(int(rating_value), 1), 5)
        except (ValueError, TypeError):
            rating = 5

        Review.objects.create(
            user=request.user if request.user.is_authenticated else None,
            author_name=request.POST.get('name', 'Anonymous').strip() or 'Anonymous',
            rating=rating,
            subject=request.POST.get('subject', '').strip(),
            message=request.POST.get('message', '').strip(),
        )
        messages.success(request, 'Your review is published. Thank you!')
        return redirect('reviews')

    reviews_list = Review.objects.all()[:20]
    return render(request, 'Knot/reviews.html', {'reviews': reviews_list})

