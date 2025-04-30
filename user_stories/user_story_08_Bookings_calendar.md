# Bookings calendar
Provide a calendar view for users and cleaners to manage bookings.

## Priority: 10
This was assigned a priority of 10 before iteration 1.

## Estimation: 4 days
(Estimated days before iteration 1)
* David: 4 days
* Bailey: 3.5 days
* Nathan: 4 days
* Quinn: 4.5 days

## Assumptions (if any):
* Users and cleaners should have separate views of the calendar.
* Cleaners should be able to mark availability.

## Description: A calendar that helps users and cleaners manage bookings.
Description-v1: A calendar that helps users and cleaners manage bookings.

## Tasks:
* Design the calendar interface, 2 days
* Implement the booking and availability tracking logic, 2 days

# UI Design:
[Bookings calendar wireframe](wireframes/Profile_WF.drawio.svg)

# Related Tests:
- [Test accessing booking calendar while not signed in](https://github.com/Nathan-Dachille/CP3407-Group-Project/blob/59ba25e24b539a83ca81f7fe64136ac89dcab4b4/src/account/tests.py#L28)
  - Tests that users that are not signed in a redirected to a sign-in page.
- [Test accessing booking calendar as a customer](https://github.com/Nathan-Dachille/CP3407-Group-Project/blob/59ba25e24b539a83ca81f7fe64136ac89dcab4b4/src/account/tests.py#L33)
  - Tests that customer accounts can correctly access their booking calendar in their profile page.
- [Test accessing booking calendar as a cleaner](https://github.com/Nathan-Dachille/CP3407-Group-Project/blob/59ba25e24b539a83ca81f7fe64136ac89dcab4b4/src/account/tests.py#L40)
  - Tests that cleaner accounts can correctly access their booking calendar in their profile page.

# Completed:
[Bookings calendar final page](final_images/Bookings_Calendar.svg)

NOTE: The booking calendar system will only be accessible once a user [signs in or creates an account](user_story_12_Account_creation.md)

NOTE: If the image is hard to see, please download and view in a separate tab for a higher resolution.