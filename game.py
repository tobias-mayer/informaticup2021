from enums.commands import Commands
from enums.directions import Directions
from enums.textures import Textures
from random import randint

class Game:

    def __init__(self, game_state=None, depth=7, tau=0.1, xi=0.4):
        self._game_state = game_state
        self._depth = depth
        self._tau = tau
        self._xi = xi
        self._move_counter = 0

    def predict_move(self, new_game_state):
        """Predicts the best possible move for the given state

        Args:
            new_game_state ([GameState]): The current state of the game

        Returns:
            [Commands]: The calculated command for the next move
        """
        self._move_counter += 1
        self._game_state = new_game_state

        snake = self._game_state.get_player()

        graph = self._calculate_graph(snake.get_pos(), snake.get_direction(), snake.get_speed(), self._depth)

        pos = snake.get_pos()
        speed = snake.get_speed()

        # Check for each player if he is nearby (in a radius of 10 blocks)
        nearby_opponents = []
        for s in self._game_state.get_players():
            opp_pos = s.get_pos()
            if abs(opp_pos[1] - pos[1]) <= 10 + speed and abs(opp_pos[0] - pos[0]) <= 10 + speed:
                nearby_opponents.append([s.get_pos(), s.get_direction(), s.get_speed()])
        
        return self._choose_option(graph, self._depth, nearby_opponents=nearby_opponents)

    def get_move_counter(self):
        """Returns the number of moves made in the game

        Returns:
            int: Amount of moves
        """
        return self._move_counter

    def _calculate_graph(self, pos, direction, speed, depth, sub_graph=False):
        # DO NOT use sub_graph flag, for method internal use only

        graph = [pos, direction, speed, dict()]
        graph_dict = graph[3]
        
        square_tl, square_tr, square_sd, square_su, square_cn = self._generate_possible_fields(
            pos, direction, speed)
        for index, square in enumerate([square_tl, square_tr, square_sd, square_su, square_cn]):
            if self._check_if_reachable(pos, square):
                new_speed = speed
                new_direction = direction.value
                command = Commands(index)
                if command == Commands.SLOW_DOWN:
                    new_speed -= 1
                elif command == Commands.SPEED_UP:
                    new_speed += 1
                elif command == Commands.TURN_LEFT:
                    new_direction -= 1
                    if new_direction == -1:
                        new_direction = 3
                elif command == Commands.TURN_RIGHT:
                    new_direction += 1
                    if new_direction == 4:
                        new_direction = 0
                if depth == 1:
                    graph_dict[Commands(index)] = [square, Directions(new_direction), new_speed, {}]
                else:
                    graph_dict[Commands(index)] = [square, Directions(new_direction), new_speed, self._calculate_graph(square, Directions(new_direction), new_speed, depth - 1, sub_graph=True)]
            else:
                graph_dict[Commands(index)] = None
        if sub_graph:
            return graph_dict
        return graph

    def _choose_option(self, graph, depth, nearby_opponents=[]):
        """Selects the best option from the given graph by calculating a score.
        If 'nearby_opponents' is specified, collisions with nearby opponents are predicted and avoided.

        Args:
            graph (list): The graph with all options
            depth (int): Depth of the graph
            nearby_opponents (list, optional): List of opponents that are near the player. Defaults to [].

        Returns:
            Commands: The chosen command
        """
        command_list = []
        score_list = []
        collision_cmds = []

        pos = graph[0]
        direction = graph[1]
        speed = graph[2]
        graph_dict = graph[3]

        for opp in nearby_opponents:
            cmds = self._calculate_collision_cmds(pos, direction, speed, opp[0], opp[1], opp[2])
            collision_cmds.extend(cmds)

        collision_dict = dict()
        for command in Commands:
            collision_count = 0
            for cmd in collision_cmds:
                if cmd == command:
                    collision_count += 1
            collision_dict[command] = collision_count

        for command in Commands:
            if graph[3][command] is not None:
                command_list.append(command)
                cmd_score = self._calculate_score(graph_dict[command], depth - 1) - depth * self._xi * collision_dict[command]
                score_list.append(cmd_score)

        if len(command_list) == 0:
            return Commands.CHANGE_NOTHING

        option = randint(0, len(command_list) - 1)
        max_score = score_list[option]
        chosen_option = command_list[option]
        for command, score in zip(command_list, score_list):
            if command == Commands.SPEED_UP and self._game_state.get_player().get_speed() > 9:
                continue
            if score > max_score:
                max_score = score
                chosen_option = command
            
        return chosen_option

    def _generate_possible_fields(self, square, direction, speed):
        """Generates the next fields for every possible command

        Args:
            square ([int, int]): The current position of the snakes head
            direction ([type]): The snakes direction
            speed ([type]): The snakes speed

        Returns:
            The new position for each command
        """
        square_cn = [0, 0]
        square_tl = [0, 0]
        square_tr = [0, 0]
        square_su = [0, 0]
        square_sd = [0, 0]

        # right and down are positive directions, left and up are negative
        dir_factor = 1 if direction == Directions.DOWN or direction == Directions.RIGHT else -1

        if direction == Directions.UP or direction == Directions.DOWN:
            square_cn = [square[0], square[1] + speed * dir_factor]
            square_tl = [square[0] + speed * dir_factor, square[1]]
            square_tr = [square[0] - speed * dir_factor, square[1]]
            square_su = [square[0], square[1] + (speed + 1) * dir_factor]
            square_sd = [square[0], square[1] + (speed - 1) * dir_factor]
        elif direction == Directions.LEFT or direction == Directions.RIGHT:
            square_cn = [square[0] + speed * dir_factor, square[1]]
            square_tl = [square[0], square[1] - speed * dir_factor]
            square_tr = [square[0], square[1] + speed * dir_factor]
            square_su = [square[0] + (speed + 1) * dir_factor, square[1]]
            square_sd = [square[0] + (speed - 1) * dir_factor, square[1]]

        return square_tl, square_tr, square_sd, square_su, square_cn

    def _is_in_game_bounds(self, block):
        """Checks whether the given block is in the bounds of the game

        Args:
            block ([int, int]): The position of the block

        Returns:
            bool: True if the block is in the bounds, otherwise False
        """
        return not (block[0] < 0 or block[0] > self._game_state.get_width() - 1 or block[1] < 0 or block[1] > self._game_state.get_height() - 1)

    def _check_if_reachable(self, start, target):
        """Checks if the target is reachable from the start position

        Args:
            start ([int, int]): starting position
            target ([int, int]): target position

        Returns:
            bool: True if the target is reachable, otherwise false
        """

        if not self._is_in_game_bounds(start) or not self._is_in_game_bounds(target):
            return False

        occupied = False

        if start[0] == target[0] and start[1] == target[1]:
            return False
        elif start[0] == target[0]:
            # squares are in the same column
            step = 1 if start[1] < target[1] else -1
            if self._is_move_six() and not self._check_occupied_by_snake(target) and not self._check_occupied_by_snake([start[0], start[1] + step]):
                return True
            else:
                for y in range(start[1] + step, target[1] + step, step):
                    occupied = occupied or self._check_occupied_by_snake([start[0], y])
                return not occupied
        elif start[1] == target[1]:
            # squares are in the same row
            step = 1 if start[0] < target[0] else -1
            if self._is_move_six() and not self._check_occupied_by_snake(target) and not self._check_occupied_by_snake([start[0] + step, start[1]]):
                return True
            else:
                for x in range(start[0] + step, target[0] + step, step):
                    occupied = occupied or self._check_occupied_by_snake([x, start[1]])
                return not occupied
        else:
            return False

    def _check_occupied_by_snake(self, square):
        """Checks if there is a player in the specified square

        Args:
            square ([x, y]): The square to check

        Returns:
            bool: True if there is a player, otherwise False
        """
        board =  self._game_state.get_cells()
        if board[square[1]][square[0]] == Textures.EMPTY:
            return False
        else:
            return True

    def _calculate_collision_cmds(self, pos1, direction1, speed1, pos2, direction2, speed2):
        """Calculates all commands that lead to a collision in 
        the next step based on the position, direction and speed of two players

        Args:
            pos1 ([int, int]): position of the first snake
            direction1 (Directions): direction of the first snake
            speed1 (int): speed of the first snake
            pos2 ([int, int]): position of the first snake
            direction2 (Directions): direction of the second snake
            speed2 (int): speed of the first snake

        Returns:
            array: A list of all commands that result in a collision
        """#
        sn_tl, sn_tr, sn_sd, sn_su, sn_cn = self._generate_possible_fields(pos1, direction1, speed1)
        opp_tl, opp_tr, opp_sd, opp_su, opp_cn = self._generate_possible_fields(pos2, direction2, speed2)
        
        all_fields_opp = set()
        collison_cmds = []

        for field in [opp_tl, opp_tr, opp_sd, opp_su, opp_cn]:
            all_fields_opp.add(tuple(field))
            for block in self._calculate_path(pos2, field):
                all_fields_opp.add(tuple(block))
        
        opp_fields_len = len(all_fields_opp)
        for index, field in enumerate([sn_tl, sn_tr, sn_sd, sn_su, sn_cn]):
            cmd_path = self._calculate_path(pos1, field)
            sum_lengths = len(cmd_path) + opp_fields_len 
            cmd_path_set = set()
            for block in cmd_path:
                cmd_path_set.add(tuple(block))
            union_set = all_fields_opp.union(cmd_path_set)
            if len(union_set) != sum_lengths:
                collison_cmds.append(Commands(index))
        
        return collison_cmds

    def _calculate_path(self, start, target):
        """Calculates a path from start to the target

        Args:
            start ([int, int]): The start block
            target ([int, int]): The target block

        Returns:
            array: All the blocks on the calculated path
        """
        path = [start]

        if not self._is_in_game_bounds(start):
            return path
        
        if start[0] == target[0] and start[1] == target[1]:
            return path
        elif start[0] == target[0]:
            # squares are in the same column
            step = 1 if start[1] < target[1] else -1
            if self._is_move_six():
                path.append([start[0], start[1] + step])
                path.append(target)
                return path
            else:
                for y in range(start[1] + step, target[1] + step, step):
                    path.append([start[0], y])
                return path
        elif start[1] == target[1]:
            # squares are in the same row
            step = 1 if start[0] < target[0] else -1
            if self._is_move_six():
                path.append([start[0] + step, start[1]])
                path.append(target)
                return path
            else:
                for x in range(start[0] + step, target[0] + step, step):
                    path.append([x, start[1]])
                return path
        else:
            # start and target neither in the same row nor column
            return path

    def _calculate_score(self, graph, depth):
        """Recursively calculates the score for the given graph with the specified depth

        Args:
            graph (list): The graph of which the score is calculated
            depth (int): Depth of the graph

        Returns:
            int: The calculated score
        """
        graph_dict = graph[3] 
        if depth == 1:
            score = 0
            for command in Commands:
                if graph_dict[command] is not None:
                    score += 1
            return score
        else:
            score = 0
            for command in Commands:
                if graph_dict[command] is None:
                    continue
                score += self._tau * self._calculate_score(graph_dict[command], depth - 1)
            return score

    def _is_move_six(self):
        """Determines whether it is the sixt move or not 

        Returns:
            [bool]: Whether it is the sixt move or not
        """
        return self._move_counter % 6 == 0