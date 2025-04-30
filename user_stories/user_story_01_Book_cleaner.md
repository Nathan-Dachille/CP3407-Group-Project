# Book cleaner
Allow users to make a booking.

## Priority: 10
This was assigned a priority of 10 before iteration 1.

## Estimation: 2 days
(Estimated days before iteration 1)
* David: 2 day
* Bailey: 1 days
* Nathan: 2 day
* Quinn: 3 day

## Assumptions (if any):
* A database table will have to be made for the bookings to be stored

## Description: A web page that will allow users to make a booking for a cleaner that is available in their area.
Description-v1: A web page that will allow users to make a booking for a cleaner that is available in their area.

## Tasks:
* Create a booking page view (Customers can book cleans), 1 day
    - Customer can select day for clean on calendar, they may then be presented with a list of cleaners
    - It will look up their area from their profile and compare to serviced area for cleaner
* Create a booking model, 1 days

# UI Design:
[Book cleaner wireframe](wireframes/Booking_WF.png)

# Related Tests:
- [Create a booking and test the booking string](https://github.com/Nathan-Dachille/CP3407-Group-Project/blob/038d723a8cbeb57250d82e70aef7724d1fb832b1/src/bookings/tests.py#L40)
  - Tests that a booking object can be created and that the string method is functioning correctly.
- [Test accessing the booking page while not signed in](https://github.com/Nathan-Dachille/CP3407-Group-Project/blob/038d723a8cbeb57250d82e70aef7724d1fb832b1/src/bookings/tests.py#L47)
  - Tests that the user gets redirected to a sign in page.
- [Test accessing the booking page while signed in as a cleaner](https://github.com/Nathan-Dachille/CP3407-Group-Project/blob/038d723a8cbeb57250d82e70aef7724d1fb832b1/src/bookings/tests.py#L52)
  - Test that cleaners are redirected to their booking management page.
- [Test accessing the booking page while signed in a a customer](https://github.com/Nathan-Dachille/CP3407-Group-Project/blob/038d723a8cbeb57250d82e70aef7724d1fb832b1/src/bookings/tests.py#L58)
  - Checks that the correct page is served to the customer and that there are no errors.

# Completed:
[Book cleaner final page](final_images/Booking.svg)

NOTE: If the image is hard to see, please download and view in a separate tab for a higher resolution.

