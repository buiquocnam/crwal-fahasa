#!/usr/bin/env python3
"""
Script để xóa tất cả các thư mục __pycache__ và file .pyc trong dự án.
Hỗ trợ xóa cache trong cả host và container Docker.
Có thể tắt tạo cache Python để tránh tạo lại __pycache__.
"""

import os
import shutil
import sys
import subprocess
import logging
import argparse

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def is_docker_running():
    """Kiểm tra xem Docker có đang chạy không."""
    try:
        subprocess.run(['docker', 'info'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def clean_container_cache(container_name, disable_cache=False):
    """Xóa cache trong container Docker và tùy chọn tắt tạo cache."""
    try:
        # Xóa cache hiện tại
        cmd = f"docker exec {container_name} find /app -type d -name '__pycache__' -exec rm -r {{}} +"
        subprocess.run(cmd, shell=True, check=True)
        cmd = f"docker exec {container_name} find /app -name '*.pyc' -delete"
        subprocess.run(cmd, shell=True, check=True)
        
        # Tắt tạo cache nếu được yêu cầu
        if disable_cache:
            cmd = f"docker exec {container_name} sh -c 'echo \"PYTHONDONTWRITEBYTECODE=1\" >> /etc/environment'"
            subprocess.run(cmd, shell=True, check=True)
            logger.info(f"Đã tắt tạo cache trong container {container_name}")
        
        logger.info(f"Đã xóa cache trong container {container_name}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Lỗi khi xử lý container {container_name}: {e}")

def clean_pycache(root_dir='.', disable_cache=False):
    """Xóa tất cả thư mục __pycache__ và file .pyc từ thư mục gốc."""
    total_dirs = 0
    total_files = 0
    
    logger.info(f"Đang quét thư mục {os.path.abspath(root_dir)}...")
    
    try:
        # Duyệt qua tất cả thư mục và file
        for dirpath, dirnames, filenames in os.walk(root_dir):
            # Bỏ qua thư mục .git và venv
            if '.git' in dirpath or 'venv' in dirpath:
                continue
                
            # Tìm và xóa các thư mục __pycache__
            if '__pycache__' in dirnames:
                pycache_path = os.path.join(dirpath, '__pycache__')
                try:
                    logger.info(f"Đang xóa thư mục {pycache_path}")
                    shutil.rmtree(pycache_path)
                    total_dirs += 1
                    dirnames.remove('__pycache__')
                except PermissionError:
                    logger.error(f"Không có quyền xóa thư mục {pycache_path}")
                except Exception as e:
                    logger.error(f"Lỗi khi xóa thư mục {pycache_path}: {e}")
            
            # Tìm và xóa file .pyc
            for filename in filenames:
                if filename.endswith('.pyc'):
                    pyc_path = os.path.join(dirpath, filename)
                    try:
                        logger.info(f"Đang xóa file {pyc_path}")
                        os.remove(pyc_path)
                        total_files += 1
                    except PermissionError:
                        logger.error(f"Không có quyền xóa file {pyc_path}")
                    except Exception as e:
                        logger.error(f"Lỗi khi xóa file {pyc_path}: {e}")
    
        logger.info(f"\nĐã xóa thành công {total_dirs} thư mục __pycache__ và {total_files} file .pyc")
        
        # Xóa cache trong container nếu Docker đang chạy
        if is_docker_running():
            containers = ['fahasa_web', 'fahasa_api', 'crawler', 'ingestion']
            for container in containers:
                clean_container_cache(container, disable_cache)
        
        # Tắt tạo cache trong môi trường hiện tại nếu được yêu cầu
        if disable_cache:
            os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
            logger.info("Đã tắt tạo cache Python trong môi trường hiện tại")
                
    except Exception as e:
        logger.error(f"Lỗi không mong muốn: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Xóa cache Python và tùy chọn tắt tạo cache')
    parser.add_argument('directory', nargs='?', default='.', help='Thư mục cần quét')
    parser.add_argument('--disable-cache', action='store_true', help='Tắt tạo cache Python')
    args = parser.parse_args()
    
    clean_pycache(args.directory, args.disable_cache)