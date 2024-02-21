class Arc: #дуга
    def __init__(self, begin, end):
        self.begin = begin
        self.end = end

class Vertex: #вершина
    def __init__(self, index, mark):
        self.mark = mark
        self.index = index

class Graph:
    def __init__(self):
        self.arcs = []
    def first(self, v):
        list_of_v = []
        for arc in self.arcs:
            if arc.begin.index == v:
                list_of_v.append(arc.end.index)
            elif arc.end.index == v:
                list_of_v.append(arc.begin.index)
        return min(list_of_v) if list_of_v else None
    def next(self, v, i):
        list_of_v = []
        for arc in self.arcs:
            if arc.begin.index == v and arc.end.index >= i:
                list_of_v.append(arc.end.index)
            elif arc.end.index == v and arc.begin.index >= i:
                list_of_v.append(arc.begin.index)
        return min(list_of_v) if list_of_v else None
    def vertex(self, v, i):
        for arc in self.arcs:
            if arc.begin.index == i and arc.end == v:
                return arc.begin
            elif arc.end.index == i and arc.begin == v:
                return arc.end
        return None
    def add_v(self, i, mark, place_to_add):
        new_arc = Arc(Vertex(index=place_to_add, mark=""), Vertex(index=i, mark=""))
        self.arcs.append(new_arc)
    def add_e(self, v, w):
        arc = Arc(Vertex(v, ""), Vertex(w, ""))
        self.arcs.append(arc)
    def del_v(self, i):
        for arc in self.arcs:
            if arc.begin.index == i or arc.end.index == i:
                self.arcs.remove(arc)
    def del_e(self, v, w):
        for arc in self.arcs:
            if arc.begin.index == v and arc.end.index == w:
                self.arcs.remove(arc)
    def edit_v(self, index, mark):
        for arc in self.arcs:
            if arc.begin.index == index:
                arc.begin.mark = mark
            if arc.end.index == index:
                arc.end.mark = mark
    def v_count(self):
        verts = []
        for arc in self.arcs:
            if arc.begin.index not in verts:
                verts.append(arc.begin.index)
            if arc.end.index not in verts:
                verts.append(arc.end.index)
        return len(verts)
    def dfs(self, v, visited):
        j = self.first(v)
        while j != None:
            if visited[j] != True:
                visited[j] = True
                self.dfs(j, visited)
            j = self.next(v, j + 1)

T = Graph()
T.add_e(1, 2)
T.add_e(1, 3)
T.add_e(1, 6)
T.add_e(3, 5)
T.add_e(5, 7)
T.add_v(7, "mark", 6)
T.add_v(4, "mark", 6)
T.add_e(4, 8)
T.add_v(8, "mark", 7)
component_1 = 0
visited_1 = [0] * (T.v_count()+1)

G = Graph()
G.add_e(1, 2)
G.add_e(1, 3)
G.add_e(1, 4)
G.add_e(3, 2)
G.add_e(2, 8)
G.add_v(7, "mark", 8)
G.add_v(6, "mark", 7)
G.add_e(6, 5)
G.add_v(4, "mark", 5)
component_2 = 0
visited_2 = [0] * (G.v_count()+1)

def cyclomatic_complexity(T: Graph, visited, component):
    for i in range(1, T.v_count()+1):
        if not visited_1[i]:
            visited[i] = True
            component += 1
            T.dfs(i, visited)
    M = len(T.arcs) - T.v_count() + component
    return M

print("Цикломатическая сложность 1-го графа: ", cyclomatic_complexity(T, visited_1, component_1))
print("Цикломатическая сложность 2-го графа: ", cyclomatic_complexity(G, visited_2, component_2))