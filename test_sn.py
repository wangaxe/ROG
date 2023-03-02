import torch
import torch.nn as nn
from torch.nn.utils.parametrizations import spectral_norm


class SeparableConv3d(nn.Module):
    def __init__(self, inplanes, planes, kernel_size=3, padding=1, stride=1,
                 dilation=1, bias=False):
        super(SeparableConv3d, self).__init__()
        self.conv = nn.Conv3d(
            inplanes, inplanes, kernel_size, stride, padding, dilation,
            groups=inplanes, bias=bias)
        self.pointwise = nn.Conv3d(inplanes, planes, 1, 1, 0, 1, 1, bias=bias)

    def forward(self, x):
        x = self.conv(x)
        x = self.pointwise(x)
        return x

if __name__ == '__main__':
    _3d_conv = SeparableConv3d(3, 3)
    # snm = spectral_norm(nn.Conv2d(32,32,3))
    snm = spectral_norm(_3d_conv.pointwise)
    print(_3d_conv.pointwise.weight.shape)

    print(torch.linalg.matrix_norm(snm.weight, 2))
