from math import inf
from copy import deepcopy

class MinHeap:
    left_child = lambda v: 2 * v + 1
    right_child = lambda v: 2 * v + 2
    parent = lambda v: (v - 1) // 2

    def __init__(self, size):
        """
        Time Complexity: O(n) where n is the size of the list
        :param size: the size of the heap
        """
        self.heap = []
        self.vertices = [None] * size
        self.size = size
        for i in range(size):
            self._add_vertex(i, inf)

    def _bubble_down(self, idx):
        """
        Starts at root node and moves greater weight items down the tree
        Time Complexity: O(logn)
        :param idx: the index in the heap queue
        """

        smallest = idx
        right_idx = MinHeap.right_child(idx)
        left_idx = MinHeap.left_child(idx)
        if left_idx < len(self.heap) and self.heap[smallest][1] > self.heap[left_idx][1]: smallest = left_idx
        if right_idx < len(self.heap) and self.heap[smallest][1] > self.heap[right_idx][1]: smallest = right_idx
        if smallest != idx:
            self.vertices[self.heap[smallest][0]], self.vertices[self.heap[idx][0]] = idx, smallest
            self.heap[idx], self.heap[smallest] = self.heap[smallest], self.heap[idx]
            self._bubble_down(smallest)

    def pop_min(self):
        """Takes the smallest item from the priority queue
        Time Complexity: O(logn)
        """
        self.vertices[self.heap[0][0]] = None
        self.vertices[self.heap[-1][0]] = 0
        self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
        min_node = self.heap.pop()
        self.size -= 1
        if len(self.heap) > 1:
            self._bubble_down(0)
        return min_node

    def _bubble_up(self, idx):
        """Starts at the right most node and moves smaller weight items up the tree
        Time Complexity: O(logn)
        :param idx: the index in the heap queue
        """
        if idx < 1:
            return
        parent = MinHeap.parent(idx)
        if self.heap[idx][1] < self.heap[parent][1]:
            self.heap[idx], self.heap[parent] = self.heap[parent], self.heap[idx]
            self.vertices[self.heap[parent][0]], self.vertices[self.heap[idx][0]] = parent, idx
            self._bubble_up(parent)

    def _add_vertex(self, vertex_id, weight):
        """Creates new vertex in tree
        Time Complexity: O(logn)
        :param vertex_id: the vertex id stored in the node
        :param weight: the weight of the vertex stored in the node
        """
        self.heap.append([vertex_id, weight])
        self.vertices[vertex_id] = len(self.heap) - 1

    def update_vertex(self, vertex_id, weight):
        """
        Given a vertex id it updates the weight, it can only ever be updated to a lower weight for the min-heap invariant
        to hold true
        Time Complexity: O(logn)
        :param vertex_id: the desired vertex to update
        :param weight: the new weight of the vertex
        """
        heap_idx = self.vertices[vertex_id]
        if heap_idx is None:
            return False
        self.heap[heap_idx][1] = weight
        self._bubble_up(heap_idx)
        return True

    def is_empty(self):
        """Checks if heap is empty"""
        return self.size <= 0:


