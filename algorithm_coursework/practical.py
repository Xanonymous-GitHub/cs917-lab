from collections import OrderedDict, defaultdict, deque
from collections.abc import Sequence
from itertools import product
from pprint import pprint
from threading import Thread, Lock
from typing import Optional, Final

from maze_block import MazeBlock, MazeBlockType, EXPECTED_MAZE_NEIGHBOUR_DIRECTIONS
from morse_code import mose_code_to_words, mose_code_tree
from utils.file import injected_cached_file_unique_lines_from


# FIXME: follow PEP8 naming conventions, this function should be called `morse_decode`.
# noinspection PyPep8Naming
def morseDecode(raw_morse_codes: Sequence[str], /) -> str:
    """
    This method should take a list of strings as input. Each string is equivalent to one letter
    (i.e. one morse code string). The entire list of strings represents a word.

    This method should convert the strings from morse code into english, and return the word as a string.
    """

    return ''.join(
        mose_code_to_words[raw_morse_code]
        for raw_morse_code in raw_morse_codes
    )


# FIXME: follow PEP8 naming conventions, this function should be called `morse_partial_decode`.
# noinspection PyPep8Naming
def morsePartialDecode(raw_morse_codes: Sequence[str], /) -> tuple[str]:
    """
    This method should take a list of strings as input. Each string is equivalent to one letter
    (i.e. one morse code string). The entire list of strings represents a word.

    However, the first character of every morse code string is unknown (represented by an 'x' (lowercase))
    For example, if the word was originally TEST, then the morse code list string would normally be:
    ['-','.','...','-']

    However, with the first characters missing, I would receive:
    ['x','x','x..','x']

    With the x unknown, this word could be tested,
    but it could also be EESE or ETSE or ETST or EEDT or other permutations.

    We define a valid words as one that exists within the dictionary file provided on the dictionary.txt

    This function should find and return a list of strings of all possible VALID words.
    """
    word_dictionary: Optional[frozenset[str]] = None

    # Define the file reading task.
    # Since the file reading task is IO-bound, we can use multi-threading to improve the performance.
    def read_word_dictionary():
        nonlocal word_dictionary
        with Lock():
            # Here we use the cached file data to ensure the file is only read once.
            word_dictionary = injected_cached_file_unique_lines_from('dictionary.txt')

    # Start asynchronous file reading task.
    read_file_task = Thread(target=read_word_dictionary)
    read_file_task.start()

    # A space to store the assumptions of each letter.
    # For example, like the doc mentioned, the first letter can be 'e' or 't',
    # so the first element of this list is ("e', "t").
    letter_assumptions: [tuple[str]] = []

    # When the raw morse code is empty, we assume the letter is 'x'.
    # So the possible answer of the letter is "e" or "t".
    # However, we can not directly use the answer to be our assumption,
    # So we use the theoretical assumption of the letter from the decision tree.
    root = mose_code_tree.root
    possible_ans_of_only_x = tuple([
        root.left.answer,
        root.right.answer,
    ])

    for raw_morse_code in raw_morse_codes:
        # Since the first character of every morse code string is unknown (represented by an 'x' (lowercase)),
        # we can ignore the first character.
        # And it is also known that using the inverse version of the raw morse code can get the nearest node,
        # which only contains two possible answers.
        inverse_raw_morse_code_without_x = raw_morse_code[:0:-1]

        # If the raw morse code is empty, we assume the letter is 'x'.
        # So we just apply the existing assumption.
        if inverse_raw_morse_code_without_x == '':
            letter_assumptions.append(possible_ans_of_only_x)
            continue

        # Find the nearest node of the inverse raw morse code.
        # This step expects to get the nearest node, which only contains maximum two possible answers.
        nearest_node = mose_code_tree.find_nearest_node(morse_signs=inverse_raw_morse_code_without_x)

        # Append our assumption of the letter into the list (`letter_assumptions`).
        left_node = nearest_node.left
        right_node = nearest_node.right

        current_assumptions = []
        if left_node is not None:
            current_assumptions.append(left_node.answer)
        if right_node is not None:
            current_assumptions.append(right_node.answer)

        letter_assumptions.append(tuple(current_assumptions))

    # Create all possible words from the assumptions of each letter.
    # The size of all_possible_words would be at most 2^len(raw_morse_codes).
    all_possible_words: frozenset[str] = frozenset([''.join(word) for word in product(*letter_assumptions)])

    # Wait for the file reading task to finish.
    read_file_task.join()

    # Filter the possible words by the word dictionary.
    return tuple(all_possible_words & word_dictionary)


