import csv

with open('News_KEYWORD.csv', 'r', encoding='utf-8') as csv_file:
    reader = csv.reader(csv_file)
    with open('KEYWORD_txt', 'w', encoding='utf-8') as txt_file:
        for row in reader:
            #csv 파일의 2번째에 담겨있는 것이 기사의 내용이기 때문에, 마침표를 기준으로 문장을 나눈다.
            sentences = row[2].split('.')
            for i, sentence in enumerate(sentences):
                # 앞뒤 공백을 제거하고 각 문장을 txt 파일에 쓴다.
                txt_file.write(sentence.strip() + '\n')
                # 다음 문장이 목록의 마지막 문장이 아닌지 확인하고 필요한 경우 개행 문자를 추가한다.
                if i != len(sentences) - 1:
                    txt_file.write('\n')


