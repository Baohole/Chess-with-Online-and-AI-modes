import chess
import minimax_ai

# Tạo một bàn cờ mới
board = chess.Board()

# Kiểm tra chế độ minimax
print("Kiểm tra chế độ minimax với độ sâu 3")
print(f"Trạng thái bàn cờ hiện tại: {board}")
print(f"Các nước đi hợp lệ: {list(board.legal_moves)}")

# Thực hiện nước đi của người chơi
player_move = chess.Move.from_uci("e2e4")
print(f"Người chơi thực hiện nước đi: {player_move}")
board.push(player_move)
print(f"Bàn cờ sau nước đi của người chơi: {board}")

# Tìm nước đi tốt nhất với độ sâu 3
best_move = minimax_ai.predict_minimax(board, 3)
print(f"Nước đi tốt nhất cho AI: {best_move}")

# Thực hiện nước đi và cập nhật bàn cờ
if best_move:
    board.push(chess.Move.from_uci(best_move))
    print(f"Bàn cờ sau nước đi AI: {board}")
    
    # Chuyển đổi sang định dạng bàn cờ của game
    game_board = minimax_ai.to_game(board)
    print("Bàn cờ đã được chuyển đổi thành công")
    
# Thực hiện nước đi thứ hai của người chơi
player_move2 = chess.Move.from_uci("g1f3")
print(f"Người chơi thực hiện nước đi thứ hai: {player_move2}")
board.push(player_move2)
print(f"Bàn cờ sau nước đi thứ hai của người chơi: {board}")

# Tìm nước đi thứ hai cho AI
best_move2 = minimax_ai.predict_minimax(board, 3)
print(f"Nước đi thứ hai cho AI: {best_move2}")

if best_move2:
    board.push(chess.Move.from_uci(best_move2))
    print(f"Bàn cờ sau nước đi thứ hai của AI: {board}")
    
    # Chuyển đổi sang định dạng bàn cờ của game
    game_board2 = minimax_ai.to_game(board)
    print("Bàn cờ đã được chuyển đổi thành công lần thứ hai") 