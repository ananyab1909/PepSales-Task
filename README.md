# Notification Service 

## Description

A modern microservice app for sending notifications via Email, SMS, and In-App messages — powered by Flask, Kafka, and MongoDB.

## Project Overview

This project is a scalable notification system designed to manage users and send notifications efficiently across multiple channels. It features:
  - A Flask REST API for user management and notification requests.
  - A Kafka message broker to handle asynchronous notification dispatching.
  - A Worker service that consumes Kafka messages and triggers notification delivery via email, SMS, or in-app.
  - MongoDB as the persistent store for user data and notifications.

## Functions

  - User Management: Create users with unique emails and phone numbers.
  - Notification Sending: Queue notifications (email, SMS, in-app) via Kafka.
  - Notification Processing: Worker consumes Kafka messages and dispatches notifications.
  - Retry Mechanism: Uses tenacity to retry failed notifications for better reliability.
  - Notification History: Retrieve past notifications per user from MongoDB.

## Technologies used

  - Backend: Python Flask 
  - Database: MongoDB 
  - Messaging: Apache Kafka 
  - Containerization: Docker & Docker Compose

## Prerequisites

  - Python 3.8
  - MongoDB Atlas account / local MongoDB
  - Kafka setup (handled by Docker Compose in this project)

## Implementation

1. Clone the repository
   ```
   https://github.com/ananyab1909/PepSales-Task.git
   ```

3. Enter into the directory
   ```
   cd PepSales-Task
   ```

5. Create environment config for Flask - Inside the root directory, create a .env file or edit your config.py file to include:
    ```
    MONGO_URI = "your_mongodb_connection_string"
    ```

7. Set up Docker and run the project
   ```
   docker-compose up --build
   ```

9. Access the API
     ```
     python app.py
     ```

11. Access the Kafka Consumer
     ```
     python worker.py
     ```

## User Routes

1. Register the USER -
   
   - *URL:* `/users`
   - *Method:* `POST`
   - *Request Body:*
   
     ```
     {
         "name" : "ananya",
         "email" : "ananya@gmail.com",
         "phone" : "1236889367" 
      }
     ```
   - *Response:*
     ```
     {
         "message": "User created",
         "user_id": "fe0e5082-d561-4b41-b4de-aed24b0d7ed1"
      }
     ```

3. Send Notifications

   - *URL:* `/notifications`
   - *METHOD:* `POST`
   - *Request Body:*
   
     TYPE I : SMS Services
     ```
       {
           "type" : "sms",
           "recipient" : "1236889367",
           "message" : "sms success" 
        }
     ```
     
     TYPE II : Email Services
     ```
       {
           "type" : "email",
           "recipient" : "ananya@gmail.com",
           "message" : "email success" 
        }
     ```
     TYPE III : In-App Services
      ```
        {
            "type" : "inapp",
            "recipient" : "fe0e5082-d561-4b41-b4de-aed24b0d7ed1",
            "message" : "inapp success" 
        }
      ```

    - *Response:*
    
      TYPE I : SMS Services
      ```
        {
            "status": "sms notification queued"
        }
      ```
      
      TYPE II : Email Services
      ```
        {
            "status": "email notification queued"
        }
      ```
    
      TYPE III : In-App Services
      ```
        {
            "status": "inapp notification queued"
        }
      ```
  
    - *Queue responses:*
    
      TYPE I : SMS Services
      ```
        Found user with ID: fe0e5082-d561-4b41-b4de-aed24b0d7ed1
        Sending SMS to user_id=fe0e5082-d561-4b41-b4de-aed24b0d7ed1
        Sending SMS to fe0e5082-d561-4b41-b4de-aed24b0d7ed1: sms success
        SMS notification stored in DB.
      ```
  
      TYPE II : Email Services
      ```
        Found user with ID: fe0e5082-d561-4b41-b4de-aed24b0d7ed1
        Sending email to user_id=fe0e5082-d561-4b41-b4de-aed24b0d7ed1
        Sending EMAIL to fe0e5082-d561-4b41-b4de-aed24b0d7ed1: email success     
        Email notification stored in DB.
      ```
    
      TYPE III : In-App Services
      ```
        Found user with ID: fe0e5082-d561-4b41-b4de-aed24b0d7ed1
        Storing in-app notification for user_id=fe0e5082-d561-4b41-b4de-aed24b0d7ed1
        Storing IN-APP notification for fe0e5082-d561-4b41-b4de-aed24b0d7ed1: inapp success
        In-app notification stored in DB.
      ```
      
  4. Get user notifications
     
     - *URL:* `/users/<user_id>/notifications` (using /users/fe0e5082-d561-4b41-b4de-aed24b0d7ed1/notifications)
     - *METHOD:* `GET`
     - *Response:*
     ```
       [
      	  {
        		"type": "inapp",
        		"message": "inapp success"
        	},
        	{
      		"type": "email",
      		"message": "email success"
      	},
      	{
      		"type": "sms",
      		"message": "sms success"
      	}
      ]
     ```
## About Me

Hello, my name is Ananya Biswas. I am an Engineering Student at [Kalinga Institute of Industrial Technology](https://kiit.ac.in/). I enjoy making projects and now that my this project is over, I am open-sourcing the project. Hope you like it! Lastly, I would like to put it out there that I have worked on other projects that you may like. You can check them out at my [Github](https://github.com/ananyab1909/). Give it a whirl and let me know your thoughts.

## Socials
  - Portfolio : https://dub.sh/ananyabiswas
  - LinkedIn : https://linkedin.com/in/ananya-biswas-kiit/
  - Mastodon : https://mastodon.social/@captain_obvious/
  - Twitter : https://x.com/not_average_x/
  - Github : https://github.com/ananyab1909/
