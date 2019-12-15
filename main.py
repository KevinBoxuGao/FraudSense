import torch
import torch.nn as nn
import torch.optim as optim
import csv
import os
import random
import aggregate
import time
import pickle
os.chdir('/home/biscuit/Desktop/blockcondom/data')

class classifier(nn.Module):
    def __init__(self):
        super(classifier, self).__init__()

        # Input Spec:
        # One-Hot Vectors:
        # proxy: len 4
        # os: len 7
        # browser: len 14
        # devicetype: len 3
        # deviceinfo: len 23
        # P_emaildomain: len 62
        # R_emaildomain: len 62
        # And:
        # Amt: float
        
        self.net = nn.Sequential(nn.Linear(176, 200),
                                 nn.Dropout(0.1),
                                 nn.Linear(200, 100),
                                 nn.Dropout(0.1),
                                 nn.Linear(100, 50),
                                 nn.Dropout(0.1),
                                 nn.Linear(50, 25),
                                 nn.Dropout(0.1),
                                 nn.Linear(25, 10),
                                 nn.Dropout(0.1),
                                 nn.Linear(10, 2),
                                 nn.Softmax())
        self.net.cuda()

    def forward(self, in_tensor):
        return self.net(in_tensor.cuda()).float()

    def saveNet(self):
        torch.save(self.net.state_dict(), "fraudnet.pt")

    def loadNet(self):
        try:
            self.net.load_state_dict(torch.load("fraudnet.pt"))
        except:
            print("no network found")

proxy_map = dict(zip(['', 'IP_PROXY:TRANSPARENT', 'IP_PROXY:ANONYMOUS', 'IP_PROXY:HIDDEN'], range(4)))
os_identifier_map = dict(zip(['android', 'windows', 'osx', 'ios', 'other', 'unknown', 'linux'], range(7)))
browser_identifier_map = dict(zip(['google search application', 'ie for tablet', 'firefox', 'opera', 'chrome for android', 'samsung browser', 'chrome', 'edge', 'safari', 'other', 'chrome for ios', 'ie for desktop', 'unknown', 'android browser'], range(14)))
device_type_map = dict(zip(['mobile', 'desktop', ''], range(3)))
dev_info_map = dict(zip(['windows', 'pixel', 'blade', 'samsung', 'ilium', 'xt', 'lg', 'unknown', 'htc', 'zte', 'redmi', 'mac', 'moto', 'other', 'linux', 'sm', 'android', 'lenovo', 'ios', 'huawei', 'lm', 'nexus', 'z9'], range(23)))
email_map = dict(zip(['unknown', 'gmail.com', 'outlook.com', 'yahoo.com', 'mail.com', 'anonymous.com', 'hotmail.com', 'verizon.net', 'aol.com', 'me.com', 'comcast.net', 'optonline.net', 'cox.net', 'charter.net', 'rocketmail.com', 'prodigy.net.mx', 'embarqmail.com', 'icloud.com', 'live.com.mx', 'gmail', 'live.com', 'att.net', 'juno.com', 'ymail.com', 'sbcglobal.net', 'bellsouth.net', 'msn.com', 'q.com', 'yahoo.com.mx', 'centurylink.net', 'servicios-ta.com', 'earthlink.net', 'hotmail.es', 'cfl.rr.com', 'roadrunner.com', 'netzero.net', 'gmx.de', 'suddenlink.net', 'frontiernet.net', 'windstream.net', 'frontier.com', 'outlook.es', 'mac.com', 'netzero.com', 'aim.com', 'web.de', 'twc.com', 'cableone.net', 'yahoo.fr', 'yahoo.de', 'yahoo.es', 'sc.rr.com', 'ptd.net', 'live.fr', 'yahoo.co.uk', 'hotmail.fr', 'hotmail.de', 'hotmail.co.uk', 'protonmail.com', 'yahoo.co.jp', 'scranton.edu', 'other'], range(62)))

id_data = {}

with open("train_identity.csv", "r") as file:
    pfile = csv.reader(file)
    for row in pfile:
        id_data[row[0]] = row

def getIdentity(transaction_id):
    try:
        return id_data[transaction_id]
    except:
        return None

frauds = []
'''
def getFrauds():
    global frauds
    with open("train_transaction.csv", "r") as file:
        pfile = csv.reader(file)
        for row in pfile:
            if row[1] == "1":
                t_id = getIdentity(row[0])
                if t_id:
                    frauds.append((row[:17], t_id))
print("Begin indexing frauds...", time.time())
getFrauds()
print("End indexing frauds.", time.time())
print("Found", len(frauds), "frauds.")
with open("frauds.pickle", "wb") as file:
    pickle.dump(frauds, file)
'''
with open("frauds.pickle", "rb") as file:
    frauds = pickle.load(file)

