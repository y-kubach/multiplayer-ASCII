from dataclasses import dataclass
from queue import SimpleQueue
from Coord import *

WORLD_SIZE = 10
gObjectManager = None


@dataclass
class Object:
    x: int
    y: int
    id: int
    shape = None


@dataclass
class ObjectManager:
    objectsDict = dict()
    total_objects = 0  # is used for the id, ids are always unique and never re-used.
    world_size = WORLD_SIZE
    world = Grid(WORLD_SIZE, WORLD_SIZE)
    queue = SimpleQueue()

    def __init__(self):
        self.world = Grid(self.world_size, self.world_size)
        global gObjectManager
        gObjectManager = self

    def create_object(self, x, y, datatype):
        obj = datatype(x, y, self.total_objects)
        self.total_objects += 1
        self.objectsDict[obj.id] = obj
        self.world[(x, y)] = obj.shape
        self.queue.put((x, y))

    def delete_object(self, object_or_id):
        if object_or_id is Object:
            is_deleted = self.objectsDict.pop(object_or_id.id)
        else:
            is_deleted = self.objectsDict.pop(object_or_id)
        if not is_deleted:
            assert False, "ERROR: Attempt to delete an object that is not in objectsDict."

    def move_object(self, object_or_id: Object | int, right, down, relative=True):
        """down and right are relative coordinates. right = 2 means obj.x += 2"""
        if object_or_id is Object:
            obj = object_or_id
        else:
            if object_or_id not in self.objectsDict:
                assert False, "ERROR: Attempt to move an object that is not in objectsDict."
            obj = self.objectsDict[object_or_id]

        try:
            if self.world.coord[obj.x + right][obj.y + down] == self.world.default_char:
                # Place '0' where the object used to be - add to draw queue
                self.world[(obj.x, obj.y)] = self.world.default_char
                self.queue.put((obj.x, obj.y))

                # Update Object position
                if relative:
                    x, y = obj.x + right, obj.y + down
                else:
                    x, y = right, down
                obj.x, obj.y = min(max(x, 0), self.world_size - 1), min(max(y, 0), self.world_size - 1)

                # Place obj.shape where object should go - add to draw queue
                self.world[(obj.x, obj.y)] = obj.shape
                self.queue.put((obj.x, obj.y))
        except KeyError:
            pass

    def get_pos(self, object_or_id):
        """A tuple is returned, unpack with: x, y = get_pos(object_or_id)"""
        if object_or_id is Object:
            return object_or_id.x, object_or_id.y
        return self.objectsDict[id].x, self.objectsDict[id].y

    def dequeue(self):
        return self.queue.get()
