import torch
import torch.nn

def classifier(nn.Module):
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
                                 nn.Linear(200, 300),
                                 nn.Linear(300, 300),
                                 nn.Linear(300, 300),
                                 nn.Linear(300, 200),
                                 nn.Linear(200, 100),
                                 nn.Linear(100, 50),
                                 nn.Linear(50, 25),
                                 nn.Linear(25, 10),
                                 nn.Linear(10, 2))

    def forward(self, in_tensor):
        return self.net(in_tensor)

    def saveNet(self):
        