def randomSlice(l):
    global frauds
    start = random.randint(0, len(frauds))
    init = frauds[start:min(start+l, len(frauds))]
    wrap = frauds[0:max(0, start+l-len(frauds))]
    random.shuffle(frauds)
    return init+wrap



def getNextInp():
    # find 200 non fraudulent transactions and 200 fraudulent transactions
    print("init data search", time.time())
    data = randomSlice(6000)
    start = random.randint(0, 500000)
    nonfraud_count = 0
    with open("train_transaction.csv", "r") as file:
        pfile = csv.reader(file)
        ctr = 0
        for row in pfile:
            ctr += 1
            if nonfraud_count > 6000:
                return data
            if ctr>start:
                if row[1] == "0" and nonfraud_count < 6020:
                    t_id = getIdentity(row[0])
                    if t_id:
                        #print(nonfraud_count)
                        data.append((row[:17], t_id))
                        nonfraud_count += 1
    return data

def one_hot_vectorize(n, l):
    return [0]*(n)+[1]+[0]*(l-n-1)

def swap(s):
    if s == '':
        return "unknown"
    return s

def parse(trans_data):
    ttrans_data, id_data = trans_data
    t_id, isFraud = ttrans_data[:2]
    amt = ttrans_data[3]
    p_email = swap(ttrans_data[15])
    r_email = swap(ttrans_data[16])
    id_data = getIdentity(t_id)
    if not id_data:
        return None
    proxy_state = id_data[23]
    os_id = aggregate.interpret_os_identifier(id_data[30])
    browser_id = aggregate.interpret_browser_identifier(id_data[31])
    dev_type = id_data[39]
    dev_info = aggregate.interpret_device_info(id_data[40])
    return  one_hot_vectorize(proxy_map[proxy_state], 4) + \
                         one_hot_vectorize(os_identifier_map[os_id], 7) + \
                         one_hot_vectorize(browser_identifier_map[browser_id], 14) + \
                         one_hot_vectorize(device_type_map[dev_type], 3) + \
                         one_hot_vectorize(dev_info_map[dev_info], 23) + \
                         one_hot_vectorize(email_map[p_email], 62) + \
                         one_hot_vectorize(email_map[r_email], 62) + \
                         [float(amt)], isFraud

def merge_data(raw_transcation_inp):
    rdata = []
    for inp_data in raw_transcation_inp:
        p = parse(inp_data)
        if p:
            rdata.append(p)
    return rdata

def group(array, batchsize):
    return [array[i*batchsize:min((i+1)*batchsize, len(array))] for i in range(0, len(array)//batchsize+1)]

def accuracy(net, batchsize):
    with torch.no_grad():
        correct = 0
        tested = 0
        raw_transcation_inp = getNextInp()
        data = merge_data(raw_transcation_inp)
        for batch in group(data, batchsize):
            inps = torch.tensor([data[0] for data in batch])
            outs = [int(data[1]) for data in batch]
            out = list(net.forward(inps))
            for i in range(len(outs)):
                #print(list(out[i]))
                tested += 1
                if list(out[i])[outs[i]] > list(out[i])[(outs[i]+1)%2] and list(out[i])[outs[i]]>0.7:
                    correct += 1
                    
        print("Accuracy",correct/tested)

def train(net, criterion, optimizer, epochs, batchsize):
    for epoch in range(1, epochs+1):
        running_loss = 0
        raw_transcation_inp = getNextInp()
        data = merge_data(raw_transcation_inp)
        print("loaded data", time.time())
        #print(len(data))
        for batch in group(data, batchsize):
            inps = torch.tensor([data[0] for data in batch])
            outs = torch.tensor([one_hot_vectorize(int(data[1]), 2) for data in batch])
            optimizer.zero_grad()
            out = net.forward(inps)
            loss = criterion(out, outs.float())
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
        print("Epoch:",epoch,"loss:",running_loss/len(data))
        net.saveNet()
        if epoch%10 == 0:
            accuracy(net, 32)

net = classifier()
net.loadNet()
criterion = nn.BCELoss()
optimizer = optim.Adam(net.parameters())
train(net, criterion, optimizer, 1000, 32)
        
    
