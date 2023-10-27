<H1>Some usefule informations for troubleshooting</H1>

1. Connectivity
    * Still connected to VPN...well that will not work...disconnect
    * Try to ping the desired device..
2. Troubleshoot the publisher
    * Do you recieve messages from the device...can you verify that messages are published using for example using UAExpert when using a opc-ua device ?
3. Check the logs
    * check the logs of the docker container...


### Check if the agent recieves opc-ua values by checking the logs in the telegraf docker container
1) Log into the container
```bash
docker exec -it telegraf_opcua_influx /bin/bash
root@telegraf_opcua_influx:/# ls
bin  boot  dev  entrypoint.sh  etc  home  lib  lib64  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
root@telegraf_opcua_influx:/# cd tmp
root@telegraf_opcua_influx:/tmp# ls
metrics.out
root@telegraf_opcua_influx:/tmp#
```
2) Check the file which holds all the readouts...using cat   
```bash
cat metrics.out
opcua,host=telegraf_opcua_influx Quality="OK (0x0)",IIoTgateway_xHeartbeat=false 1660907837509000000
opcua,host=telegraf_opcua_influx IIoTgateway_xDoorSwitch=true,Quality="OK (0x0)" 1660907837509000000
opcua,host=telegraf_opcua_influx IIoTgateway_xHeartbeat=false,Quality="OK (0x0)" 1660907838009000000
opcua,host=telegraf_opcua_influx Quality="OK (0x0)",IIoTgateway_xDoorSwitch=true 1660907838009000000
```

### Check if kafka recieves the information by subscribing to the topic 
1) Log into the container
```bash
docker exec -it kafka /bin/bash
```
2) Subscribe to the topic of the opc-ua agent...in our example see telegraf config file entry output....topic "IIotBox_no1" 
```bash
/bin/kafka-console-consumer --bootstrap-server localhost:29092 --topic IIotBox_no1
iiot_box_alive,building=Halle_03,department=3H34,division=EMT,host=telegraf_opcua_kafka,machine=Pama156,site=LHB xHeartbeat=true,Quality="OK (0x0)" 1662454349000000000
```