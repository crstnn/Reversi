##PREFIX TRIE <br/>
'Trie' class has the following important methods (hash map explicitly not used as it makes this problem trivial):<br/>
- Object constructor method (__init__): accepts a list of text for which can only contain text a-z<br/>
- String frequency method (string_freq): given an string input to this method it returns the number of times the said word occurred in the original string input list<br/>
- Prefix frequency method (prefix_freq): given an string input to this method it returns the number of times the said prefix occurred in the original string input list<br/>
- Wildcard prefix frequency method (wildcard_prefix_freq): given a string input to this method (containing a single wildcard represented by '?', i.e. a symbol that can match any single character), 
which complete words in the text have that string as a prefix (returned in a list)<br/>
