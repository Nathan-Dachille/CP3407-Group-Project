# Rescheduling bookings
Allow users to reschedule their bookings.

## Priority: 20
This was assigned a priority of 20 before iteration 1.

## Estimation: 2 days
(Estimated days before iteration 1)
* David: 2 days
* Bailey: 2.5 days
* Nathan: 1.5 days
* Quinn: 2 days

## Assumptions (if any):
* Users must reschedule within a certain timeframe.
* Cleaners must be notified of any rescheduled bookings.

## Description: A system that allows users to reschedule their bookings easily.
Description-v1: A system that allows users to reschedule their bookings easily.

## Tasks:
* Develop a rescheduling interface for users, 1 day
* Notify cleaners of rescheduled bookings via email or dashboard alerts, 1 day (This task was not completed)

# UI Design:
[Rescheduling bookings wireframe](wireframes/Profile_WF.drawio.svg)

# Related Tests:
- [Test accessing profile page while not signed in](https://github.com/Nathan-Dachille/CP3407-Group-Project/blob/59ba25e24b539a83ca81f7fe64136ac89dcab4b4/src/account/tests.py#L28)
  - Tests that users that are not signed in a redirected to a sign-in page.
- [Test accessing profile page as a customer](https://github.com/Nathan-Dachille/CP3407-Group-Project/blob/59ba25e24b539a83ca81f7fe64136ac89dcab4b4/src/account/tests.py#L33)
  - Tests that customer accounts can correctly access timetable to reschedule.
- [Test accessing profile page as a cleaner](https://github.com/Nathan-Dachille/CP3407-Group-Project/blob/59ba25e24b539a83ca81f7fe64136ac89dcab4b4/src/account/tests.py#L40)
  - Tests that cleaner accounts can correctly access timetable to reschedule.

# Completed:
[Rescheduling as a cleaner final page](final_images/Reschedule_Cleaner.svg)

NOTE: The rescheduling system will only be accessible once a user [signs in or creates an account](user_story_12_Account_creation.md). It also uses the [calendar](user_story_08_Bookings_calendar.md) functionality.

NOTE: If the image is hard to see, please download and view in a separate tab for a higher resolution.