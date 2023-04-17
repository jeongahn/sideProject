import re

with open('KEYWORD_txt', 'r', encoding='utf-8') as txt_file:
    with open('KEYWORD_txt_clean', 'w', encoding='utf-8') as txt_clean_file:
        for line in txt_file:
            # 각 줄의 앞뒤 공백을 제거한다.
            line = line.strip()
            # 줄이 비어 있지 않으면 들여쓰기된 부분을 제거한 후 정리된 txt 파일에 추가합니다.
            if line:
                # 공백이 아닌 첫 번째 문자의 인덱스를 찾는다.
                first_char_index = 0
                while first_char_index < len(line) and line[first_char_index] == ' ':
                    first_char_index += 1
                # 들여쓰기 된 부분을 제거하고 정리 된 줄을 정리 된 txt 파일에 쓴다.
                cleaned_line = line[first_char_index:]
                # 정리된 줄의 길이를 확인하고, 길이가 15보다 큰 경우와 한글로만 구성된 문장만 txt 파일에 쓴다. (기자의 이름, 불필요한 정보 전처리)
                
                if len(cleaned_line) > 15:
                    if re.search('[a-zA-Z]', cleaned_line):
                        continue
                    cleaned_line += '\n'
                    txt_clean_file.write(cleaned_line)


