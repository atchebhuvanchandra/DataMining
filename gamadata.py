#!/usr/bin/python
import pymysql
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
from functools import reduce
from decimal import Decimal

def str_to_float_with_precision(data):
    precision = 2
    return float(Decimal(data, precision))
Sales_IN = ['NA_Sales','EU_Sales','JP_Sales','Other_Sales','Global_Sales']

# Connect
db = pymysql.connect(host="localhost", user="root",passwd="abc5s3",db="mydb")
cursor = db.cursor()

for index in Sales_IN:
  # Execute SQL select statement
  cursor.execute("SELECT sum({}) FROM `mytable` GROUP BY `Platform`".format(index))
  sales = cursor.fetchall()
  cursor.execute("SELECT Platform FROM `mytable` GROUP BY `Platform`")
  platform = cursor.fetchall()

  '''The data we retrieve from the sql table is in tuple format for generating
  the graph we use list data so we use reduce function to make the nested listed
  flattered lists'''
  platform = list(reduce(lambda x,y:x+y ,platform))
  sales = list(reduce(lambda x,y:x+y ,sales))

  '''And the generatd list for y-axis is in string of decimal format so converting
  it into list of decimals format'''
  np.round([float(i) for i in sales],2)


  plt.plot(platform, sales, color='red', marker='o')
  plt.title(index, fontsize=14)
  plt.xlabel('Platform', fontsize=14)
  plt.ylabel(index, fontsize=14)
  plt.grid(True)
  plt.show()
for index in Sales_IN:
  # Execute SQL select statement
  cursor.execute("SELECT sum({}) FROM `mytable` GROUP BY `Genre`".format(index))
  sales = cursor.fetchall()
  cursor.execute("SELECT Genre FROM `mytable` GROUP BY `Genre`")
  genre = cursor.fetchall()
  '''The data we retrieve from the sql table is in tuple format for generating
  the graph we use list data so we use reduce function to make the nested listed
  flattered lists'''
  genre = list(reduce(lambda x,y:x+y ,genre))
  sales = list(reduce(lambda x,y:x+y ,sales))

  '''And the generatd list for y-axis is in string of decimal format so converting
  it into list of decimals format'''
  np.round([float(i) for i in sales],2)


  plt.plot(genre, sales, color='red', marker='o')
  plt.title(index, fontsize=14)
  plt.xlabel('Genre', fontsize=14)
  plt.ylabel(index, fontsize=14)
  plt.grid(True)
  plt.show()
