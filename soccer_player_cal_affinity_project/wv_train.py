# word embedding for "tokenized text file"
# C> wv_train.py "tokenized_text_file"

from gensim.models import word2vec
import sys

def wv_KMA_tokens_train(filename):
		print(f"\nTraining word embedding vectors for <{filename}>.")
		f = open(filename, "r", encoding='utf-8')
		#f = open(filename, "r", encoding='cp949')
		text = f.readlines()
		f.close()

		tokens = []
		for sent in text:
			tokens.append(sent.split())

		#model = word2vec.Word2Vec(tokens)
		model = word2vec.Word2Vec(sentences=tokens, vector_size=300, window=5, min_count=2, workers=4)

		model_file = 'word2vec-' + filename[:-4] + '.model'
		model.save(model_file)
		print(f"--> Model file <{model_file}> was created!\n")
		return model

if __name__ == "__main__":
		if len(sys.argv) < 2:
				print("C> wv_train.py test.txt")
				exit()
		model = wv_KMA_tokens_train(sys.argv[1])  # 'KMA tokenized text file'

		#print(model.wv.get_vector('배우'))
		#print(model.wv.get_vector('여배우'))
		
		#print(model.wv.similarity('배우', '여배우'))
		#print(model.wv.similarity('배우', '남자'))
		#print(model.wv.similarity('남자', '여배우'))
		
		#print(model.wv.most_similar(positive=['남자'], topn=5))
		# calculate: (남자 - 배우) + 여배우 = ?
		#print(model.wv.most_similar(positive=['남자', '여배우'], negative=['배우'], topn=5))
