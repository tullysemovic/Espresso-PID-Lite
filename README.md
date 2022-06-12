# Espresso-PID
A web-based PID controller primarily aimed for controlling espresso machines. In my case: the Gaggia Classic Pro

![Main Dashboard](https://github.com/tsemovic/Espresso-PID/blob/main/images/theme5.jpg?raw=true)


## Why 
The most popular entry-level espresso machines such as the Gaggia Classic Pro and the Rancilio Silvia don't come with a PID. Installing a PID is one of the best upgrades to pull consistent shots and avoid temp-surfing. 

There are many hardware-based PID controllers designed for espresso machines but the kits usually cost around $200. I wanted a more affordable solution to this so I went with the software route. There are also many different web-app controlled PID's but I wanted to create my own as other dashboards weren't very appealing and lacked customisation.


## Built With
The front-end of the app is built on [Vue 3](https://vuejs.org/guide/introduction.html) with the [Quasar](https://quasar.dev/) framework. The back-end server for this app is built using [Python](https://www.python.org/) and [Flask](https://flask.palletsprojects.com/en/2.1.x/). The front-end and back-end communicate using [socketio](https://socket.io/)


## Requirements
| Component | Cost (AUD) | Notes |
| ------ | ------ | ------ |
| [MAX31855 Breakout Board](https://www.amazon.com.au/JulyCrab-Thermocouple-Temperature-Controller-Interface/dp/B09VPP79QQ/ref=sr_1_14?crid=2XNNMTMY603P1&keywords=max31855&qid=1651638270&refresh=1&sprefix=max3185%2Caps%2C257&sr=8-14) | $15 |
| [K-Type thermocouple probe](https://www.amazon.com.au/uxcell%C2%AE-Thermocouple-Temperature-Sensor-Printer/dp/B07MGJX5N5/ref=sr_1_6?crid=2RKLQZEV7ZHWZ&keywords=k-type+thermocouple+m4&qid=1651638706&sprefix=k-type+thermocouple+m%2Caps%2C263&sr=8-6) | $15 | The GCP uses an m4 thread screw so I got the same one in the link, you may need to get a different probe depending on your machine |
| [Solid State Relay (SSR)](https://www.amazon.com.au/SSR-100DD-Module-Control-Voltage-Industrial/dp/B08F54DX5V/ref=sr_1_1_sspa?crid=1HSW8FYWP52UM&keywords=SSR&qid=1651638725&sprefix=ssr%2Caps%2C266&sr=8-1-spons&psc=1&smid=AILSKCC2Q2KS0&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEzU09QWjJJVzNLWlBCJmVuY3J5cHRlZElkPUEwNDcyNDk3MzY1NE5HU1FPRTBaVyZlbmNyeXB0ZWRBZElkPUExVDhaV0FXTVpKREhRJndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ==) | $25 |
| High Temp rated wire | $10 | Silicone wire rated for ***high-temperature*** at 14 gauge or lower (I used 12 gauge) |
| [Single-Board Computer (Raspberry Pi)](https://core-electronics.com.au/raspberry-pi-3-model-b-plus.html) | $60 | I had a spare Raspberry Pi 3b+ so my total cost was much lower as this is the most expensive part of the build |
| Total | ~$120 | ~$60 if you already have an SBC


## Hardware Installation
This is how all of the components should be physically connected together (wire colours may vary depending on the model and region of the machine)
![Wiring Diagram](https://github.com/tsemovic/Espresso-PID/blob/main/images/wiringDiagramGCP.jpg?raw=true)

Here is a more colourful diagram

![Wiring Diagram](https://github.com/tsemovic/Espresso-PID/blob/main/images/System%20Diagram.jpg?raw=true)


## Software Installation
### Docker
This espresso PID is very easy to install and deploy in a Docker container.

By default, this app runs on port 5000, so change this within the
Dockerfile if necessary. This app must be run in privileged mode to work correctly

docker-compose:
```sh
---
version: "2.1"
services:
  espresso-pid:
    image: tsemovic/espresso-pid:latest
    container_name: espresso-pid
    ports:
      - 80:5000
    restart: unless-stopped
    privileged: true
```

### Manual Install
1. Download & extract this repository
2. Navigate to the /server folder in your terminal
2. Run ```pip install -r requirements.txt```
3. Run ```sudo python run.py``` from inside the main /server folder

## Usage 
Click the settings button to configure the PID parameters and the target temperature
![Settings Dashboard](https://github.com/tsemovic/Espresso-PID/blob/main/images/theme5_settings.jpg?raw=true)

## Theming
This app allows you to fully customise the colours and images used for that personalised touch

To do this you will need to edit the ```settings_global.json``` file
![Settings Configuration](https://github.com/tsemovic/Espresso-PID/blob/main/images/config.jpg?raw=true)

To change the background image you will need to set ```BACKGROUND_IMAGE``` to ```true``` and then replace the background image at ```server/dist/static/img/background.xyz.jpg```. Be sure to keep the same file the same as the template image already in there.

To change the colours used throughout the app you will need to change ```VUE_COLOUR``` section
| Name | Region |
| --- | --- |
| primary | Main heading |
| secondary | Info card headings |
| accent | Graph line |
| dark | Graph card background |
| positive | Settings Button |
| negative | Main background colour (only used if ```BACKGROUND_IMAGE``` is ```false```)
| info | Info card sub-heading |
| warning | Info card |


### Theme examples
![Theme 1](https://github.com/tsemovic/Espresso-PID/blob/main/images/theme1.jpg?raw=true)
![Theme 4](https://github.com/tsemovic/Espresso-PID/blob/main/images/theme4.jpg?raw=true)
![Theme 2](https://github.com/tsemovic/Espresso-PID/blob/main/images/theme2.jpg?raw=true)
![Theme 3](https://github.com/tsemovic/Espresso-PID/blob/main/images/theme6.jpg?raw=true)


[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [dill]: <https://github.com/joemccann/dillinger>
   [git-repo-url]: <https://github.com/joemccann/dillinger.git>
   [john gruber]: <http://daringfireball.net>
   [df1]: <http://daringfireball.net/projects/markdown/>
   [markdown-it]: <https://github.com/markdown-it/markdown-it>
   [Ace Editor]: <http://ace.ajax.org>
   [node.js]: <http://nodejs.org>
   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
   [jQuery]: <http://jquery.com>
   [@tjholowaychuk]: <http://twitter.com/tjholowaychuk>
   [express]: <http://expressjs.com>
   [AngularJS]: <http://angularjs.org>
   [Gulp]: <http://gulpjs.com>

   [PlDb]: <https://github.com/joemccann/dillinger/tree/master/plugins/dropbox/README.md>
   [PlGh]: <https://github.com/joemccann/dillinger/tree/master/plugins/github/README.md>
   [PlGd]: <https://github.com/joemccann/dillinger/tree/master/plugins/googledrive/README.md>
   [PlOd]: <https://github.com/joemccann/dillinger/tree/master/plugins/onedrive/README.md>
   [PlMe]: <https://github.com/joemccann/dillinger/tree/master/plugins/medium/README.md>
   [PlGa]: <https://github.com/RahulHP/dillinger/blob/master/plugins/googleanalytics/README.md>
