import heapq


class PriorityQueue:
    def __init__(self):
        self.heap = []

    def is_empty(self):
        return len(self.heap) == 0

    # make state_cost a two-tuple
    def push(self, state_cost):
        heapq.heappush(self.heap, state_cost)

    def pop(self):
        return heapq.heappop(self.heap)
