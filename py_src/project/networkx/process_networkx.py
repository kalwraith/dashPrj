import os
import pandas as pd
import urllib.request
import pickle
import re
from konlpy.tag import Okt
from soynlp import DoublespaceLineCorpus
from soynlp.word import WordExtractor
from soynlp.tokenizer import LTokenizer
from soynlp.noun import LRNounExtractor_v2
from py_src.common_conf.postgres_config import PostgresConfig
from soynlp.noun import LRNounExtractor
from py_src.common_conf.postgres_config import PostgresConfig
from sklearn.feature_extraction.text import TfidfVectorizer
from datetime import datetime

class ProcessNetworkx():
    def __init__(self, year, month):
        self.year = year
        self.month = month

    def processing(self):
        # 1. csv 가져오기
        news_pd = self.get_csv_files()

        # 2. 전처리하기
        news_pd = self.get_okt_nouns(news_pd)

        # 3. TF-IDF 적용
        news_pd = self.get_tfidf_processing(news_pd)

        # 4. db저장
        self.insrt_db(news_pd)

    def get_csv_files(self):
        self.csv_dir = f'csv/{self.year}{str(self.month).rjust(2,"0")}'
        file_lst = os.listdir(self.csv_dir)
        news_org_pd = pd.DataFrame()
        for file in file_lst:
            tmp_pd = pd.read_csv(f'{self.csv_dir}/{file}', encoding='utf-8', index_col=0)
            news_org_pd = pd.concat([news_org_pd, tmp_pd])
        return news_org_pd

    def get_okt_nouns(self, df):
        try:
            df = pd.read_csv('201903_okt.csv', encoding='utf-8', index_col=0)
        except:
            df['newsText'] = df['newsText'].map(lambda x:re.sub('[^ㄱ-ㅎ|가-힣a-zA-Z0-9]'," ",x))
            corpus = df['newsText'].tolist()
            okt = Okt()
            okt_nouns_lst = []
            for news in corpus:
                nouns_per_news_lst = okt.nouns(news)
                nouns_per_news_str = " ".join(nouns_per_news_lst)
                okt_nouns_lst.append(nouns_per_news_str)
            df['okt_nouns'] = okt_nouns_lst
            df.to_csv('201903_okt.csv')
        return df

        # noun_extractor = LRNounExtractor_v2(verbose=True)
        # nouns = noun_extractor.train_extract(corpus)
        # print(nouns)
        #     word_extractor = WordExtractor()
        #     word_extractor.train(corpus)
        #     word_score_table = word_extractor.extract()
        #
        #     '''
        #     word_score_table 결과에는 아래와 같은 딕셔너리 구조로 저장됨
        #     '자동심장충격기': Scores(cohesion_forward=0.2713612353596389
        #     , cohesion_backward=0
        #     , left_branching_entropy=0
        #     , right_branching_entropy=-0.0
        #     , left_accessor_variety=0
        #     , right_accessor_variety=1
        #     , leftside_frequency=11
        #     , rightside_frequency=0)
        #     '''
        #     scores = {word: score.cohesion_forward for word, score in word_score_table.items()}
        #     l_tokenizer = LTokenizer(scores=scores)
        #     with open(TOKENIZER_FILE_NM, 'wb') as f:
        #         pickle.dump(l_tokenizer, f)
        # finally:
        #     print(l_tokenizer.tokenize("국제사회와 우리의 노력들로 범죄를 척결하자", flatten=False))

    def get_tfidf_processing(self, df):
        tfidf = TfidfVectorizer(max_df=0.8, min_df=0.01, stop_words=['앵커','뉴시스','연합뉴스'])
        okt_nouns_lst = df['okt_nouns'].tolist()
        tfidf_rslt = tfidf.fit_transform(okt_nouns_lst).toarray()
        tfidf_nouns_lst = tfidf.get_feature_names()
        top_nouns_per_news = []
        for idx, tfidf_rslt_per_news in enumerate(tfidf_rslt):
            tfidf_rslt_dict = dict(zip(tfidf_nouns_lst, tfidf_rslt_per_news))
            ord_tfidf_rslt_dict = dict(sorted(tfidf_rslt_dict.items(), key=lambda x: x[1], reverse=True))
            tmp_str = ''
            for num, key in enumerate(ord_tfidf_rslt_dict.keys()):
                tmp_str += key + ','
                if num == 50:
                    break
            tmp_str = tmp_str[:-1]
            top_nouns_per_news.append(tmp_str)
        df['okt_tfidf_nouns'] = top_nouns_per_news
        return df


    def insrt_db(self, df):
        pg_cfg = PostgresConfig()
        df.columns = ['news_dt', 'news_src', 'news_url', 'org_content', 'okt_nouns', 'okt_tfidf_nouns']
        df['news_dt'] = df['news_dt'].str.replace('-', '')

        del_range_lst = df['news_dt'].unique().tolist()
        del_range_str = "','".join(del_range_lst)

        del_sql = f'''
delete from crawling_news 
where news_dt in ('{del_range_str}')'''

        try:
            pg_cfg.cur.execute(del_sql)
            pg_cfg.conn.commit()
            df.to_sql('crawling_news',pg_cfg.engine, if_exists='append', index=False)

        except Exception as e:
            print(str(e))
        else:
            print('insert 완료')


# process_networkx = ProcessNetworkx(2019, 3)
# process_networkx.processing()