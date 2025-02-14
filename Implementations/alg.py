"""
Algorithms 330 Implementations
Christian J. Rudder
November 2024
"""

from typing import List, Dict # Types for List
from collections import deque # deque allows us to treat an array as a queue
import numpy as np

"""
Gale Shapely:
Matching problem between two sets A and B. A proposes to 'b' in B
from their most to least preferred. 'b' will initially accept
'a' until 'b' gets a better offer. Then 'a' will have to propose again.

Stable Matching:
is when no two pairs would rather switch partners.
If groups would rather switch partners it's an unstable matching.

Note:
- Proposers get their best choice, if there is no conflict
- If Proposers a,b both pick c, c chooses their preferred
"""

#P proposers and A acceptors both nxn in length
def gale_shapely(P: List[int], A: List[int]):
    n = len(P)
    matches = [None] * n # index: acceptor, value: proposer
    engaged = [False] * n # prospers
    all_matched = False
    while (not all_matched):
        all_matched = True
        # Loop through all proposers i
        for i in range(n):
            if engaged[i]:
                continue
            all_matched = False
            # Look at i's next preference
            # If i's pref isn't engaged they get them 
            next_pref = P[i][-1]
            if matches[next_pref] == None:
                matches[next_pref] = i
                engaged[i] = True
                P[i].pop() 
            # If i's pref is engaged, see if they
            # prefer i over their current match
            else:
                # going from least-to-most
                for j in range(n-1):
                    # if I see they see i first, ignore i
                    if A[next_pref][j] == i:
                        P[i].pop()
                        break
                    # if they see my current match, engage i
                    elif A[next_pref][j] == matches[next_pref]:
                        engaged[matches[next_pref]] = False
                        engaged[i] = True
                        matches[next_pref] = i
    return matches

"""
Time Complexity: O(n^2). Outer for-loop is O(n), if at least one
p in P isn't engaged we have to run the for-loop again. Hence, in 
worst case every p conflicts with each other. but a in A must prefer
one of them. So we are forced to run n^2 times to resolve n conflicts.

Space Complexity : O(nxn). Size of the pref lists (counting input).
"""

# set[i] is name, set[i][...] least to most preferred
hospitals: List[int] = [[1,2,0],[1,2,0],[0,2,1]] 
residents: List[int] = [[2,1,0],[0,2,1],[0,1,2],]

# residents 0,1,2 get their first choices
# print(gale_shapely(residents, hospitals)) # [0,1,2]
# hospitals get their first choice, however
# h0, h1 conflict both wanting r0, but r0 prefers h0
# print(gale_shapely(hospitals, residents)) # [0,2,1]
        
"""
Trees:
a graph G is a tree if any two statements are true:
- G is connected
- G has n-1 edges
- G has no cycles

Types of Edges in a graph:
1. Tree-edges: an edge in a BFS tree
2. Forward-edges: a non-tree-edge connecting an ancestor to a descendant
3. Backward-edges: descendant to ancestor
4. Cross-edge: connects two nodes that don't have ancestor or defendant
               connections (Does not create cycles).
"""

"""
Breadth-First Search (BFS)

Starting from a node 's', queue 's's children 'c' to visit. Once
a 'c' is visited queue their children. It's important to keep 
nodes visited to avoid adding back nodes we've already evaluated

Properties of graph 'T' produced by BFS:
- 'T' is a tree with a root node 's'
- 's' to any node 'n' in 'T' is the shortest path between them
- Any sub-paths between 's' and 'n' are also shortest paths
  eg. s-e-b-n, s-n is the shortest path from s-n, likewise with e-b
"""

# Dictionary of int keys containing a list of integers
def bfs(G: Dict[int, List[int]],s: int):
    q = deque() # queue object to dequeue with 'popleft()'
    q.append(s)
    T = {}
    visited = [False] * len(G) 
    visited[s] = True

    # Loop the queue until empty
    while q:
        p = q.popleft()
        T[p] = []
        # loop all connections
        for c in G[p]:
            # if already visited do not add to the queue or tree
            if visited[c]:
                continue
            visited[c] = True
            T[p].append(c)
            q.append(c)
    return T

"""
Time complexity: O(n+m), for 'n' nodes and 'm' edges. Each node 'n'
has 'd' connections m:= number of all 'd' connections in the table.

Space complexity: O(n+m) the input and output graph are same length.
"""

r"""
Example G:
     2   4
    / \ /
   0   3
    \ / \ 
     1   5
"""

G = {
    0: [2,1],
    1:[0,3],
    2:[0,3],
    3:[1,2,4,5],
    4:[3],
    5:[3]
    }

# print(bfs(G,0))
r"""
     2   4
    / \ /
   0   3
    \   \ 
     1   5
"""
# print(bfs(G,1))
r"""
     2   4
    /   /
   0   3
    \ / \ 
     1   5
"""
# print(bfs(G,3))
r"""
     2   4
      \ /
   0   3
    \ / \ 
     1   5
"""

