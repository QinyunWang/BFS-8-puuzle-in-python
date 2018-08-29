__author__ = "Qinyun Wang"
import time
import numpy as np


class StateCostPair(object):
    """A class storing a state and a cost to travel to it."""

    def __init__(self, state, cost):
        """Construct a state cost pair.

        :param state: (PuzzleState) an agent problem state
        :param cost: (Float) cost to travel to the state
        """
        self.state = state
        self.cost = cost

    def compare_to(self, state_pair):
        """Required to allow StateCostPair to be used in a priority queue. Refer to
        comment in SearchTreeNode

        :param state_pair: (StateCostPair) StateCostPair to compare to
        :return: -1 if this node has a lower travel cost than pair state_pair
                0 if this node has the same travel cost as pair state_pair
                1 if this node has a greater travel cost than pair state_pair
        """
        if self.cost < state_pair.cost:
            return -1
        elif self.cost == state_pair.cost:
            return 0
        else:
            return 1


class SearchTreeNode(object):
    """
    A generic search tree node representing a path through a state graph. Stores
    a state, the cost of the last edge followed, and the total cost of all edges
    in the path associated with this node.
    """

    def __init__(self, state_cost_pair, parent=None):
        """Construct a root node of a search tree.

        :param state_cost_pair: (StateCostPair) the state (and last edge cost)
        associated with this search tree node.
        :param parent: (SearchTreeNode) the parent of this node
        """
        self.parent = parent
        self.state_cost_pair = state_cost_pair

        if self.parent is None:
            self.path_cost = 0
            self.depth = 0
        else:
            self.path_cost = self.parent.path_cost + self.state_cost_pair.cost
            self.depth = self.parent.depth + 1

    def compare_to(self, search_tree_node):
        """Compares the path cost of this node to the path cost of node search_tree_node.
        Defining a "compare_to" method is necessary in order for searchTreeNodes
        to be used in a priority queue.
        :param search_tree_node: (SearchTreeNode) node to compare path cost with
        :return:-1 if this node has a lower path cost than pair search_tree_node
                0 if this node has the same path cost as pair search_tree_node
                1 if this node has a greater path cost than pair search_tree_node
        """
        if self.path_cost < search_tree_node.path_cost:
            return -1
        elif self.path_cost == search_tree_node.path_cost:
            return 0
        else:
            return 1


class BFS(object):
    """A generic implementation of Breadth First Search."""

    def __init__(self):
        """Create a BFS search agent instance."""
        self.container = []
        self.visited = []
        self.tot_node = 0

    def search(self, initial, goal):
        """Search for a path between a given initial state and goal state.

        :param initial: (PuzzleState) the initial stage
        :param goal: (PuzzleState) the goal stage
        :return: (List(StateCostPair))the list of states and costs representing
        the path from the initial state to the goal state found by the BFS agent.
        """
        self.container.append(SearchTreeNode(StateCostPair(initial, 0)))

        while len(self.container) > 0:
            # select a tree node from the container
            current_node = self.container.pop(0)
            self.tot_node -= 1
            current_state = current_node.state_cost_pair.state

            # mark this state as visited
            self.visited.append(current_state.output_string())

            # check if this state is the goal
            if current_state.equals(goal):
                # goal found - return all steps from initial to goal
                path_to_goal = []

                while current_node.parent is not None:
                    path_to_goal.append(current_node.state_cost_pair)
                    current_node = current_node.parent

                path_to_goal.reverse()

                # reset for next search
                self.reset()

                return path_to_goal

            successors = current_state.get_successors()
            for i in successors:
                if i.state.output_string() not in self.visited:
                    self.container.append(SearchTreeNode(i, current_node))
                    self.tot_node += 1

        self.reset()
        return None

    def reset(self):
        """Resets the search agent (clears instance variables to be ready for next
        search request)."""
        self.container = []
        self.visited = []

    def tot_nodes(self):
        return self.tot_node


