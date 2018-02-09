import struct
import socket

'''

Remote is whatever is running the python program
PTR is the gimbal

'''
# controll characters
STX = 0x02 # Start of text sent by remote
ETX = 0x03 # end of text sent by remote/PTR
ACK = 0x06 # Acknowledge sent by PTR
NAK = 0x15 # Not Acknowledge sent by PTR
ESC = 0x1B # escape characters

class GimbalController:

    def __init__(self, sock=None):
        '''
        Function to initilize the socket
        can change socket if it is not tcp which is what the below code is
        '''
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        '''
        connect to host with given port
        need this method to controll multiple gimbals
        '''
        self.sock.connect((host, port))

    # stubbed out method
    def send(self, packetArray):
        '''
        after just a quick thought about this we would have to make the packet array a 
        string to send over socket
        '''
        pass
    
    # stubbed out method
    def received(self):
        '''
        we might have to do the same thing with the method above
        '''
        pass

    def closeSocket(self):
        '''
        Close the socket to be able to connect to more
        should not need to call __init__ again
        '''
        self.sock.close()

'''
==================================================================================================================
=
=               SOCKET METHODS ABOVE THIS LINE
=
==================================================================================================================
'''


    def calculateLRC(self, CommandNumberAndData): # CommandNumberAndData should be a list of bytes
        '''
        Calculates lrc by xoring all bits together
        returns lrc or none if CommandNumberAndData is none
        '''
        lrc = 0
        if CommandNumberAndData is not None:
            for byte in CommandNumberAndData:
                lrc ^= byte
            return lrc
        else:
            return None
        


    def convertIntegerToShort(self, integer):
        '''
        This replaces the setvalue24 https://github.com/ahearnkyle/GimbalProject/wiki/gimbal-connection
        
        returns the short value or none if index out of bounds

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

    def moveToHome(self):
        packetArray = []
        command = 0x36
        packetArray.append(STX)
        packetArray.append(command)
        packetArray.append(self.calculateLRC(packetArray[1:2])) 
        '''
        gets the second item in list. Must use a slice so that it returns a list itself since 
        calculateLRC expexts a list
        '''
        packetArray.append(ETX)

        # send packet
        self.send(packetArray)

        # get return packet
        self.received()
        print(packetArray)

def main():
    #print(convertIntegerToShort(-2))
    controller = GimbalController()
    controller.moveToHome()

if __name__ == '__main__':
    main()