import logging

# 로깅 설정
logging.basicConfig(
    level=logging.DEBUG,  
    format='%(asctime)s - %(message)s', 
    datefmt='%m/%d/%Y %H:%M:%S',
    handlers=[
        logging.FileHandler('./log/app.log'),
        logging.StreamHandler()
    ]
)

# 로거 생성
logger = logging.getLogger(__name__)
