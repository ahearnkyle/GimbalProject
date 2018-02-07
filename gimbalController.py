
'''

Remote is whatever is running the python program
PTR is the gimbal

'''
#controll characters
STX = 0x02 # Start of text sent by remote
ETX = 0x03 # end of text sent by remote/PTR
ACK = 0x06 # Acknowledge sent by PTR
NAK = 0x15 # Not Acknowledge sent by PTR

#stubbed out method
def sendPacket(cmd, message):
    '''
    lrc is calculated
    no need to account for controll characters since they are not added yet 

    in the java version it uses short ints (16-bit)
    python does not implement short ints 
    '''
    lrc = cmd
    if message is not None:
        for b in message:
            print(b)
            lrc ^= b
    print(lrc)

#stubbed out method
def setValue24(data, index, value):
    data[index] = (value & 0xFF)
    data[index + 1] = ((value & 0xFF00) >> 8)
    data[index + 2] = ((value & 0xFF0000) >> 16)
    return data

def main():
    #sendPacket(0x36,None)
    data = [0] * 6
    data = setValue24(data, 0, 3*100)
    data = setValue24(data, 3, 3*100)
    print(data)

if __name__ == '__main__':
    main()