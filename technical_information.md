# Technical Information for Cleaning Website

## Development Tools
 - The main development tool used for this project is [Django](https://www.djangoproject.com/).
 - Then for the deployment of the site [AWS Elastic Beanstalk](https://aws.amazon.com/elasticbeanstalk/) was used.
 - The data for the website is stored in a MySQL database.

## Deployment Information
The continuous deployment is ran from the deploy.yml workflow in the .github folder.
It uses the following process:

### Process
- The workflow is triggered when files are merged to main.
- The src folder is cloned by the GitHub action.
- A Python environment is created with the dependancies in requirements.txt.
- The static files are collected into a separate folder.
- The source code and staticfiles are compressed into a zip file.
- The zip file is uploaded to an S3 Bucket.
- Then we use the AWS CLI to create a new application version in Elastic Beanstalk.
- Finally, the current environment is updated to the new application version.

## UML Class Diagram
Below is a UML Class Diagram of the website, the rounded boxes are the names of the python modules.

![UML Class Diagram](Cleaning_Site_UML.svg)

## ERD for the Database
Below is an ERD of the MySQL database.

![ERD of Database](Cleaning_Site_ERD.svg)

