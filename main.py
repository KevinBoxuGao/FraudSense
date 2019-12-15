import torch
import torch.nn as nn
import torch.optim as optim
import csv
import os
import random
import aggregate
import time
import pickle
import math
import radam
os.chdir('/home/biscuit/Desktop/blockcondom/data')

class classifier(nn.Module):
    def __init__(self):
        super(classifier, self).__init__()

        # Input Spec:
        # One-Hot Vectors:
        # Amt: float (normalize to $100)
        # Distance between current location and past 5 transactions: float (normalized to half circum. of earth)
        # Time since last transaction: float (normalized to one day)
        # proxy: int 0 or 1
        # os: len 7
        # browser: len 14
        # devicetype: len 3
        # deviceinfo: len 23
        
        self.net = nn.RNN(input_size=51, hidden_size=2, num_layers=5, dropout=0.1, nonlinearity='relu', batch_first=True)
        self.afunc = nn.Softsign()
        #self.net.cuda()

    def forward(self, in_tensor, hidden_state):
        out, hidden = self.net(in_tensor, hidden_state)
        out = self.afunc(out)
        return  out, hidden # returns output, hidden state

    def saveNet(self):
        torch.save(self.net.state_dict(), "fraudnet.pt")

    def loadNet(self):
        try:
            self.net.load_state_dict(torch.load("fraudnet.pt"))
        except:
            print("no network found")

class Account():
    def __init__(self):
        self.lastState = None
        self.os = random.choice(['android', 'windows', 'osx', 'ios', 'other', 'unknown', 'linux'])
        self.browser = random.choice(['google search application', 'ie for tablet', 'firefox', 'opera', 'chrome for android', 'samsung browser', 'chrome', 'edge', 'safari', 'other', 'chrome for ios', 'ie for desktop', 'unknown', 'android browser'])
        self.devtype = random.choice(['mobile', 'desktop', ''])
        self.devinfo = random.choice(['windows', 'pixel', 'blade', 'samsung', 'ilium', 'xt', 'lg', 'unknown', 'htc', 'zte', 'redmi', 'mac', 'moto', 'other', 'linux', 'sm', 'android', 'lenovo', 'ios', 'huawei', 'lm', 'nexus', 'z9'])
        # compute dist with random.uniform(0, 0.002)
        # compute time with random.uniform(0, 1)
        # compute amt with random.uniform(0, 1)

# proxy : 1 or 0 (True or False)
os_identifier_map = dict(zip(['android', 'windows', 'osx', 'ios', 'other', 'unknown', 'linux'], range(7)))
browser_identifier_map = dict(zip(['google search application', 'ie for tablet', 'firefox', 'opera', 'chrome for android', 'samsung browser', 'chrome', 'edge', 'safari', 'other', 'chrome for ios', 'ie for desktop', 'unknown', 'android browser'], range(14)))
device_type_map = dict(zip(['mobile', 'desktop', ''], range(3)))
dev_info_map = dict(zip(['windows', 'pixel', 'blade', 'samsung', 'ilium', 'xt', 'lg', 'unknown', 'htc', 'zte', 'redmi', 'mac', 'moto', 'other', 'linux', 'sm', 'android', 'lenovo', 'ios', 'huawei', 'lm', 'nexus', 'z9'], range(23)))
email_map = dict(zip(['unknown', 'gmail.com', 'outlook.com', 'yahoo.com', 'mail.com', 'anonymous.com', 'hotmail.com', 'verizon.net', 'aol.com', 'me.com', 'comcast.net', 'optonline.net', 'cox.net', 'charter.net', 'rocketmail.com', 'prodigy.net.mx', 'embarqmail.com', 'icloud.com', 'live.com.mx', 'gmail', 'live.com', 'att.net', 'juno.com', 'ymail.com', 'sbcglobal.net', 'bellsouth.net', 'msn.com', 'q.com', 'yahoo.com.mx', 'centurylink.net', 'servicios-ta.com', 'earthlink.net', 'hotmail.es', 'cfl.rr.com', 'roadrunner.com', 'netzero.net', 'gmx.de', 'suddenlink.net', 'frontiernet.net', 'windstream.net', 'frontier.com', 'outlook.es', 'mac.com', 'netzero.com', 'aim.com', 'web.de', 'twc.com', 'cableone.net', 'yahoo.fr', 'yahoo.de', 'yahoo.es', 'sc.rr.com', 'ptd.net', 'live.fr', 'yahoo.co.uk', 'hotmail.fr', 'hotmail.de', 'hotmail.co.uk', 'protonmail.com', 'yahoo.co.jp', 'scranton.edu', 'other'], range(62)))

def one_hot_vectorize(n, l):
    return [0]*(n)+[1]+[0]*(l-n-1)

def swap(s):
    if s == '':
        return "unknown"
    return s

def pop(array, val):
    array = array.copy()
    array.remove(val)
    return array

