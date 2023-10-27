<H1>telegraf_opcua_influx</H1>



### Using docker-compose...
Below an example how to integrate the service to your docker-compose file...
I do highly recommend to create for each device a seperate docker instance / configuration..therefore you have the possebiity to update each single agent individualy..
Since we output all data to a influxdb data base, the influxdb configuration is alos added. Note you do require the influxdb folder...which should be a part of this repository...
# WARNING: Do not deploy this configuration directly to a production environment

# As-Is config 
```bash
groupswitch-batman#show config
Using 2641 out of 33554432 bytes
!
! Last configuration change at 09:41:16 UTC Thu Oct 28 2021
!
version 17.3
service timestamps debug datetime msec
service timestamps log datetime msec
service call-home
no platform punt-keepalive disable-kernel-core
no platform punt-keepalive settings
no platform bridge-security all
!
hostname groupswitch-batman
!
enable password ansible
!
no aaa new-model
rep bpduleak    
ptp mode e2etransparent 
!
ip domain name simulator.com
!
login on-success log
no device-tracking logging theft
scada modbus tcp server connections 5
scada modbus tcp server
!
crypto pki trustpoint TP-self-signed-703295296
 enrollment selfsigned
 subject-name cn=IOS-Self-Signed-Certificate-703295296
 revocation-check none
 rsakeypair TP-self-signed-703295296
!
crypto pki trustpoint SLA-TrustPoint
 enrollment pkcs12
 revocation-check crl
!
crypto pki certificate chain TP-self-signed-703295296
 certificate self-signed 01 nvram:IOS-Self-Sig#2.cer
crypto pki certificate chain SLA-TrustPoint
 certificate ca 01 nvram:CiscoLicensi#1CA.cer
!        
diagnostic bootup level minimal    
!        
spanning-tree mode rapid-pvst
spanning-tree extend system-id
memory free low-watermark processor 89156
!        
alarm-profile defaultPort
 alarm not-operating 
 syslog not-operating 
 notifies not-operating 
!        
username ansible privilege 15 password 0 pwansible   
!        
transceiver type all
 monitoring
vlan internal allocation policy ascending
lldp run     
!        
interface GigabitEthernet1/1
!        
interface GigabitEthernet1/2
!        
interface GigabitEthernet1/3
!        
interface GigabitEthernet1/4
!        
interface GigabitEthernet1/5
!        
interface GigabitEthernet1/6
!        
interface GigabitEthernet1/7
!        
interface GigabitEthernet1/8
 spanning-tree portfast
 spanning-tree bpduguard enable
 spanning-tree guard root
!        
interface GigabitEthernet1/9
!        
interface GigabitEthernet1/10
!        
interface Vlan1
 ip address 192.168.178.95 255.255.255.0
!        
ip default-gateway 192.168.178.1
ip http server
ip http authentication local
ip http secure-server
ip http client source-interface Vlan1
ip forward-protocol nd    
!        
snmp-server manager
!        
control-plane
!        
!        
line con 0
 exec-timeout 0 0
 stopbits 1
line aux 0
 stopbits 1
line vty 0 4
 login local
 length 0
 transport input ssh
line vty 5 15
 login local
 transport input ssh
!        
call-home
 ! If contact email address in call-home is configured as sch-smart-licensing@cisco.com
 ! the email address configured in Cisco Smart License Portal will be used as contact email address 
to send SCH notifications.
 contact-email-addr sch-smart-licensing@cisco.com
 profile "CiscoTAC-1"
  active 
  destination transport-method http
!             
restconf 
end  
```

# As-Is config 
* https://github.com/YangModels/yang/tree/main/vendor/cisco/xe
* https://github.com/YangModels/yang/tree/main/vendor/cisco/xe/1731
* https://community.cisco.com/t5/physical-and-virtual-network-elements/telemetry-subscription-not-working-on-virtual-routers/td-p/4421665
* flo pachinger
    mittels NETCONF (22): https://github.com/CiscoDevNet/industrial-netdevops/blob/master/NETCONF/netconf-getting-started.py
    mittels RESTCONF (443): https://github.com/CiscoDevNet/industrial-netdevops/blob/master/RESTCONF/restconf-getting-started.py 

    Learning Labs dazu (kostenloser Account notwendig): https://developer.cisco.com/learning/modules/industrial-netdevops 
* https://community.cisco.com/t5/physical-and-virtual-network-elements/telemetry-subscription-not-working-on-virtual-routers/td-p/4421665

```bash
groupswitch-batman enable
groupswitch-batman#
groupswitch-batman#config t
groupswitch-batman(config)#
groupswitch-batman(config)#netconf-yang
groupswitch-batman(config)#exit
groupswitch-batman#wr


```




config for the switch 
```bash
conf t 
telemetry ietf subscription 1
...
.
..
```

* video --> https://www.youtube.com/watch?v=ifCLVVcnqRs
* plugin --> https://www.influxdata.com/integration/cisco-model-driven-telemetry/


### Check if kafka recieves opc-ua values
1) Log into the container
    ```bash
    docker exec -it kafka /bin/bash
    ```
2) use the script kafka-console-consumer in the bin directory and consume the topic pfc200
    ```bash
    /bin/kafka-console-consumer --bootstrap-server localhost:29092 --topic cisco
    ```