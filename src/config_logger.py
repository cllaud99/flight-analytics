import os
import time
from functools import wraps

from loguru import logger


def setup_logger():
    """
    Configura o logger com rotação de logs e armazenamento em arquivos zipados.
    """
    # Definindo o diretório onde os logs serão armazenados
    log_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "..", "data", "logs"
    )

    # Criando o diretório de logs se não existir
    os.makedirs(log_dir, exist_ok=True)

    # Configuração do Loguru para salvar logs
    logger.add(
        os.path.join(log_dir, "app_{time:YYYY-MM-DD}.log"),  # Nome do arquivo de log
        rotation="00:00",  # Rotaciona todos os dias à meia-noite
        retention="7 days",  # Mantém os logs por 7 dias
        compression="zip",  # Compacta os logs antigos em .zip
        level="WARNING",  # Nível mínimo de log (pode ser DEBUG, INFO, WARNING, ERROR, etc.)
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",  # Formato do log
    )

    # Exemplo de log para garantir que o logger está configurado corretamente
    logger.info("Logger configurado com sucesso.")


def logger_time_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(
            f"Tempo de execução da função '{func.__name__}': {execution_time} segundos"
        )
        return result

    return wrapper


@logger_time_decorator
def logger_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(
            f"Chamada da função: {func.__name__} com argumentos: {args}, {kwargs}"
        )
        try:
            result = func(*args, **kwargs)
            logger.info(f"Resultado da função '{func.__name__}'	: {result}")
            return result
        except Exception as e:
            logger.exception(f"Erro na função '{func.__name__}': {e}")
            raise

    return wrapper
