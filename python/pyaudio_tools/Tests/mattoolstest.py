__author__ = 'Adam Miller'
import unittest
import numpy as np
import scipy.fftpack as fftp
from pa_tools.stftmanager import StftManager
import pa_tools.mattools as mat


class MatToolsTest(unittest.TestCase):

    def setUp(self):
        self.dft_len = 8
        self.stft = StftManager(dft_length=self.dft_len,
                                window_length=self.dft_len,
                                hop_length=self.dft_len,
                                use_window_fcn=False)

    def testZipFFT(self):
        reals = [4, 0, 1, 0]
        imags = [2, 1, 0, 0]
        zipped = mat.zip_fft(reals, imags)
        self.assertListFloatEqual(zipped, [4, 0, 1, 1, 0, 0, 0, 2])

    def testToNumpyFormat(self):
        dfts = []
        dfts.append(([[4, 0, 1, 0]], [[2, 1, 0, 0]]))
        dfts.append(([[1, 0, 0, 1]], [[0, 1, 1, 0]]))
        arr = mat.to_numpy_format(dfts)
        self.assertListFloatEqual(arr[:, 0], [4, 0, 1, 1, 0, 0, 0, 2])
        self.assertListFloatEqual(arr[:, 1], [1, 0, 1, 0, 1, 1, 0, 0])

    def testFFTComp(self):
        data = np.array([1, 0, 0, 1, 1, 0, 0, 1], dtype=np.float32)
        self.stft.performStft(data)
        dfts = self.stft.getDFTs()
        transformed = mat.to_numpy_format(dfts)
        ifftout = fftp.irfft(transformed[:, 0] / 2)
        print ifftout
        self.assertListFloatEqual(data, ifftout)

    def testFullFft(self):
        data = np.array([1, 2, 1, 3, 1, 4, 1, 2], dtype=np.float32)
        dft = np.array([15, -2.1213 + 0.7071j, -1j, 2.1213 + 0.7071j,
                        -7, 2.1213 - 0.7071j, 1j, -2.1213 - 0.7071j])
        self.stft.performStft(data)
        dfts = self.stft.getDFTs()
        reals = dfts[0][0][0]
        imags = dfts[0][1][0]
        full_fft = mat.to_full_fft(reals, imags)
        print full_fft / 2
        self.assertListFloatEqual(dft, full_fft / 2)

    def testRIFFT(self):
        data = np.array([1, 2, 1, 3, 1, 4, 1, 2], dtype=np.float32)
        dft = np.array([15, -2.1213 + 0.7071j, -1j, 2.1213 + 0.7071j, -7])
        inver = np.fft.irfft(dft)
        self.assertListFloatEqual(data, inver)

    def testFullFfft2(self):
        reals = [4, 0, 1, 0]
        imags = [1, 2, 0, 0]
        full_fft = mat.to_full_fft(reals, imags)
        self.assertListFloatEqual(
            np.array([4, 2j, 1, 0, 1, 0, 1, -2j]), full_fft)

    def testRealFFT(self):
        reals = [4, 0, 1, 0]
        imags = [1, 2, 0, 0]
        half_fft = mat.to_real_fft(reals, imags)
        self.assertListFloatEqual(np.array([4, 2j, 1, 0, 1]), half_fft)

    def testToMatlab(self):
        dfts = []
        dfts.append(([[4, 0, 1, 0]], [[2, 1, 0, 0]]))
        dfts.append(([[1, 0, 0, 1]], [[0, 1, 1, 0]]))
        dft_arr = mat.to_matlab_format(dfts)
        chan1 = np.array([4, 1j, 1, 0, 2, 0, 1, -1j], dtype=np.complex64)
        chan2 = np.array([1, 1j, 1j, 1, 0, 1, -1j, -1j], dtype=np.complex64)
        print dft_arr
        self.assertListFloatEqual(chan1, dft_arr[0, :])
        self.assertListFloatEqual(chan2, dft_arr[1, :])

    def testToRealMatlab(self):
        dfts = []
        dfts.append(([[4, 0, 1, 0]], [[2, 1, 0, 0]]))
        dfts.append(([[1, 0, 0, 1]], [[0, 1, 1, 0]]))
        dft_arr = mat.to_real_matlab_format(dfts)
        chan1 = np.array([4, 1j, 1, 0, 2], dtype=np.complex64)
        chan2 = np.array([1, 1j, 1j, 1, 0], dtype=np.complex64)
        print dft_arr
        self.assertListFloatEqual(chan1, dft_arr[0, :])
        self.assertListFloatEqual(chan2, dft_arr[1, :])

    def testNormalizeRows(self):
        data = np.array([[1, 0, 3],
                         [0, 0, 0],
                         [2, 2, 4]], dtype=np.float32)
        a = mat.normalize_rows(data.copy())
        correct = np.array([[.25, 0., 0.75],
                            [0.,  0.,   0.],
                            [0.25, 0.25, 0.5]])
        self.assertEquals((a - correct).any(), False)
        # Test normalization of only submatrix
        mat.normalize_rows(data[1:, :])
        self.assertEquals((data[1:, :] - correct[1:, :]).any(), False)
        self.assertEquals((data[0] - np.array([1, 0, 3])).any(), False)

    def assertListFloatEqual(self, list1, list2):
            if not len(list1) == len(list2):
                raise AssertionError("Lists differ in lenght. Cannot be equal")
            for i in range(len(list1)):
                try:
                    self.assertLessEqual(abs(list1[i] - list2[i]), 1e-4)
                except AssertionError:
                    err_str = "Lists differ on element " + str(i) + ": " + \
                              str(list1[i]) + " vs. " + str(list2[i])
                    raise AssertionError(err_str)

    def tearDown(self):
        pass