"""
Depth-First-Search:
visit each branch fully (does not find longest path)
method (stack):
Process a node, then put it's children on a stack. Pop an item
from the stack then process that node. Continue till stack is empty
"""

def dfs(G: Dict[int,List[int]],s: int):
    n = len(G)
    stack = []
    T = {} # Parent table
    visited = [False] * n
    stack.append(s)
    last_node = None
    while stack:
        # print(stack)
        p = stack[-1]
        if visited[p]:
            stack.pop()
        else:
            visited[p] = True
            T[p] = last_node
            last_node = p
            for c in G[p]:
                if not visited[c]:
                    stack.append(c)
    return T
r"""
Time complexity: O(n+m), we traverse all nodes, every node we traverse we 
mark as visited, and is not added to the stack

Space complexity: O(n+m), for incoming Graph
Example G:
     2   4
    / \ /
   0   3
    \ / \ 
     1   5
"""
# print(dfs(G,0)) # 0-1-3-5-4-2

r"""
Stack:
            5  5v 
            4  4  4  4v
            2  2  2  2  2  2v
         3  3v 3v 3v 3v 3v 3v 3v 
      1  1v 1v 1v 1v 1v 1v 1v 1v 1v 
      2  2  2  2  2  2  2  2v 2v 2v 2v
    0 0v 0  0v 0v 0v 0v 0v 0v 0v 0v 0v 0v
    -------------------------------------
    0 1  2  3  4  5  6  7  8  9  10 11 12

Resulting traversal:
     2---4
         |
   0   3 |
    \ / \|  
     1   5
Which mimics the backtracking 0->1->3->5->3->4->3->2
This works because we place on the stack what is reachable from each node
essentially working as a bfs queue but we only explore one path at a time.
We keep track what path/nodes have already been visited

"""

H = {
    0: [2,1],
    1: [4,3],
    2: [5],
    3: [],
    4: [],
    5: []
}
r"""
      0
     / \
    1   2
   / \   \
  3   4   5
"""        
# print(dfs(H,0)) # 0-1-3-4-2-5
"""
[0]
[0v, 2, 1]
[0v, 2, v1, 4, 3]
[0v, 2, v1, 4, 3v]
[0v, 2, v1, 4]
[0v, 2, v1, 4v]
[0v, 2, v1]
[0v, 2]
[0v, 2v, 5]
[0v, 2v, 5v]
[0v, 2v]
[0v]
"""

r"""
Topological Sort:

A topological sort can be given to DAGs, meaning there's an 
order to nodes. Like putting on clothes

underwear->pants--\
shirt->hoodie------> school
socks->shoes------/

possible orderings:
underwear->pants->shirt...
shirt->socks->hoodie...
underwear->shirt->socks...

using our DFS stack method we can obtain the topological sort 
tracing our backtracking. This tells us, what comes before what,
we should finish processing the final node at the end of our algorithm.
"""

# assuming connected graph and s is the only node with no incoming degrees
def dfs_top(G: Dict[int,List[int]],s: int):
    n = len(G)
    stack = []
    proc = [] # processed stack
    visited = [False] * n
    processed = [False] * n
    stack.append(s)
    while stack:
        # print(stack)
        p = stack[-1]
        if visited[p]:
            if not processed[p]:
                proc.append(p)
                processed[p] = True
            stack.pop()
        else:
            visited[p] = True
            for c in G[p]:
                if not visited[c]:
                    stack.append(c)
    reverse_stack = []
    for _ in range(n):
        reverse_stack.append(proc.pop())
    return reverse_stack
"""
time complexity: O(n+m). Still the same dfs, just that we are evaluating it
differently
space complexity: O(n+m)
"""

J = {
    0: [2,1],
    1: [3],
    2: [1,4],
    3: [],
    4: []
}
K = {
    0: [1,2],
    1: [3],
    2: [1,4],
    3: [],
    4: []
}
# Figure 3.15 does not with the current implementation, 
# as 1,3,5 are disjoint starting points
# L = {
#     1: [2,4],
#     2: [],
#     3: [4,7],
#     4: [],
#     5: [7,6],
#     6: [7],
#     7: []
# }
        
"""
left to right directed graph
  /-1-3
 / /
0-2--4

possible valid orderings 0-2-1-3-4 or 0-2-4-1-3
"""

# print(dfs_top(J,0)) # 0-2-4-1-3
# print(dfs_top(K,0)) # 0-2-1-3-4



"""
classes in python
__init__: is the constructor function, each function needs 
self as the first parameter to refer to the class itself. Similar to 
'this' is java and other languages.
__str__: is the toString for the class
"""

