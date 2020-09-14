# pi-gps-tracker
Create a portable GPS tracker and interface with Raspberry Pi. SIM7100A 4G modem, Ting.com simcard, dweet.io, and OpenLayers


### Ting.com sim card and account

In order for this to work, you need a 4G sim card.  Ting.com sells them for $6/month + whatever data you use, which will be very low for this project. Once you receive the sim card, activate it with your normal cell phone, then you can insert into the SIM7100A sim card slot. Write down the email address and password you create for this account, as well as the sim card IMEI number, you will need these later.

### SIM7100A Notes

There are different boards out there that use the SIM7100A modem. Make sure you get one that can automatically powers on (doesn't require manually pushing a button). Attach the GPS and 4G antennas, then insert the Ting.com sim card 

### Raspberry Pi Setup Instructions

Copy the /etc and /home/pi files into the respective folders on the Raspberry Pi filesystem and hook up the modem to the Raspberry Pi's USB port. Once everything is connected, it should look like this:

![alt text](https://github.com/jeffrey-bowles/pi-gps-tracker/blob/master/img/pi-sim7100.jpg?raw=true)

Now, run the following:

    sudo apt-get install wvdial
    wvdialconf

wvdialconf should set up the parameters, but you will still need to change the username and password to your Ting.com account:

    sudo nano wvdial.conf

Also, if you still have trouble after setting this up, try using the parameters in the included wvdial.conf file.

Once this is completed, open and edit the gps.py, change the imei variable to the IMEI number of your Ting.com sim card, and save the file.

That should be it! The /etc/rc.local file should execute when you reboot the Pi, so every time you turn the Pi on, the 4G modem will start sending the GPS location to [dweet.io](https://dweet.io). We will use this site to create a real-time map of the current location on a remote computer.


### Setting up tracking interface on another device

Run:
    sudo apt-get install -y nodejs

- OR -
    curl -sL https://deb.nodesource.com/setup_14.x | sudo -E bash -

Once Node.js and npm are installed:

    mkdir gps
    cd gps
    npm init
    npm install ol
    npm install --save-dev parcel-bundler

Next, copy the files in the Github gps directory to the gps directory on your device.

Open the index.js file, change the imei variable to the IMEI number of your Ting.com sim card again, and save the file.

Now, if the Raspberry Pi tracker is on (or has been within the last 24 hours, because that's how long dweet.io stores information for free), you should be able to see a map of the current location by running:

    npm start

and then going to [localhost:1234](http://localhost:1234) in your browser! It should look like this:

![alt text](https://github.com/jeffrey-bowles/pi-gps-tracker/blob/master/img/shellandbrowser.png?raw=true)
