# Smart Weight Tracker with Google Home Actions

## Why
Recently I started my journey towards a healthy life and started working out for loosing weight. Everyday at the gym, I would stand on a weighing scale
for measuring weight and check if things are changing or not. Somedays i would miss the gym and somedays i simply forgot to use the scale. It became very difficult to keep track of my weight and somewhere my motivation kept going downwards. Due to Gym timing restrictions and work, i started missing the gym sessions so I decided to start my workout at home. To keep track of my weight I thought about ordering a weighing scale. There were multiple options of smart scalers which could provide you insights about your weight change journey. I was already looking to invest sometime in improving my python skills so i decided to purchase a simple weighing scale and build a tracker on my own. 
We had a google home at home and interacting with it is quite fun. The thought og Building something that works on voice commands sounded interesting and hence this project came up in my mind.



## What
This is a python based API used as backend (also called as Fullfilment in google terms) to fullfill intentins triggered by user's voice commands.
This project is in phase one where I have created 3 functionalities
1) Asking google home to log your current weight as and when you measure it
2) Asking google home to check your last logged weight
3) Asking google home to calculate if you have lost/gained weight in last 7 or 30 days

## Tech Stack
1) Language : API is written in python v3
2) Databse : Using mongoDB atlas for storing user data
3) Platform : Deployed it on AWS lambda using serverless framework
4) AWS Services involved :  API Gateway, Route53, Secrets manager and Lambda

## Diagram deplocting flow between google home device, api and the database
https://developers.google.com/assistant/identity/oauth-concept-guide


![Image description](.resources/smart_weight_tracker.png)