class Dog:
    # optional typing
    name: str
    age: int
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def bark(self):
        print(f"{self.name}, says a-woof-a-doodle-doo!")
    def __str__(self):
        return f"This dog's ol' name is {self.name}, {self.age}yrs of age~"

# cool_dog = Dog("Reinhardt", 5)
# cool_dog.bark()
# print(cool_dog)

r"""
Min-Max Heaps:
- complete binary tree (binary and balanced)
- Min heaps: nodes with lesser values live at the top
- Max heaps: nodes with higher values live at the top
Functions:
- PEEK: Return root       O(1)
- INSERT: Add new element O(log n)
- EXTRACT: Remove root    O(log n)
- UPDATE: Update a node   O(log n)

Heap Structure:
        10
       /  \
     15    20
    /  \
  17   25

Array Representation: [10, 15, 20, 17, 25]
for index i
'//':= integer division (floor division)
- Left Child:  (2*i)+1
- Right Child: (2*i)+2
- Parent:      (index-1) // 2

Pseudo Code min-heap:
H <- is our array
PEEK: return H[0]
INSERT: 
    - add to the end of the array
    - keep swapping with parent if parent it's smaller
DELETE: 
    - add to the end of the array
    - swap with H[0]
    - keep swapping with children who are smaller
EXTRACT:
    - return H[0] and DELETE it in H
UPDATE:
    - update element at index i
    - if the new value is smaller than the old value
      preform swaps with parents who might be larger
      else, preform swaps with children who might be smaller

This is all log n because the height of a balance tree is log n where
n is the number of nodes.
"""


class MinHeap:
    def __init__(self):
        """Initialize an empty heap."""
        self.heap = []

    def _parent(self, index):
        """Get the parent index."""
        return (index - 1) // 2

    def _left_child(self, index):
        """Get the left child index."""
        return 2 * index + 1

    def _right_child(self, index):
        """Get the right child index."""
        return 2 * index + 2

    def _swap(self, i,j):
        # This syntax avoids having to make a temp variable
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def _heapify_up(self, index):
        """Maintain heap property after insertion."""
        while index > 0: # Stop if at root
            parent = self._parent(index)
            if self.heap[index] < self.heap[parent]:
                # Swap if current node is smaller than the parent
                self._swap(index, parent)
                index = parent
            else:
                break
      
    def _heapify_down(self, index):
        """Maintain heap property after deletion."""
        size = len(self.heap)
        while True:
            left = self._left_child(index)
            right = self._right_child(index)
            smallest = index # Assume the current node is the smallest

            if left < size and self.heap[left] < self.heap[smallest]: # Compare with left child
                smallest = left
            if right < size and self.heap[right] < self.heap[smallest]: # Compare with right child
                smallest = right

            if smallest != index:
                # Swap with the smaller child
                self._swap(index, smallest)
                index = smallest # repeat with the newly swapped position
            else:
                break

    def insert(self, value):
        """Insert a value into the heap."""
        self.heap.append(value)  # Add the value to the end
        self._heapify_up(len(self.heap) - 1)  # Restore heap property

    def update(self, index, new_value):
        """Update a value at a given index."""
        if 0 <= index < len(self.heap):
            old_value = self.heap[index]
            self.heap[index] = new_value
            # If the new value is smaller, heapify up
            if new_value < old_value:
                self._heapify_up(index)
            # If the new value is larger, heapify down
            else:
                self._heapify_down(index)
        else:
            raise IndexError("Index out of range.")

    def delete(self, index):
        """Delete a value at a given index."""
        if 0 <= index < len(self.heap):
            # Swap with the last element and remove it
            self._swap(index,-1)
            self.heap.pop()
            # Restore heap property
            if index < len(self.heap):
                self._heapify_down(index)
        else:
            raise IndexError("Index out of range.")

    def extract_min(self):
        """Extract the minimum value (root) from the heap."""
        if len(self.heap) == 0:
            raise IndexError("Heap is empty.")
        min_value = self.heap[0]
        self.delete(0)
        return min_value

    def __str__(self):
        """String representation of the heap."""
        return str(self.heap)

