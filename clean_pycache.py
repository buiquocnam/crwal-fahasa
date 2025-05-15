#!/usr/bin/env python3
"""
Script để xóa tất cả các thư mục __pycache__ và file .pyc trong dự án.
"""

import os
import shutil
import sys

def clean_pycache(root_dir='.'):
    """Xóa tất cả thư mục __pycache__ và file .pyc từ thư mục gốc."""
    total_dirs = 0
    total_files = 0
    
    print(f"Đang quét thư mục {os.path.abspath(root_dir)}...")
    
    # Duyệt qua tất cả thư mục và file
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Tìm và xóa các thư mục __pycache__
        if '__pycache__' in dirnames:
            pycache_path = os.path.join(dirpath, '__pycache__')
            print(f"Đang xóa thư mục {pycache_path}")
            shutil.rmtree(pycache_path)
            total_dirs += 1
            dirnames.remove('__pycache__')  # Tránh duyệt vào thư mục đã xóa
        
        # Tìm và xóa file .pyc
        for filename in filenames:
            if filename.endswith('.pyc'):
                pyc_path = os.path.join(dirpath, filename)
                print(f"Đang xóa file {pyc_path}")
                os.remove(pyc_path)
                total_files += 1
    
    print(f"\nĐã xóa thành công {total_dirs} thư mục __pycache__ và {total_files} file .pyc")

if __name__ == "__main__":
    # Sử dụng thư mục được chỉ định hoặc thư mục hiện tại
    directory = sys.argv[1] if len(sys.argv) > 1 else '.'
    clean_pycache(directory) 