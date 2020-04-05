import networkx as nx
from networkx.algorithms.traversal.depth_first_search import dfs_edges
from networkx.algorithms.dag import dag_longest_path


def largest_distance(my_graph):
    """
    Function which takes a graph and returns a tuple containing:
    1. the maximum degree of separation between any two vertices
    2. a set of all pairs of vertices whose separation is maximum
    
    Arguments:
    ----------
    my_graph : nx.Graph
        - graph for which we want to find the pairs of nodes which have the highest degree of separation
    
    Returns:
    --------
    (tuple) 
        - maximum degree of separation, set of pairs of vertices whose separation is maximum
    """
    assert str(type(my_graph)) == "<class 'networkx.classes.graph.Graph'>"
    
    #keep track of highest degree of separation
    largest_nodes_set = set()
    largest_distance = 0

    for node, dict_of_distances in nx.shortest_path_length(my_graph):
        
        #keep track of highest degree of separation for current node
        max_node_distance = 0
        furthest_nodes_from_node = set()
        
        #check degree of separation with other nodes, form new set if greater than current max degree of separation
        for other_node, distance in dict_of_distances.items():
            
            if distance > max_node_distance:
                max_node_distance = distance
                new_pair = tuple(sorted((node, other_node)))
                furthest_nodes_from_node = {new_pair}
            
            #add pair of notes to set if equal to current max degree
            elif distance == max_node_distance and distance:
                new_pair = tuple(sorted((node, other_node)))
                furthest_nodes_from_node.add(new_pair)
        
        #check if max degree of seperation for this node is greater than overall max degree of separation
        #form new set if greater than current max degree of separation
        if max_node_distance > largest_distance:
            largest_distance = max_node_distance
            largest_nodes_set = furthest_nodes_from_node
        #add pairs of nodes to set if equal to current max degree of separation
        elif max_node_distance == largest_distance:
            largest_nodes_set = largest_nodes_set | furthest_nodes_from_node

    return largest_distance, largest_nodes_set


def get_sequences(my_graph):
    """
    Takes a graph and returns sequences of nodes of all connected components.

    Arguments
    ---------
    event_graph : nx.Graph
        - graph object

    Returns
    -------
    list of lists
    """
    sequences = []
    for connected_comp in list(nx.connected_components(my_graph)):
        graph = my_graph.subgraph(connected_comp)
        nodes = largest_distance(my_graph)
        if nodes[0] != 0:
            path = nx.shortest_path(my_graph,
                                    source=list(nodes[1])[0][0], 
                                    target=list(nodes[1])[0][1])

            sequences.append(path)
    
    return sequences