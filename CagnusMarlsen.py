import numpy as np
from tensorflow.keras.models import load_model
import chess
import random
 
from board import Board
from piece import Pawn, Rook, Knight, Bishop, Queen, King

def board_to_matrix(board):#converts the board from chess.Board() to a numpy matrix so the model can read it
    string_board=str(board)
    string_board=string_board.replace("\n", " ")
    board_array=string_board.split(" ")
    
    Pawns=[[0 for _ in range(8)] for _ in range(8)]
    Rooks=[[0 for _ in range(8)] for _ in range(8)]
    Knights=[[0 for _ in range(8)] for _ in range(8)]
    Bishops=[[0 for _ in range(8)] for _ in range(8)]
    Queens=[[0 for _ in range(8)] for _ in range(8)]
    Kings=[[0 for _ in range(8)] for _ in range(8)]
    BPawns=[[0 for _ in range(8)] for _ in range(8)]
    BRooks=[[0 for _ in range(8)] for _ in range(8)]
    BKnights=[[0 for _ in range(8)] for _ in range(8)]
    BBishops=[[0 for _ in range(8)] for _ in range(8)]
    BQueens=[[0 for _ in range(8)] for _ in range(8)]
    BKings=[[0 for _ in range(8)] for _ in range(8)]
    whiteMoves=[[0 for _ in range(8)] for _ in range(8)]
    blackMoves=[[0 for _ in range(8)] for _ in range(8)]

    Types={"P":Pawns, "R":Rooks, "N":Knights, "B":Bishops, "Q":Queens, "K":Kings, "p":BPawns, "r":BRooks, "n":BKnights, "b":BBishops, "q":BQueens, "k":BKings }        
    
    for x in range(len(board_array)):
        if board_array[x] in Types:
            Types[board_array[x]][x//8][x%8]=1 


    #for move matrixs
    let_to_num={
        "a":0,
        "b":1,
        "c":2,
        "d":3,
        "e":4,
        "f":5,
        "g":6,
        "h":7
        
    }
    def indexs_of(square):
        letter=chess.square_name(square)
        return 8-int(letter[1]), let_to_num[letter[0]]
        
    aux=board.turn
    
    board.turn=chess.WHITE
    for move in board.legal_moves:
        x,y= indexs_of(move.to_square)
        whiteMoves[x][y]=1 
        
    board.turn=chess.BLACK
    for move in board.legal_moves:
        x,y= indexs_of(move.to_square)
        blackMoves[x][y]=1 
    
    board.turn=aux  
    final = np.array([Pawns, Rooks, Knights, Bishops, Queens, Kings,BPawns, BRooks, BKnights, BBishops, BQueens, BKings, whiteMoves, blackMoves])  
        
    return final  

def encode_moves(moves):
    move_to_int={move:idx for idx,move in enumerate(set(moves))}
    return [move_to_int[move] for move in moves], move_to_int

#load model and data and prepare for prediction
model=load_model("CagnusMarlsen.keras")
Y_train=np.load("Y_train.npy")
Y_train, move_to_int=encode_moves(Y_train)
int_to_move=dict(zip(move_to_int.values(),move_to_int.keys()))

def check_if_pawn_moved(board):#checks the precious moved pawn, used to check if black pawn was moved to itterate el passant, double pawn push trackers
    let_to_num={
        "a":0,
        "b":1,
        "c":2,
        "d":3,
        "e":4,
        "f":5,
        "g":6,
        "h":7
        
    }
    pawn_was_moved=False
    pawn_was_moved,pawn_moved_to=None,None
    previous_move=board.peek()
    double_pawn_push=is_double_pawn_push(previous_move)
    moved_piece = board.piece_at(previous_move.to_square)
    piece_name = moved_piece.symbol() 
    previous_move=previous_move.uci()
    if piece_name == "p":
        pawn_was_moved=True
        pawn_moved_to=previous_move[2:]
        pawn_moved_to=let_to_num[pawn_moved_to[0]],8-int(pawn_moved_to[1])
    return pawn_was_moved,pawn_moved_to,double_pawn_push

def is_double_pawn_push(move):
    #Double pawn push moves are from rank 2 to 4 for white pawns and rank 7 to 5 for black pawns
    if move.from_square // 8== 1 and move.to_square//8 == 3:  #White double pawn push
        return True
    elif move.from_square // 8 ==6 and move.to_square//8 == 4:  #Black double pawn push
        return True
    return False

def predict(board):#uses trained moved to predict next move. 
    board_matrix=board_to_matrix(board).reshape(1,14,8,8)
    predictions=model.predict(board_matrix)[0]
    legal_moves=list(board.legal_moves)
    legal_moves_uci=[move.uci() for move in legal_moves]
    sorted_indices=np.argsort(predictions)[::-1]
    for move_index in sorted_indices:
        move=int_to_move[move_index]
        if move in legal_moves_uci:
            return move
    # Get a list of all legal moves
    legal_moves = list(board.legal_moves)
    if not legal_moves:
        return None
    
    random_move = random.choice(legal_moves)
    return random_move.uci()
   

#converts board from chess.Board() to board that game can understand and use . 
def to_game(board,):
    black_pawn_moved, black_pawn_moved_to,black_double_pawn_push = check_if_pawn_moved(board)
    Types={"P":Pawn, "R":Rook, "N":Knight, "B":Bishop, "Q":Queen, "K":King, "p":Pawn, "r":Rook, "n":Knight, "b":Bishop, "q":Queen, "k":King }        
    
    bo=Board(8,8)
    bo.board=[[None for _ in range(8)] for _ in range(8)]
    string_board=str(board)
    string_board=string_board.replace("\n", " ")
    board_array=string_board.split(" ")
    
    for x in range(len(board_array)):
        if board_array[x] in Types:
            if board_array[x].isupper():
                bo.board[x//8][x%8]=Types[board_array[x]](x%8,x//8,'w')   
            else:
                bo.board[x//8][x%8]=Types[board_array[x]](x%8,x//8,'b')
    
    for i in range(8):# itterates through board adjusts pawn trackers so el passant and double pawn push works
        for j in range(8):
            if bo.board[i][j] is not None and type(bo.board[i][j])==Pawn:
                if black_pawn_moved:
                    if bo.board[i][j].color=='b' and i==black_pawn_moved_to[1] and j==black_pawn_moved_to[0] :
                        bo.board[i][j].turn+=1
                        if black_double_pawn_push:
                            bo.board[i][j].UsedMove=1 
                    elif i!=black_pawn_moved_to[1] and j!=black_pawn_moved_to[0] and (i!=1 and bo.board[i][j].color=='b')or (i!=6 and bo.board[i][j].color=='w'):
                        bo.board[i][j].turn+=2
                        
                else:
                    print(i, bo.board[i][j].color)
                    if (i!=1 and bo.board[i][j].color=='b')or(i!=6 and bo.board[i][j].color=='w'):
                        print(i,bo.board[i][j].color, "turn set to + 2")
                        bo.board[i][j].turn+=2
                        
                    

    
    return bo