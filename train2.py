import numpy as np
import os
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
path = r"D:\`\embedded"#r'C:\Users\chuka\Documents\GitHub\GenDaBot\tweets\embeded'
sexes = [r'\m',r'\f']
toFloat = lambda y: float(y)

class LinearNetwork(nn.Module):
    def __init__(self, features):
        super(LinearNetwork, self).__init__()
        self.linear = nn.Sequential(
            nn.Linear(features, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            #nn.Dropout(p=0.4),
            nn.Linear(128, 8),
            nn.ReLU(),
            nn.Linear(8, 1)
        )
    def forward(self, x):
        return torch.sigmoid(self.linear(x))#self.linearReLuStack(x)
def getInstances():
    start = 0
    for sex in sexes:
        for i,_,j in os.walk(path+sex):
            for k in j:
                with open(os.path.join(i,k)) as f:
                    embeds = list(map(lambda x: [int(sex==r'\m')]+x.split(), f.readlines()))
                    embeds = [[float(j) for j in i] for i in embeds]
                    f.close()
                    if start == 0:
                        data = np.array(embeds)
                        start += 1
                    else:
                        if embeds:
                            data=np.concatenate((data, embeds))
    return data
data = getInstances()
FEATURES = 4096
np.random.shuffle(data)
print('processed')
Y = data.T[0] #labels
X = data[:,range(1,FEATURES+1)] #features
testInstances = int(10*len(X)/100)
xTest = torch.from_numpy(X[:testInstances].astype(np.float32))
xTrain = torch.from_numpy(X[testInstances:].astype(np.float32))
yTest = torch.from_numpy(Y[:testInstances].astype(np.float32))
yTrain = torch.from_numpy(Y[testInstances:].astype(np.float32))
yTrain = yTrain.view(yTrain.shape[0],1)
yTest = yTest.view(yTest.shape[0],1)

class LogisticRegression(nn.Module):
    def __init__(self, nInputFeatures):
        super(LogisticRegression,self).__init__()
        self.linear = nn.Linear(nInputFeatures, 1)
        
        #ADD MORE LAYERS, THIS MODEL IS A PERCEPTRON
        #I used to be surrounded by real deep learners...
    def forward(self, x):
        yPred = torch.sigmoid(self.linear(x))
        return yPred

model = LogisticRegression(FEATURES)
#LinearNetwork(FEATURES)
criterion = nn.BCELoss()#nn.BCELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.011)#SGD
numEpochs = 220
for epoch in range(numEpochs):
    yPred = model(xTrain)
    loss = criterion(yPred, yTrain)

    loss.backward()

    optimizer.step()

    optimizer.zero_grad()

    if (epoch+1) % 10 == 0:
        print(f'{epoch+1}:, loss = {loss.item():.4f}')

with torch.no_grad():
    yPred = model(xTest)
    yPredCls = yPred.round()
    acc = yPredCls.eq(yTest).sum()/float(yTest.shape[0])
    print(f'accuracy: {acc:.4f}')
input()
torch.save(model, r'C:\Users\chuka\Documents\GitHub\GenDaBot\model74.pt')

