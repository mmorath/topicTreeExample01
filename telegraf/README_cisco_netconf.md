<H1>Cisco_netconf_influx.conf</H1>
Readme for the telegraf agent which reads out the cisco ie3300 or ie3400 switch

link: --> https://github.com/jeremycohoe/cisco-ios-xe-mdt

### Using docker-compose...
Below an example how to integrate the service to your docker-compose file...
I do highly recommend to create for each device a seperate docker instance / configuration..therefore you have the possebiity to update each single agent individualy..
Since we output all data to a influxdb data base, the influxdb configuration is also added. Note you do require the influxdb folder...which should be a part of this repository...
# WARNING: Do not deploy this configuration directly to a production environment
Lets configure the switch first... open the terminal --> in our example we did use ssh..which was preconfigure, otherwise use a cli cable and use putty to build up a connection using the com interface..
1) basic setup

  ```bash
  Switch>en
  Switch#config t
  Enter configuration commands, one per line.  End with CNTL/Z.
  Switch(config)#int vlan1
  Switch(config-if)#no shutdown
  Switch(config-if)#ip address 192.168.178.95 255.255.255.0
  Switch(config-if)#do sh int vlan1
  Vlan1 is up, line protocol is up
    Hardware is EtherSVI, address is 002f.5c07.ebc0 (bia 002f.5c07.ebc0)
    Internet address is 192.168.4.13/24
    MTU 1500 bytes, BW 1000000 Kbit/sec, DLY 10 usec,
      reliability 255/255, txload 1/255, rxload 1/255
    Encapsulation ARPA, loopback not set
    Keepalive not supported
    ARP type: ARPA, ARP Timeout 04:00:00
    Last input 00:00:00, output 00:00:04, output hang never
    Last clearing of "show interface" counters never
    Input queue: 0/75/0/0 (size/max/drops/flushes); Total output drops: 0
    Queueing strategy: fifo
    Output queue: 0/40 (size/max)
    5 minute input rate 1000 bits/sec, 3 packets/sec
    5 minute output rate 0 bits/sec, 0 packets/sec
      160972 packets input, 11241187 bytes, 0 no buffer
      Received 0 broadcasts (0 IP multicasts)
      0 runts, 0 giants, 0 throttles
      0 input errors, 0 CRC, 0 frame, 0 overrun, 0 ignored
      3312 packets output, 782233 bytes, 0 underruns
      0 output errors, 2 interface resets
      0 unknown protocol drops
      0 output buffer failures, 0 output buffers swapped out
  Switch(config-if)#end
  Switch#config t
  Switch(config)#ip default-gateway 192.168.178.1
  Switch(config)#hostname groupswitch-batman
  groupswitch-batman(config)#username ansible privilege 15 password pwansible
  groupswitch-batman(config)#ip domain-name simulator.com
  groupswitch-batman(config)#crypto key generate rsa
  The name for the keys will be: groupswitch-batman.simulator.com
  Choose the size of the key modulus in the range of 360 to 4096 for your
    General Purpose Keys. Choosing a key modulus greater than 512 may take
    a few minutes.
  
  How many bits in the modulus [512]: 1024
  % Generating 1024 bit RSA keys, keys will be non-exportable...
  [OK] (elapsed time was 1 seconds)
  groupswitch-batman(config)#line vty 0 15
  groupswitch-batman(config-line)#transport input ssh
  groupswitch-batman(config-line)#login local
  groupswitch-batman(config-line)#enable password ansible
  groupswitch-batman(config-line)#end
  groupswitch-batman#copy run start
  Destination filename [startup-config]?
  Building configuration...
  [OK]
  groupswitch-batman#
```

## Next we need to configure the model

```bash
conf t
aaa new-model
aaa authentication login default local
aaa authorization exec default local 
aaa session-id common
username alex privilege 15 password 0 CB30TEST!
exit
conf t
gnxi
gnxi server
exit
!
```

## delete a subscription and create on ....
```bash
conf t
no telemetry ietf subscription 1
telemetry ietf subscription 1
encoding encode-kvgpb
filter xpath /process-cpu-ios-xe-oper:cpu-usage/cpu-utilization/five-seconds
source-address 192.168.20.220
stream yang-push
update-policy periodic 500
receiver ip address 192.168.178.43 57500 protocol grpc-tcp
exit
exit
```

## To check if the subscription was taken over 
```bash
show run | sec telemetry
```

## Check the subscription
```bash
show telemetry ietf subscription all
ID         Type       State      State Description
1          Configured Valid      Subscription validated
```

## Check the reciever 
```bash
show telemetry ietf subscription 1 receiver
Telemetry subscription receivers detail:

  Subscription ID: 1
  Name: grpc-tcp://192.168.178.43:57000
  Connection: 0
  State: Disconnected
  Explanation: Receiver invalid
```

## Verifying RESTCONF Configuration
```bash
show platform software yang-management process monitor 
show platform software yang-management process
show netconf-yang sessions
show netconf-yang sessions detail

```

https://ultraconfig.com.au/blog/cisco-telemetry-tutorial-with-telegraf-influxdb-and-grafana/
https://github.com/jeremycohoe/cisco-ios-xe-mdt



### Check log if messages are recieved
1) Log into the container
    ```bash
    docker exec -it cisco_netconf_influx /bin/bash
    ```
2) use the script kafka-console-consumer in the bin directory and consume the topic pfc200
    ```bash
    tail -f /tmp/metrics.out
    ```

### check if port is open 
    ```bash
    nmap -p 57500 192.168.20.220
    ```
### wire shark filter for switch and port
```bash
ip.addr == 192.168.20.220 && tcp.port == 57500
```