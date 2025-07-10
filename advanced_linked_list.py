from typing import Optional


class Node:
    def __init__(self, data):
        self.data = data
        self.next: Optional['Node'] = None
        self.prev: Optional['Node'] = None


class AdvancedLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
        self._lock = None  # Placeholder for thread-safety (can be extended)

    def insert_sorted(self, data, key=lambda x: x):
        """Insert data in sorted order based on the key function."""
        new_node = Node(data)
        self.size += 1

        if not self.head:
            self.head = new_node
            self.tail = new_node
            return

        # Find insertion point
        current = self.head
        while current and key(current.data) < key(data):
            current = current.next

        if not current:  # Insert at tail
            new_node.prev = self.tail
            if self.tail is not None:
                self.tail.next = new_node
            self.tail = new_node
        elif current == self.head:  # Insert at head
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        else:  # Insert in middle
            new_node.prev = current.prev
            new_node.next = current
            if current.prev is not None:
                current.prev.next = new_node
            current.prev = new_node

    def find(self, key, value):
        """Find a node by key-value pair."""
        current = self.head
        while current:
            if current.data[key] == value:
                return current
            current = current.next
        return None

    def remove(self, key, value):
        """Remove a node by key-value pair."""
        node = self.find(key, value)
        if not node:
            return False

        self.size -= 1
        if node == self.head:
            self.head = node.next
            if self.head:
                self.head.prev = None
            else:
                self.tail = None
        elif node == self.tail:
            self.tail = node.prev
            if self.tail is not None:
                self.tail.next = None
            else:
                self.head = None
        else:
            if node.prev is not None:
                node.prev.next = node.next
            if node.next is not None:
                node.next.prev = node.prev
        return True


class SchoolSystem:
    def __init__(self):
        self.students = AdvancedLinkedList()

    def add_student(self, student_id, name, grade):
        """Add a student to the system in sorted order by ID."""
        record = {
            'id': student_id,
            'name': name,
            'grade': grade,
            'courses': []
        }
        self.students.insert_sorted(record, key=lambda x: x['id'])

    def transfer_student(self, student_id, to_grade):
        """Transfer a student to a new grade by ID."""
        node = self.students.find('id', student_id)
        if node:
            node.data['grade'] = to_grade
            # Re-sort by moving the node to maintain sorted order
            self.students.remove('id', student_id)
            self.students.insert_sorted(node.data, key=lambda x: x['id'])
            return True
        return False

    def get_student(self, student_id):
        """Retrieve a student by ID."""
        node = self.students.find('id', student_id)
        return node.data if node else None