class MaxHeap:
    def __init__(self):
        """Initialize an empty heap."""
        self.heap = []

    def _parent(self, index):
        """Get the parent index."""
        return (index - 1) // 2

    def _left_child(self, index):
        """Get the left child index."""
        return 2 * index + 1

    def _right_child(self, index):
        """Get the right child index."""
        return 2 * index + 2

    def _swap(self, i,j):
        # This syntax avoids having to make a temp variable
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def _heapify_up(self, index):
        """Maintain heap property after insertion."""
        while index > 0: # Stop if at root
            parent = self._parent(index)
            if self.heap[index] > self.heap[parent]:
                # Swap if current node is greater than the parent
                self._swap(index, parent)
                index = parent
            else:
                break
      
    def _heapify_down(self, index):
        """Maintain heap property after deletion."""
        size = len(self.heap)
        while True:
            left = self._left_child(index)
            right = self._right_child(index)
            largest = index # Assume the current node is the greatest

            if left < size and self.heap[left] > self.heap[largest]: # Compare with left child
                largest = left
            if right < size and self.heap[right] > self.heap[largest]: # Compare with right child
                largest = right

            if largest != index:
                # Swap with the smaller child
                self._swap(index, largest)
                index = largest # repeat with the newly swapped position
            else:
                break

    def insert(self, value):
        """Insert a value into the heap."""
        self.heap.append(value)  # Add the value to the end
        self._heapify_up(len(self.heap) - 1)  # Restore heap property

    def update(self, index, new_value):
        """Update a value at a given index."""
        if 0 <= index < len(self.heap):
            old_value = self.heap[index]
            self.heap[index] = new_value
            # If the new value is greater, heapify up
            if new_value > old_value:
                self._heapify_up(index)
            # If the new value is smaller, heapify down
            else:
                self._heapify_down(index)
        else:
            raise IndexError("Index out of range.")

    def delete(self, index):
        """Delete a value at a given index."""
        if 0 <= index < len(self.heap):
            # Swap with the last element and remove it
            self._swap(index,-1)
            self.heap.pop()
            # Restore heap property
            if index < len(self.heap):
                self._heapify_down(index)
        else:
            raise IndexError("Index out of range.")

    def extract_min(self):
        """Extract the minimum value (root) from the heap."""
        if len(self.heap) == 0:
            raise IndexError("Heap is empty.")
        min_value = self.heap[0]
        self.delete(0)
        return min_value

    def __str__(self):
        return str(self.heap)


"""
Interval scheduling:
When we have a list of jobs, with start and finish times. Our job 
is to find the largest subset of jobs without conflict

Our strategy (Earliest Finish Time [EFT]):
    - Sort schedules in ascending order  
    - Keep taking the next earliest finish time
EFT works as each interval there is some deadline. We want to start 
collecting as many jobs as possible, so we start with the one that 
finishes first. This will give us more opportunity to collect.


If job 'i' is what we pick and job 'j' is optimal 
and both are interchangeable within an interval-deadline. Then 'i' 
is also an optimal solution.

Recursively do this for each interval and we achieve an optimal like solution.
"""

def insertion_sort(A):
    for i in range(1, len(A)):
        j = i
        while j >= 1:
            if A[j] < A[j-1]:
                A[j],A[j-1] = A[j-1],A[j]
            else:
                break
            j-=1

# arr = [2,4,1,10,5,3]
# print(arr)
# insertion_sort(arr)
# print(arr)

def interval_est_sort(A):
    """Sorting by earliest start time using insertion sort"""
    for i in range(1, len(A)):
        j=i
        while j >=1:
            # tuples (start, finish)
            if A[j][0] < A[j-1][0]:
                A[j], A[j-1] = A[j-1], A[j]
            elif A[j][0] == A[j-1][0] and A[j][1] < A[j-1][1]:
                A[j], A[j-1] = A[j-1], A[j]
            j-=1
def interval_eft_sort(A):
    """Sorting by earliest finish using insertion sort"""
    for i in range(1, len(A)):
        j=i
        while j >=1:
            # tuples (start, finish)
            if A[j][1] < A[j-1][1]:
                A[j], A[j-1] = A[j-1], A[j]
            elif A[j][1] == A[j-1][1] and A[j][0] < A[j-1][0]:
                A[j], A[j-1] = A[j-1], A[j]
            j-=1

# (start, finish)     
times = [(4,7),(3,8),(0,6),(8,11),(1,4),(6,10),(5,9),(3,5)]
# interval_est_sort(times)
# print(times)
# interval_eft_sort(times)
# print(times)
def is_compatible(i,j):
        if i[0] == j[0]:
            return False
        comes_first, comes_second = (i, j) if i[0] < j[0] else (j, i)
        return comes_first[1] <= comes_second[0]

def interval_schedule(L):
    interval_eft_sort(L)
    sol = []
    sol.append(L[0])
    last_compatible = 0
    for i in range (1,len(L)):
        if is_compatible(L[last_compatible],L[i]):
            sol.append(L[i])
            last_compatible = i 
    return sol
"""
(For this Algorithm)
Time complexity: O(n^2). Bottle necked by choosing insertion sort for 
sorting. Would be O(n log n) if merge sort were used. The routine takes 
O(n), if we assumed the array is already sorted by earliest finish time

Space complexity: O(n). We store n tuples and return at most n of them.
"""

# Figure 4.3
# print(interval_schedule(times)) #[(1, 4), (4, 7), (8, 11)]

