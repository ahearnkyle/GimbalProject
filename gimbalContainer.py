class Node(object):
    def __init__(self, gimbal, prev, next):
        self.gimbal = gimbal
        self.next = next
        self.prev = prev

class GimbalContainer:
    def __init__(self):
        self.head = None
        self.tail = None
    
    def append(self, gimbal):
        new_gimbal = Node(gimbal, None, None)
        if self.head is None:
            self.head = self.tail = new_gimbal
        else:
            new_gimbal.prev = self.tail
            new_gimbal.next = self.head
            self.tail.next = new_gimbal
            self.tail = new_gimbal
