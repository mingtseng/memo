import time
from docx2pdf import convert
start = time.perf_counter()
convert('word/', 'pdf/')
end = time.perf_counter()
interval = end - start
print("运行时间：{:.1f}s".format(interval))
