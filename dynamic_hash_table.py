from hash_table import HashSet, HashMap
from prime_generator import get_next_size

class DynamicHashSet(HashSet):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
        
    def rehash(self):
        # Store the old table and its size
        old_hash_table = self.hash_table        
        # Get new size and reset the table
        next_size = get_next_size()
        self.table_size = next_size
        self.total_elements = 0
        
        # Initialize new table based on collision type
        if self.collision_type == "Chain":
            self.hash_table = []
            for i in range(self.table_size):
                self.hash_table.append([])
                
            # Rehash all elements from old table
            for every_slot in old_hash_table:
                for key in every_slot:
                    self.insert(key)
                    
        else:  # Linear or Double hashing
            self.hash_table = [None] * self.table_size
            
            # Rehash all elements from old table
            for key in old_hash_table:
                if key is not None:
                    self.insert(key)
        
    def insert(self, x):
        # YOU DO NOT NEED TO MODIFY THIS
        super().insert(x)
        
        if self.get_load() >= 0.5:
            self.rehash()
            
            
class DynamicHashMap(HashMap):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
        
    def rehash(self):
        # Store the old table
        old_hash_table = self.hash_table
        
        # Get new size and reset the table
        next_size = get_next_size()
        self.table_size = next_size
        self.total_elements = 0
        
        # Initialize new table based on collision type
        if self.collision_type == "Chain":
            self.hash_table = []
            for i in range(self.table_size):
                self.hash_table.append([])
                
            # Rehash all elements from old table
            for every_slot in old_hash_table:
                for key_pair in every_slot:
                    # Each entry is a (key, value) pair
                    # We pass the whole pair to insert, but hashing uses only the key
                    self.insert(key_pair)
                    
        else:  # Linear or Double hashing
            self.hash_table = [None] * self.table_size
            
            # Rehash all elements from old table
            for key_pair in old_hash_table:
                if key_pair is not None:
                    # Each entry is a (key, value) pair
                    # We pass the whole pair to insert, but hashing uses only the key
                    self.insert(key_pair)


    def insert(self, key):
        # YOU DO NOT NEED TO MODIFY THIS
        super().insert(key)
        
        if self.get_load() >= 0.5:
            self.rehash()

