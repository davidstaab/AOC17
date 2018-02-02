def new_group(graph: list) -> set:
    for i in range(len(graph)):
        if graph[i] is not None:
            return set(graph[i])
    return None


def fill_group(graph: list, to_visit: set) -> set:
    visited = set()
    while 1:
        try:  # to find a node in `to_visit` that hasn't already been visited
            curr = to_visit.pop()
            while curr in visited:
                curr = to_visit.pop()
        except KeyError:
            break
        visited.add(curr)
        to_visit.update({_ for _ in graph[curr]})
        graph[curr] = None
    return visited


if __name__ == '__main__':

    graph = []
    with open('./pipes.txt') as file:
        graph = file.readlines()
    for i, line in enumerate(graph):
        graph[i] = [int(x) for x in line.split(' <-> ')[1].split(',')]

    groups = []
    while any(graph):
        to_visit = new_group(graph)
        if to_visit is None:
            break
        groups.append(fill_group(graph, to_visit))

    print('{} groups found.'.format(len(groups)))
    for g in groups:
        print('Programs in group {}: {}'.format(min(g), len(g)))
