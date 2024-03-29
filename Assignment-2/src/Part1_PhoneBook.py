from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Dict

"""
    Interface for a phone book.
    Each entry in the phone book is made up of 2 components: a name (String) and a
    phone number (long).

    For example, assume we have a phone book with the following data:
    {"name": "ABC", "phoneNumber": 1111111111}
    {"name": "XYZ", "phoneNumber": 9999999999}
    {"name": "DEF", "phoneNumber": 2222222222}

    then,
    the size() method should return 3,
    find("ABC") should return 1111111111,
    find("XYZ") should return 9999999999,
    find("PQR") should return -1.
"""
class PhoneBook(ABC):
    """
    @return The number of entries in this phone book.
    """
    @abstractmethod
    def size(self) -> int:
        pass

    """
    Inserts an entry in this phone book.
    @param name The name for the entry.
    @param phoneNumber The phone number for the entry.
    """
    @abstractmethod
    def insert(self, name: str, phoneNumber: int) -> None:
        pass

    """
    Returns the phone number associated with a name in the phone book.
    @param name The name to search for.
    @return The phone number for the entry, or -1 if the name is not present in the phone book.
    """
    @abstractmethod
    def find(self, name: str) -> int:
        pass

"""
    1st implementation: ListPhoneBook, use a List (specifically an ArrayList) as the underlying data structure.
"""
class ListPhoneBook(PhoneBook):
    phonebook: List[Dict] = None

    def __init__(self):
        self.phonebook = []

    """
    @return The number of entries in this phone book.
    """
    def size(self) -> int:
        return len(self.phonebook)

    """
    Inserts an entry in this phone book.
    @param name The name for the entry.
    @param phoneNumber The phone number for the entry.
    """
    def insert(self, name: str, phoneNumber: int) -> None:
        entry = {"name": name, "phoneNumber": phoneNumber}
        self.phonebook.append(entry)

    """
    Returns the phone number associated with a name in the phone book.
    @param name The name to search for.
    @return The phone number for the entry, or -1 if the name is not present in the phone book.
    """
    def find(self, name: str) -> int:
        try:
            for entry in self.phonebook:
                if entry.get("name") == name:
                    return entry.get("phoneNumber")
            raise AssertionError
        except AssertionError:
            return -1

"""
    2nd implementation: BinarySearchTreePhoneBook, use a binary search tree as the underlying data structure.
"""
class BinarySearchTreePhoneBook(PhoneBook):
    root: PhoneBookNode = None

    def __init__(self, root: PhoneBookNode = None):
        self.root = root

    """
    @return The number of entries in this phone book.
    """
    def size(self) -> int:
        return self.size_helper(self.root)

    """
    Helper method for size.
    """
    def size_helper(self, current_node: PhoneBookNode) -> int:
        if current_node is None:
            return 0

        left = current_node.left
        right = current_node.right
        if left is None and right is None:
            return 1
        elif left is None:
            return self.size_helper(right) + 1
        elif right is None:
            return self.size_helper(left) + 1
        elif left is not None and right is not None:
            return 1 + self.size_helper(left) + self.size_helper(right)


    """
    Inserts an entry in this phone book.
    @param name The name for the entry.
    @param phoneNumber The phone number for the entry.
    """
    def insert(self, name: str, phoneNumber: int) -> None:
        entry = PhoneBookNode(name, phoneNumber, None, None)
        current_node = self.root
        parent_node = self.root

        while current_node:
            parent_node = current_node
            assert current_node.name != name
            if current_node.name > name:
                current_node = current_node.left
            elif current_node.name < name:
                current_node = current_node.right

        if parent_node is None:
            self.root = entry
        elif parent_node.name > name:
            parent_node.left = entry
        elif parent_node.name < name:
            parent_node.right = entry


    """
    Returns the phone number associated with a name in the phone book.
    @param name The name to search for.
    @return The phone number for the entry, or -1 if the name is not present in the phone book.
    """
    def find(self, name: str) -> int:
        return self.find_helper(name, self.root)

    """
    Helper method for find.
    """
    def find_helper(self, name: str, current_node) -> int:
        if current_node is None:
            return -1
        elif current_node.name == name:
            return current_node.phoneNumber
        elif current_node.name > name and current_node.left is not None:
            return self.find_helper(name, current_node.left)
        elif current_node.name > name and current_node.left is None:
            return self.find_helper(name, current_node.right)
        elif current_node.name < name and current_node.right is not None:
            return self.find_helper(name, current_node.right)
        elif current_node.name < name and current_node.right is None:
            return self.find_helper(name, current_node.left)

    """
    Prints out tree.
    """
    def print(self):
        stack = [self.root]
        while stack:
            node = stack.pop()
            print(node)
            if node.left:
                stack.append(node.left)
            if node.right:
                stack.append(node.right)

"""
    Node for phone-book.
"""
class PhoneBookNode():
    name: str = None
    phoneNumber: int = None
    left: PhoneBookNode = None
    right: PhoneBookNode = None

    def __init__(self, name, phoneNumber, left, right):
        self.name = name
        self.phoneNumber = phoneNumber
        self.left = left
        self.right = right

    def __str__(self):
        return "{} {} {} {}".format(self.name, self.phoneNumber, self.left is not None, self.right is not None)
