import chess
import random

# Giá trị tĩnh cho các quân cờ
PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}

# Bảng vị trí cho quân tốt (đánh giá vị trí tốt cho quân tốt)
PAWN_TABLE = [
    0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
    5,  5, 10, 25, 25, 10,  5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5, -5,-10,  0,  0,-10, -5,  5,
    5, 10, 10,-20,-20, 10, 10,  5,
    0,  0,  0,  0,  0,  0,  0,  0
]

# Bảng vị trí cho quân mã (đánh giá vị trí tốt cho quân mã)
KNIGHT_TABLE = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50
]

# Bảng vị trí cho quân tượng (đánh giá vị trí tốt cho quân tượng)
BISHOP_TABLE = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  5,  5,  5,  5,  5,  5,-10,
    -10,  0,  5,  0,  0,  5,  0,-10,
    -20,-10,-10,-10,-10,-10,-10,-20
]

# Bảng vị trí cho quân xe (đánh giá vị trí tốt cho quân xe)
ROOK_TABLE = [
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10, 10, 10, 10, 10,  5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    0,  0,  0,  5,  5,  0,  0,  0
]

# Bảng vị trí cho quân hậu (đánh giá vị trí tốt cho quân hậu)
QUEEN_TABLE = [
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5,  5,  5,  5,  0,-10,
    -5,  0,  5,  5,  5,  5,  0, -5,
    0,  0,  5,  5,  5,  5,  0, -5,
    -10,  5,  5,  5,  5,  5,  0,-10,
    -10,  0,  5,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20
]

# Bảng vị trí cho quân vua (giai đoạn đầu/giữa) (đánh giá vị trí tốt cho quân vua)
KING_TABLE = [
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -10,-20,-20,-20,-20,-20,-20,-10,
    20, 20,  0,  0,  0,  0, 20, 20,
    20, 30, 10,  0,  0, 10, 30, 20
]

# Bảng vị trí cho quân vua (giai đoạn cuối) (đánh giá vị trí tốt cho quân vua)
KING_ENDGAME_TABLE = [
    -50,-40,-30,-20,-20,-30,-40,-50,
    -30,-20,-10,  0,  0,-10,-20,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-30,  0,  0,  0,  0,-30,-30,
    -50,-30,-30,-30,-30,-30,-30,-50
]

def is_endgame(board):
    """Kiểm tra xem ván cờ đã vào giai đoạn cuối chưa (ít quân hơn)"""
    # Nếu mỗi bên có ít hơn hoặc bằng một quân tướng (ngoài vua) hoặc 
    # tổng giá trị quân cờ ít hơn 3300 thì coi là giai đoạn cuối
    queens = len(board.pieces(chess.QUEEN, chess.WHITE)) + len(board.pieces(chess.QUEEN, chess.BLACK))
    rooks = len(board.pieces(chess.ROOK, chess.WHITE)) + len(board.pieces(chess.ROOK, chess.BLACK))
    minors = (len(board.pieces(chess.KNIGHT, chess.WHITE)) + len(board.pieces(chess.KNIGHT, chess.BLACK)) +
              len(board.pieces(chess.BISHOP, chess.WHITE)) + len(board.pieces(chess.BISHOP, chess.BLACK)))
    
    return queens == 0 or (queens == 1 and rooks <= 1) or (queens == 0 and rooks <= 2 and minors <= 1)

def evaluate_piece_position(piece_type, square, is_endgame=False):
    """Đánh giá vị trí của một quân cờ dựa trên bảng giá trị vị trí"""
    rank = chess.square_rank(square)
    file = chess.square_file(square)
    
    # Đảo ngược thứ tự cho quân đen
    position_value_idx = 8 * (7 - rank) + file
    
    if piece_type == chess.PAWN:
        return PAWN_TABLE[position_value_idx]
    elif piece_type == chess.KNIGHT:
        return KNIGHT_TABLE[position_value_idx]
    elif piece_type == chess.BISHOP:
        return BISHOP_TABLE[position_value_idx]
    elif piece_type == chess.ROOK:
        return ROOK_TABLE[position_value_idx]
    elif piece_type == chess.QUEEN:
        return QUEEN_TABLE[position_value_idx]
    elif piece_type == chess.KING:
        if is_endgame:
            return KING_ENDGAME_TABLE[position_value_idx]
        else:
            return KING_TABLE[position_value_idx]
    
    return 0

