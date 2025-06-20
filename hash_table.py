from prime_generator import get_next_size

class HashTable:
    def __init__(self, collision_type, params):
        '''
        Possible collision_type:
            "Chain"     : Use hashing with chaining
            "Linear"    : Use hashing with linear probing
            "Double"    : Use double hashing
        '''

        self.collision_type = collision_type # Specifies the type of collision handling method
        self.total_elements = 0 #Counts the total number of elements in the hash table
        self.parameters = params # Stores parameters like size and z value



        # If using chaining to handle collisions
        if collision_type == "Chain":
            self.z, self.table_size = params
            self.hash_table = []
            for i in range(self.table_size):
                # Add an empty list at each index in the hash table beacause in chaining every slot contains list 
                self.hash_table.append([])

        # If using linear probing to handle collisions
        elif collision_type == "Linear":
            self.z, self.table_size = params 
            self.hash_table = [None] * self.table_size # Initialize the hash table with None values because in linear probing every slot contains key 

        # If using double hashing to handle collisions
        else:
            self.z, self.z2, self.c2, self.table_size = params
            self.hash_table = [None] * self.table_size # Initialize the hash table with None values in double hashing every slot contains a key 


    def assign_char(self, char):

        #assign each Latin letter to a unique integer (0–51) based on character type (upper or lower case) according to guidelines.

        if 'a' <= char <= 'z':
            return ord(char) - ord('a')  # assign 'a' to 0, 'b' to 1, ..., 'z' to 25
        elif 'A' <= char <= 'Z':
            return ord(char) - ord('A') + 26  # assign 'A' to 26, 'B' to 27, ..., 'Z' to 51
        else:
            return 0  # Default for non-alphabet characters (if applicable)
        
    def get_slot_hash(self, key):


        # Primary hash function using polynomial accumulation with mod table_size.
        #Initialize slot_number as 0
        slot_number = 0
        z_power = 1  # Initial power of z (z ki power 0)

        for char in key:
            charactervalue = self.assign_char(char)

            # Update the slot_number by adding the product of charactervalue and z_power, mod table_size

            slot_number = (slot_number + (charactervalue * z_power) ) % self.table_size
            z_power = (z_power * self.z) % self.table_size  # apply power of z incrementally

        return slot_number
    
    def second_double_hash(self, key):

        # Secondary hash function for double hashing using polynomial accumulation with mod c2.

        jump = 0 # Initialize jump as 0
        z_power = 1 # Initial power of z (z ki power 0)

        for char in key:

            charactervalue = self.assign_char(char)   # Get the assigned value for the character

            # Update jump by adding the product of charactervalue and z_power, mod c2
            jump = (jump + (charactervalue * z_power) ) % self.c2
            z_power = (z_power * self.z2) % self.c2  # Update p_pow for next character
        
        return self.c2 - (jump % self.c2)

    def insert(self, x):
        pass

    def find(self, key):
        pass
        
    def get_slot(self, key):
        # Check if the key is a tuple; if so, take the key element
        if isinstance(key, tuple):
            key = key[0] 

        # Calculate the index using the primary hash function
        initial_index = self.get_slot_hash(key)

        return initial_index
    
    def get_load(self):

        #Return the load factor of the hash table by usiing the formula of load factor 
        if self.table_size > 0 :
            return self.total_elements / self.table_size 
        else:
            return 0
    
    def __str__(self):
        pass
    
    # TO BE USED IN PART 2 (DYNAMIC HASH TABLE)
    def rehash(self):
        pass
        
  
# IMPLEMENT ALL FUNCTIONS FOR CLASSES BELOW
# IF YOU HAVE IMPLEMENTED A FUNCTION IN HashTable ITSELF, 
# YOU WOULD NOT NEED TO WRITE IT TWICE
    