class Maze:
    __known_max_x: int = 0
    __known_max_y: int = 0

    __wall_char: Final[str] = '*'
    __empty_char: Final[str] = ' '

    # The map of the maze, the key is the x coordinate, points to the y coordinate, then points to a MazeBlock.
    # For example, when we want to get the MazeBlock at (x=1, y=2), we can do:
    # maze[1][2]
    __maze: Final[OrderedDict[int, OrderedDict[int, MazeBlock]]]

    def __init__(self):
        self.__maze = OrderedDict()

    def __update_known_edge(self, /, *, new_x: int, new_y: int) -> None:
        self.__known_max_x = max(self.__known_max_x, new_x)
        self.__known_max_y = max(self.__known_max_y, new_y)

    def __is_valid_coordinate(self, /, *, x: int, y: int) -> bool:
        return 0 <= x <= self.__known_max_x and 0 <= y <= self.__known_max_y

    def __is_block_configured(self, /, *, x: int, y: int) -> bool:
        return x in self.__maze and y in self.__maze[x]

    @staticmethod
    def __describe_visited_path(*, end_block: MazeBlock) -> tuple[tuple[int, int], ...]:
        path: list[tuple[int, int]] = []
        current_block = end_block
        while current_block is not None:
            path.append((current_block.x, current_block.y))
            current_block = current_block.last_visited_block
        return tuple(path[::-1])

    @staticmethod
    def __new_wall_block_at(*, x: int, y: int) -> MazeBlock:
        new_wall_block = MazeBlock(
            x=x,
            y=y,
            category=MazeBlockType.WALL
        )
        return new_wall_block

    # FIXME: follow PEP8 naming conventions, this function should be called `add_coordinate`.
    # noinspection PyPep8Naming
    def addCoordinate(self, x, y, is_wall: bool, /) -> None:
        """
        Add information about a coordinate on the maze grid
        x is the x coordinate
        y is the y coordinate
        blockType should be 0 (for an open space) of 1 (for a wall)
        """
        self.__update_known_edge(new_x=x, new_y=y)
        new_maze_block = MazeBlock(
            x=x,
            y=y,
            category=MazeBlockType.WALL if bool(is_wall) else MazeBlockType.EMPTY
        )
        self.__maze.setdefault(x, OrderedDict())[y] = new_maze_block

    # FIXME: follow PEP8 naming conventions, this function should be called `print_maze`.
    # noinspection PyPep8Naming
    def printMaze(self) -> None:
        """
        Print out an ascii representation of the maze.
        A * indicates a wall and an empty space indicates an open space in the maze
        """
        buffer: list[str] = []
        for y in range(self.__known_max_y + 1):
            for x in range(self.__known_max_x + 1):
                if x in self.__maze and y in self.__maze[x]:
                    buffer.append(
                        self.__wall_char if self.__maze[x][y].category == MazeBlockType.WALL
                        else self.__empty_char
                    )
                else:
                    buffer.append(self.__wall_char)
            buffer.append('\n')
        buffer.pop()
        print(''.join(buffer))

    # FIXME: follow PEP8 naming conventions, this function should be called `find_route`.
    # noinspection PyPep8Naming
    def findRoute(self, x1: int, y1: int, x2: int, y2: int) -> tuple[tuple[int, int], ...]:
        """
        This method should find a route, traversing open spaces, from the coordinates (x1,y1) to (x2,y2)
        It should return the list of traversed coordinates followed along this route as a list of tuples (x,y),
        in the order in which the coordinates must be followed
        If no route is found, return an empty list
        """
        # A map-like structure that stores the visited coordinates.
        visited: dict[int, dict[int, bool]] = defaultdict(lambda: defaultdict(lambda: False))

        # Mark the start coordinate as visited.
        visited[x1][y1] = True

        # A queue-like structure that stores the coordinates to be visited.
        to_be_visited: deque[MazeBlock] = deque((self.__maze[x1][y1],))

        # Implement the BFS algorithm to find the shortest path.
        while len(to_be_visited) > 0:
            # Obtain the next block to be visited.
            current_block = to_be_visited.popleft()

            # Check if the current block is the end block.
            if current_block == self.__maze[x2][y2]:
                return self.__describe_visited_path(end_block=current_block)

            # Try to visit the neighbours of the current block.
            for move_y, move_x in EXPECTED_MAZE_NEIGHBOUR_DIRECTIONS:
                next_x = current_block.x + move_x
                next_y = current_block.y + move_y

                # Check if the next coordinate is inside the maze.
                # If not, skip the current iteration.
                if not self.__is_valid_coordinate(x=next_x, y=next_y):
                    continue

                # Check if the next block is configured.
                # Since we expect all un-configured blocks are walls,
                # we can skip the configuration process.
                if self.__is_block_configured(x=next_x, y=next_y):
                    next_block = self.__maze[next_x][next_y]
                    if next_block.category == MazeBlockType.WALL:
                        continue

                    # Check if the next block is visited.
                    # We expect not to visit the same block twice.
                    if visited[next_x][next_y]:
                        continue
                else:
                    # Since we expect all un-configured blocks are walls,
                    # we can skip the configuration process.
                    continue

                # Mark the next block as visited.
                # The distance of the next block is the distance of the current block plus one.
                next_block.distance = current_block.distance + 1

                # Record the last visited block of the next block.
                # This is used to describe the visited path.
                next_block.last_visited_block = current_block

                # Mark the next block as visited.
                visited[next_x][next_y] = True

                # Add the next block to the queue, for the next iteration.
                to_be_visited.append(next_block)
        else:
            return ()


