import logging
def barcode_reader():
    """
    Read barcode data from a HID barcode scanner.

    The function reads barcode data from a HID barcode scanner connected
    to the system and returns the scanned barcode as a string.

    Returns:
        str: The scanned barcode as a string.
    """
    logging.info("Initializing barcode reader...")
    
    hid = {4: 'a', 5: 'b', 6: 'c', 7: 'd', 8: 'e', 9: 'f', 10: 'g', 11: 'h', 12: 'i', 13: 'j', 14: 'k', 15: 'l', 16: 'm',
           17: 'n', 18: 'o', 19: 'p', 20: 'q', 21: 'r', 22: 's', 23: 't', 24: 'u', 25: 'v', 26: 'w', 27: 'x', 28: 'y',
           29: 'z', 30: '1', 31: '2', 32: '3', 33: '4', 34: '5', 35: '6', 36: '7', 37: '8', 38: '9', 39: '0', 44: ' ',
           45: '-', 46: '=', 47: '[', 48: ']', 49: '\\', 51: ';', 52: '\'', 53: '~', 54: ',', 55: '.', 56: '/'}

    hid2 = {4: 'A', 5: 'B', 6: 'C', 7: 'D', 8: 'E', 9: 'F', 10: 'G', 11: 'H', 12: 'I', 13: 'J', 14: 'K', 15: 'L', 16: 'M',
            17: 'N', 18: 'O', 19: 'P', 20: 'Q', 21: 'R', 22: 'S', 23: 'T', 24: 'U', 25: 'V', 26: 'W', 27: 'X', 28: 'Y',
            29: 'Z', 30: '!', 31: '@', 32: '#', 33: '$', 34: '%', 35: '^', 36: '&', 37: '*', 38: '(', 39: ')', 44: ' ',
            45: '_', 46: '+', 47: '{', 48: '}', 49: '|', 51: ':', 52: '"', 53: '~', 54: '<', 55: '>', 56: '?'}

    fp = open('/dev/hidraw0', 'rb')

    ss = ""
    shift = False
    done = False

    while not done:
        #logging.info("Waiting for barcode scan...")
        
        # Get the character from the HID
        buffer = fp.read(8)
        for c in buffer:
            if c > 0:
                #logging.info(f"Received character: {c}")
                
                # Ensure that the scanner will add a carriage return after each successful scan,
                # otherwise, this will not work and will not quit the while loop.
                # 40 is a carriage return which signifies we are done looking for characters.
                if c == 40:
                    #logging.info("End of barcode scan.")
                    done = True
                    break

                # If we are shifted, use the hid2 characters.
                if shift:
                    # If it is a '2', then it is the shift key
                    if c == 2:
                        #logging.info("Shift key detected.")
                        shift = True
                    # If not a '2', lookup the mapping
                    else:
                        ss += hid2[c]
                        #logging.info(f"Appended character: {hid2[c]}")
                        shift = False

                # If we are not shifted, use the hid characters
                else:
                    # If it is a '2', then it is the shift key
                    if c == 2:
                        #logging.info("Shift key detected.")
                        shift = True
                    # If not a '2', lookup the mapping
                    else:
                        ss += hid[c]
                        #logging.info(f"Appended character: {hid[c]}")

    return ss

