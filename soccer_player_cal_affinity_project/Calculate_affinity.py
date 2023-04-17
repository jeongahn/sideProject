# Cacluate_affinity.py

from gensim.models import Word2Vec
import sys

try:
    import matplotlib.pyplot as plt
except:
    raise

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

from matplotlib import rc
import matplotlib as mpl
import networkx as nx
import numpy as np
import os


# get the current value of the classpath environment variable
classpath = os.environ.get('CLASSPATH', '')

# add the path of the HamPack.jar file to the classpath
classpath += os.pathsep + '/path/to/HamPack.jar'

# set the updated classpath environment variable
os.environ['CLASSPATH'] = classpath


# most_similar 결과를 수치를 기반으로 한 막대그래프를 시각화하여 보여주는 메소드
def visualize_most_similar(model, keywords):
    font_name = fm.FontProperties(
        fname="c:/Windows/Fonts/malgun.ttf").get_name()
    rc('font', family=font_name)
    mpl.rcParams['axes.unicode_minus'] = False  # 한글 폰트 사용시 마이너스 폰트 깨짐 해결

    with open('불용어.txt', 'r', encoding='utf-8') as stop_words:
        stopwords = [line.strip() for line in stop_words.readlines()]

    similar_words = model.wv.most_similar(
        positive=[keywords, u'동료', '콤비'], negative=[u'다툼'], topn=10)

    result = []
    count = 0
    for word, score in similar_words:
        if word not in stopwords:
            result.append((word, score))
            count += 1
        if count == 5:  # 불용어를 제외한 상위 5개 단어를 출력
            break

    words = [word[0] for word in result]
    scores = [word[1] for word in result]
    plt.bar(words, scores)
    plt.xticks(rotation=90)

    plt.show()


def setEdges_simWords(model, word, n1=10, n2=5):
    with open('불용어.txt', 'r', encoding='utf-8') as stop_words:
        stopwords = [line.strip() for line in stop_words.readlines()]
        simWords = model.wv.most_similar(word, topn=n1)

        G = nx.Graph()
        for (w2, wgt) in simWords:  # 1차 확장
            if w2 not in stopwords:
                G.add_edge(word, w2, weight=round(wgt, 2))

        for (w2, wgt) in simWords:
            simWords2 = model.wv.most_similar(w2, topn=n2)
            for (w3, wgt) in simWords2:  # 2차 확장
                if w2 not in stopwords:
                    G.add_edge(w2, w3, weight=round(wgt, 2))

        return G


def visualization(G, imageFileName, nodecolor='skyblue', edgelabel='yes'):
	plt.figure(figsize=(15, 15), dpi=80)

	font_name = fm.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
	rc('font', family=font_name)
	mpl.rcParams['axes.unicode_minus'] = False  # 한글 폰트 사용시 마이너스 폰트 깨짐 해결

	elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] > 0.5]
	esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] <= 0.5]

	pos = nx.spring_layout(G)  # positions for all nodes

	# nodes
	d = dict(G.degree)
	nx.draw_networkx_nodes(G, pos, node_size=[v*100+1000 for v in d.values()],
                        node_color=nodecolor)  # default color: '#1f78b4'

	# edges
	nx.draw_networkx_edges(G, pos, edgelist=elarge,
                        width=1.2, edge_color='blue')
	nx.draw_networkx_edges(G, pos, edgelist=esmall,
                        width=1.2, alpha=0.5, edge_color='b', style='dashed')

	# edge labels
	if edgelabel == 'yes':
		edge_weight = nx.get_edge_attributes(G, 'weight')
		nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_weight)

		# labels
		nx.draw_networkx_labels(G, pos, font_family=font_name, font_size=14)

		plt.axis('off')
		plt.savefig('%s' % (imageFileName))  # save as png
		print('It was saved %s' % (imageFileName))
		plt.show()  # display


if __name__ == "__main__":

    keyword = "test"
    color = "skyblue"
    nsim_1 = 5
    nsim_2 = 5
    elabel = 'yes'
    # model_name = "word2vec-combined_KMA_UTF_8.model"
    model_name = "word2vec-combined_KMA_UTF_8.model"

    if len(sys.argv) < 2:
        print("C> Calculate_affinity.py word2vec.model keyword(you want to know)")
        exit()
    elif len(sys.argv) == 2:
        keyword = sys.argv[1]
    elif len(sys.argv) == 3:
        keyword = sys.argv[1]
        color = sys.argv[2]
    elif len(sys.argv) == 4:
        keyword = sys.argv[1]
        color = sys.argv[2]
        nsim_1 = sys.argv[3]
    elif len(sys.argv) == 5:
        keyword = sys.argv[1]
        color = sys.argv[2]
        nsim_1 = sys.argv[3]
        nsim_2 = sys.argv[4]

    print('Loading word2vec model -- %s' % (model_name))
    model = Word2Vec.load(model_name)

    with open('불용어.txt', 'r', encoding='utf-8') as stop_words:
        stopwords = [line.strip() for line in stop_words.readlines()]

    similar_words = model.wv.most_similar(
        positive=[keyword, u'동료', '콤비'], negative=[u'다툼'], topn=10)

    result = []
    count = 0
    for word, score in similar_words:
        if word not in stopwords:
            result.append((word, score))
            count += 1
        if count == 5:  # 불용어를 제외한 상위 5개 단어를 출력
            break

    print(result)

    G = setEdges_simWords(model, keyword, nsim_1, nsim_2)
    fileName = "{}-FILE.png".format(keyword)

    visualize_most_similar(model, keyword)
    visualization(G, fileName, nodecolor=color, edgelabel=elabel)
    exit()
