import pandas as pd

csv = 'globecover_codes.csv'
code_df = pd.read_csv(csv)
years = ['no loss', '2001', '2002', '2003', '2004', '2005', '2006',
'2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']
melted = pd.melt(code_df, id_vars=['globe_cover'], value_vars= years)


# convert df to csv
melted.to_csv('globecover_codes_melted.csv')