"""
Interval Partitioning:
Say you have n classes and k classrooms. You want to find the the best
set such that we utilize the least amount of k classrooms to hold n classes.

Formally, given j jobs and k resources, run j jobs without conflict
allocating the minimum resources needed.

Strategy: Earliest Start Time First [EST]
- sort in EST
- if there's a conflict allocate a new resource
"""
        
def interval_partition_schedule(L):
    interval_est_sort(L)
    resources = [[]]
    resources[0].append(L[0])
    # Go through each class
    for i in range(1,len(L)):
        found_space = False
        # Compatible with any of the present resources?
        for r in resources:
            if is_compatible(r[-1], L[i]):
                r.append(L[i])
                found_space = True
                break
        if not found_space:
            resources.append([L[i]])
    return resources

"""
Time Complexity: O(n^2). Ignoring our sorting algorithm it's still O(n^2).
As in the worst case no job is compatible with each other, creating a new
resource. We iterate n jobs, then we follow the arithmetic sum, as we 
iterate over each r resource, which will increase by 1 each iteration.

Space Complexity: O(n). Input of n items and despite creating some 2D
structure, we never have to allocate any more space than n in either 
direction.
"""

# Figure 4.4
# classes = [(4,10),(8,11),(10,15),(12,15),(0,7),(4,7),(12,15),(0,3),(8,11),(0,3)]
# schedule = interval_partition_schedule(classes)

# for i in range(len(schedule)):
#     print(f"{i}: {schedule[i]}")

"""
Minimizing Lateness:

When forced to use a single recourse we might still want to run every task,
but minimize how many deadlines we pass.

Just like in a fast paste kitchen, all dishes must get done. Some will be 
prepared late, but all will be prepared. We want to minimize this lateness.

Strategy: Earliest Finish Time first (EFT)(Earliest Deadline)
    that's it.

Why? Say you have to clean your room completely by 'l' time. You are confused whether to
clean your bed first or your desk. The desk takes 'd' time and the bed takes 'b' time. Whether
you choose to clean your bed or your desk first, does not make a difference, as 'd + b' will always
be the same.
"""
"""
Time complexity: O(n^2), because we chose insertion sort. best is O(n log n)
with merge-sort.

Space complexity: O(n), the incoming list.
"""
# Figure 4.7
# tasks = [(3,14),(2,8),(2,15),(1,9),(4,9),(3,6)]
# interval_eft_sort(tasks)
# print(tasks)
class TupleMinHeap:
    def __init__(self):
        """Initialize an empty heap."""
        self.heap = []

    def get(self):
        return self.heap
    def _parent(self, index):
        """Get the parent index."""
        return (index - 1) // 2

    def _left_child(self, index):
        """Get the left child index."""
        return 2 * index + 1

    def _right_child(self, index):
        """Get the right child index."""
        return 2 * index + 2

    def _swap(self, i,j):
        # This syntax avoids having to make a temp variable
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def _heapify_up(self, index):
        """Maintain heap property after insertion."""
        while index > 0: # Stop if at root
            parent = self._parent(index)
            if self.heap[index][0] < self.heap[parent][0]:
                # Swap if current node is smaller than the parent
                self._swap(index, parent)
                index = parent
            else:
                break
      
    def _heapify_down(self, index):
        """Maintain heap property after deletion."""
        size = len(self.heap)
        while True:
            left = self._left_child(index)
            right = self._right_child(index)
            smallest = index # Assume the current node is the smallest

            if left < size and self.heap[left][0] < self.heap[smallest][0]: # Compare with left child
                smallest = left
            if right < size and self.heap[right][0] < self.heap[smallest][0]: # Compare with right child
                smallest = right

            if smallest != index:
                # Swap with the smaller child
                self._swap(index, smallest)
                index = smallest # repeat with the newly swapped position
            else:
                break

    def insert(self, value):
        """Insert a value into the heap."""
        self.heap.append(value)  # Add the value to the end
        self._heapify_up(len(self.heap) - 1)  # Restore heap property

    def update(self, index, new_value):
        """Update a value at a given index."""
        if 0 <= index < len(self.heap):
            old_value = self.heap[index]
            self.heap[index] = new_value
            # If the new value is smaller, heapify up
            if new_value[0] < old_value[0]:
                self._heapify_up(index)
            # If the new value is larger, heapify down
            else:
                self._heapify_down(index)
        else:
            raise IndexError("Index out of range.")

    def delete(self, index):
        """Delete a value at a given index."""
        if 0 <= index < len(self.heap):
            # Swap with the last element and remove it
            self._swap(index,-1)
            self.heap.pop()
            # Restore heap property
            if index < len(self.heap):
                self._heapify_down(index)
        else:
            raise IndexError("Index out of range.")

    def extract_min(self):
        """Extract the minimum value (root) from the heap."""
        if len(self.heap) == 0:
            raise IndexError("Heap is empty.")
        min_value = self.heap[0]
        self.delete(0)
        return min_value

    def __str__(self):
        """String representation of the heap."""
        return str(self.heap)

