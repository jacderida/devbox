import unittest
import testinfra


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.host = testinfra.get_host("local://")

    def test_cmake_package_is_installed(self):
        package = self.host.package('cmake')
        self.assertTrue(package.is_installed)

    def test_curl_package_is_installed(self):
        package = self.host.package('curl')
        self.assertTrue(package.is_installed)

    def test_dos2unix_package_is_installed(self):
        package = self.host.package('dos2unix')
        self.assertTrue(package.is_installed)

    def test_flac_package_is_installed(self):
        package = self.host.package('flac')
        self.assertTrue(package.is_installed)

    def test_git_package_is_installed(self):
        package = self.host.package('git')
        self.assertTrue(package.is_installed)

    def test_htop_package_is_installed(self):
        package = self.host.package('htop')
        self.assertTrue(package.is_installed)

    def test_mpc_package_is_installed(self):
        package = self.host.package('mpc')
        self.assertTrue(package.is_installed)

    def test_mpd_package_is_installed(self):
        package = self.host.package('mpd')
        self.assertTrue(package.is_installed)

    def test_mpdscribble_dev_package_is_installed(self):
        package = self.host.package('mpdscribble')
        self.assertTrue(package.is_installed)

    def test_ncmpcpp_package_is_installed(self):
        # For some reason it just won't register this package as being installed.
        self.assertEqual(self.host.run('which ncmpcpp').rc, 0)

    def test_ncurses_dev_package_is_installed(self):
        package = self.host.package('libncurses5-dev')
        self.assertTrue(package.is_installed)

    def test_python_dev_package_is_installed(self):
        package = self.host.package('python-dev')
        self.assertTrue(package.is_installed)

    def test_python_dev_package_is_installed(self):
        package = self.host.package('python-dev')
        self.assertTrue(package.is_installed)

    def test_silversearcher_ag_package_is_installed(self):
        package = self.host.package('silversearcher-ag')
        self.assertTrue(package.is_installed)

    def test_subversion_package_is_installed(self):
        package = self.host.package('subversion')
        self.assertTrue(package.is_installed)

    def test_terminator_package_is_installed(self):
        package = self.host.package('terminator')
        self.assertTrue(package.is_installed)

    def test_tree_package_is_installed(self):
        package = self.host.package('tree')
        self.assertTrue(package.is_installed)

    def test_unzip_package_is_installed(self):
        package = self.host.package('unzip')
        self.assertTrue(package.is_installed)
