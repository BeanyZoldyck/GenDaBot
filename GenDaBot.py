import os
from functools import reduce
import dotenv
import cohere
import torch
import torch.nn as nn
from nltk.tokenize import TweetTokenizer
dotenv.load_dotenv()
COHERE_SECRET_KEY = os.environ.get("COHERE_KEY_1")
co = cohere.Client(COHERE_SECRET_KEY)

class Vec:
    def __init__(self, rep):
        self.rep = rep

    def __add__(self, b):
        return Vec([self.rep[i] + b.rep[i] for i in range(len(self.rep))])

    def __sub__(self, b):
        return Vec([self.rep[i] - b.rep[i] for i in range(len(self.rep))])

    def __mul__(self, b):
        return Vec([i * b for i in self.rep])

    def __rmul__(self, b):
        return self.__mul__(self, b)


class LogisticRegression(nn.Module):
    def __init__(self, nInputFeatures):
        super(LogisticRegression, self).__init__()
        self.linear = nn.Linear(nInputFeatures, 1)

    def forward(self, x):
        yPred = torch.sigmoid(self.linear(x))
        return yPred


torch.serialization.add_safe_globals([LogisticRegression])

class LinearNetwork(nn.Module):
    def __init__(self):
        super(LinearNetwork, self).__init__()
        self.linear = nn.Sequential(
            nn.Linear(64, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 8),
            nn.ReLU(),
            nn.Linear(8, 1),
        )

    def forward(self, x):
        return torch.sigmoid(self.linear(x))


def invSigmoid(x):
    return torch.log(x / (1 - x))


paf = r"D:\`\embeddings.csv"
word2Vec = {}
# with open(paf, "rb") as f:
#     listOfVecs = f.readlines()
#     f.close()
#     for line in listOfVecs:
#         listed = line.split(b",")
#         try:
#             word2Vec[listed[0].decode("utf-8")] = Vec(list(map(float, listed[1:])))
#         except ValueError:
#             word2Vec[listed[0]] = Vec(
#                 list(map(float, listed[2:]))
#             )  # word2Vec[listed[0]] = list(map(float,listed[2:]))


def GenDaBot(tweet):
    if not tweet:
        return 0.500001
    model = torch.load("model.pt")
    model.eval()
    tknzr = TweetTokenizer(preserve_case=False, reduce_len=True)
    tokens = tknzr.tokenize(tweet)
    notUsed = 0
    # sumVec = reduce(lambda x,y: x+y if (y.rep[0]!=0 or succ()!=None) else x+y,[word2Vec.get(i, Vec([0]*64)) for i in tokens])
    sumVec = Vec([0] * 64)
    blankVec64 = Vec([0] * 64)
    for i in tokens:
        vec = word2Vec.get(i, Vec([0] * 64))
        if vec == blankVec64:
            notUsed += 1
        else:
            sumVec += vec
    avgVec = torch.tensor((sumVec * (1 / (len(tokens) - notUsed))).rep)

    with torch.no_grad():
        confidence = model(avgVec)
        return float(confidence)


def GenDaBotexp(tweet):
    if not tweet:
        return 0.50001
    model = torch.load("model74.pt", weights_only=False)
    model.eval()
    embed = co.embed(texts=[tweet], model="embed-english-v2.0").embeddings
    with torch.no_grad():
        confidence = model(torch.tensor(embed))
        return confidence


def appraise(flt):
    print(2 * abs(0.5 - flt), 2)
    return (round(float(2 * abs(0.5 - flt)),2) * 100, round(float(flt)), flt)


if __name__ == "__main__":
    while 1:
        tweet = input("text: ")
        conf = GenDaBotexp(tweet)
        print(conf)
        # cert, ans, _ = appraise(conf)
        # print(f'this was tweeted by a {["female","male"][ans]} ({cert}% confidence)')
