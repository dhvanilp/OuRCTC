# Pseudo-RCTC

## Introduction

The Indian Railways (IR) carries about 5.5 lakhs passengers in reserved accommodation every day. The Computerised Passenger Reservation System (PRS) facilitates the booking and cancellation of tickets from any of the 4000 terminals (i.e. PRS booking window all over the countries). These tickets can be booked or cancelled for journeys commencing in any part of India and ending in any other part, with travel time as long as 72 hours and distance up to several thousand kilometres.

In the given project we will be developing a SQL Database which will help users to find train details, enquire about trains running between given two stations, book tickets and know the exact rates of their tickets to the desired destination. 



## Implementaion Details

- Users have a unique serial number (SN) used as primary key, name, email, phone, and adminship(decides if the user is an admin or not).

- Each station has a unique serial number(PK) and station name.

- All routes across the country are present here, each is identified by a serial number and the station which it passes through. One route contains more than one station.

- Train entries have a unique train number(PK), name, source, destination, route, number of seats available, start time and end time. One train runs only on one route and has a single sou+rce and destination stations.

- Booking details of each ticket contain a unique serial number, user who booked the ticket, train for which the ticket is booked, user’s departure and arrival station. One user may have more than one tickets also many tickets can be booked for the same train. Each ticket can have only one departure and one arrival stations.

- Each region has a unique serial number(PK), name and the stations which fall under that region. One region may have more than one station.

## Project Images

### 1. Login Form
<div align="center">
  <img src="https://raw.githubusercontent.com/DhvanilP/OuRCTC/master/im1.png" />
</div>

### 2. SignUp Form
<div align="center">
  <img src="https://raw.githubusercontent.com/DhvanilP/OuRCTC/master/im2.png" />
</div>

### 3. Home Page
<div align="center">
  <img src="https://raw.githubusercontent.com/DhvanilP/OuRCTC/master/im3.png" />
</div>

### 4. Select From Map
<div align="center">
  <img src="https://raw.githubusercontent.com/DhvanilP/OuRCTC/master/im4.png" />
</div>

# 5. Display Trains
<div align="center">
  <img src="https://raw.githubusercontent.com/DhvanilP/OuRCTC/master/im5.png" />
</div>

### 6. Display Available Seats
<div align="center">
  <img src="https://raw.githubusercontent.com/DhvanilP/OuRCTC/master/im6.png" />
</div>

### 7. Display Connecting Trains
<div align="center">
  <img src="https://raw.githubusercontent.com/DhvanilP/OuRCTC/master/im7.png" />
</div>

### 8. Booked Ticket History
<div align="center">
  <img src="https://raw.githubusercontent.com/DhvanilP/OuRCTC/master/im8.png" />
</div>

## Team Members
* [Suyash Ghuge](https://github.com/suyash0103), 16IT114
* [Nishant Kumar](https://github.com/NishantKr97),16IT123
* [Shreyas Shankar](https://github.com/shrey920), 16IT138
* [Dhvanil Parikh](https://github.com/DhvanilP), 16IT217
