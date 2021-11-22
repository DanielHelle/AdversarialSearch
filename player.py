#!/usr/bin/env python3
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
        max_val = -inf
        for i in range[5]:
            a = self.alphabeta(act_nodes[i], 0, -inf, inf, 7)
            if( a > max_val):
                max_val = a
                move = i

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

    def heuristic(state):
        scores = state.get_player_scores()
        p1 = scores[0]
        p2 = scores[1]
        return p1 - p2


    def alphabeta(self, node, player, alpha, beta, depth):
        '''node.state.set_player(player)'''
        children = node.compute_and_get_children()
        if not children or depth == 0:
           v = self.heuristic(node.state)
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
