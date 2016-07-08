import cv2
import csv
import os
import fnmatch
import unittest
from nose_parameterized import parameterized
from nose.tools import nottest
from operator import itemgetter
from vision.measurements.detect_ruler import ruler_scale_factor
from vision.measurements.detect_ruler import remove_multiples
from vision.tests import TEST_DATA


folder_distort = os.path.join(TEST_DATA, 'ruler', 'distorted')
folder_measure = os.path.join(TEST_DATA, 'ruler', 'measured')


class TestTransforms(unittest.TestCase):
    scale_factor_base = 0

    def setUp(self):
        image_base = cv2.imread(os.path.join(folder_distort, 'test.JPG'))
        self.scale_factor_base = ruler_scale_factor(image_base)

    def tearDown(self):
        pass

    @nottest
    def generate_test_files():
        test_dir_files = os.listdir(folder_distort)
        return sorted(fnmatch.filter(test_dir_files, '*.JPG'))

    @parameterized.expand(generate_test_files())
    def test_transform(self, file):
        image = cv2.imread(os.path.join(folder_distort, file))
        scale_factor = ruler_scale_factor(image)
        self.assertAlmostEqual(self.scale_factor_base, scale_factor, delta=0.2)


class TestMeasured(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    @nottest
    def generate_test_files():
        with open(os.path.join(folder_measure, 'data.csv'), 'r') as csv_file:
            reader = csv.reader(csv_file, delimiter=' ')
            data = [(filename, float(separation)) for filename, separation in reader]
        return sorted(data, key=itemgetter(0))

    @parameterized.expand(generate_test_files())
    def test_measurement(self, file, separation):
        image = cv2.imread(os.path.join(folder_measure, file))
        scale_factor = ruler_scale_factor(image)
        self.assertAlmostEqual(separation, 0.5 / scale_factor, delta=0.5)


class TestRemoveMultiples(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_evens(self):
        evens = zip(range(2, 10, 2), range(2, 10, 2))
        evens_no_multiples = remove_multiples(evens)
        self.assertEqual(evens_no_multiples, [(2, 2)])
