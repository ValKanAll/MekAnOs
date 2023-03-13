import numpy as np


def gl2density(intercept, slope, no_min=False):
    def f(gl_mat):
        s = gl_mat.shape
        rho_mat = np.zeros(s)
        for i in range(s[0]):
            if len(s) >= 2:
                for j in range(s[1]):
                    if len(s) == 3:
                        for k in range(s[2]):
                            if no_min:
                                rho_mat[i, j, k] = intercept + slope * gl_mat[i, j, k]
                            else:
                                rho_mat[i, j, k] = max(0, intercept + slope * gl_mat[i, j, k])
                    else:
                        if no_min:
                            rho_mat[i, j] = intercept + slope * gl_mat[i, j]
                        else:
                            rho_mat[i, j] = max(0, intercept + slope * gl_mat[i, j])
            else:
                if no_min:
                    rho_mat[i] = intercept + slope * gl_mat[i]
                else:
                    rho_mat[i] = max(0, intercept + slope * gl_mat[i])

        return rho_mat
    return f


gl2density_JPR_HRpQCT = gl2density(-0.35746, 0.0001773)
gl2density_WL_HRpQCT_predefect = gl2density(-0.3503, 0.000176797)
gl2density_WL_QCT_predefect = gl2density(-0.0308734, 0.000656626)
#gl2density_WL_QCT_predefect_corrected = gl2density(-0.0, 0.001, no_min=True)
#gl2density_WL_QCT_postdefect = gl2density(-0.052869324, 0.000640576)
#gl2density_WL_QCT_postdefect_corrected = gl2density(-0.052869324 + 1024*0.000640576, 0.000640576)
gl2density_ARTORG_microCT = gl2density(-191.56*0.001, 369.154/4096*0.001)
gl2density_IBHGC = gl2density(0, 1)
gl2density_MCC = gl2density(0.01745, 0.0006855)


def density2E(_min_E=1):
    def dens2E(rho_mat, with_min=True, _min_E=1,
                  intercept=-34.7, slope=3230, c=1):
        s = rho_mat.shape
        E_mat = np.zeros(s)

        for i in range(len(rho_mat)):
            if len(s) >= 2:
                for j in range(s[1]):
                    if len(s) == 3:
                        for k in range(s[2]):
                            if with_min:
                                E_mat[i, j, k] = max(intercept + slope * rho_mat[i, j, k] ** c, _min_E)
                            else:
                                E_mat[i, j, k] = intercept + slope * rho_mat[i, j, k] ** c
                    else:
                        if with_min:
                            E_mat[i, j] = max(intercept + slope * rho_mat[i, j] ** c, _min_E)
                        else:
                            E_mat[i, j] = intercept + slope * rho_mat[i, j] ** c
            else:
                if with_min:
                    E_mat[i] = max(intercept + slope * rho_mat[i] ** c, _min_E)
                else:
                    E_mat[i] = intercept + slope * rho_mat[i] ** c

        return E_mat

    return dens2E


def E2density(E_mat, min_rho=0.000001, intercept=-34.7, slope=3230, c=1):
    rho_mat = []

    for i in range(len(E_mat)):
        rho_mat.append(((E_mat[i] - intercept) / slope) ** (1/c))
        #rho_mat.append(max(((E_mat[i] - intercept) / slope) ** (1/c), min_rho))

    return rho_mat