def dijkstra(G,s):
    """
    Dijkstra's Algorithm:
    find shortest path from node 's' to all other nodes in a graph
    """
    n = len(G)
    distances = [np.inf] * n # list of shortest paths for each node
    parents = [None] * n     # parent child table
    visited = [False] * n    # check if we've already evaluated a node
    q = TupleMinHeap()       # minHeap to track next shortest path
    q.insert((0,s))
    distances[s] = 0
    while q.get():
        # pop off heap
        dist,node = q.extract_min()
        visited[node] = True
        # add neighbors which have not been visited
        for c in G[node]:
            # adding total path length to next path
            next = (dist+c[0],c[1])
            if not visited[c[1]]:
                q.insert(next)
                if next[0] < distances[next[1]]:
                    distances[next[1]] = next[0]
                    parents[next[1]] = node
    return distances, parents

"""
Time complexity: O(mlog(n)). For 'm' edges and 'n' nodes. Since in our BFS
approach we visit all edges. For every new edge, we insert into our queue
which takes log(n) time.

Space complexity: (n+m)
"""

# G[node][(weight,node)]
# a=0, b=1, c=2,...
# Figure 5.3
G = {
    0: [(10,1),(3,2)],
    1: [(1,0),(2,3)],
    2: [(4,1),(2,4),(8,3)],
    3: [(7,4)],
    4: [(9,3)]
}

# Figure 5.2
H = {
    0: [(2,1),(10,5)],
    1: [(10,2)],
    5: [(2,4)],
    2: [(10,3)],
    3: [(10,2),(2,4)],
    4: [(2,3)]
    
}

# print(dijkstra(G,0))
# print(dijkstra(H,0))

def prims(G,s):
    """
     Prim's algorithm:
     finds the Minimal Spanning Tree (MST)
     Strategy:
         The same as dijkstra, except for the relax function.
         (Relax meaning, smoothing out the graph, like in spinning
         pottery, we relax the clay to get a desired shape).
         here we want to find minimum edges so we don't 
         care about keeping track of the accumulated weights
     """
    n = len(G)
    distances = [np.inf] * n # list of shortest paths for each node
    parents = [None] * n     # parent child table
    visited = [False] * n    # check if we've already evaluated a node
    q = TupleMinHeap()       # minHeap to track next shortest path
    q.insert((0,s))
    distances[s] = 0
    # (weight, node)
    while q.get():
        dist,node = q.extract_min()
        visited[node] = True
        for c in G[node]:
            #in dijkstra's we do (dist+c[0],c[1])  
            if not visited[c[1]]: 
                q.insert(c)
                if c[0] < distances[c[1]]:
                    distances[c[1]] = c[0]
                    parents[c[1]] = node
    return parents
"""
Time complexity: O(m log n), or O((n+m) log n) if disconnected. Logic applies
the same as Dijkstra's

Space complexity: O(n+m), the incoming graph
"""

# Figure 5.8
K = {

    0: [(3,1),(10,5),(8,2)],
    1: [(3,0),(14,2)],
    2: [(14,1),(8,0),(6,3),(5,4)],
    3: [(6,2),(12,4)],
    4: [(12,3),(5,2),(9,6),(7,5)],
    5: [(7,4),(15,7),(10,0)],
    6: [(9,4)],
    7: [(15,5)]
}
# print(dijkstra(K,0))
# print(prims(K,0))

r"""
        (3)
       /  \
      6   12
     /      \
    (2)--5--(4)-9-(6)
    | \      |
    14 \     7
    |   8   (5)-15-(7)
    (1)  \   |
     \-3-(0)-10
"""
"""
0:null, 
1:0,
2:0,
3:2,
4:2,
5:4,
6:4,
7:5
"""       