class HashSet(HashTable):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
    
    def insert(self, key):

        # Insertion for "Chain" collision handling        
        if self.collision_type == "Chain":
            table_slot = self.get_slot_hash(key)
            
            # Check if the key already exists in the slot to avoid duplicates
            for i in range(len(self.hash_table[table_slot])):
                if self.hash_table[table_slot][i] == key:
                    return
                
             # Add the key if it doesn't exist and increase the total elements count
            self.hash_table[table_slot].append(key)
            self.total_elements += 1 

        # Insertion for "Linear" collision handling

        elif self.collision_type == "Linear":
            # Check if the table is already full
            if self.total_elements >= self.table_size:
                raise Exception("Table is full")
            
            table_slot = self.get_slot_hash(key)
            initial_slot = table_slot
            # Find an empty slot or if key already exists
            while self.hash_table[table_slot] is not None :
                if self.hash_table[table_slot] == key:
                    return
                table_slot = (table_slot + 1) % self.table_size
                # if table_slot == initial_slot:
                #     raise Exception("Table is full")
                
            # Find an empty slot or if key already exists
            self.hash_table[table_slot] = key
            self.total_elements += 1


        # Insertion for "Double" collision handling

        elif self.collision_type == "Double":

            # Check if the table is already full

            if self.total_elements >= self.table_size:
                raise Exception("Table is full")
            
            table_slot = self.get_slot_hash(key)
            jump_size = self.second_double_hash(key)
            initial_slot = table_slot
            while self.hash_table[table_slot] is not None:
                if self.hash_table[table_slot] == key:
                    return
                table_slot = (table_slot + jump_size) % self.table_size
                if table_slot == initial_slot:
                    raise Exception("Table is full")

            self.hash_table[table_slot] = key
            self.total_elements += 1

    
    def find(self, key):

        # Finding a key for "Chain" collision handling
        if self.collision_type == "Chain":
            table_slot = self.get_slot_hash(key)
             # Check each element in the slot’s list to find the key
            for i in range(len(self.hash_table[table_slot])):
                if self.hash_table[table_slot][i] == key:
                    return True
                
            return False 

        # Finding a key for "Linear" collision handling
        elif self.collision_type == "Linear":
            table_slot = self.get_slot_hash(key)
            initial_slot = table_slot

            # Look through table slots in linear order until key is found or loop completes
            while self.hash_table[table_slot] is not None:
                if self.hash_table[table_slot] == key:
                    return True
                table_slot = (table_slot + 1) % self.table_size
                if table_slot == initial_slot:
                    return False
            return False

        # Finding a key for "Double" collision handling
        elif self.collision_type == "Double":


            table_slot = self.get_slot_hash(key)
            jump_size = self.second_double_hash(key)
            initial_slot = table_slot

            # Look through table slots using jump size until key is found or loop completes
            while self.hash_table[table_slot] is not None:
                if self.hash_table[table_slot] == key:
                    return True
                table_slot = (table_slot + jump_size) % self.table_size

                if table_slot == initial_slot:
                    return False 

            return False
    
    def get_slot(self, key):
        return super().get_slot()
    
    def get_load(self):
        return super().get_load()
    
    def __str__(self):
        result = []

        if self.collision_type == "Chain":
            for slot in self.hash_table:
                # Join all elements in the slot with ' ; ' if the slot is non-empty
                result.append(" ; ".join(slot) if slot else "<EMPTY>")
        else:
            for entry in self.hash_table:
                # Append entry directly or "<EMPTY>" if the slot is None
                result.append(entry if entry is not None else "<EMPTY>")

        # Join the accumulated results into a single output string
        return " | ".join(result)


    
class HashMap(HashTable):
    def __init__(self, collision_type, params):
        super().__init__(collision_type, params)
    
    def insert(self, x):
        # x = (key, value)
        
        key, value = x
        
        if self.collision_type == "Chain":
            table_slot = self.get_slot_hash(key)  
            for i in range(len(self.hash_table[table_slot])):
                if self.hash_table[table_slot][i][0] == key:
                    # self.hash_table[table_slot][i] = (key, value)
                    return 
            self.hash_table[table_slot].append((key, value))
            self.total_elements += 1

        elif self.collision_type == "Linear":
            if self.total_elements >= self.table_size:
                raise Exception("Table is full")
            table_slot = self.get_slot_hash(key)
            initial_slot = table_slot
            
            while self.hash_table[table_slot] is not None:
                if self.hash_table[table_slot][0] == key:
                    # self.hash_table[table_slot] = (key, value)
                    return
                table_slot = (table_slot + 1) % self.table_size
                # if table_slot == initial_slot:
                #     raise Exception("Table is full")

            
            self.hash_table[table_slot] = (key, value)
            self.total_elements += 1

        elif self.collision_type == "Double":
            if self.total_elements >= self.table_size:
                raise Exception("Table is full")
            table_slot = self.get_slot_hash(key)
                
                
            jump_size = self.second_double_hash(key)
            initial_slot = table_slot
            
            while self.hash_table[table_slot] is not None:
                if self.hash_table[table_slot][0] == key:
                    # self.hash_table[table_slot] = (key, value) 
                    return 
                table_slot = (table_slot + jump_size) % self.table_size
                if table_slot == initial_slot:
                    raise Exception("Table is full")
            
            self.hash_table[table_slot] = (key, value)
            self.total_elements += 1
    
    def find(self, key):
        if self.collision_type == "Chain":
            table_slot = self.get_slot_hash(key)
            for k , v in self.hash_table[table_slot]:
                if k == key:
                    return v
            return None

        elif self.collision_type == "Linear":

            table_slot = self.get_slot_hash(key)
            initial_slot = table_slot

            while self.hash_table[table_slot] is not None:
                if self.hash_table[table_slot][0] == key:
                    return self.hash_table[table_slot][1]
                table_slot = (table_slot + 1) % self.table_size
                if table_slot == initial_slot:
                    return None

            return None

        elif self.collision_type == "Double":
            table_slot = self.get_slot_hash(key)      
            jump_size = self.second_double_hash(key)
            initial_slot = table_slot 

            while self.hash_table[table_slot] is not None:
                if self.hash_table[table_slot][0] == key:
                    return self.hash_table[table_slot][1]
                table_slot = (table_slot + jump_size) % self.table_size

                if table_slot == initial_slot:
                    return False 
            return None
    
    def get_slot(self, key):
        return super().get_slot()

    def get_load(self):
        return super().get_load()
    
    def __str__(self):
        result = []

        if self.collision_type == "Chain":       
            for slot in self.hash_table:
                # Join all elements in the slot with ' ; ' if the slot is non-empty
                if not slot:
                    result.append("<EMPTY>")
                else:
                    result.append(" ; ".join(f"({k}, {v})" for k, v in slot))
            
        else:
            
            for entry in self.hash_table:
                # Append entry directly or "<EMPTY>" if the slot is None

                if entry is None:
                    result.append("<EMPTY>")
                else:
                    k, v = entry
                    result.append(f"({k}, {v})")

         # Join the accumulated results into a single output string          
        return " | ".join(result)


