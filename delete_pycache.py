import os
import shutil

# Menelusuri seluruh folder mulai dari direktori saat ini
for root, dirs, files in os.walk("."):
    for dir in dirs:
        if dir == "__pycache__":
            # Menghapus folder __pycache__ yang ditemukan
            shutil.rmtree(os.path.join(root, dir))
            print(f"Deleted: {os.path.join(root, dir)}")