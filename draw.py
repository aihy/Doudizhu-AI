import matplotlib

matplotlib.use('Agg')
import sys

import matplotlib.pyplot as plt


def rfe(str):
    f = open(str)
    return eval(f.read())


plt.figure(figsize=(14, 8))
c1 = rfe(sys.argv[1] + "+1")
c2 = rfe(sys.argv[1] + "+2")
c3 = rfe(sys.argv[1] + "+3")
c4 = rfe(sys.argv[1] + "+4")
c5 = rfe(sys.argv[1] + "+5")
c6 = rfe(sys.argv[1] + "+6")
c7 = rfe(sys.argv[1] + "+7")
c8 = rfe(sys.argv[1] + "+8")
c9 = rfe(sys.argv[1] + "+9")
c10 = rfe(sys.argv[1] + "+10")
c11 = rfe(sys.argv[1] + "+11")
c12 = rfe(sys.argv[1] + "+12")
c13 = rfe(sys.argv[1] + "+13")
c14 = rfe(sys.argv[1] + "+14")
c15 = rfe(sys.argv[1] + "+15")
c16 = rfe(sys.argv[1] + "+16")
c17 = rfe(sys.argv[1] + "+17")
c18 = rfe(sys.argv[1] + "+18")
c19 = rfe(sys.argv[1] + "+19")
c20 = rfe(sys.argv[1] + "+20")
c21 = rfe(sys.argv[1] + "+21")
c22 = rfe(sys.argv[1] + "+22")
c23 = rfe(sys.argv[1] + "+23")
c24 = rfe(sys.argv[1] + "+24")
c25 = rfe(sys.argv[1] + "+25")
c26 = rfe(sys.argv[1] + "+26")
c27 = rfe(sys.argv[1] + "+27")
c28 = rfe(sys.argv[1] + "+28")
c29 = rfe(sys.argv[1] + "+29")
c30 = rfe(sys.argv[1] + "+30")
c = c1 + c2 + c3 + c4 + c5 + c6 + c7 + c8 + c9 + c10 + c11 + c12 + c13 + c14 + c15 + c16 + c17 + c18 + c19 + c20 + c21 + c22 + c23 + c24 + c25 + c26 + c27 + c28 + c29 + c30
y = []
sum = 0
for i in range(6000):
    sum += c[i]
    y.append(sum / (i + 1))
x = list(range(6000))
plt.scatter(x, y, color='m', label='MAXLEVEL=' + sys.argv[1] + ' ' + "%.2f%%" % (y[5999] * 100))
plt.legend(loc='upper right')
# plt.show()
plt.savefig(sys.argv[1] + "a30.png")
