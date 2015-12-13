Program uses input.txt as input file stream.
After that it parses input stream to a hash table which contains coordinates of the states and whitespace charaters.
Using a priority queue it makes an A* Search with Manhattan Dis. heuristic.
Node function Object class' and Uniform node class' cmp function overwritten to adapt them to priority queue.
After that program creates a hash table to store shortest paths and find solutions accordingly BFS and UCS algorithms.