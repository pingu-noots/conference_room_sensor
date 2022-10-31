# Human sensor for conference room
You can be notified by slack about availability　of conference room!
## enviroment
Hard -> Raspberry Pi zero WH
snesor -> HC-SR501
## How to use
1. Get incoming webhook url slack
2. Write your API　on 
> YOUR API
3. run
> python3 conference_room_sensor.py
## Specification
If sensor senses, you can be notified by slack only once while sensor has no sense for 10m.
If sensor has no sense for 10m, you can be notified about that conference room is available.
Sensor senses After sent notification about available, it notify again.
