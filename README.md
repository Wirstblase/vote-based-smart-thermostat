# vote-based-smart-thermostat
A project that I developed while studying at University and living with roommates. 
Our thermostat broke and we needed a fancy wireless one so I've decided to build one myself.

requirements: Wifi, internet access, a firebase project Raspberry pi pico, cheap relay module, raspberry pi [whatever] and a DHT22 temperature and humidity sensor.

main functionality:
  - temperature sensor gets mounted in the coldest room that you want to be heated
  - each of the roommates gets their own script to vote on the desired temperature
  - the thermostat gets set to the vote average
  - everyone is happy 
