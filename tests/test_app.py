import unittest
from tests.test_mod_auth import TestAuth

test_classes_to_run = [TestAuth]

# Run all test cases in test_classes_to_run
loader = unittest.TestLoader()
suites_list = [loader.loadTestsFromTestCase(x) for x in test_classes_to_run]
big_suite = unittest.TestSuite(suites_list)
runner = unittest.TextTestRunner()
results = runner.run(big_suite)
