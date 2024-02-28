import pandas as pd
import glob

data_path = glob.glob('./crawling_data/reviews_gyeongsang*.csv')
print(data_path)

df = pd.DataFrame()

for path in data_path:
    df_temp = pd.read_csv(path)
    df_temp.columns = ['names', 'reviews']
    df_temp.dropna(inplace=True)
    df = pd.concat([df, df_temp], ignore_index=True)

df.drop_duplicates(inplace=True)
df.info()
print(df.head(5))
df.to_csv('./reviews_gyeongsang.csv', index=False)
