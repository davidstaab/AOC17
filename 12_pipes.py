if __name__ == '__main__':
    anchor_id = 0
    with open('./pipes.txt') as file:
        graph = file.readlines()
        for i, line in enumerate(graph):
            graph[i] = [int(x) for x in line.split(' <-> ')[1].split(',')]

        to_visit = {anchor_id}
        visited = set()
        while 1:
            try:
                curr = to_visit.pop()
                while curr in visited:
                    curr = to_visit.pop()
            except KeyError:
                break

            visited.add(curr)
            to_visit.update({_ for _ in graph[curr]})

        print('Programs in group {}: {}'.format(anchor_id, len(visited)))
