import torch
from torch import nn
import torchvision
import os
import struct
from torchsummary import summary
from senet.se_resnet import se_resnet50

def main():
    print('cuda device count: ', torch.cuda.device_count())
    net = se_resnet50(num_classes=1000)
    net.load_state_dict(torch.load("seresnet50-60a8950a85b2b.pkl"))
    net = net.to('cuda:0')
    net.eval()
    print('model: ', net)
    #print('state dict: ', net.state_dict().keys())
    tmp = torch.ones(1, 3, 224, 224).to('cuda:0')
    print('input: ', tmp)
    out = net(tmp)
    print('output:', out)

    summary(net, (3,224,224))
    return
    f = open("se_resnet50.wts", 'w')
    f.write("{}\n".format(len(net.state_dict().keys())))
    for k,v in net.state_dict().items():
        print('key: ', k)
        print('value: ', v.shape)
        vr = v.reshape(-1).cpu().numpy()
        f.write("{} {}".format(k, len(vr)))
        for vv in vr:
            f.write(" ")
            f.write(struct.pack(">f", float(vv)).hex())
        f.write("\n")

if __name__ == '__main__':
    main()
