
import datetime
import matplotlib.pyplot as plt

yrange = ["Star", "Sun", "Sea", "Sea"]

lst_lft = [datetime.datetime(2019, 3, 13),
           datetime.datetime(2019, 4, 26),
           datetime.datetime(2019, 6, 18),
           datetime.datetime(2019, 8, 18)]

lst_rgt = [datetime.datetime(2019, 5, 26),
           datetime.datetime(2019, 10, 2),
           datetime.datetime(2019, 8, 6),
           datetime.datetime(2019, 9, 1)]

plt.hlines(yrange, lst_lft, lst_rgt)
plt.scatter(lst_lft, yrange, color='green')
plt.scatter(lst_rgt, yrange, color='red')

plt.show()
