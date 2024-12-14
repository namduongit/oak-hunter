import os
from PIL import Image

# Đường dẫn tới thư mục chứa các ảnh
folder_path = 'Entity/Boss/Hurt'

# Lấy danh sách các tệp PNG trong thư mục
image_files = [f for f in os.listdir(folder_path) if f.endswith('.png')]

# Duyệt qua từng tấm ảnh và lật ảnh
for image_file in image_files:
    # Đường dẫn đầy đủ đến tấm ảnh
    image_path = os.path.join(folder_path, image_file)

    # Mở tấm ảnh
    image = Image.open(image_path)

    # Lật ảnh theo trục x
    flipped_image = image.transpose(Image.FLIP_LEFT_RIGHT)

    # Lưu ảnh đã lật vào thư mục mới hoặc cùng thư mục
    flipped_image_path = os.path.join(folder_path, f"{image_file}")
    flipped_image.save(flipped_image_path)

    print(f"Đã lật và lưu ảnh: {flipped_image_path}")
