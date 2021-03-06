import numpy as np


def raytrace(Vp, thic, offset):

    pm = np.zeros((len(thic), len(offset)))
    tm = np.zeros((len(thic), len(offset)))
    for ii in xrange(len(thic)):  # for each interface
        for io in xrange(len(offset)):  # for each offset
            err = offset[io]
            counter = 0
            p0 = np.sin(np.pi/4) / Vp[ii]
            flag = False
            while err > 0.01 * offset[io]:
                y0 = 0
                for i in xrange(ii + 1):
                    y0 += (thic[i] * Vp[i] * p0) / np.sqrt(1 - Vp[i]**2 *
                                                           p0**2)
                y0 = 2 * y0

                ydelta = offset[io] - y0

                pg = 0  # gradient of p relate to y
                for i in range(ii + 1):
                    pg += (thic[i] * Vp[i]) / ((1 - Vp[i]**2 * p0**2)**(1.5))
                pg = pg**(-1)
                pg = 0.5 * pg

                p0 += pg * ydelta  # corrected p

                y = 0
                for i in range(ii + 1):
                    y += (thic[i] * Vp[i] * p0) / np.sqrt(1 - Vp[i]**2 * p0**2)
                y = 2 * y

                err = np.abs(y - offset[io])

                counter += 1
                if counter == 100:
                    flag = True
                    break
            if flag is True:
                pm[ii, io] = np.NaN
            else:
                pm[ii, io] = p0

    for ii in xrange(len(thic)):  # for each interface
        for io in xrange(len(offset)):  # for each offset
            traveltime = 0
            p = pm[ii, io]
            for i in range(ii + 1):
                traveltime = traveltime + 2 * thic[i] /\
                             (Vp[i] * np.sqrt(1 - Vp[i]**2 * p**2))
            tm[ii, io] = traveltime

    return pm, tm

if __name__ == "__main__":
    pass
