---
Solar data stats script for EPEVER MPPT Charge Controllers
---

This was my solution to pulling stats from my EPEVER 3210AN charge controller via the EPEVER WiFi Box.  

The WiFi box exposes the RS485 Serial connection on TCP/8088 by default. You can then query the controller via Modbus.  

You'll need to reconfigure your EPEVER WiFi box to run in STA mode rather than AP mode to connect it to your network. (To do this browse to the IP of the WiFI box once connected to it in AP mode)  

If you are just wanting to connect and monitor the controller via serial I highly recommend https://github.com/alexnathanson/EPSolar_Tracer who's work helped a lot with figuring out how to query the controller.  

Personally I am ingesting the CSV generated via Telegraf into InfluxDB, then viewing the metrics in Grafana like so.  

![alt text](https://github.com/liamalxd/epsolarmon/blob/main/dc2power1.PNG)
