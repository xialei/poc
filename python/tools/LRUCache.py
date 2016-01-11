# encoding=utf-8

'''
Created on 2015年6月10日

@author: Roger.xia
'''

class LRUCache(object):
    
    def __init__(self, maxsize):
        # cache 的最大记录数
        self.maxsize = maxsize
        # 用于真实的存储数据
        self.inner_dd = {}
        # 链表-头指针
        self.head = None
        # 链表-尾指针 
        self.tail = None
        
    def set(self, key, value):
        # 达到指定大小      
        if len(self.inner_dd) >= self.maxsize:
            self.remove_head_node()
        node = Node()
        node.data = (key, value)
        self.insert_to_tail(node)
        self.inner_dd[key] = node
        
    def insert_to_tail(self, node):
        if self.tail is None:
            self.tail = node
            self.head = node
        else:
            self.tail.next = node
            node.pre = self.tail
            self.tail = node
            
    def remove_head_node(self):
        node = self.head
        del self.inner_dd[node.data[0]]
        node = None
        self.head = self.head.next
        self.head.pre = None
        
    def get(self, key):
        if key in self.inner_dd:
            # 如果命中, 需要将对应的节点移动到队列的尾部
            node = self.inner_dd.get(key)
            self.move_to_tail(node)
            return node.data[1]
        return None
    
    def move_to_tail(self, node):
        # 只需处理在队列头部和中间的情况
        if not (node == self.tail):
            if node == self.head:
                self.head = node.next
                self.head.pre = None
                self.tail.next = node
                node.pre = self.tail
                node.next = None
                self.tail = node
            else:
                pre_node = node.pre
                next_node = node.next
                pre_node.next = next_node
                next_node.pre = pre_node
                self.tail.next = node
                node.pre = self.tail
                node.next = None
                self.tail = node

class Node(object):
    def __init__(self):
        self.pre = None
        self.next = None
        # (key, value)
        self.data = None
    def __eq__(self, other):
        if self.data[0] == other.data[0]:
            return True
        return False
    def __str__(self):
        return str(self.data)
   
if __name__ == '__main__':
    cache = LRUCache(10)
    for i in xrange(1000):
        cache.set(i, i + 1)
        cache.get(2)
    for key in cache.inner_dd:
        print key, cache.inner_dd[key]
