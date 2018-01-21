from anytree import Node, PostOrderIter, PreOrderIter
import re

file_name = './circus.txt'
list_sep = '->'
sup_list_sep = ', '


def create_child_nodes(parent: Node, children: dict, weights: dict):
    for c in children[parent.name]:
        node = Node(c, weight=weights.pop(c), cum_weight=None, parent=parent)
        create_child_nodes(node, children, weights)


def accumulate_weights(root: Node):
    for n in PostOrderIter(root):
        n.cum_weight = n.weight + sum([c.cum_weight for c in n.children])


if __name__ == '__main__':

    # PART 1
    # find name at bottom of tree. just need the one in no other name's support list.
    bases = []
    supported = []
    with open(file_name) as file:
        for line in file:
            if line.find(list_sep) >= 0:
                line_parts = line.split(list_sep)
                sup_list = line_parts[1].strip().split(sep=sup_list_sep)
                supported.extend([x for x in sup_list if x not in supported])
                bases.append(line_parts[0].strip().split()[0])
            else:
                bases.append(line.strip().split()[0])
    root_name = (set(bases) ^ set(supported)).pop()
    print('Bottom of tree: {}\n\n'.format(root_name))

    # PART 2
    # okay, fine, i'll build the damned tree.

    # scrape the file and suck its data into memory
    weights = {}
    children = {}
    with open(file_name) as file:
        for line in file:
            line_parts = line.split(list_sep)
            node_attribs = line_parts[0].strip().split()
            weights[node_attribs[0]] = int(re.search('\d+', node_attribs[1]).group(0))
            children[node_attribs[0]] = line_parts[1].strip().split(sep=sup_list_sep) if len(line_parts) > 1 else []

    # build the tree. give each node 3 attribs: name, weight, cumulative weight. start with the root element.
    root = Node(root_name, weight=weights.pop(root_name), cum_weight=None)
    create_child_nodes(root, children, weights)
    accumulate_weights(root)

    # walk it looking for the cause of an imbalance (farthest from `root`)
    bad_node = None
    walker = PreOrderIter(root)
    while 1:
        next(walker)  # throw away 'root' of this (sub)tree
        node = next(walker)
        towers = list(node.siblings) + [node]
        sibs = towers
        bad_node_found = False
        for i, t in enumerate(towers):
            sibs.pop(i)
            if all([t.cum_weight != s.cum_weight for s in sibs]):
                walker = PreOrderIter(t)  # search down this sub-tree
                bad_node = t
                bad_node_found = True
                break
        if not bad_node_found:  # bad node was in parent layer. stop searching.
            break

    if bad_node:
        print('Imbalance found.')
        print('{}: weight: {} cumulative weight: {}'.format(bad_node.name, bad_node.weight, bad_node.cum_weight))
        for s in bad_node.siblings:
            print('{}: weight: {} cumulative weight: {}'.format(s.name, s.weight, s.cum_weight))
    else:
        print('No imbalance found!')
