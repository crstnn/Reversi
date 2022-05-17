class TrieNode:
    ALPH_SIZE = 26
    ASCII_REMOVAL = ord("a")

    def __init__(self, letter=None):
        """Creates a node for the Trie which contains other node links and various stats
        Time Complexity: O(1)"""
        self.node_links = [None] * TrieNode.ALPH_SIZE
        self.node_letter = letter
        self.prefix_occurrences = 0
        self.word_termination_count = 0
        self.next_nodes = []

    def add_termination(self):
        """Increments the number of terminations"""
        self.word_termination_count += 1

    def get_word_termination_count(self):
        return self.word_termination_count

    def is_next(self, letter):
        """Is there a node for letter after the current node
        Time Complexity: O(1)"""
        links_idx = ord(letter) - TrieNode.ASCII_REMOVAL
        if self.node_links[links_idx] is None:
            return False
        return True

    def increment_prefix_occurrences(self):
        self.prefix_occurrences += 1

    def get_or_create_child(self, letter):
        """Moves pointer to the next node, If letter is not there then a node is created
        Time Complexity: O(1)"""
        links_idx = ord(letter) - TrieNode.ASCII_REMOVAL
        if self.node_links[links_idx] is None:
            result = TrieNode(letter)
            self.node_links[links_idx] = result
            self.next_nodes.append(links_idx)
        else:
            result = self.node_links[links_idx]
        result.increment_prefix_occurrences()
        return result

    def add_suffix(self, word, word_char_index):
        """Adds to the the tries current word
        Time Complexity: O(n), where n is the length of the word"""
        if word_char_index == len(word):
            self.word_termination_count += 1
            return
        letter = word[word_char_index]
        self.get_or_create_child(letter).add_suffix(word, word_char_index + 1)

    def get_next(self, letter):
        """Returns the next node given a currently letter
        Time Complexity: O(1)"""
        links_idx = ord(letter) - TrieNode.ASCII_REMOVAL
        if self.node_links[links_idx] is None:
            return None
        return self.node_links[links_idx]

    def get_children(self, letter):
        """Returns all the child node given a letter, if letter is '?' then all children are returned
        Time Complexity: O(1)"""
        if letter != "?":
            links_idx = ord(letter) - TrieNode.ASCII_REMOVAL
            result = self.node_links[links_idx]
            return [result] if result else []
        # else wildcard match
        return [self.node_links[links_idx] for links_idx in self.next_nodes]

    def get_letter(self):
        return self.node_letter

    def get_freq(self):
        return self.prefix_occurrences

    def get_next_nodes(self):
        return self.next_nodes

    def is_root(self):
        return self.node_letter is None

    
class Trie:
    def __init__(self, text):
        """
        Generates a Trie object, for which the input is sorted - this means that traversing through the trie ensures
        lexicographical order without having double links in the TrieNode class
        :param text: a list of english alphabet lower-case characters (list could be empty and may contain duplicates)
        Time Complexity: O(T), length of the whole string in the text param
        """
        self.root = TrieNode(None)
        if text:
            self._add_list_text(radix_sort_str(text))

    def _add_list_text(self, text):
        for word in text:
            self.root.prefix_occurrences += 1
            self.root.add_suffix(word, 0)

    def string_freq(self, query_str):
        """Given a query_str, this method tells us how many times that word occurred in the original input text
        Time Complexity: O(q), q is the length of query_str
        """
        current_node = self.root
        if not query_str:
            return current_node.get_word_termination_count()
        for word_idx in range(len(query_str)):
            letter = query_str[word_idx]
            current_node = current_node.get_next(letter)
            if not current_node:
                return 0
            if word_idx == len(query_str) - 1:
                return current_node.get_word_termination_count()

    def prefix_freq(self, query_str):
        """
        Given a query_str, this method tells us how many times that prefix occurred in the original input text
        Time Complexity: O(q), q is the length of query_str
        """
        current_node = self.root
        if not query_str:
            return current_node.get_freq()
        for word_idx in range(len(query_str)):
            letter = query_str[word_idx]
            if current_node.is_next(letter):
                current_node = current_node.get_next(letter)
            else:
                return 0
            if len(query_str) - 1 == word_idx:
                return current_node.get_freq()

    def wildcard_prefix_freq(self, query_str):
        """
         Given a query_str containing a single wildcard, which complete words in the text have that string as a prefix. Returned as a list
         Time Complexity: O(q + S), where q is the length of query_str and S is the total number of characters in all strings of the text.
        """
        result_lst = []
        if not query_str:
            return result_lst
        Trie._wild_aux(self.root, [], query_str, 0, result_lst)
        return result_lst

    @staticmethod
    def _wild_aux(current_node, curr_prefix, query_str, depth, result_lst):
        """Auxiliary function for wildcard prefix. Recurses over trie"""
        query_str_len = len(query_str)
        curr_char = query_str[depth] if depth < query_str_len else "?"
        if not current_node.is_root():
            curr_prefix.append(current_node.get_letter())
        count_words_at_current_node = current_node.get_word_termination_count()
        if count_words_at_current_node and depth >= query_str_len:
            word = "".join(curr_prefix)
            # append possibly multiple copies
            result_lst.extend([word] * count_words_at_current_node)
        child_nodes = current_node.get_children(curr_char)
        # print("Exploring depth %d child nodes (%s)." % (depth, "".join(n.get_letter() for n in child_nodes)))
        for node in child_nodes:
            Trie._wild_aux(node, curr_prefix, query_str, depth + 1, result_lst)
        if not current_node.is_root():
            curr_prefix.pop()

