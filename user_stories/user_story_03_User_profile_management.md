# User profile management
Each user/ cleaner user will be able to view their profile and update their details.

## Priority: 10
This was assigned a priority of 10 before iteration 1.

## Estimation: 3 days
(Estimated days before iteration 1)
* David: 4 day
* Bailey: 3 days
* Nathan: 2 day
* Quinn: 3 day

## Assumptions (if any):
A database table must be made for the profiles to be stored.

## Description: A web page that will allow users to view their personal details and profile information.
Description-v1: A web page that will allow users to view their personal details and profile information.

## Tasks:
* Create a profile page view, 1 day
  - Will include forms to update personal details such as password, email, phone, etc.
* Create a dashboard to house the booking details, 2 days

# UI Design:
[User profile management wireframe](wireframes/Profile_WF.drawio.svg)

# Related Tests
- [Test accessing profile page while not signed in](https://github.com/Nathan-Dachille/CP3407-Group-Project/blob/59ba25e24b539a83ca81f7fe64136ac89dcab4b4/src/account/tests.py#L28)
  - Tests that users that are not signed in a redirected to a sign-in page.
- [Test accessing profile page as a customer](https://github.com/Nathan-Dachille/CP3407-Group-Project/blob/59ba25e24b539a83ca81f7fe64136ac89dcab4b4/src/account/tests.py#L33)
  - Tests that customer accounts can correctly access their profile page.
- [Test accessing profile page as a cleaner](https://github.com/Nathan-Dachille/CP3407-Group-Project/blob/59ba25e24b539a83ca81f7fe64136ac89dcab4b4/src/account/tests.py#L40)
  - Tests that cleaner accounts can correctly access their profile page.

# Completed:
[User profile management final page (normal)](final_images/Profile_Normal.png)\
[User profile management final page (phone)](final_images/Profile_Phone.png)
