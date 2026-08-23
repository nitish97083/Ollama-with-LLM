
import warnings

from sympy import true
warnings.filterwarnings('ignore')

from markitdown import MarkItDown 
from pathlib import Path

md = MarkItDown();
import os
os.makedirs('markitdown',exist_ok=true)

def conver_and_save(relative_path):
    file_path = Path(relative_path)
    result = md.convert(file_path)
    with open(f"markitdown/{file_path.stem}.md",'w',encoding= "utf-8") as  f:
     f.write(result.text_content)
     
conver_and_save("result_pdf/Dixon_Q1_result.pdf")

ymd = MarkItDown()  

result = ymd.convert("https://www.youtube.com/watch?v=ld0xui3d6-k")

data = result.text_content[:100]

print(f"response is --> {data}")

      
