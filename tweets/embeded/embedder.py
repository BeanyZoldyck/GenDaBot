import os
from functools import reduce

import cohere
from nltk.tokenize import TweetTokenizer


class Vec:
    def __init__(self, rep):
        self.rep = rep

    def __add__(self, b):
        return Vec([self.rep[i] + b.rep[i] for i in range(len(self.rep))])

    def __sub__(self, b):
        return Vec([self.rep[i] - b.rep[i] for i in range(len(self.rep))])

    def __mul__(self, b):
        return Vec([i * b for i in self.rep]) if type(b) != Vec else "1"

    def __rmul__(self, b):
        return self.__mul__(self, b)  # Vec([i*b for i in self.rep])


paf = r"D:\`\embeddings.csv"
word2Vec = {}
with open(paf, "rb") as f:
    listOfVecs = f.readlines()
    f.close()
    for line in listOfVecs:
        listed = line.split(b",")
        try:
            word2Vec[listed[0].decode("utf-8")] = Vec(list(map(float, listed[1:])))
        except ValueError:
            word2Vec[listed[0]] = Vec(
                list(map(float, listed[2:]))
            )  # word2Vec[listed[0]] = list(map(float,listed[2:]))
mag = lambda vec: (sum(map(lambda r: r**2, vec))) ** 0.5
findCos = lambda vec1, vec2: dot(vec1.rep, vec2.rep) / (mag(vec1.rep) * mag(vec2.rep))
findDis = lambda vec1, vec2: mag(vec1 - vec2)
tknzr = TweetTokenizer(preserve_case=False, reduce_len=True)
blankVec64 = Vec([0] * 64)
COHERE_SECRET_KEY = os.environ.get("COHERE_KEY_2")
co = cohere.Client(COHERE_SECRET_KEY)


def embed(file, sex):
    with open(file, "rb") as f:
        tweets = f.readlines()
        f.close()
    k = file.split("\\")[-1]
    with open(
        rf"C:\Users\chuka\Documents\GitHub\GenDaBot\tweets\embeded\{sex[0]}\{k}", "a"
    ) as g:
        for tweet in tweets:
            if tweet:
                tokens = tknzr.tokenize(tweet)
                notUsed = 0
                try:
                    sumVec = Vec([0] * 64)
                    blankVec64 = Vec([0] * 64)
                    for i in tokens:
                        vec = word2Vec.get(i, blankVec64)
                        if vec == blankVec64:
                            notUsed += 1
                        else:
                            sumVec += vec
                    if len(tokens) != notUsed:
                        avgVec = (sumVec * (1 / (len(tokens) - notUsed))).rep
                        g.write(
                            (" ".join(map(lambda x: str(round(x, 10)), avgVec)) + "\n")
                            * int(avgVec != [0.0] * 64)
                        )
                except TypeError:
                    pass


chunk = 10


def embed2(file, sex):
    with open(file, "rb") as f:
        tweets = f.readlines()
        f.close()
    k = file.split("\\")[-1]
    print(k)
    with open(rf"D:\`\embedded\{sex[0]}\{k}", "a") as g:
        for i in range(0, len(tweets), chunk):
            tweetChunk = list(map(lambda x: x.decode("utf-8"), tweets[i : i + chunk]))
            soup1 = co.embed(tweetChunk).embeddings
            g.writelines(list(map(lambda x: str(x) + "\n", soup1)))
        g.close()
    print(f"done with {k}")


def parse(file):
    with open(file) as f:
        vecs = f.readlines()
        input(vecs[1:3])
        for vec in vecs:
            fltList = vec.split(" ")


def sortLict(dic):
    """sorts dictionary by values {'b':2,'a':1,'d':4,'c':3}->{'a':1,'b':2','c':3,d':4}"""
    v = [i[0] for i in dic]
    return [(i, [j[1] for j in dic if j[0] == i][0]) for i in sorted(v)]


def succ():
    lengthNotUsed += 1


# embed(r"C:\Users\chuka\Documents\GitHub\MTAG\Chuck.txt","m")
# input('done')
if __name__ == "__main__":
    for sex in ["fem", "man"]:
        for i, _, j in os.walk(
            "C:\\Users\\chuka\\Documents\\GitHub\\GenDaBot\\tweets\\" + sex
        ):
            for k in j:
                embed2(os.path.join(i, k), sex[0])
