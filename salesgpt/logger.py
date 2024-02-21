import logging
import time
from functools import wraps

# Configuração do logger
logger = logging.getLogger(__name__)

# Manipuladores de saída para logging
stream_handler = logging.StreamHandler()
log_filename = "output.log"
file_handler = logging.FileHandler(filename=log_filename)
handlers = [stream_handler, file_handler]

# Filtro personalizado para filtrar registros com a mensagem "Running"
class TimeFilter(logging.Filter):
    def filter(self, record):
        return "Running" in record.getMessage()

# Adiciona o filtro ao logger
logger.addFilter(TimeFilter())

# Configuração básica do módulo de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(name)s %(asctime)s - %(levelname)s - %(message)s",
    handlers=handlers,
)

# Decorador para registrar o tempo de execução de uma função
def time_logger(func):
    """Decorator function to log time taken by any function."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Tempo inicial antes da execução da função
        result = func(*args, **kwargs)  # Execução da função
        end_time = time.time()  # Tempo final após a execução da função
        execution_time = end_time - start_time  # Calcula o tempo de execução
        logger.info(f"Running {func.__name__}: --- {execution_time} seconds ---")
        return result

    return wrapper
