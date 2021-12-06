#!/usr/bin/env python3
import math
import random
from math import inf

from fishing_game_core.game_tree import Node
from fishing_game_core.player_utils import PlayerController
from fishing_game_core.shared import ACTION_TO_STR


class PlayerControllerHuman(PlayerController):
    def player_loop(self):
        """
        Function that generates the loop of the game. In each iteration
        the human plays through the keyboard and send
        this to the game through the sender. Then it receives an
        update of the game through receiver, with this it computes the
        next movement.
        :return:
        """

        while True:
            # send message to game that you are ready
            msg = self.receiver()
            if msg["game_over"]:
                return


class PlayerControllerMinimax(PlayerController):

    def __init__(self):
        super(PlayerControllerMinimax, self).__init__()

    def player_loop(self):
        """
        Main loop for the minimax next move search.
        :return:
        """

        # Generate first message (Do not remove this line!)
        first_msg = self.receiver()

        while True:
            msg = self.receiver()

            # Create the root node of the game tree
            node = Node(message=msg, player=0)

            # Possible next moves: "stay", "left", "right", "up", "down"
            best_move = self.search_best_next_move(initial_tree_node=node)

            # Execute next action
            self.sender({"action": best_move, "search_time": None})

    def search_best_next_move(self, initial_tree_node):
        
        act_nodes = initial_tree_node.compute_and_get_children()
        actions = []
        for act in act_nodes:
            actions.append(self.alphabeta(act, 0, -math.inf, math.inf, 2))
        opt_act = random.randint(0,4)
        m = max(actions)
        for idx, val in enumerate(actions):
            if(val == m):
                opt_act = idx

        return ACTION_TO_STR[opt_act]

    def manhattan(self,hookPos, fishPos):
        return abs(fishPos[0] - hookPos[0]) + abs(fishPos[1] - hookPos[1])

    def heuristic(self, node, player):
        p0_points, p1_points = node.state.get_player_scores()
        val = p0_points - p1_points
        if player == 0:
            val = val - self.fish_player_dist(node, player)
        elif player == 1:
            val *= -1
        return val

    def fish_player_dist(self, node, player):
        dist = []
        hooks = node.state.get_hook_positions()
        for fish in list(node.state.get_fish_positions().values()):
            dist.append(self.manhattan(hooks[player], fish))
        if(dist == []):
            return 0
        return min(dist)

    def alphabeta(self, node, player, alpha, beta, depth):
        '''node.state.set_player(player)'''
        children = node.compute_and_get_children()
        if len(children) == 0 or depth == 0:
           v = self.heuristic(node, player)
        elif player == 0:
            v = -inf
            max_val = -inf
            for child in children:
                v = max(v, self.alphabeta(child, 1, alpha, beta, depth-1))
                alpha = max(alpha, v)
                if alpha >= max_val:
                    max_val = alpha
                if(beta <= alpha): 
                    break
        else:
            v = inf
            for child in children:
                v = min(v, self.alphabeta(child, 0, alpha, beta, depth-1))
                beta = min(beta, v)
                if(beta <= alpha):
                    break
        return v




    def minimax(self, node, player):
        node.state.set_player(player)
        children = node.compute_and_get_children()
        if not children:
           return self.heuristic(node.state)
        else:
            if player == 0:
                bestPossible = -inf
                for child in children:
                    v = self.minimax(child, 1)
                    bestPossible = max(bestPossible, v)
                return bestPossible
            else:
                bestPossible = inf
                for child in children:
                    v = self.minimax(child, 0)
                    bestPossible = min(bestPossible, v)
                return bestPossible
