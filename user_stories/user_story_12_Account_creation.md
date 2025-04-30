# User story title: Account creation
User authentication, sign in and registration. Storing of key user details.

## Priority: 10

## Estimation: 2 days
(Estimated days before iteration 1)
* David: 2 day
* Bailey: 2 days
* Nathan: 1 day
* Quinn: 2 day

## Assumptions (if any):
* The account creation should include creation of a database table/system to store the account.
* Create a basic home/landing page to link to the account creation.

## Description: Web pages that will allow the user to create an account and sign in
Description-v1: Web pages that will allow the user to create an account and sign in

## Tasks, see chapter 4.
* Create sign up page view, 0.5 days
* Create sign in page view, 0.5 days
* Create home page view, 0.25 days
* Create custom user model in Django to store account type and key details, 0.75 days

# UI Design:
[Register account wireframe](wireframes/Registration_WF.png)\
[Sign in account wireframe](wireframes/Sign_In_WF.png)

# Related Tests:
- [Test sign-in page](https://github.com/Nathan-Dachille/CP3407-Group-Project/blob/038d723a8cbeb57250d82e70aef7724d1fb832b1/src/authuser/tests.py#L28)
  - Tests that users can access the sign-in page.
- [Test register page](https://github.com/Nathan-Dachille/CP3407-Group-Project/blob/038d723a8cbeb57250d82e70aef7724d1fb832b1/src/authuser/tests.py#L34)
  - Tests that users can access the registration page.
- [Test custom phone number validation](https://github.com/Nathan-Dachille/CP3407-Group-Project/blob/038d723a8cbeb57250d82e70aef7724d1fb832b1/src/authuser/tests.py#L21)
  - Test the custom phone number validator only allows valid phone numbers.

****

# Completed:
[Register account final page](final_images/Register.svg)\
[Sign in account final page](final_images/Sign_In.svg)

NOTE: If the image is hard to see, please download and view in a separate tab for a higher resolution.

