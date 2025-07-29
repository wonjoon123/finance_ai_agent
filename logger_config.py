import logging
from logging.handlers import RotatingFileHandler

def setup_logger(name="main", log_file="app.log", level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:  # 중복 핸들러 방지
        formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s')

        # 콘솔
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        
        # ✅ 로그 파일: 최대 1MB, 5개까지 보관
        log_file = "app.log"
        max_size = 1 * 1024 * 1024 * 1024  # 1GB
        backup_count = 5            # 이전 로그 5개까지 보관

        # 핸들러 설정
        fh = RotatingFileHandler(log_file, maxBytes=max_size, backupCount=backup_count)
        fh.setFormatter(formatter)

        logger.addHandler(ch)
        logger.addHandler(fh)

    return logger