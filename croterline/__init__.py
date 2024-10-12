from multiprocessing import set_start_method

# 设置Linux下默认开新进程的方式
set_start_method("spawn", force=True)
