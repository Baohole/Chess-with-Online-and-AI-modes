import pygame
import main

print("Chạy game với minimax depth=3. Các nước đi sẽ được hiển thị trực quan trên bàn cờ:")
print("- Ô xuất phát được tô màu xanh lá")
print("- Ô đích được tô màu đỏ")

# Khởi chạy game với chế độ minimax
if __name__ == "__main__":
    # Khởi tạo pygame
    pygame.init()
    
    # Gọi hàm main với các tham số mặc định
    # black và white là các tham số cho quyền castle
    main.main(True, True) 