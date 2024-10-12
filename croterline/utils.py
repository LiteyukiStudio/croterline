from multiprocessing import current_process

IsMainProcess = current_process().name == "MainProcess"