class PuzzleState(object):
    """A state of the 8-puzzle problem."""

    def __init__(self, state):
        """Create an 8-puzzle state from a string.

        :param state: (str) string representing tile positions
        """
        self.state = state

        # find the position of blank tile
        self.index_of_blank = -1
        for i, tile in enumerate(self.state):
            if tile == "_":
                if self.index_of_blank != -1:
                    raise ValueError("Too many blank spaces!")
                self.index_of_blank = i
        if self.index_of_blank == -1:
            raise ValueError("Blank space missing")

        self.successors = []

    def output_string(self):
        """Output a string representation of this puzzle state.

        :return: (String) representation
        """
        return self.state

    def get_number_at(self, index):
        """Return the number at position i (counting from 0, left to right then
        top to bottom).

        :param index
        :return: (String) number at index i
        """
        return self.state[index]

    def get_successors(self):
        """Return a list of all states reachable from this state. Each successor
        has a cost of 1 (indicating it is reached in 1 move).

        :return: (List(StateCostPair)) list of successors
        """

        # blank is not in the left column - left move is valid
        if self.index_of_blank % 3 != 0:
            self.successors.append(StateCostPair(self.swap_positions(self.index_of_blank - 1), 1))

        # blank is not in the right column - right move is valid
        if self.index_of_blank % 3 != 2:
            self.successors.append(StateCostPair(self.swap_positions(self.index_of_blank + 1), 1))

        # blank is not in the top row - up move is valid
        if self.index_of_blank > 2:
            self.successors.append(StateCostPair(self.swap_positions(self.index_of_blank - 3), 1))

        # blank is not in the bottom row - down move is valid
        if self.index_of_blank < 6:
            self.successors.append(StateCostPair(self.swap_positions(self.index_of_blank + 3), 1))

        return self.successors

    def swap_positions(self, index):
        """Clone the puzzle state and swap the blank tile with the tile at the
        given index.

        :param index: (Integer) position to swap blank with
        :return: (PuzzleState) puzzle state after swap
        """
        list_state = list(self.state)
        list_state[self.index_of_blank] = list_state[index]
        list_state[index] = "_"

        return PuzzleState("".join(list_state))

    def equals(self, goal_state):
        """Check if this puzzle state is equivalent to goal state

        :param goal_state: (PuzzleState) state to check equality with
        :return: (Boolean) true if all tiles are in the same position
        """
        if self.output_string() == goal_state.output_string():
            return True
        else:
            return False

    def parity(self):
        """Compute the parity of this state.

        :return: 0 if puzzle state has even parity
                 1 if puzzle state has odd parity
        """
        total = 0
        for i, num1 in enumerate(self.state):
            if num1 == "_":
                continue
            for j, num2 in enumerate(self.state[i:]):
                if num2 == "_":
                    continue
                if num1 > num2:
                    total += 1

        return total % 2


def solve_eight_puzzle(search_type, init_str, goal_str, show_steps, show_num_steps,
                       show_elapsed_time, show_total_nodes):
    if search_type == "BFS":
        agent = BFS()

    initial = PuzzleState(init_str)
    goal = PuzzleState(goal_str)

    if not parity_match(initial.output_string(), goal.output_string()):
        print(initial.parity())
        print(goal.parity())
        print("No solution - parity mismatch ")
        return

    start = time.clock()

    path_to_goal = agent.search(initial, goal)

    end = time.clock()

    time_taken = end - start

    if show_steps:
        print("Solution:")
        print(np.array(list(initial.output_string())).reshape(3, 3))
        print("\n")
        for i in path_to_goal:
            twoD = i.state.output_string()
            print(np.array(list(twoD)).reshape(3, 3))
            print("\n")

    if show_num_steps:
        print("No. of steps:")
        print(" " + str(len(path_to_goal)))

    if show_total_nodes:
        print("Total nodes:")
        print(" " + str(agent.tot_nodes()))

    if show_elapsed_time:
        print("Time taken:")
        print(" " + str("{:2f}".format(time_taken * 1000)) + "ms")


def parity_match(state1, state2):

    p1 = PuzzleState(state1)
    p2 = PuzzleState(state2)

    if p1.parity() == p2.parity():
        return True
    else:
        return False

def parity(self):
    """Compute the parity of this state.

    :return: 0 if puzzle state has even parity
             1 if puzzle state has odd parity
    """
    total = 0
    for i, char1 in enumerate(self):
        if char1 == "_":
            continue
        for j, char2 in enumerate(self[i+1:]):
            if char2 == "_":
                continue
            if char1 > char2:
                total += 1

    return total


if __name__ == "__main__":



    # show_steps = True
    # show_num_steps = True
    # show_elapsed_time = True
    # show_total_nodes = True

    solve_eight_puzzle("BFS", "3184_2756", "12345678_", False, True, True, True)



    # solve_eight_puzzle("BFS", "281_43765", "1238_4765", show_steps, show_num_steps, show_elapsed_time, show_total_nodes)
    # solve_eight_puzzle("BFS", "281463_75", "1238_4765", show_steps, show_num_steps, show_elapsed_time, show_total_nodes)