<H1>README_cisco_modbusTCPIP</H1>


1.  Step 1	
Enter global configuration mode:

configure terminal

2. 
Enable MODBUS TCP on the switch:

scada modbus tcp server

To disable MODBUS on the switch and return to the default settings, enter the no scada modbus tcp server global configuration command.

The system displays a message to warn you that starting the MODBUS TCP server is a security risk:

WARNING: Starting Modbus TCP server is a security risk. Please understand the security issues involved before proceeding further. Do you still want to start the server? [yes/no]:

Step 3	
Enter yes to confirm that you understand the security issues and to proceed with starting the server.

Step 4	
(Optional) Set the TCP port to which clients send messages:

scada modbus tcp server port tcp-port-number

The range for tcp-port-number is 1 to 65535. The default is 502.

Step 5	
(Optional) Set the number of simultaneous connection requests sent to the switch:

scada modbus tcp server connection connection-requests

The range for connection-requests is 1 to 5. The default is 1.

Step 6	
Return to privileged EXEC mode:

end

```bash
Switch# configure terminal
Switch(config)# scada modbus tcp server
WARNING: Starting Modbus TCP server is a security risk. Please understand the security issues involved 
before proceeding further. Do you still want to start the server? [yes/no]: y
Switch(config)# end

Switch# show scada modbus tcp server
Summary: enabled, running, process id 142
Conn Stats: listening on port 801, 4 max simultaneous connections
    0 current client connections
    0 total accepted connections, 0 accept connection errors
    0 closed connections, 0 close connection errors
Send Stats: 0 tcp msgs sent, 0 tcp bytes sent, 0 tcp errors
    0 responses sent, 0 exceptions sent, 0 send errors
Recv Stats: 0 tcp msgs received, 0 tcp bytes received, 0 tcp errors
    0 requests received, 0 receive errors
```

What can be read out 
--> https://www.cisco.com/c/en/us/td/docs/switches/lan/cisco_ie3X00/software/17_3/b_cip-modbus_17-3_iot_switch_cg/m_modbus.html