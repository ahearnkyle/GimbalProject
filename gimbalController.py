import struct

'''

Remote is whatever is running the python program
PTR is the gimbal

'''
#controll characters
STX = 0x02 # Start of text sent by remote
ETX = 0x03 # end of text sent by remote/PTR
ACK = 0x06 # Acknowledge sent by PTR
NAK = 0x15 # Not Acknowledge sent by PTR
ESC = 0x1B # escape characters

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


def convertIntegerToShort(integer):
    '''
    This replaces the setvalue24 https://github.com/ahearnkyle/GimbalProject/wiki/gimbal-connection

    This method will take an integer between 32768 and -32768 and will convert that
    integer into a short int and return that as a byte string so 
    32768 now equals b'\xff\x7f' with the \ signifying the different bits

    This satisfies the following section of the protocol manual
    
    Passing Integer Values:
    As noted in the protocol command descriptions, some values sent between the remote and PTR units are integer
    values.  These integer values should be passed and received as 16-bit signed two's-complement little endian
    integers simply split between two bytes.  The first byte should represent the LSB of the integer with the second byte
    containing the MSB of the integer.  Negative values are represented as the two's-complement of the positive value 
    '''
    if integer > 32767 or integer < -32768:
        return None
    else:
        return struct.pack("<h", integer) # < stands for little endian and h is for short

def main():
    #sendPacket(0x36,None)
    print(convertIntegerToShort(-2))

if __name__ == '__main__':
    main()