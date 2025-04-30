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

# UI Design:
[Rating wireframe](wireframes/Profile_WF.drawio.svg)

# Related Tests:
- [Test accessing ratings in profile while not signed in](https://github.com/Nathan-Dachille/CP3407-Group-Project/blob/59ba25e24b539a83ca81f7fe64136ac89dcab4b4/src/account/tests.py#L28)
  - Tests that users that are not signed in a redirected to a sign-in page.
- [Test accessing ratings as a customer](https://github.com/Nathan-Dachille/CP3407-Group-Project/blob/59ba25e24b539a83ca81f7fe64136ac89dcab4b4/src/account/tests.py#L33)
  - Tests that customer accounts can correctly view their rating and rate bookings in their profile page.
- [Test accessing ratings as a cleaner](https://github.com/Nathan-Dachille/CP3407-Group-Project/blob/59ba25e24b539a83ca81f7fe64136ac89dcab4b4/src/account/tests.py#L40)
  - Tests that cleaner accounts can correctly view their own rating and rate customers in their profile page.

# Completed:
[Rating final page](final_images/Rate_a_Cleaner.svg)

NOTE: The rating system will only be accessible once a user [signs in or creates an account](user_story_12_Account_creation.md).
When rating a cleaner the user must be signed in with a customer account. They must have also made a [booking](user_story_01_Book_cleaner.md) with that cleaner in order to rate them.

NOTE: If the image is hard to see, please download and view in a separate tab for a higher resolution.
