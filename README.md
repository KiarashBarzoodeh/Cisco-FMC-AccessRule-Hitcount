# Cisco Firepower Management Center Access Rules Hit Counts

Firewalls by default block any session or traffic which started from a security zone to another. However to allowing traffic flow we must create access rule based on some information like ingress and egress zone, source and destination IP, source and Destination Port, and …, but leaving unused access rule on firewall is mistake and it can make breach. So there is question: how can we find which access rule used and which on not? Awareness of rule hit counts can make good information for decision to keeping rule or not. Fortunately **Cisco Firepower Management Center 6.4 and later** create Hit Count feature in access policies. You can access to this feature by GUI and API.  
I made script that look at your desirable sensor (FTD/NGIPS) and access policy which assign to the sensor, and create excel file based on rule name, rule ID, hit count, first hit time and last hit time in your desktop. I know it is not 100% coded correctly, but it’s worked, and I try to make it better based on efficiently and clean codding.  
Now it’s work just on **windows client**.  

## Installation

pip3 install -r requirements.txt

## Usage Example

In windows CMD or Powershell enter: *``` python Cisco-FMC-AccessRule-Hitcount.py https://fmc_address Username ```*  
It will prompt for enter password and then create excel file in desktop. The file name start date.  
Notice in FMC address it's **``` https ```**.  

## To do list

- [x] Export Hit Count as Excel file in desktop
- [x] Possible use for multiple devices and multiple access policies
- [ ] Refresh Hit Counts
- [ ] Check user and password correction
- [ ] Check IP Connectivity
- [ ] Make error detection and exception
- [ ] Make containerization script
