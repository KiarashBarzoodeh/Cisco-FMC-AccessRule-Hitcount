# Cisco Firepower Managmenent Center Access Rules Hit Counts

Firewalls by default block any session which started from a security zone to another security zone. However for make accessibility we have to create access rule from based on some information like source and destination IP, source and Destination Port, and …, leaving unused access rule on firewall is mistake and it can make breach. So there is question: how can we find which rule used and which on not? Awareness of rule hit counts can make good information for decision. Fortunately **_ Cisco Firepower Management Center 6.4 and later _** create Hit Count feature in access policy. You can use this feature by GUI and API.
I made script that look at your desirable sensor (FTD/NGIPS) and access policy which assign to the sensor, and create excel file based on rule name, rule ID, hit count, first hit time and last hit time in your desktop. I know it is not 100% coded correctly. However it’s worked, I try to make it better based on efficiently and clean codding.
It’s work on **_ windows client _**.

## Installation

pip3 install -r requirements.txt

## To do list

- [x] Export Hit Count as Excel file in desktop
- [x] Possible use for multiple devices and multiple access policies
- [ ] Refresh Hit Counts
- [ ] Check user and password correction
- [ ] Check IP Connectivity
- [ ] Make error detection and exception
- [ ] Make containerization secript