def gen_rmat():
    m = torch.randn(5).abs()
    m = m/(2*sum(m))
    return m

# rmat has length 5, sum 0.5.
def gen_inp_out_pair(user, rmat):
    susfactor = 0
    
    seed = random.uniform(0, 1)
    if seed > rmat[0]:
        rdist = random.uniform(0.1, 1)
    else:
        rdist = random.uniform(0, 0.002)

    dt = random.uniform(0, 1)
    susfactor += math.tanh(rdist/(dt+0.02))

    seed = random.uniform(0, 1)
    if seed > rmat[1]:
        amt = random.uniform(1, 100)
        susfactor += amt/100
    else:
        amt = random.uniform(0, 1)

    seed = random.uniform(0, 1)
    if seed > rmat[2]:
        os = random.choice(pop(['android', 'windows', 'osx', 'ios', 'other', 'unknown', 'linux'], user.os))
        devtype = random.choice(pop(['mobile', 'desktop', ''], user.devtype))
        devinfo = random.choice(pop(['windows', 'pixel', 'blade', 'samsung', 'ilium', 'xt', 'lg', 'unknown', 'htc', 'zte', 'redmi', 'mac', 'moto', 'other', 'linux', 'sm', 'android', 'lenovo', 'ios', 'huawei', 'lm', 'nexus', 'z9'], user.devinfo))
        susfactor += 0.1
    else:
        os = user.os
        devtype = user.devtype
        devinfo = user.devinfo
    
    seed = random.uniform(0, 1)
    if seed > rmat[3]:
        browser = random.choice(pop(['google search application', 'ie for tablet', 'firefox', 'opera', 'chrome for android', 'samsung browser', 'chrome', 'edge', 'safari', 'other', 'chrome for ios', 'ie for desktop', 'unknown', 'android browser'], user.browser))
        susfactor *= 1.2
    else:
        browser = user.browser

    proxy = 0
    seed = random.uniform(0, 1)
    if seed > rmat[4]:
        proxy = 1
        susfactor += 0.9

    if susfactor > 0.8:
        susfactor = 1
    else:
        susfactor = 0

    return [amt, rdist, dt, proxy] + \
            one_hot_vectorize(os_identifier_map[os], 7) + \
            one_hot_vectorize(browser_identifier_map[browser], 14) + \
            one_hot_vectorize(device_type_map[devtype], 3) + \
            one_hot_vectorize(dev_info_map[devinfo], 23), susfactor


def group(array, batchsize):
    return [array[i*batchsize:min((i+1)*batchsize, len(array))] for i in range(0, len(array)//batchsize+1)]

def accuracy(net, batchsize):
    with torch.no_grad():
        correct = 0
        tested = 0
        mat = gen_rmat()
        data = [gen_inp_out_pair(user, mat) for user in users]
        for batch in group(data, batchsize):
            inps = torch.tensor([[data[0]] for data in batch])
            states = None
            if type(users[0].lastState) == type(torch.Tensor):
                states = torch.tensor([user.lastState for user in users])
            outs = torch.tensor([one_hot_vectorize(int(data[1]), 2) for data in batch]).float().view(len(batch), 1, 2)
            
            out, newStates = net.forward(inps, states)
            #print(out)
            for i in range(len(outs)):
                nout = list(out[i][0])
                eout = list(outs[i][0])
                tested += 1
                if nout[eout.index(max(eout))] > nout[(eout.index(max(eout))+1)%2] and nout[eout.index(max(eout))]>0.7:
                    correct += 1
                    
        print("Accuracy",correct/tested)

def train(net, criterion, optimizer, epochs, batchsize):
    for epoch in range(1, epochs+1):
        running_loss = 0
        tested = 0
        mat = gen_rmat()
        data = [gen_inp_out_pair(user, mat) for user in users]
        for batch in group(data, batchsize):
            optimizer.zero_grad()
            inps = torch.tensor([[data[0]] for data in batch])
            states = None
            if type(users[0].lastState) == type(torch.Tensor):
                states = torch.tensor([user.lastState for user in users])
            outs = torch.tensor([one_hot_vectorize(int(data[1]), 2) for data in batch]).float().view(len(batch), 1, 2)
            
            out, newStates = net.forward(inps, states)
            newStates = list(newStates)
            for i in range(len(newStates)):
                users[i].lastState = newStates[i]
            #print(inps.shape, out.shape, outs.shape)
            loss = criterion(out, outs)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
            tested+=1
        print("Epoch:",epoch,"loss:",running_loss/tested)
        net.saveNet()
        if epoch%10 == 0:
            accuracy(net, 32)

users = [Account() for i in range(10000)]
net = classifier()
net.loadNet()
criterion = nn.BCELoss()
optimizer = radam.RAdam(net.parameters(), lr=1e-7, weight_decay=0.01, eps=1)
train(net, criterion, optimizer, 10000, 32)
        
    
