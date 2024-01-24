from Node import Node
import Player
import random, pygame


class Graph:
    def __init__(self, player):

        self.start = Node(0, 0, 0, self)
        self.nodes = {self.start : self.start}
        self.edge_nodes = [self.start]

        self.player = player

    def update(self):
        self._extend()
        if len(self.edge_nodes) <= 1:
            nodes_out = [node for node in self.nodes.values() if node.pos.distance_to(self.player.pos) < self.player.radius]
            self.edge_nodes.extend(nodes_out)

    def draw(self, screen):
        for node in self.nodes:
            node.draw(screen)

    def _extend(self):
        updated = False
        updated_edge_nodes = []
        for node in self.edge_nodes:
            if node.pos.distance_to(self.player.pos) < self.player.radius:
                updated = True
                updated_edge_nodes.extend(self._add_sib(node))
            else:
                updated_edge_nodes.append(node)
        self.edge_nodes = updated_edge_nodes

        if updated:
            #print(f"Updated edge nodes. Now: ${self.get_str_temp()}")
            self.player.increaseRadius()
            self._extend()

    def get_str_temp(self):
        new_str = ''
        for node in self.edge_nodes:
            new_str += str(node)
        return new_str

    def _add_sib(self,node):

        num_sibs = 1 if random.random() > 0.3 else 2
        none_count = node.siblings.count(None)
        if not none_count:
            return []
        if none_count == 1:
            num_sibs = 1

        new_sibs = []

        for _ in range(num_sibs):
            index = random.choice([i for i, value in enumerate(node.siblings) if value is None])
            new_node = node.add(index)
            if new_node is not None:
                new_sibs.append(new_node)
            else:
                self.updateDjikstra(node)

        return new_sibs
    def updateDjikstra(self, node):
        updated = False
        for sib in node.siblings:
            if sib is None:
                continue
            if node.dist + 1 < sib.dist:
                sib.dist = node.dist + 1
                updated = True
            if node.dist > sib.dist + 1:
                node.dist = sib.dist + 1
                updated = True
        if not updated:
            return
        for sib in node.siblings:
            if sib is not None:
                self.updateDjikstra(sib)





    def Print(self):
        for node in self.edge_nodes:
            print(node)
