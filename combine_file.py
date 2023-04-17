import glob
import os

# 폴더 내 모든 txt파일 불러오기
txt_files = glob.glob("*.txt")

# 합칠 모든 텍스트 파일 불러와서 합치기
with open("combined.txt", "w", encoding="utf-8") as outfile:
    
    for file in txt_files:
        with open(file, "r", encoding="utf-8") as infile:
            outfile.write(infile.read())
            outfile.write("\n")  
