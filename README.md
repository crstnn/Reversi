# Collection of Some Algorithms
A (small) collection of my algorithm implementations.

## SHALLOWEST SPANNING AND SHORTEST ERRAND <br/><br/>
'Graph' class has the following important methods: <br/>
- Object constructor method (__init__): accepts a text file (given in parameter: gfile) for which it reads line by line. The file should contain only connected, undirected and simple graphs. The file is set up as following: The first line contains a single integer v, which is the number of vertices in the graph. Each following new line in the file consists of three integers separated by spaces. The first two integers are vertex IDs (range: [0, v - 1]), and the third is the (non-negative) weight of that edge. <br/>
- Shallowest spanning tree (shallowest_spanning_tree): Finds an MST that minimises the depth of the tree. The weights of the graph have been considered arbitrary because I minimise the number of edges from the yet-to-be-chosen root as it searches for the depth, not minimise the total weight of the MST. As a result it returns the root vertex that minimises the depth (following the aformentioned approach) and also the value of the minimum depth <br/>
- Shortest errand (shortest_errand): given an input 'home' and 'destination' (integer by vertex ID) this method finds the shortest path from home to destination but constrained by having to first go through an ice_loc and then through an ice_cream_loc (both ice_loc and ice_cream_loc are represented by a list of vertex IDs). The algorithm would output the weight and the walk of the shortest path. The algorithm automatically selects the optimal ice_loc and subsequently ice_cream_loc to go through giving the shortest path from home to destination. <br/>

[link to code](shallowest_span_tree_AND_shortest_errand.py)

## REVERSI PROJECT (for reversi.py)<br />
Reversi is a two player game with black or while pieces (denoted by 'W' & 'B') in the ouput window. The rules can be found here https://en.wikipedia.org/wiki/Reversi#Rules. 
The solution that I created works for a single player (with a basic computer opponent) or two players.
Pick one of the last two lines of the reversi.py file if you want to change it from its default two player mode

[link to code](reversi.py)

## PREFIX TRIE <br/>
'Trie' class has the following important methods (hash map explicitly not used as it makes this problem trivial):<br/>
- Object constructor method (__init__): accepts a list of text for which can only contain text a-z<br/>
- String frequency method (string_freq): given an string input to this method it returns the number of times the said word occurred in the original string input list<br/>
- Prefix frequency method (prefix_freq): given an string input to this method it returns the number of times the said prefix occurred in the original string input list<br/>
- Wildcard prefix frequency method (wildcard_prefix_freq): given a string input to this method (containing a single wildcard represented by '?', i.e. a symbol that can match any single character), 
which complete words in the text have that string as a prefix (returned in a list)<br/>

[link to code](prefix_trie.py)

##  (basic) CALCULATOR PROJECT (for parsing.py)<br />
This is a calculator that reads in user inputs, accepting the following operators "+", "-", "*", "/", "^", parentheses "(" and ")". It also deals with whitespace " " and non-negative floating point numbers only.

[link to code](parsing.py)
