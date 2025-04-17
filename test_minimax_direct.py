import chess
import minimax_ai

def test_minimax_sequence():
    # Tạo bàn cờ mới
    board = chess.Board()
    print("Bàn cờ ban đầu:")
    print(board)
    
    # Danh sách các nước đi người chơi sẽ thực hiện
    player_moves = ["e2e4", "g1f3", "d2d4", "b1c3"]
    
    # Mô phỏng lượt đi luân phiên
    for i, move in enumerate(player_moves):
        print(f"\nLượt đi {i+1} của người chơi: {move}")
        # Người chơi đi quân trắng
        board.push(chess.Move.from_uci(move))
        print("Bàn cờ sau nước đi của người chơi:")
        print(board)
        
        # AI đi quân đen
        ai_move = minimax_ai.predict_minimax(board, 3)
        if ai_move:
            print(f"AI (quân đen) chọn nước đi: {ai_move}")
            board.push(chess.Move.from_uci(ai_move))
            print("Bàn cờ sau nước đi của AI:")
            print(board)
        else:
            print("AI không tìm được nước đi phù hợp!")
            break
    
    print("\nKết thúc kiểm thử.")

if __name__ == "__main__":
    test_minimax_sequence() 