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
        max_val = float('-inf')
        depth = 3
        found_move = False

        for i in range(len(act_nodes)):
            a = self.alphabeta(act_nodes[i], 0, float('-inf'), float('inf'), depth)
        
            if( a > max_val):
                found_move = True
                max_val = a
                move = i
        if(not found_move):
            move = random.randint(0,4)
        return ACTION_TO_STR[move]
        """
        Use minimax (and extensions) to find best possible next move for player 0 (green boat)
        :param initial_tree_node: Initial game tree node
        :type initial_tree_node: game_tree.Node
            (see the Node class in game_tree.py for more information!)
        :return: either "stay", "left", "right", "up" or "down"
        :rtype: str
        """
        
        # EDIT THIS METHOD TO RETURN BEST NEXT POSSIBLE MODE USING MINIMAX ###

        # NOTE: Don't forget to initialize the children of the current node
        #       with its compute_and_get_children() method!

    #    random_move = random.randrange(5)
     #   return ACTION_TO_STR[random_move]
    
    def manhattan(self,hookPos, fishPos):
        xDist = abs(fishPos[0] - hookPos[0])
        yDist = abs(fishPos[1] - hookPos[1])

        x = min(xDist, 20 - xDist)

        return x + yDist
    
    def heuristic(self,node):
        total_score = node.state.player_scores[0] - node.state.player_scores[1]

        val = 0
        for key, value in node.state.fish_positions.items():
            distance = self.manhattan(node.state.fish_positions[key], node.state.hook_positions[0])
            if distance == 0 and node.state.fish_scores[key] > 0:
                return float('inf')
            val = max(val, node.state.fish_scores[key] * math.exp(-distance))

        return 2 * total_score + val


    def alphabeta(self, node, player, alpha, beta, depth):
        '''node.state.set_player(player)'''
        children = node.compute_and_get_children()
        if len(children) == 0 or depth == 0:
           v = self.heuristic(node)
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
