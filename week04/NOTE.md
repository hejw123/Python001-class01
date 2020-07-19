学习笔记

data = pandas.DataFrame({
    'id':numpy.arange(1,16),
    'age':numpy.random.randint(20,90,15)
})
1. SELECT * FROM data;
data
2. SELECT * FROM data LIMIT 10;
data.iloc[:10]
3. SELECT id FROM data;  //id 是 data 表的特定一列
data['id']
4. SELECT COUNT(id) FROM data;
data.id.shape[0]
5. SELECT * FROM data WHERE id<1000 AND age>30;
data[(data['id']<1000) & (data['age']>30)]
6. SELECT id,COUNT(DISTINCT order_id) FROM table1 GROUP BY id;
data.groupby('id').aggregate({'id': 'count', })
7. SELECT * FROM table1 t1 INNER JOIN table2 t2 ON t1.id = t2.id;
data.merge(data, left_on='id', right_on='id2')
8. SELECT * FROM table1 UNION SELECT * FROM table2;
pd.concat([data, data2])
9. DELETE FROM table1 WHERE id=10;
data = data.loc[data['id'] != 10]
10. ALTER TABLE table1 DROP COLUMN column_name;
data.rename(columns={'gender': 'id'}, inplace=True)