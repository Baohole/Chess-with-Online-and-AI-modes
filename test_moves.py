import chess

def test_move_conversion():
    # Mô phỏng thông tin từ game
    xcoord = 4  # vị trí bắt đầu (cột e2)
    ycoord = 6  # vị trí bắt đầu (hàng 2)
    col = 4     # vị trí đích (cột e4)
    row = 4     # vị trí đích (hàng 4)
    
    board_to_uci = {0:'a', 1:'b', 2:'c', 3:'d', 4:'e', 5:'f', 6:'g', 7:'h'}
    
    # Tạo nước đi UCI
    from_square = board_to_uci[xcoord] + str(8-ycoord)
    to_square = board_to_uci[col] + str(8-row)
    move_uci = from_square + to_square
    
    print(f"Nước đi từ tọa độ board ({xcoord},{ycoord}) đến ({col},{row})")
    print(f"Trong hàm convert nước đi UCI: {from_square} -> {to_square}")
    print(f"Move UCI hoàn chỉnh: {move_uci}")
    
    # Kiểm tra với thư viện chess
    board = chess.Board()
    try:
        move = chess.Move.from_uci(move_uci)
        print(f"Nước đi hợp lệ: {move}")
        print(f"Bàn cờ ban đầu:\n{board}")
        board.push(move)
        print(f"Bàn cờ sau nước đi:\n{board}")
    except ValueError as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    test_move_conversion() 