def evaluate_board(board):
    """Đánh giá trạng thái hiện tại của bàn cờ"""
    if board.is_checkmate():
        # Nếu bị chiếu bí, đó là điều tồi tệ nhất
        return -10000 if board.turn else 10000
    
    if board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_fivefold_repetition():
        # Hòa có giá trị 0
        return 0
    
    # Tính tổng giá trị vật chất và vị trí
    total_value = 0
    endgame = is_endgame(board)
    
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is None:
            continue
        
        # Cộng/trừ giá trị quân cờ
        value = PIECE_VALUES[piece.piece_type]
        # Cộng thêm giá trị vị trí
        value += evaluate_piece_position(piece.piece_type, square, endgame)
        
        # Nếu là quân trắng thì cộng, đen thì trừ
        if piece.color == chess.WHITE:
            total_value += value
        else:
            total_value -= value
    
    # Thêm một số đánh giá khác
    # Quân tốt đôi (khuyết điểm)
    doubled_pawns_w = 0
    doubled_pawns_b = 0
    for file in range(8):
        pawns_w_in_file = 0
        pawns_b_in_file = 0
        for rank in range(8):
            square = chess.square(file, rank)
            piece = board.piece_at(square)
            if piece and piece.piece_type == chess.PAWN:
                if piece.color == chess.WHITE:
                    pawns_w_in_file += 1
                else:
                    pawns_b_in_file += 1
        if pawns_w_in_file > 1:
            doubled_pawns_w += 1
        if pawns_b_in_file > 1:
            doubled_pawns_b += 1
    
    total_value -= doubled_pawns_w * 15
    total_value += doubled_pawns_b * 15
    
    # Cộng điểm cho quân tốt tiến xa vào lãnh thổ địch
    for square in board.pieces(chess.PAWN, chess.WHITE):
        rank = chess.square_rank(square)
        total_value += rank * 10  # Càng tiến gần đích (rank cao) càng tốt
        
    for square in board.pieces(chess.PAWN, chess.BLACK):
        rank = chess.square_rank(square)
        total_value -= (7 - rank) * 10  # Càng tiến gần đích (rank thấp) càng tốt
    
    # Đang bị chiếu (khuyết điểm)
    if board.is_check():
        if board.turn == chess.WHITE:
            total_value -= 50
        else:
            total_value += 50
    
    return total_value if board.turn == chess.WHITE else -total_value

