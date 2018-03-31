# -*- coding: utf-8 -*-
"""
Created on Tue Aug 09 11:19:10 2016

@author: hp
"""

class queue:
    def __init__(self, capacity = 10):
        self.capacity = capacity
        self.size = 0
        self.front = 0
        self.rear = 0
        self.array = [0]*capacity

    def is_empty(self):
        return 0 == self.size

    def is_full(self):
        return self.size == self.capacity

    def enqueue(self, element):
        if self.is_full():
            raise Exception('queue is full')

        self.array[self.rear] = element
        self.size += 1
        self.rear = (self.rear + 1) % self.capacity

    def dequeue(self):
        if self.is_empty():
            raise Exception('queue is empty')

        self.size -= 1
        self.front = (self.front + 1) % self.capacity

    def get_front(self):
        return self.array[self.front]


q = queue(3)

for i in range(3):
    q.enqueue(i)
#q.enqueue(10)
q.dequeue()
q.dequeue()
q.enqueue(333)

while False == q.is_empty():
    print q.get_front(),
    q.dequeue()
#q.dequeue()

