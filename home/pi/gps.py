#!/usr/bin/python

import subprocess, serial, requests, time


time.sleep(10)

# use a unique number like IMEI for dweet
imei = "014339000047387"


def restart_modem():
    subprocess.call(["/bin/sh", "/home/pi/wv.sh"])

    inetisup = False
    while inetisup == False:
        try:
            r = requests.get("https://www.dweet.io")
            inetisup = True
        except:
            print "False"

    dweet = requests.get(
        "https://dweet.io/dweet/for/"+imei+"?lat="
        + str(0.0)
        + "&long=-"
        + str(0.0)
        + "&speed="
        + str(0.0)
        + "&altitude="
        + str(0.0)
    )

    ser = serial.Serial("/dev/ttyUSB3", 9600, timeout=None)

    # Change sleep variables to update more or less frequently
    ser.write("AT+CGPS=1,1\r")
    time.sleep(1)
    ser.write("AT+CGPSINFOCFG=10,511\r")
    time.sleep(1)


    # This code was written as a backup tracking method for a hot air balloon
    # and since it is against FCC Regulations to transmit above 19,000 ft,
    # this shuts off the modem if the altitude is too high.
    last_five_alts = []
    airplane_mode = 0

    while True:
        data = ser.readline()
        if data.startswith("$GPGGA"):
            lat, longit, speed, altitude = "", "", "", 0
            gpsdata = data.split(",")
            if gpsdata[2]:
                prelat = float(str(gpsdata[2].split(".")[0][:-2]))
                prelatminutes = (
                    float(str(gpsdata[2].split(".")[0][-2:])) / 60.0
                )
                prelatseconds = (
                    float("0." + str(gpsdata[2].split(".")[0])) / 60.0
                )
                lat = prelat + prelatminutes + prelatseconds
            if gpsdata[4]:
                prelong = float(str(gpsdata[4].split(".")[0][:-2]))
                prelongminutes = (
                    float(str(gpsdata[4].split(".")[0][-2:])) / 60.0
                )
                prelongseconds = (
                    float("0." + str(gpsdata[4].split(".")[0])) / 60.0
                )
                longit = prelong + prelongminutes + prelongseconds
            if gpsdata[6]:
                speed = float(gpsdata[6])
            if gpsdata[9]:
                altitude = float(gpsdata[9])
                last_five_alts.append(altitude)
                if len(last_five_alts) > 5:
                    last_five_alts.pop(0)
            print str(lat) + ", " + str(longit) + ", " + str(
                speed
            ) + ", " + str(altitude)
            if lat and longit and altitude and speed:
                last_five_alts.append(altitude)
                if len(last_five_alts) > 5:
                    last_five_alts.pop(0)
                if altitude < 5000:
                    if airplane_mode == 0:
                        try:
                            dweet = requests.get(
                                "https://dweet.io/dweet/for/"+imei+"?lat="
                                + str(lat)
                                + "&long=-"
                                + str(longit)
                                + "&speed="
                                + str(speed)
                                + "&altitude="
                                + str(altitude)
                            )
                            print "dweet sent"
                        except:
                            print "dweet wasnt sent"
                            pass
                    else:
                        if len([x for x in last_five_alts if x < 5000]) == 5:
                            ser.write("AT+CFUN=1,0\r")
                            time.sleep(15)
                            ser.close()
                            subprocess.call(["reboot"])
                else:
                    subprocess.call(["killall", "wvdial"])
                    time.sleep(5)
                    ser.write("AT+CFUN=4\r")
                    airplane_mode = 1
            print data


restart_modem()
