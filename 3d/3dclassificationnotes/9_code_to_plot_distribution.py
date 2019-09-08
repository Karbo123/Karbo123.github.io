#coding=utf-8
'''the code to plot the KPConv distribution'''
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcol
import matplotlib.cm as cm

# the range to calc: [-FLOATRANGE, FLOATRANGE]
FLOATRANGE = 5
SIGMA = 3  # for float

# picture resolution: [-RESOLUTION, RESOLUTION]
RESOLUTION = 100

#############################################


def float2int(floatmin, floatmax, floatval, intmin, intmax):
    return round((floatval - floatmin) / (floatmax - floatmin) *
                 (intmax - intmin) + intmin)


def int2float(intmin, intmax, intval, floatmin, floatmax):
    return float(intval - intmin) / (intmax - intmin) * (floatmax -
                                                         floatmin) + floatmin


#############################################


def show_it(kernel_points, pic):
    plt.imshow(pic, cmap='seismic', origin='lower')
    plt.colorbar()

    for kp in kernel_points:
        i = float2int(-FLOATRANGE, FLOATRANGE, kp['floatx'], -RESOLUTION,
                      RESOLUTION)
        j = float2int(-FLOATRANGE, FLOATRANGE, kp['floaty'], -RESOLUTION,
                      RESOLUTION)
        plt.scatter([i + RESOLUTION], [j + RESOLUTION],
                    color='k',
                    marker='*',
                    s=300)
    plt.xticks([])
    plt.yticks([])
    plt.show()


#############################################


def dist(x, y):
    return (x**2 + y**2)**0.5


# using the KPConv algorithm to calc the weight matrix
def inter(kernel_points, floatx, floaty):
    contri = []
    for kp in kernel_points:
        contri.append(
            max([
                0,
                1 - dist(floatx - kp['floatx'], floaty - kp['floaty']) / SIGMA
            ]))
    s = 0
    for i in range(len(kernel_points)):
        s = s + contri[i] * kernel_points[i]['value']

    return s


def generate(kernel_points, pic):
    for i in range(-RESOLUTION, RESOLUTION + 1):
        for j in range(-RESOLUTION, RESOLUTION + 1):
            floatx, floaty = int2float(-RESOLUTION, RESOLUTION, i, -FLOATRANGE,
                                       FLOATRANGE), int2float(
                                           -RESOLUTION, RESOLUTION, j,
                                           -FLOATRANGE, FLOATRANGE)

            pic[j + RESOLUTION][i + RESOLUTION] = inter(
                kernel_points, floatx, floaty)

    return pic


if __name__ == '__main__':

    # define kernel point positions and its associate weight matrix
    kernel_points = []
    kernel_points.append({'floatx': -4.5, 'floaty': -4, 'value': 5})
    kernel_points.append({'floatx': -3, 'floaty': 2, 'value': 3})
    kernel_points.append({'floatx': 3, 'floaty': 4, 'value': 7})
    kernel_points.append({'floatx': 4, 'floaty': -2, 'value': 0})
    kernel_points.append({'floatx': 0, 'floaty': 0, 'value': -7})

    # define the matrix to draw color
    pic = np.zeros([RESOLUTION * 2 + 1, RESOLUTION * 2 + 1])

    # generate picture
    pic = generate(kernel_points, pic)

    # show picture
    show_it(kernel_points, pic)
