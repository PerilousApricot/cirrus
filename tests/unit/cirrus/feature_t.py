"""
feature command tests

"""
import mock
import os
import tempfile
import unittest

from cirrus.feature import new_feature_branch

from harnesses import CirrusConfigurationHarness, write_cirrus_conf


class FeatureCommandTest(unittest.TestCase):
    """
    Test Case for new_feature_branch function
    """
    def setUp(self):
        """set up test files"""
        self.dir = tempfile.mkdtemp()
        self.config = os.path.join(self.dir, 'cirrus.conf')
        write_cirrus_conf(self.config,
            {'name': 'cirrus_unittest', 'version': '1.2.3'},
            {'develop_branch': 'develop', 'feature_branch_prefix': 'feature/'}
            )
        self.harness = CirrusConfigurationHarness(
            'cirrus.feature.load_configuration',
            self.config)
        self.harness.setUp()

    def tearDown(self):
        self.harness.tearDown()
        if os.path.exists(self.dir):
            os.system('rm -rf {0}'.format(self.dir))

    def test_new_feature_branch(self):
        """
        _test_new_feature_branch_
        """
        opts = mock.Mock()
        opts.command = 'new'
        opts.name = 'testbranch'
        opts.push = False

        with mock.patch('cirrus.feature.checkout_and_pull') as mock_pull:
            with mock.patch('cirrus.feature.branch') as mock_branch:
                with mock.patch('cirrus.feature.push') as mock_push:
                    new_feature_branch(opts)
                    self.failUnless(mock_pull.called)
                    self.assertEqual(mock_pull.call_args[0][1], 'develop')
                    self.failUnless(mock_branch.called)
                    self.assertEqual(
                        mock_branch.call_args[0][1],
                        ''.join(('feature/', opts.name)))
                    self.failIf(mock_push.called)

    def test_new_feature_branch_push(self):
        """
        _test_new_feature_branch_push_

        test creating a new feature branch and pushing it to
        remote
        """
        opts = mock.Mock()
        opts.command = 'new'
        opts.name = 'testbranch'
        opts.push = True

        with mock.patch('cirrus.feature.checkout_and_pull') as mock_pull:
            with mock.patch('cirrus.feature.branch') as mock_branch:
                with mock.patch('cirrus.feature.push') as mock_push:
                    new_feature_branch(opts)
                    self.failUnless(mock_pull.called)
                    self.assertEqual(mock_pull.call_args[0][1], 'develop')
                    self.failUnless(mock_branch.called)
                    self.assertEqual(
                        mock_branch.call_args[0][1],
                        ''.join(('feature/', opts.name)))
                    self.failUnless(mock_push.called)


if __name__ == '__main__':
    unittest.main()