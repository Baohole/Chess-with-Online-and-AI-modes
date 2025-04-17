import pygame
import main

print("Chạy game với minimax depth=2. Khi chơi, hãy đi quân e2e4 để kiểm tra.")

if __name__ == "__main__":
    # Khởi tạo pygame
    pygame.init()
    
    # Gọi hàm main với các tham số mặc định và độ sâu minimax = 2
    main.main(True, True) 