def minimax(board, depth, alpha, beta, maximizing_player):
    """Thuật toán minimax với cắt tỉa alpha-beta"""
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)
    
    if maximizing_player:
        max_eval = float('-inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Cắt tỉa beta
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Cắt tỉa alpha
        return min_eval

def get_best_move(board, depth=3):
    """Tìm nước đi tốt nhất sử dụng minimax"""
    try:
        best_move = None
        best_value = float('-inf') if board.turn == chess.WHITE else float('inf')
        alpha = float('-inf')
        beta = float('inf')
        maximizing_player = board.turn == chess.WHITE
        
        # Sắp xếp các nước đi để tối ưu hóa cắt tỉa alpha-beta
        moves = list(board.legal_moves)
        print(f"Tìm nước đi tốt nhất từ {len(moves)} nước đi hợp lệ với độ sâu {depth}")
        
        # Các nước đi được ưu tiên (kiểm tra, ăn quân, phong cấp) sẽ được xem xét trước
        # Heuristic đơn giản: Cố gắng đánh giá trước các nước đi có tiềm năng tốt
        def move_score(move):
            try:
                score = 0
                # Kiểm tra xem nước đi có phải là ăn quân
                if board.is_capture(move):
                    score += 10
                    # Ăn quân có giá trị cao được ưu tiên
                    to_piece = board.piece_at(move.to_square)
                    if to_piece:
                        score += PIECE_VALUES[to_piece.piece_type] // 100
                        
                # Phong cấp quân tốt
                if move.promotion:
                    score += 15
                    
                # Nước đi vào trung tâm
                to_file = chess.square_file(move.to_square)
                to_rank = chess.square_rank(move.to_square)
                center_distance = abs(3.5 - to_file) + abs(3.5 - to_rank)
                score += max(0, 5 - center_distance)
                    
                return score
            except Exception as e:
                print(f"Lỗi khi tính điểm nước đi {move}: {e}")
                return 0
        
        # Sắp xếp nước đi theo điểm số
        try:
            moves.sort(key=move_score, reverse=True)
        except Exception as e:
            print(f"Lỗi khi sắp xếp nước đi: {e}")
        
        # Kiểm tra xem có nước đi nào có thể chiếu hết ngay lập tức không
        for move in moves:
            board.push(move)
            if board.is_checkmate():
                print(f"Tìm thấy nước chiếu hết ngay lập tức: {move}")
                board.pop()
                return move
            board.pop()
        
        # Thực hiện minimax cho các nước đi
        for move in moves:
            try:
                board.push(move)
                
                # Kiểm tra nhanh xem có phải chiếu bí ngay không
                if board.is_checkmate():
                    board.pop()
                    return move
                    
                board_value = minimax(board, depth - 1, alpha, beta, not maximizing_player)
                board.pop()
                
                if maximizing_player and board_value > best_value:
                    best_value = board_value
                    best_move = move
                    alpha = max(alpha, best_value)
                elif not maximizing_player and board_value < best_value:
                    best_value = board_value
                    best_move = move
                    beta = min(beta, best_value)
            except Exception as e:
                print(f"Lỗi khi phân tích nước đi {move}: {e}")
                board.pop()
        
        if best_move is None:
            # Nếu không tìm được nước đi tốt nhất (hiếm khi xảy ra), chọn ngẫu nhiên
            if moves:
                best_move = random.choice(moves)
                print(f"Không tìm thấy nước đi tốt nhất, chọn ngẫu nhiên: {best_move}")
        else:
            print(f"Nước đi tốt nhất là: {best_move} với giá trị {best_value}")
        
        return best_move
    except Exception as e:
        print(f"Lỗi trong get_best_move: {e}")
        import traceback
        traceback.print_exc()
        
        # Chọn một nước đi ngẫu nhiên nếu có lỗi
        try:
            moves = list(board.legal_moves)
            if moves:
                random_move = random.choice(moves)
                print(f"Chọn ngẫu nhiên nước đi sau lỗi trong get_best_move: {random_move}")
                return random_move
        except:
            pass
        
        return None

def predict_minimax(board, depth=3):
    """API tương thích với CagnusMarlsen.predict"""
    try:
        # Đảm bảo depth là số nguyên
        depth = int(depth)
        print(f"Minimax đang tính toán với độ sâu {depth}")
        print(f"Trạng thái bàn cờ: {board}")
        legal_moves = list(board.legal_moves)
        print(f"Các nước đi hợp lệ: {legal_moves}")
        
        if not legal_moves:
            print("Không có nước đi hợp lệ")
            return None
        
        # Nếu chỉ có một nước đi hợp lệ, không cần tính toán
        if len(legal_moves) == 1:
            only_move = legal_moves[0]
            print(f"Chỉ có một nước đi hợp lệ: {only_move}")
            return only_move.uci()
        
        # Tăng độ sâu nếu ít nước đi để tăng hiệu suất
        if len(legal_moves) <= 5 and depth < 4:
            depth += 1
            print(f"Tăng độ sâu lên {depth} vì chỉ có {len(legal_moves)} nước đi hợp lệ")
        
        best_move = get_best_move(board, depth)
        print(f"Nước đi tốt nhất: {best_move}")
        
        if best_move:
            return best_move.uci()
        else:
            print("Không tìm thấy nước đi tốt nhất, chọn ngẫu nhiên")
            random_move = random.choice(legal_moves)
            return random_move.uci()
    except Exception as e:
        print(f"Lỗi trong predict_minimax: {e}")
        import traceback
        traceback.print_exc()
        
        # Luôn đảm bảo trả về một nước đi hợp lệ
        try:
            legal_moves = list(board.legal_moves)
            if legal_moves:
                random_move = random.choice(legal_moves)
                print(f"Chọn ngẫu nhiên nước đi sau lỗi: {random_move}")
                return random_move.uci()
        except:
            pass
        
        return None

def to_game(board):
    """Triển khai lại hàm to_game để tương thích với CagnusMarlsen"""
    from board import Board
    from piece import Pawn, Rook, Knight, Bishop, Queen, King
    
    try:
        print(f"Minimax to_game được gọi với bàn cờ: {board}")
        
        # Kiểm tra nước đi trước đó cho en passant
        try:
            previous_move = board.peek()
            print(f"Nước đi trước đó: {previous_move}")
            double_pawn_push = is_double_pawn_push(previous_move)
            moved_piece = board.piece_at(previous_move.to_square)
            piece_name = moved_piece.symbol() if moved_piece else None
            
            pawn_was_moved = False
            pawn_moved_to = None
            black_double_pawn_push = False
            
            if piece_name == "p":  # Quân tốt đen
                pawn_was_moved = True
                previous_move_uci = previous_move.uci()
                let_to_num = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
                pawn_moved_to = (let_to_num[previous_move_uci[2]], 8 - int(previous_move_uci[3]))
                black_double_pawn_push = double_pawn_push
                print(f"Tốt đen được di chuyển đến: {pawn_moved_to}, double push: {black_double_pawn_push}")
        except (IndexError, ValueError, AttributeError) as e:
            print(f"Không thể lấy nước đi trước đó: {e}")
            # Không có nước đi trước đó
            pawn_was_moved = False
            pawn_moved_to = None
            black_double_pawn_push = False
        
        bo = Board(8, 8)
        bo.board = [[None for _ in range(8)] for _ in range(8)]
        
        Types = {"P": Pawn, "R": Rook, "N": Knight, "B": Bishop, "Q": Queen, "K": King, 
                "p": Pawn, "r": Rook, "n": Knight, "b": Bishop, "q": Queen, "k": King}
        
        string_board = str(board)
        string_board = string_board.replace("\n", " ")
        board_array = string_board.split(" ")
        
        for x in range(len(board_array)):
            if board_array[x] in Types:
                if board_array[x].isupper():
                    bo.board[x//8][x%8] = Types[board_array[x]](x%8, x//8, 'w')   
                else:
                    bo.board[x//8][x%8] = Types[board_array[x]](x%8, x//8, 'b')
        
        # Điều chỉnh trạng thái các quân tốt để hỗ trợ chức năng en passant
        for i in range(8):
            for j in range(8):
                if bo.board[i][j] is not None and isinstance(bo.board[i][j], Pawn):
                    if pawn_was_moved:
                        if bo.board[i][j].color == 'b' and i == pawn_moved_to[1] and j == pawn_moved_to[0]:
                            bo.board[i][j].turn += 1
                            if black_double_pawn_push:
                                bo.board[i][j].UsedMove = 1 
                        elif (i != pawn_moved_to[1] or j != pawn_moved_to[0]) and ((i != 1 and bo.board[i][j].color == 'b') or (i != 6 and bo.board[i][j].color == 'w')):
                            bo.board[i][j].turn += 2
                    else:
                        if (i != 1 and bo.board[i][j].color == 'b') or (i != 6 and bo.board[i][j].color == 'w'):
                            bo.board[i][j].turn += 2
        
        print("Bàn cờ đã được khởi tạo thành công từ minimax")
        return bo
    except Exception as e:
        print(f"Lỗi trong to_game: {e}")
        import traceback
        traceback.print_exc()
        # Tạo một bàn cờ trống trong trường hợp lỗi
        bo = Board(8, 8)
        return bo

def is_double_pawn_push(move):
    """Kiểm tra xem nước đi có phải là đẩy tốt 2 ô không"""
    if move.from_square // 8 == 1 and move.to_square // 8 == 3:  # Tốt trắng đẩy 2 ô
        return True
    elif move.from_square // 8 == 6 and move.to_square // 8 == 4:  # Tốt đen đẩy 2 ô
        return True
    return False 