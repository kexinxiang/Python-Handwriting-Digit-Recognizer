import flask
import numpy as np
import pickle
from flask import request
import math

app = flask.Flask(__name__)
app.config["DEBUG"] = True

mnist = np.genfromtxt("mnist_train.csv", delimiter=",")

@app.route('/recognize', methods=['POST'])
def recognize():
    num_row = 0
    for row in mnist:
        num_row += 1
    k = int(math.sqrt(num_row))
    serialized_drawn_digit = request.data
    drawn_digit = pickle.loads(serialized_drawn_digit)
    ans = knn(k,drawn_digit)
    return pickle.dumps(ans)



def Eucli(p1, p2):
    return np.linalg.norm(p1-p2)

def distance(drawn_digit):
    distances = []
    for row in mnist:
        distances.append(Eucli(drawn_digit, row[1:]))  
    return distances

def index_sort(k, l):
    index = np.argpartition(l, k)[:k]
    return index

def predict(k, drawn_digit):
    dist = distance(drawn_digit)
    closest_k = index_sort(k, dist)
    guesses = []
    for point in closest_k:
        guesses.append(mnist[point][0])
    return guesses

def knn(k, drawn_digit):
    guesses = predict(k, drawn_digit)
    d = {}
    for item in guesses:
        if item in d:
            d[item] += 1
        else:
            d[item] = 1
    return max(d, key=d.get)



app.run()
