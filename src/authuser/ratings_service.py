from django.apps import apps


def update_user_rating(user):
    # Use `apps.get_model` to dynamically get the Booking model
    Booking = apps.get_model('bookings', 'Booking')  # Dynamically get the 'Booking' model from 'bookings' app

    # Check if the user is a customer or a cleaner
    if user.role == user.Role.CLEANER:
        # Get all ratings where this user is assigned as the cleaner
        bookings = Booking.objects.filter(assigned=user)
        ratings = [booking.cleaner_rating for booking in bookings if booking.cleaner_rating is not None]
    elif user.role == user.Role.CUSTOMER:
        # Get all ratings where this user is the customer
        bookings = Booking.objects.filter(user=user)
        ratings = [booking.customer_rating for booking in bookings if booking.customer_rating is not None]
    else:
        ratings = []

    if ratings:
        # Calculate the average rating and round it
        average_rating = sum(ratings) / len(ratings)
        user.rating = round(average_rating)  # Round to the nearest integer
    else:
        user.rating = None  # No ratings available, so set to None

    user.save()  # Save the updated rating back to the User model