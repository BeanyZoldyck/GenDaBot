class Vec:
    def __init__(self, rep):
        self.rep = rep
    def __add__(self,b):
        return Vec([self.rep[i] + b.rep[i] for i in range(len(self.rep))])
    def __sub__(self,b):
        return Vec([self.rep[i] - b.rep[i] for i in range(len(self.rep))])
    def __mul__(self,b):
        return Vec([i*b for i in self.rep])
    def __rmul__(self, b):
        return Vec([i*b for i in self.rep])
def dot(a,b):
    sum=0
    for i in enumerate(a):
            sum+=(i[1]*b[i[0]])
    return sum
def b(i,b):
    while i>=b:
        print((int(i/b),i%b))
        i=int(i/b)
    print((int(i/b),i%b))
def pm(a,b,op='+'):
    if op == '+':
        return [sum(i) for i in zip(a,b)]
    if op == '-':
        return [sum(i) for i in zip(a,map(lambda r: -r, b))]
#b(int('EB',16),2)
#queen woman
paf = r"D:\`\glove.6B.txt"
word2Vec = {}
with open(paf,'rb') as f:
    listOfVecs = f.readlines()
    f.close()
    for line in listOfVecs:
        listed = line.split(b' ')
        try:
            word2Vec[listed[0].decode('utf-8')] = Vec(list(map(float,listed[1:])))
        except ValueError:
            word2Vec[listed[0]] = Vec(list(map(float,listed[2:])))#word2Vec[listed[0]] = list(map(float,listed[2:]))
mag = lambda vec: (sum(map(lambda r: r**2,vec)))**.5
findCosine = lambda vec1, vec2: dot(vec1,vec2)/(mag(vec1)*mag(vec2))

def sortLict(dic):
    v = [i[0] for i in dic]
    return [(i,[j[1] for j in dic if j[0] == i][0]) for i in sorted(v)]
while 1:
    lens = []
    word1 = input("Word: ").split(' ')#king,-,man
    vector1 = word2Vec[word1[0]]+word2Vec[word1[2]] if word1[1] == '+' else word2Vec[word1[0]]-word2Vec[word1[2]]
    #vec1 = word2Vec[word1]
    for word, vec in word2Vec.items():
        if len(lens) < 7:
            lens.append([mag((vec1-vec).rep), word])
        else:
            distance = mag((vec1-vec).rep)
            if distance < lens[-1][0]:
                lens.pop()
                lens.append([distance,word])
        #print(' '.join([f"({i}, {j})" for i, j in lens]),end='\r',flush=True)
        lens = sortLict(lens)
    print(lens)
    #input('')
    '''cos(king - man + woman, queen)
    vector1 = word2Vec[word1[0]]+word2Vec[word1[2]] if word1[1] == '+' else word2Vec[word1[0]]-word2Vec[word1[2]]
    vector1 += word2Vec[input("Vec to add: ")]
    vector2 = word2Vec[input("Vec 2: ")]#pm(word2Vec['king'], word2Vec['male'],'-')
    '''
    #print(findCosine(vector1.rep, vector2.rep))

#king = '-0.003524828,-0.49723786,-0.15489304,-0.05203741,0.5893758,-0.17818405,0.59563386,0.20116737,0.17819884,-0.065824546,0.047945775,0.15876931,0.23226467,0.2792681,-0.5412035,0.2383498,-0.20405824,0.3135219,-0.09955562,-0.0025000647,0.06562875,-0.16223432,0.30438617,0.022529155,-0.15844166,0.56471026,0.24733028,0.07995252,0.26324674,0.075210534,-0.5950815,0.30504942,-0.24879973,0.20368183,-0.5500499,-0.19553159,0.2716701,-0.5673772,0.27181092,0.29573965,-0.2709237,-0.0397766,0.12347255,-0.05075133,0.3612962,-0.30702114,0.26190978,0.36640638,0.4632417,-0.056619108,-0.078864455,0.16521665,0.056129195,0.19659066,0.5848559,-0.038660616,0.04121542,-0.6994016,0.13521647,-0.33517456,0.10783972,-0.38233292,0.056045797,0.3406815'
#

#print(dot(king,kingg)/(mag(map(float, king.split(',')))*mag(kingg)))
#queen - woman ~ king



