from enum import Enum, auto
import pygame
import Graph


class Directions(Enum):
    UP = 0
    DOWN = 1
    RIGHT = 2
    LEFT = 3


def _get_opposite(direction):
    match direction:
        case Directions.UP.value:
            return Directions.DOWN.value
        case Directions.DOWN.value:
            return Directions.UP.value
        case Directions.LEFT.value:
            return Directions.RIGHT.value
        case Directions.RIGHT.value:
            return Directions.LEFT.value


class Node:
    def __init__(self, pos_x, pos_y, dist=1, graph=None):
        self.siblings = [None, None, None, None]
        self.pos = pygame.math.Vector2(pos_x, pos_y)
        self.dist = dist
        self.graph = graph
        self.SCALE_FACTOR = 2
        self.image = self.getImage()
        self.font = pygame.font.Font("./textures/font/retro_computer/retro_computer_personal_use.ttf", 9)
        self.SIZE = 25 * self.SCALE_FACTOR

    def draw(self, screen):
        screen_pos = pygame.math.Vector2((self.pos.x * self.SIZE) + screen.get_width() / 2,
                                         (self.pos.y * self.SIZE) + screen.get_height() / 2)
        screen.blit(self.getImage(), (screen_pos.x - self.SIZE / 2, screen_pos.y - self.SIZE / 2))
        pos_text = self.font.render(f'{self.pos.x} - {self.pos.y}', True, (200, 65, 98))
        dist_text = self.font.render(f'{self.dist}', True, (200, 65, 98))
        #screen.blit(pos_text, (screen_pos.x, screen_pos.y))
        screen.blit(dist_text, (screen_pos.x, screen_pos.y))
        # if self.dist == 0:
        #     color = "blue"
        # elif self in self.graph.edge_nodes:
        #     color = "green"
        # else:
        #     color = "red"
        # pygame.draw.circle(screen, color, screen_pos, 5)
        # if (self.siblings[Directions.UP.value] is not None):
        #     pygame.draw.line(screen, color, screen_pos, (screen_pos.x, screen_pos.y - 12))
        # if (self.siblings[Directions.DOWN.value] is not None):
        #     pygame.draw.line(screen, color, screen_pos, (screen_pos.x, screen_pos.y + 12))
        # if (self.siblings[Directions.RIGHT.value] is not None):
        #     pygame.draw.line(screen, color, screen_pos, (screen_pos.x + 12, screen_pos.y))
        # if (self.siblings[Directions.LEFT.value] is not None):
        #     pygame.draw.line(screen, color, screen_pos, (screen_pos.x - 12, screen_pos.y))

    def add(self, direction):
        node = Node(0, 0)
        match direction:
            case Directions.UP.value:
                node = self.getNodeUp()
                node.siblings[Directions.DOWN.value] = self
            case Directions.DOWN.value:
                node = self.getNodeDown()
                node.siblings[Directions.UP.value] = self
            case Directions.LEFT.value:
                node = self.getNodeLeft()
                node.siblings[Directions.RIGHT.value] = self
            case Directions.RIGHT.value:
                node = self.getNodeRight()
                node.siblings[Directions.LEFT.value] = self

        # node is getting connected to an existing node if the condition is passed :)
        if node in self.graph.nodes:
            self.siblings[direction] = self.graph.nodes[node]
            self.graph.nodes[node].siblings[_get_opposite(direction)] = self
            return None

        self.siblings[direction] = node
        self.graph.nodes[node] = node
        # print(f'Added Node {node}')
        return node

    def getNodeUp(self):
        return Node(self.pos.x, self.pos.y - 1, self.dist + 1, self.graph)

    def getNodeDown(self):
        return Node(self.pos.x, self.pos.y + 1, self.dist + 1, self.graph)

    def getNodeLeft(self):
        return Node(self.pos.x - 1, self.pos.y, self.dist + 1, self.graph)

    def getNodeRight(self):
        return Node(self.pos.x + 1, self.pos.y, self.dist + 1, self.graph)

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.pos == other.pos
        return False

    def __hash__(self):
        return hash(self.pos.x) + hash(self.pos.y)

    def __str__(self):
        return f"Node {self.pos.x}, {self.pos.y}"

    def getImage(self):
        binary_list = [0 if n is None else 1 for n in self.siblings]
        file_str = ''
        for i, sib in enumerate(binary_list):
            if sib:
                if (len(file_str) > 0):
                    file_str += '_'
                dir = ''
                match i:
                    case Directions.UP.value:
                        dir = 'up'
                    case Directions.DOWN.value:
                        dir = 'down'
                    case Directions.RIGHT.value:
                        dir = 'right'
                    case Directions.LEFT.value:
                        dir = 'left'

                file_str += dir
        if sum(binary_list) == 0:
            file_str += 'up'
        self.image = pygame.image.load(f'./textures/temp_rooms/{file_str}/{file_str}.png').convert_alpha()

        self.image = pygame.transform.scale(self.image, (
        self.image.get_width() * self.SCALE_FACTOR, self.image.get_height() * self.SCALE_FACTOR))

        return self.image
