import hash_table as ht

class DigitalLibrary:
    # DO NOT CHANGE FUNCTIONS IN THIS BASE CLASS
    def __init__(self):
        pass
    
    def distinct_words(self, book_title):
        pass
    
    def count_distinct_words(self, book_title):
        pass
    
    def search_keyword(self, keyword):
        pass
    
    def print_books(self):
        pass
    
class MuskLibrary(DigitalLibrary):
    # Merge function for tuples in library_info based on the title
    def merge_library_info(self, left, right):
        result = []
        i = j = 0
        # Loop through both lists until we reach the end of one
        while i < len(left) and j < len(right):
            # Compare based on book titles (first element of each tuple)
            
            if left[i][0] < right[j][0]:
                result.append(left[i])    # Add book from 'left' if its title is smaller
                i += 1
            else:
                result.append(right[j])     # Otherwise, add book from 'right'
                j += 1

        # Add any remaining books from 'left' or 'right' list
        result.extend(left[i:])
        result.extend(right[j:])
        
        return result
    
    # Merge sort function for library_info(sort a list of book tuples)
    def merge_sort_library_info(self, arr_books):
            if len(arr_books) <= 1:  # Base case: list is already sorted if it has 0 or 1 book
                return arr_books
            
            mid = len(arr_books) // 2
            left = self.merge_sort_library_info(arr_books[:mid])  # Sort left half
            right = self.merge_sort_library_info(arr_books[mid:])  # Sort right half
            
            return self.merge_library_info(left, right)  # Merge the two sorted halves
        
    def merge_distwords(self, left_word_list, right_word_list):
        result_list = []
        i = j = 0
        
        while i < len(left_word_list) and j < len(right_word_list):
            if left_word_list[i] < right_word_list[j]:
                if not result_list or result_list[-1] != left_word_list[i]:
                    result_list.append(left_word_list[i])
                i += 1
            elif left_word_list[i] > right_word_list[j]:
                if not result_list or result_list[-1] != right_word_list[j]:
                    result_list.append(right_word_list[j])
                j += 1
            else:
                if not result_list or result_list[-1] != left_word_list[i]:
                    result_list.append(left_word_list[i])
                i += 1
                j += 1
        
        # Add remaining elements from left_word_list with distinctness
        while i < len(left_word_list):
            if not result_list or result_list[-1] != left_word_list[i]:
                result_list.append(left_word_list[i])
            i += 1
        
        # Add remaining elements from right_word_list with distinctness
        while j < len(right_word_list):
            if not result_list or result_list[-1] != right_word_list[j]:
                result_list.append(right_word_list[j])
            j += 1
        
        return result_list


    def merge_sort_distwords(self, word_list):
        if len(word_list) <= 1:
            return word_list
        
        mid_index = len(word_list) // 2
        left_word_list = self.merge_sort_distwords(word_list[:mid_index])
        right_word_list = self.merge_sort_distwords(word_list[mid_index:])
        
        return self.merge_distwords(left_word_list, right_word_list)
    
    def __init__(self, book_titles, texts):
        # Initialize library_info to store (title, distinct sorted words list) for each book
        self.library_info = []
        
        for i in range(len(book_titles)):
            distinct_words_sorted_list = self.merge_sort_distwords(texts[i])
            self.library_info.append((book_titles[i], distinct_words_sorted_list))
        
        # Sort library_info by book titles alphabetically using merge sort
        self.library_info = self.merge_sort_library_info(self.library_info) 

    
    def binary_search_title(self, book_title):
        left, right = 0, len(self.library_info) - 1
        
        while left <= right:
            mid_index = (left + right) // 2
            mid_index_btitle = self.library_info[mid_index][0]
            
            if mid_index_btitle == book_title:
                return self.library_info[mid_index][1]  # Return the list of distinct words
            elif mid_index_btitle < book_title:  #search in right half
                left = mid_index + 1
            else:                     #search in left half
                right = mid_index - 1
        
        return []  # Return empty if the book is not found

    # Use binary search for faster retrieval
    def distinct_words(self, book_title):
        return self.binary_search_title(book_title) 
    
    def count_distinct_words(self, book_title):
        words = self.binary_search_title(book_title)
        return len(words) 
    
    def binary_search_word(self, words, keyword):
        left, right = 0, len(words) - 1
        
        while left <= right:
            mid_index = (left + right) // 2
            mid_index_word = words[mid_index]
            
            if mid_index_word == keyword: # word found 
                return True
            elif mid_index_word < keyword: # If the middle word is less than the keyword, search in the right half
                left = mid_index + 1
            else:    # If the middle word is greater than the keyword, search in the left half
                right = mid_index - 1
        
        return False  # If loop ends, the word is not in the list

    # Updated search_keyword to use binary search on each book's words
    def search_keyword(self, keyword):
        matching_books = []
        
        # Iterate through each book title and its words list
        for book_title, words in self.library_info:
            # Check if keyword exists in the current book's sorted words list
            if self.binary_search_word(words, keyword):
                matching_books.append(book_title)
        
        return matching_books
    
    def print_books(self):
        for title, words in self.library_info:
            print(f"{title}: {' | '.join(words)}")
        