# FIXME: follow PEP8 naming conventions, this function should be called `morse_code_test`.
# noinspection PyPep8Naming
def morseCodeTest():
    """
    This test program passes the morse code as a list of strings for the word
    HELLO to the decode method. It should receive a string "HELLO" in return.
    This is provided as a simple test example, but by no means covers all possibilities, and you should
    fulfill the methods as described in their comments.
    """

    hello = ['....', '.', '.-..', '.-..', '---']
    print(morseDecode(hello))


# FIXME: follow PEP8 naming conventions, this function should be called `morse_partial_code_test`.
# noinspection PyPep8Naming
def partialMorseCodeTest():
    """
    This test program passes the partial morse code as a list of strings 
    to the morsePartialDecode method. This is provided as a simple test example, but by
    no means covers all possibilities, and you should fulfill the methods as described in their comments.
    """

    # This is a partial representation of the word TEST, amongst other possible combinations
    test = ['x', 'x', 'x..', 'x']
    print(morsePartialDecode(test))

    # This is a partial representation of the word DANCE, amongst other possible combinations
    dance = ['x..', 'x-', 'x.', 'x.-.', 'x']
    print(morsePartialDecode(dance))


# FIXME: follow PEP8 naming conventions, this function should be called `maze_test`.
# noinspection PyPep8Naming
def mazeTest():
    """
    This sets the open space coordinates for an example
    maze for the testing purpose in the assignment.
    The remainder of coordinates within the max bounds of these specified coordinates
    are assumed to be walls
    """
    my_maze = Maze()
    my_maze.addCoordinate(1, 0, False)  # Start index
    my_maze.addCoordinate(1, 1, False)
    my_maze.addCoordinate(1, 3, False)
    my_maze.addCoordinate(1, 4, False)
    my_maze.addCoordinate(1, 5, False)
    my_maze.addCoordinate(1, 6, False)
    my_maze.addCoordinate(1, 7, False)

    my_maze.addCoordinate(2, 1, False)
    my_maze.addCoordinate(2, 2, False)
    my_maze.addCoordinate(2, 3, False)
    my_maze.addCoordinate(2, 6, False)

    my_maze.addCoordinate(3, 1, False)
    my_maze.addCoordinate(3, 3, False)
    my_maze.addCoordinate(3, 4, False)
    my_maze.addCoordinate(3, 5, False)
    my_maze.addCoordinate(3, 7, False)
    my_maze.addCoordinate(3, 8, False)  # End index

    my_maze.addCoordinate(4, 1, False)
    my_maze.addCoordinate(4, 5, False)
    my_maze.addCoordinate(4, 7, False)

    my_maze.addCoordinate(5, 1, False)
    my_maze.addCoordinate(5, 2, False)
    my_maze.addCoordinate(5, 3, False)
    my_maze.addCoordinate(5, 5, False)
    my_maze.addCoordinate(5, 6, False)
    my_maze.addCoordinate(5, 7, False)

    my_maze.addCoordinate(6, 3, False)
    my_maze.addCoordinate(6, 5, False)
    my_maze.addCoordinate(6, 7, False)

    my_maze.addCoordinate(7, 1, False)
    my_maze.addCoordinate(7, 2, False)
    my_maze.addCoordinate(7, 3, False)
    my_maze.addCoordinate(7, 5, False)
    my_maze.addCoordinate(7, 7, False)

    my_maze.printMaze()

    def maze_find_route_test() -> None:
        print('Find route from (1, 0) to (1, 7):')
        route = my_maze.findRoute(1, 0, 1, 7)
        pprint(route)

        print('Find route from (1, 0) to (3, 8):')
        route = my_maze.findRoute(1, 0, 3, 8)
        pprint(route)

        print('Find route from (1, 0) to (7, 7):')
        route = my_maze.findRoute(1, 0, 7, 7)
        pprint(route)

        print('Find route from (1, 0) to (1, 0):')
        route = my_maze.findRoute(1, 0, 1, 0)
        pprint(route)

    maze_find_route_test()


def main():
    morseCodeTest()
    partialMorseCodeTest()
    mazeTest()


if __name__ == "__main__":
    main()