class Graph:
    def __init__(self, gfile: str) -> None:
        """
        Creates an instance of the Graph class which reads in a file and converts it to an adjacency matrix
        Pre-condition: The vertices' data is newline delimited and the data elements are space delimited - only works
        for valid input
        Time Complexity: O(V^2) where V is the number of vertices in the graph
        Auxiliary Space: O(V^2) where V is the number of vertices in the graph
        :param gfile: a text file from the current directory
        """

        with open(gfile, "r") as curr_file:
            iter_newline_delimited_lst = iter(curr_file.read().splitlines())
            self.N = int(next(iter_newline_delimited_lst))
            self.GRAPH_ADJ_MATRIX = [[None for _ in range(self.N)] for _ in range(self.N)]
            self.ADJ_LIST = [[] for _ in range(self.N)]
            for line in iter_newline_delimited_lst:
                vertex_id1, vertex_id2, weight = list(map(int, line.split()))
                self.GRAPH_ADJ_MATRIX[vertex_id1][vertex_id2], self.GRAPH_ADJ_MATRIX[vertex_id2][vertex_id1] = weight, weight
                self.ADJ_LIST[vertex_id1].append(vertex_id2)
                self.ADJ_LIST[vertex_id2].append(vertex_id1)
            for j in range(self.N):
                # no loops
                self.GRAPH_ADJ_MATRIX[j][j] = 0

    def shallowest_spanning_tree(self) -> tuple:
        """
        Finds the shallowest spanning tree given the class instance adjacency matrix (IGNORES EDGE WEIGHTS (no negative
        edges therefore))
        :return: 2-tuple which contains the vertex ID of the root as the first element and an integer that represents
        the height of the shallowest spanning tree.
        Time Complexity: O(V^3) where V is the number of vertices in the graph
        """

        dist_matrix = deepcopy(self.GRAPH_ADJ_MATRIX)
        for i in range(self.N):
            for j in range(self.N):
                if i != j:
                    if dist_matrix[i][j] is None:
                        dist_matrix[i][j] = inf
                    else:
                        # ignoring edge weights
                        dist_matrix[i][j] = 1

        # Floyd-Warshall utilised
        for vert_a in range(self.N):
            for vert_b in range(self.N):
                for vert_c in range(self.N):
                    dist_matrix[vert_b][vert_c] = min(dist_matrix[vert_b][vert_c],
                                                      dist_matrix[vert_b][vert_a] + dist_matrix[vert_a][vert_c])

        # the index of shallowest walk indicates the vertex ID of the root
        shallowest_walk = [0] * self.N
        for row_idx in range(self.N):
            for col_idx in range(self.N):
                shallowest_walk[row_idx] = max(shallowest_walk[row_idx], dist_matrix[row_idx][col_idx])

        shortest_ret_walk = min(shallowest_walk)
        return shallowest_walk.index(shortest_ret_walk), shortest_ret_walk

    def _shortest_errand_subgraph(self, beginnings: list, ends: list) -> list:
        """Finds the partial solution between significant nodes in graph"""
        ret_lst = []
        for beg in beginnings:
            for end in ends:
                ret_lst.append(self._dijkstras_algorithm(beg, end))
        return ret_lst

    def _aux_shortest_errand(self, *args) -> list:
        """Brings together all the partial solutions into one list"""
        optimal_sols = []
        for arg_idx in range(len(args)-1):
            optimal_sols.append(self._shortest_errand_subgraph(args[arg_idx], args[arg_idx + 1]))
        return optimal_sols

    def shortest_errand(self, home: int, destination: int, ice_locs: list, ice_cream_locs: list) -> tuple:
        """
        :param home: starting vertex ID
        :param destination: ending vertex ID
        :param ice_locs: list containing vertex IDs (at least one vertex) (one of these vertices must be visited
        before an ice_cream_locs IDs gets visited)
        :param ice_cream_locs: list containing vertex IDs (at least one vertex)
        :return: 2-tuple which contains the vertex ID of 'home' as the first element and the second element
        representing a list of vertices visited on the walk
        Time Complexity: O(V_i * E log(V)) where V is the number of vertices in the graph and E is the number of edges and
        V_i is the max length of destination, ice_locs, ice_cream_locs lists (i.e. number of edges)
        """
        ret_sol = (inf, [])
        unprocessed_sols = self._aux_shortest_errand([home], ice_locs, ice_cream_locs, [destination])

        for s_to_il_walk in unprocessed_sols[0]:
            for il_to_icl_walk in unprocessed_sols[1]:
                for icl_to_end_walk in unprocessed_sols[2]:
                    curr_len_walk = s_to_il_walk[0] + il_to_icl_walk[0] + icl_to_end_walk[0]
                    if curr_len_walk < ret_sol[0] and s_to_il_walk[1][-1] == il_to_icl_walk[1][0] and il_to_icl_walk[1][-1] == icl_to_end_walk[1][0]:
                        if s_to_il_walk[1][-1] == icl_to_end_walk[1][0]:
                            ret_sol = (curr_len_walk, s_to_il_walk[1][:] + icl_to_end_walk[1][1:])
                        else:
                            ret_sol = (curr_len_walk, s_to_il_walk[1][:] + il_to_icl_walk[1][1:-1] + icl_to_end_walk[1][:])

        return ret_sol

    def _get_walk(self, pred_arr: list, vert_of_interest: int) -> list:
        """
        Finds the walk given a predecessor array given from dijkstra's
        Time complexity: O(n)
        :param pred_arr: vertex predecessors from dijkstra's
        :param vert_of_interest: the desired end vertex
        :return: the walk given a walk from start vertex to end vertex
        """
        ret_walk = []
        while pred_arr[vert_of_interest] is not None and pred_arr:
            ret_walk.append(vert_of_interest)
            vert_of_interest = pred_arr[vert_of_interest]
        ret_walk.append(vert_of_interest)
        ret_walk.reverse()
        return ret_walk

    def _dijkstras_algorithm(self, start: int, end: int) -> tuple:
        """
        Straightforward implementation of dijkstra's algorithm (but terminates early when end vertex reached)
        Time Complexity: O(Elogv)
        :param start: the initial vertex that dijkstra's alg starts from
        :param start: the ed vertex that dijkstra's alg terminates at
        :return: a 2-tuple: consisting of an array for which represents the shortest walk from 'start' to vertex_id AND
        a predecessor array
        """
        if start == end: return 0, [start]
        
        def relax(u, v, edge_weight):
            temp_dist = distance[u] + edge_weight
            if temp_dist < distance[v]:
                min_heap.update_vertex(v, temp_dist)
                distance[v] = temp_dist
                predecessor[v] = u

        distance = [inf] * self.N
        predecessor = [None] * self.N
        min_heap = MinHeap(self.N)
        distance[start] = 0
        min_heap.update_vertex(start, 0)

        while not min_heap.is_empty():
            curr_min_node = min_heap.pop_min()[0]
            if curr_min_node == end: return distance[end], self._get_walk(predecessor, end)
            for edge in self.ADJ_LIST[curr_min_node]:
                relax(curr_min_node, edge, self.GRAPH_ADJ_MATRIX[curr_min_node][edge])
