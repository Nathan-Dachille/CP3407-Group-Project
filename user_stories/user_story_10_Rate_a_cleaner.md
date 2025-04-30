# Rate a cleaner
Allow users to rate cleaners after a booking.

## Priority: 10
This was assigned a priority of 10 before iteration 1.

## Estimation: 1 day
(Estimated days before iteration 1)
* David: 1 day
* Bailey: 1 day
* Nathan: 0.5 days
* Quinn: 1.5 days

## Assumptions (if any):
* Users can only rate cleaners after a completed booking.
* Ratings will be visible on the cleaner's profile.

## Description: A rating system for users to review their cleaners.
Description-v1: A rating system for users to review their cleaners.

## Tasks:
* Design the rating system UI, 0.5 days
* Implement backend logic to store and display ratings, 0.5 days

# Related Tests
- [Test accessing ratings in profile while not signed in](https://github.com/Nathan-Dachille/CP3407-Group-Project/blob/59ba25e24b539a83ca81f7fe64136ac89dcab4b4/src/account/tests.py#L28)
  - Tests that users that are not signed in a redirected to a sign-in page.
- [Test accessing ratings as a customer](https://github.com/Nathan-Dachille/CP3407-Group-Project/blob/59ba25e24b539a83ca81f7fe64136ac89dcab4b4/src/account/tests.py#L33)
  - Tests that customer accounts can correctly view their rating and rate bookings in their profile page.
- [Test accessing ratings as a cleaner](https://github.com/Nathan-Dachille/CP3407-Group-Project/blob/59ba25e24b539a83ca81f7fe64136ac89dcab4b4/src/account/tests.py#L40)
  - Tests that cleaner accounts can correctly view their own rating and rate customers in their profile page.

# UI Design:
[Rating wireframe](wireframes/Profile_WF.drawio.svg)

# Completed:
[Rating final page (normal)](final_images/Profile_Normal.png) \
[Rating final page (phone)](final_images/Profile_Phone.png)
