# Actual iteration-2 board, (see chapters 3 and 4), Start: 11/03/2025, End: 10/04/2025

* Assumed Velocity FROM iteration-1: 0.4
* Number of developers: 4
* Total estimated amount of work: 6

### User stories or tasks (see chapter 4):

* [Bookings calendar](./user_stories/user_story_08_Bookings_calendar.md), priority 10, 4 days
* [Rate a cleaner](./user_stories/user_story_10_Rate_a_cleaner.md), priority 10, 1 day

Continued from iteration 1:

* [Accept a booking](./user_stories/user_story_02_Accept_a_booking.md)
  * how cleaner booking requests, 0.5 days
  * Assign cleaner to the booking request if it's accepted, 0.5 days
* [User profile management](./user_stories/user_story_03_User_profile_management.md)
  * Create a profile page view, 1 day
  * Create a dashboard to house the booking details, 2 days
* [Account Creation](./user_stories/user_story_03_User_profile_management.md)
  * Create custom user model in Django to store account type and key details, 0.75 days

### In progress:

### Completed:

**Accept a booking**
* Show cleaner booking requests, 0.5 days, Quinn, End Date: 08/04/2025
* Assign cleaner to the booking request if it's accepted, 0.5 days, Quinn, End Date: 08/04/2025

**Bookings calendar**
* Design the calendar interface, 2 days, Quinn, End Date: 08/04/2025
* Implement the booking and availability tracking logic, 2 days, Quinn, End Date: 08/04/2025

**Rate a cleaner**
* Design the rating system UI, 0.5 days, Quinn, End Date: 08/04/2025
* Implement backend logic to store and display ratings, 0.5 days, Quinn, End Date: 08/04/2025

**User profile management**
* Create a profile page view, 1 day, Quinn, End Date: 30/03/2025
* Create a dashboard to house the booking details, 2 days, Bailey, End Date: 30/03/2025

**Account Creation**
* Create custom user model in Django to store account type and key details, 0.75 days, David, End Date: 23/03/2025

**Setup Continuous Deployment**
* Setup continuous deployment with AWS and github actions, 2 days, Nathan, End Date: 10/04/2025

### Burn Down for iteration-2 (see chapter 4):
Update this at least once per week
* 4 weeks left, 6 days of estimated amount of work 
* 2 weeks left, 5.25 days
* 1 weeks left, 2.25 days
* 0 weeks left, -5.75 days
* Actual Velocity:  1.5

A lot of the tasks that were not finished in iteration 1 rolled over to iteration 2, meaning that we ended
up with a very large iteration 2 actual velocity. Despite this, this is not 100% indicative of the actual velocity 
of the team. If the project were continued for a longer number of iterations this oscillation between small and large
velocities would shallow out and the predictions would become more accurate.