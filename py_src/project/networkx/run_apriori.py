from py_src.common_conf.postgres_config import PostgresConfig
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
import pandas as pd

class RunApriori():
    def __init__(self, news_dt):
        self.news_dt = news_dt

    def get_apriori_rslt(self, min_support):
        # 1. Transaction Encoder 결과를 데이터프레임으로
        trx_df = self.get_te_fmt()

        # 2. Apriori 수행
        apriori_rslt_df = self.get_apriori(df=trx_df, min_support=min_support)

        return apriori_rslt_df

    def get_te_fmt(self):
        pg_cfg = PostgresConfig()
        sql = f'''
select news_dt, okt_tfidf_nouns from crawling_news 
where news_dt like '{self.news_dt}%'
'''
        pg_cfg.cur.execute(sql)
        rslt_df = pd.DataFrame(pg_cfg.cur.fetchall())
        if rslt_df.empty:
            raise Exception(f"{self.news_dt}: 데이터 없음)")
        else:
            rslt_df.columns = ['news_dt', 'okt_tfidf_nouns']

        trx = []
        for one_news in rslt_df['okt_tfidf_nouns'].tolist():
            trx.append(one_news.split(','))

        te = TransactionEncoder()
        te_result = te.fit(trx).transform(trx)

        trx_df = pd.DataFrame(te_result, columns=te.columns_)
        return trx_df

    def get_apriori(self, df, min_support):
        frequent_itemsets = apriori(df, min_support=min_support, use_colnames=True)     # 출력 포맷은 데이터프레임
        frequent_itemsets['len'] = frequent_itemsets['itemsets'].map(lambda x:len(x))
        return frequent_itemsets.query(f"(len == 2)")



# run_apriori = RunApriori('201903')
# run_apriori.get_apriori_rslt(min_support=0.05)