#Page 54
class UnionFind():
    """
    Forest Data structure: 
    What do you call a group of pair-wise disjoint trees? A forest!
    (to me this wasn't obvious at first, and I found it very funny)
    """

    def __init__(self, elements=None, is_compressed=True):
        """
        Initializes Dictionary (Hash-table) and optionally 
        takes an array of elements.
        """
        self.is_compressed=is_compressed
        self.forest = {}
        if elements:
            for e in elements:
                self.forest[e] = {"rep": e, "len": 1}

    def get(self):
        """Get forest"""
        return self.forest

    def append(self, e): 
        """Add a tree to the forest"""
        self.forest[e] = {"rep": e, "len": 1}
    
    def union(self, a,b):
        """Union two trees in the forest O(log n)"""

        al, bl = self.forest[a]["len"], self.forest[b]["len"]
        if al > bl:
            self.forest[b]["rep"] = a
            
        else:
            self.forest[a]["rep"] = b
            
        self.forest[a]["len"] = bl + al
        self.forest[b]["len"] = bl + al
    
    def find(self, e):
        """
        Find an element's leader, compress graph after the find.
        This means settings e's rep directly to its leader
        O(log n)
        """
        traversed = False
        old = self.forest[e]["rep"]
        who = self.forest[e]["rep"]
        while(self.forest[who]["rep"] != who):
            traversed = True
            who = self.forest[who]["rep"]
        # Compress
        
        if traversed and self.is_compressed:
            # Update the old leader's new party length
            self.forest[e]["rep"] = who
        return who
    def give(self, e, d):
        """Give element a data to hold onto"""
        self.forest[e]["data"] = d

    def parents(self):
        """Returns a (index:child, value: parent) array"""
        p = {}
        for i in self.forest:
            p[i] = self.forest[i]["rep"]
        return p
    def data(self):
        """Returns a (index:node, value: data) array"""
        p = {}
        for i in self.forest:
            p[i] = self.forest[i]["data"]
        return p

    def __str__(self):
        """String representation of forest"""
        return str(self.forest)

# Figure 5.10
# E = ['a','b','c','d','e']
# T = UnionFind(E, False) # with no compression
# print(T.parents()) #1.
# T.union('b','a') 
# T.union('d','c')
# print(T.parents()) #2. 
# T.union('c','a')
# print(T.parents()) #3.
# T.union('e','d')
# print(T.parents()) #4.
# T.find('e')
# print(T.parents())

# R = UnionFind(E, True) # with compression
# R.union('b','a') 
# R.union('d','c')
# R.union('c','a')
# R.union('e','d')
# print(R.parents())
# R.find('e')
# print(R.parents()) # e is now compressed to a

def kruskals(G):
    """
    Kruskal's algorithm:
    Find MST by sorting edges, adding them to a forest for n-1,
    we know to break early at n-1 iterations.

    Strategy: 
    We know the MST contains the lightest nodes. So if we order 
    the lightest nodes, and add willy-nilly we should get our MST.

    Constraints:
        - We don't add an edge if it doesn't create a new connection to 
          a node outside of the MST we are generating
        We can track this with a UnionFind data structure. This will tell 
        us if a node is already part of a group
    """
    edges = TupleMinHeap()
    keys = list(G.keys())
    T = UnionFind(keys)
    MST = {}
    for v in G:
        MST[v] = []
        for u in G[v]:
            # (weight, parent, child)
            edges.insert((u[0],v,u[1]))
    W = len(edges.get())
    i = 0
    while(i < W) and (i < len(G)):
        w,v,u = edges.extract_min()
        if T.find(v) != T.find(u):
            T.union(v,u)
            MST[v].append(u)
    return MST


# Figure 5.8
# parent: (weight, child)
K = {

    0: [(3,1),(10,5),(8,2)],
    1: [(3,0),(14,2)],
    2: [(14,1),(8,0),(6,3),(5,4)],
    3: [(6,2),(12,4)],
    4: [(12,3),(5,2),(9,6),(7,5)],
    5: [(7,4),(15,7),(10,0)],
    6: [(9,4)],
    7: [(15,5)]
}
r"""
        (3)
       /  \
      6   12
     /      \
    (2)--5--(4)-9-(6)
    | \      |
    14 \     7
    |   8   (5)-15-(7)
    (1)  \   |
     \-3-(0)-10
"""

# print(kruskals(K))

"""
-----------------DYNAMIC PROGRAMMING-----------------
The act of utilizing memoization to build a solution
memoization: storing previous recurvie calls
"""

def plain_fib(n):
    """Recursive Fibinocci"""
    if n <= 1:
        return n
    else:
        return plain_fib(n-1) + plain_fib(n-2)
"""
Time complexity: O(2^n). The two calls depend on each other, therefore
T(n) = T(n-1) + T(n-2) + O(1). We iterate n times to the base case twice,
hence O(2^n) calls.
"""

# print(plain_fib(38)) # Super Slow!!!

def memo_fib(n):
    """Memo Fibinocci"""
    M = {}
    def rec(m):
        # If already in the table reuse the value
        if m in M:
            return M[m]
        if m <= 1:
            return m
        M[m] = rec(m-1) + rec(m-2)
        return M[m]
    rec(n)
    return M[n]
"""
Time complexity: O(n). We only need to compute each recursive call once.
We start with n, and keep going to the base case. Every other call is some
combination of calls we've made before.

Space complexity: O(n). For the levels of recursion on the stack.
"""

# print(memo_fib(100)) #Way Faster

def fib(n):
    """
    Bottom-up Approach Fibinocci:
    In bottom up we must first state our base cases in our 
    memo-table. Then preform our recursive steps, building off of 
    our memo
    """
    M = [0] * (n+1) # we know there's only n levels of recursion
    M[0] = 0
    M[1] = 1
    for i in range(2,n+1):
        M[i] = M[i-1] + M[i-2]
    return M[n]
