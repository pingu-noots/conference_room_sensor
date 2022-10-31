from datetime import datetime
import time
import RPi.GPIO as GPIO
import json
import urllib.request
import logging
from collections import OrderedDict
import pprint

# if sense
SLEEP = 20
# use this GPIO
GPIO_PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN, GPIO.IN)

def post_slack(flg, msg):
  if (flg == "sense"):
    message = msg + " に人を感知\n会議室は使用中です"
  elif (flg == "10m"):
    message = msg + " 10分間の人感知なし\n会議室は空室です"
  send_data = {
    "text": message,
  }
  send_text = json.dumps(send_data)
  request = urllib.request.Request(
    "YOUR API", 
    data=send_text.encode('utf-8'), 
    method="POST"
  )
  with urllib.request.urlopen(request) as response:
    response_body = response.read().decode('utf-8')

if __name__ == '__main__':
  try:
    start_timer = time.time()
    posted_sense = 0
    posted_10m = 0
    while True:
      if(GPIO.input(GPIO_PIN) == GPIO.HIGH and posted_sense == 0):
        sensing_date = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        post_slack("sense" ,sensing_date)
        print("Sensing! POST request was sent to slack.")
        start_timer = time.time()
        posted_sense = 1
        posted_10m = 0
        time.sleep(SLEEP)
      # No sensing 10m
      elif (60 * 10 <= time.time() - start_timer and posted_10m == 0):
        sensing_date = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        post_slack("10m", sensing_date)
        print("No sensing in 10m. POST request was sent to slack.")  
        posted_10m = 1
        posted_sense = 0
      else:
        print(time.time() - start_timer)
        time.sleep(5)

  except KeyboardInterrupt:
    print("suspending a process")

  finally:
    GPIO.cleanup()
    print("GPIO clean complete")
