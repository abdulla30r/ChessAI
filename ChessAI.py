"""
Handling the AI moves.
"""
import random
import ChessMain


piece_score = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}

knight_scores = [[0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
                 [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
                 [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
                 [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
                 [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
                 [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
                 [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
                 [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]]

bishop_scores = [[0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
                 [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                 [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
                 [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
                 [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
                 [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
                 [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
                 [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]]

rook_scores = [[0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
               [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25]]

queen_scores = [[0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
                [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]]

pawn_scores = [[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
               [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
               [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
               [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
               [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
               [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
               [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
               [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]]

piece_position_scores = {"wN": knight_scores,
                         "bN": knight_scores[::-1],
                         "wB": bishop_scores,
                         "bB": bishop_scores[::-1],
                         "wQ": queen_scores,
                         "bQ": queen_scores[::-1],
                         "wR": rook_scores,
                         "bR": rook_scores[::-1],
                         "wp": pawn_scores,
                         "bp": pawn_scores[::-1]}

CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3

POPULATION_SIZE = 20
GENERATIONS = 100
MUTATION_RATE = 0.1
TOURNAMENT_SIZE = 5



def findBestMove(game_state, valid_moves, return_queue,difficulty):
    """
    Helper method to make first recursive call
    """
    global next_move, counter
    next_move = None
    random.shuffle(valid_moves)
    counter = 0

    if difficulty == "medium":
        print("ekhon chole: " + difficulty)
        findMoveMinMax(game_state, valid_moves, DEPTH, game_state.white_to_move)

    if difficulty == "easy":
        print("ekhon chole: " + difficulty)
        findMoveGeneticAlgorithm(game_state, valid_moves)

    if difficulty == "hard":
        print("ekhon chole: " + difficulty)
        findMoveAlphaBeta(game_state, valid_moves, DEPTH, -CHECKMATE, CHECKMATE,1 if game_state.white_to_move else -1)
    
    if difficulty=="greedy":
        print("ekhon chole: " + difficulty)
        findBestMoveGreedy(game_state, valid_moves)

    if difficulty == "negamax":
        print("ekhon chole: " + difficulty)
        findMoveNegaMax(game_state, valid_moves, DEPTH, 1 if game_state.white_to_move else -1)

    #print(counter)
    return_queue.put(next_move)

def findMoveMinMax(gs, validMoves, depth, whiteToMove):

    global nextMove
    if depth == 0:  # evaluate
        return scoreMaterial(gs.board)

    if not whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore

    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore
    
def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
    """
    combine min max, find score and negate it if it is black to move
    """
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth - 1, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        # score = max(score, maxScore)
        gs.undoMove()
    return maxScore


def findBestMoveGreedy(gs, validMoves):
    turnMultiplier = 1 if gs.white_to_move else -1
    opponentsMinMaxScore = CHECKMATE
    bestPlayerMove = None
    random.shuffle(validMoves)

    for playerMove in validMoves:
        gs.makeMove(playerMove)
        opponanetsMoves = gs.getValidMoves()
        if gs.stalemate:
            opponanetMaxScore = STALEMATE
        elif gs.checkmate:
            opponanetMaxScore = -CHECKMATE
        else:
            opponanetMaxScore = -CHECKMATE

            for opponanetsMove in opponanetsMoves:
                gs.makeMove(opponanetsMove)
                gs.getValidMoves()
                if gs.checkmate:
                    score = CHECKMATE
                elif gs.stalemate:
                    score = STALEMATE
                else:
                    score = -turnMultiplier * scoreMaterial(gs.board)

                if score > opponanetMaxScore:
                    opponanetMaxScore = score
                gs.undoMove()
        if opponentsMinMaxScore > opponanetMaxScore:
            opponentsMinMaxScore = opponanetMaxScore
            bestPlayerMove = playerMove
        gs.undoMove()
    return bestPlayerMove


def findMoveAlphaBeta(game_state, valid_moves, depth, alpha, beta, turn_multiplier):
    global next_move
    if depth == 0:
        return turn_multiplier * scoreBoard(game_state)
    # move ordering - implement later //TODO
    max_score = -CHECKMATE
    for move in valid_moves:
        game_state.makeMove(move)
        next_moves = game_state.getValidMoves()
        score = -findMoveAlphaBeta(game_state, next_moves, depth - 1, -beta, -alpha, -turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        game_state.undoMove()
        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            break
    return max_score


# Genetic Algorithm
def findMoveGeneticAlgorithm(gs, validMoves):
    population = generateInitialPopulation(validMoves)
    for generation in range(GENERATIONS):
        fitnessScores = evaluatePopulation(gs, population)
        newPopulation = []
        for _ in range(POPULATION_SIZE // 2):
            parent1 = selectParent(population, fitnessScores)
            parent2 = selectParent(population, fitnessScores)
            child1, child2 = crossover(parent1, parent2)

            # newPopulation.extend([mutate(child1), mutate(child2)])
            newPopulation.extend([child1, child2])

        population = newPopulation
    bestMove = max(population, key=lambda move: evaluateMove(gs, move))
    return bestMove

def generateInitialPopulation(validMoves):
    return [random.choice(validMoves) for _ in range(POPULATION_SIZE)]

def evaluatePopulation(gs, population):
    return [evaluateMove(gs, move) for move in population]

def evaluateMove(gs, move):
    gs.makeMove(move)
    score = scoreBoards(gs.board)
    gs.undoMove()
    return score

def scoreBoards(board):
    score = 0
    pieceScore = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
    return score

def selectParent(population, fitnessScores):
    tournament = random.sample(list(zip(population, fitnessScores)), TOURNAMENT_SIZE)
    return max(tournament, key=lambda item: item[1])[0]

def crossover(parent1, parent2):
    if random.random() < 0.5:
        return parent1, parent2
    return parent2, parent1

def mutate(move):
    if random.random() < MUTATION_RATE:
        move.end_row = (move.end_row + random.choice([-1, 1])) % 8
        move.end_row = (move.end_row + random.choice([-1, 1])) % 8
    return move


'''
A positive score is good for white, negative for black
'''
def scoreBoard(game_state):
    """
    Score the board. A positive score is good for white, a negative score is good for black.
    """
    if game_state.checkmate:
        if game_state.white_to_move:
            return -CHECKMATE  # black wins
        else:
            return CHECKMATE  # white wins
    elif game_state.stalemate:
        return STALEMATE
    score = 0
    for row in range(len(game_state.board)):
        for col in range(len(game_state.board[row])):
            piece = game_state.board[row][col]
            if piece != "--":
                piece_position_score = 0
                if piece[1] != "K":
                    piece_position_score = piece_position_scores[piece][row][col]
                if piece[0] == "w":
                    score += piece_score[piece[1]] + piece_position_score
                if piece[0] == "b":
                    score -= piece_score[piece[1]] + piece_position_score

    return score

# def scoreBoard(gs):
#     if gs.checkmate:
#         if gs.white_to_move:
#             return -CHECKMATE #black wins
#         else:
#             return CHECKMATE #white wins
#     elif gs.stalemate:
#         return STALEMATE

#     score = 0
#     for row in gs.board:
#         for square in row:
#             if square[0] == 'w':
#                 score += piece_score[square[1]]
#             elif square[0] == 'b':
#                 score -= piece_score[square[1]]
    
#     return score

def findRandomMove(valid_moves):
    """
    Picks and returns a random valid move.
    """
    return random.choice(valid_moves)

def scoreMaterial(board):
    """
    Score the board based on material
    """
    score = 0
    for row in board:
        for square in row:
            if square[0] == "w":
                score += piece_score[square[1]]
            elif square[0] == "b":
                score -= piece_score[square[1]]
    return score


# knight_scores = [[0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
#                  [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
#                  [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
#                  [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
#                  [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
#                  [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
#                  [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
#                  [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]]

# bishop_scores = [[0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
#                  [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
#                  [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
#                  [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
#                  [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
#                  [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
#                  [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
#                  [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]]

# rook_scores = [[0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
#                [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
#                [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
#                [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
#                [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
#                [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
#                [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
#                [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25]]

# queen_scores = [[0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
#                 [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
#                 [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
#                 [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
#                 [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
#                 [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
#                 [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
#                 [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]]

# pawn_scores = [[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
#                [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
#                [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
#                [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
#                [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
#                [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
#                [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
#                [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]]

# piece_position_scores = {"wN": knight_scores,
#                          "bN": knight_scores[::-1],
#                          "wB": bishop_scores,
#                          "bB": bishop_scores[::-1],
#                          "wQ": queen_scores,
#                          "bQ": queen_scores[::-1],
#                          "wR": rook_scores,
#                          "bR": rook_scores[::-1],
#                          "wp": pawn_scores,
#                          "bp": pawn_scores[::-1]}


# def scoreBoard(game_state):
#     """
#     Score the board. A positive score is good for white, a negative score is good for black.
#     """
#     if game_state.checkmate:
#         if game_state.white_to_move:
#             return -CHECKMATE  # black wins
#         else:
#             return CHECKMATE  # white wins
#     elif game_state.stalemate:
#         return STALEMATE
#     score = 0
#     for row in range(len(game_state.board)):
#         for col in range(len(game_state.board[row])):
#             piece = game_state.board[row][col]
#             if piece != "--":
#                 piece_position_score = 0
#                 if piece[1] != "K":
#                     piece_position_score = piece_position_scores[piece][row][col]
#                 if piece[0] == "w":
#                     score += piece_score[piece[1]] + piece_position_score
#                 if piece[0] == "b":
#                     score -= piece_score[piece[1]] + piece_position_score

#     return score