"""
Time complexity: O(n).
Space complexity: O(n).
"""
# print(fib(100))

"""
Weighted interval Scheduling:

say we have n paying jobs which overlap each other. We want to find 
the best set of jobs to maximize our profits.

This differs from interval scheduling of just grabbing the most jobs,
as any one job could be worth more than a group.

We state our sub-problems (going from n->0):
    - base case: return 0 if i < 0
    - choices: 
        * take this job gain its value 
        * take the next job, gain its value

    recursive formula:
    OPT(i)= {
        if i < 0: return 0
        max{value+OPT(next_compatible_job),OPT(i-1)}
    }
"""

def next_compatible(S,i):
    for j in range(i,len(S)):
        if is_compatible(S[i],S[j]):
            return j 
    return -1
def weighted_interval_schedule(S):
    """
    Time complexity: O(n); Space complexity: O(n)
    """
    n = len(S)
    M = [None] * n # adding the base case shifts over our array
    M[0] = 0
    interval_eft_sort(S)
    print(S)
    for i in range(1, n):
        compatible = next_compatible(S,i)
        # add the next compatible, if there's none, add 0
        build = S[compatible][2] if compatible > -1 else 0
        next = M[i-1]
        print(f"i:{i} compat: {compatible} i+j: ({S[i][2]} + {S[compatible][2]}) build: {build}, next: {next}")
        M[i] = max(S[i][2]+build, next)
    return M

# Decided to spare my time on implementing the compatible find backwards
# def wis_backtrack(S,M): 
#     n = len(M)-1
#     sol = []
#     while n > 0:
#         ...
#     return sol
#(start, finish, value)
# Figure 8.2, though zero-indexed
S = [
    (1,4,10),  
    (3,5,4),   
    (0,6,3),   
    (4,7,12),  
    (3,8,3),   
    (5,9,15),  
    (6,10,9),  
    (8,11,8)   
    ]
# A = weighted_interval_schedule(S)
# print(A)

#p84
def subset_sum(A, W):
    """
    Subset Sum (Weighted Ceiling)
    Given a set of integers, say S = {3, 6, 1, 7, 2}, 
    and a target sum T = 9, find the max subset P
    of S, such that P ≤ T .

    2d problems, 2d combinations
    we track both weight and index
    """
    n = len(A)
    # Don't do this VVVVV it makes all rows reference the same array
    # M = [[0] * (W+1)] * (n + 1)
    M = [[0] * (W+1) for _ in range(n + 1)]

    # A-1 because i starts counting too far
    for i in range(1, n + 1):
        for w in range(1, W + 1):
            if A[i-1] > w:
                M[i][w] = M[i-1][w]
            else:
                M[i][w] = max(A[i-1] + M[i-1][w-A[i-1]], M[i-1][w])

    return M

"""
Time complexity: O(nW). 
"""

def subset_sum_backtrack(A,M):
    sol = []
    i = len(M)-1 

    W = len(M[-1])-1
    # print(A)
    while i > 0:
        # print (f"M[{i}][{W}] > M[{i-1}][{W}]: {M[i][W]} > {M[i-1][W]} ")
        if(M[i][W] > M[i-1][W]):
            sol.append(A[i-1])
            W -= A[i]
        i -= 1
    return sol

arr = [2,7,1,6,3]

# S = subset_sum(arr, 9)
# print(subset_sum_backtrack(arr,S))


def unbounded_knapsack(A, W):
    """
    Unbounded Knapsack:
        Subset sum, but each item can be taken infinitely and has 
        a value to be taken.
    """
    n = len(A)
    M = [[0] * (W + 1) for _ in range(n+1)]
    
    for i in range(1,(n+1)):
        for w in range(1,(W+1)):
            v = A[i-1][0]  # value
            wi = A[i-1][1] # weight
            if wi > w:
                M[i][w] = M[i-1][w]
            else:
                M[i][w] = max(v + M[i][w-wi], M[i-1][w]) 
    return M
"""
Time complexity: O(nW). 
"""

def unbounded_knapsack_backtrack(A,M):
    sol = []
    W = len(M[-1])-1

    i = len(A)-1
    while i > 0:
        v = A[i-1][0]
        wi = A[i-1][1]
        if W >= wi and (v + M[i-1][W] > M[i-1][W]):
            sol.append(A[i-1])
            W -= wi
        else:
            i -= 1
    return sol

#(value, weight)
arr = [(1,1),(6,2),(18,5),(22,6),(28,7)]
# U = unbounded_knapsack(arr,11)
# for u in U:
#     print(u)

# print(unbounded_knapsack_backtrack(arr,U))















        