class JGBLibrary(DigitalLibrary):
    # IMPLEMENT ALL FUNCTIONS HERE
    def __init__(self, name, params):
        '''
        name    : "Jobs", "Gates" or "Bezos"
        params  : Parameters needed for the Hash Table:
            z is the parameter for polynomial accumulation hash
            Use (mod table_size) for compression function
            
            Jobs    -> (z, initial_table_size)
            Gates   -> (z, initial_table_size)
            Bezos   -> (z1, z2, c2, initial_table_size)
                z1 for first hash function
                z2 for second hash function (step size)
                Compression function for second hash: mod c2
        '''
        super().__init__()
        self.name = name  # Store the name to check the type of collision handling

        # Store the name to check the type of collision handling
        if name == "Jobs":   # Jobs uses Chaining for collision handling
            collision_type = "Chain"
            z, table_size = params
            hash_params = (z, table_size)
        elif name == "Gates": # Gates uses Linear Probing for collision handling
            collision_type = "Linear"
            z, table_size = params
            hash_params = (z, table_size)
        else:  # Bezos   # Bezos uses Double Hashing for collision handling
            collision_type = "Double"
            z1, z2, c2, table_size = params
            hash_params = (z1, z2, c2, table_size)

        # books_hashmap: book_title -> hashset of words

        self.books_hashmap = ht.HashMap(collision_type, hash_params)
        self.book_list = []   # List to keep track of all books added to the library
        
        
    
    def add_book(self, book_title, text):

        if self.name == "Bezos":
            z1, z2, c2, size = self.books_hashmap.parameters
            word_hashset = ht.HashSet(self.books_hashmap.collision_type, (z1, z2, c2, size))
        else:
            z, size = self.books_hashmap.parameters
            word_hashset = ht.HashSet(self.books_hashmap.collision_type, (z, size))
                
            # Add all words to the set
        for word in text:
            if word_hashset.find(word) is False:
                word_hashset.insert(word)
            
            # Add the set to the books map
        self.books_hashmap.insert((book_title, word_hashset))

        # add the added book in book_list
        self.book_list.append(book_title) 
    
    def distinct_words(self, book_title):
        word_hashset = self.books_hashmap.find(book_title)
        if word_hashset is None:
            return []
        
        # Convert the hashset to a list maintaining the hash table order
        words = []

        #convert hashset into list and then return word 

        if word_hashset.collision_type == "Chain":
            for slot in word_hashset.hash_table:
                for word in slot:
                    words.append(word)

        # For linear probing or double hashing, each slot has a single word
        elif word_hashset.collision_type == "Linear" or word_hashset.collision_type == "Double":
            for word in word_hashset.hash_table:
                if word is not None:
                    words.append(word)

        return words

    
    def count_distinct_words(self, book_title):
        word_hashset = self.books_hashmap.find(book_title)
        
        return word_hashset.total_elements 
    
    def search_keyword(self, keyword):
        ans = [] 
        for book in self.book_list:

            b1 = self.books_hashmap.find(book)
            if b1.find(keyword):
                ans.append(book) 

        return ans 

    
    def print_books(self):
        goyal = []
        for i in range(len(self.books_hashmap.hash_table)):
            if self.books_hashmap.hash_table[i] is None:
                continue
            if self.name == 'Jobs' and self.books_hashmap.hash_table[i] != None:
                goyal.extend(self.books_hashmap.hash_table[i])
            else:
                goyal.append(self.books_hashmap.hash_table[i])
        for ayush in goyal:
            print(ayush[0] + ":", ayush[1])
        

