import unittest
import testinfra


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.host = testinfra.get_host(
            'paramiko://vagrant@localhost:2222',
            ssh_identity_file='.vagrant/machines/default/virtualbox/private_key')

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
        package = self.host.package('ncmpcpp')
        self.assertTrue(package.is_installed)

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


class DotfilesTests(unittest.TestCase):
    def setUp(self):
        self.host = testinfra.get_host(
            'paramiko://vagrant@localhost:2222',
            ssh_identity_file='.vagrant/machines/default/virtualbox/private_key')

    def test_dotfiles_cloned(self):
        self.assertTrue(self.host.file('/home/vagrant/dev/dotfiles').is_directory)

    def test_vimrc_hard_linked(self):
        hard_link_file = self.host.file('/home/vagrant/.vimrc')
        dotfiles_file = self.host.file('/home/vagrant/dev/dotfiles/vim/.vimrc')
        self.assertTrue(hard_link_file.is_file)
        self.assertEqual(hard_link_file.size, dotfiles_file.size)

    def test_gvimrc_hard_linked(self):
        hard_link_file = self.host.file('/home/vagrant/.gvimrc')
        dotfiles_file = self.host.file('/home/vagrant/dev/dotfiles/vim/.gvimrc')
        self.assertTrue(hard_link_file.is_file)
        self.assertEqual(hard_link_file.size, dotfiles_file.size)

    def test_gitconfig_hard_linked(self):
        hard_link_file = self.host.file('/home/vagrant/.gitconfig')
        dotfiles_file = self.host.file('/home/vagrant/dev/dotfiles/git/.gitconfig')
        self.assertTrue(hard_link_file.is_file)
        self.assertEqual(hard_link_file.size, dotfiles_file.size)

    def test_bashrc_hard_linked(self):
        hard_link_file = self.host.file('/home/vagrant/.bashrc')
        dotfiles_file = self.host.file('/home/vagrant/dev/dotfiles/bash/.bashrc')
        self.assertTrue(hard_link_file.is_file)
        self.assertEqual(hard_link_file.size, dotfiles_file.size)

    def test_bash_aliases_hard_linked(self):
        hard_link_file = self.host.file('/home/vagrant/.bash_aliases')
        dotfiles_file = self.host.file('/home/vagrant/dev/dotfiles/bash/.bash_aliases')
        self.assertTrue(hard_link_file.is_file)
        self.assertEqual(hard_link_file.size, dotfiles_file.size)

    def test_bash_profile_hard_linked(self):
        hard_link_file = self.host.file('/home/vagrant/.bash_profile')
        dotfiles_file = self.host.file('/home/vagrant/dev/dotfiles/bash/.bash_profile')
        self.assertTrue(hard_link_file.is_file)
        self.assertEqual(hard_link_file.size, dotfiles_file.size)

    def test_profile_hard_linked(self):
        hard_link_file = self.host.file('/home/vagrant/.profile')
        dotfiles_file = self.host.file('/home/vagrant/dev/dotfiles/bash/.profile')
        self.assertTrue(hard_link_file.is_file)
        self.assertEqual(hard_link_file.size, dotfiles_file.size)

    def test_profile_hard_linked(self):
        hard_link_file = self.host.file('/home/vagrant/.profile')
        dotfiles_file = self.host.file('/home/vagrant/dev/dotfiles/bash/.profile')
        self.assertTrue(hard_link_file.is_file)
        self.assertEqual(hard_link_file.size, dotfiles_file.size)

    def test_i3_config_hard_linked(self):
        hard_link_file = self.host.file('/home/vagrant/.i3/config')
        dotfiles_file = self.host.file('/home/vagrant/dev/dotfiles/i3/config')
        self.assertTrue(hard_link_file.is_file)
        self.assertEqual(hard_link_file.size, dotfiles_file.size)


class VimTests(unittest.TestCase):
    def setUp(self):
        self.host = testinfra.get_host(
            'paramiko://vagrant@localhost:2222',
            ssh_identity_file='.vagrant/machines/default/virtualbox/private_key')

    def test_vim_version_8_is_installed(self):
        self.assertEqual(
            self.host.run("vim --version | grep '^VIM' | awk '{ print $5 }'").stdout.strip(), '8.0')

    def test_gitgutter_plugin_is_installed(self):
        self.assertTrue(self.host.file('/home/vagrant/.vim/bundle/vim-gitgutter').is_directory)

    def test_ctrlp_plugin_is_installed(self):
        self.assertTrue(self.host.file('/home/vagrant/.vim/bundle/ctrlp.vim').is_directory)

    def test_vundle_plugin_is_installed(self):
        self.assertTrue(self.host.file('/home/vagrant/.vim/bundle/Vundle.vim').is_directory)

    def test_tabular_plugin_is_installed(self):
        self.assertTrue(self.host.file('/home/vagrant/.vim/bundle/tabular').is_directory)

    def test_gruvbox_plugin_is_installed(self):
        self.assertTrue(self.host.file('/home/vagrant/.vim/bundle/gruvbox').is_directory)

    def test_indent_guides_plugin_is_installed(self):
        self.assertTrue(self.host.file('/home/vagrant/.vim/bundle/vim-indent-guides').is_directory)

    def test_rainbow_plugin_is_installed(self):
        self.assertTrue(self.host.file('/home/vagrant/.vim/bundle/rainbow').is_directory)

    def test_ansible_plugin_is_installed(self):
        self.assertTrue(self.host.file('/home/vagrant/.vim/bundle/ansible-vim').is_directory)

    def test_delimit_mate_plugin_is_installed(self):
        self.assertTrue(self.host.file('/home/vagrant/.vim/bundle/delimitMate').is_directory)

    def test_devicons_plugin_is_installed(self):
        self.assertTrue(self.host.file('/home/vagrant/.vim/bundle/vim-devicons').is_directory)

    def test_nerd_commenter_plugin_is_installed(self):
        self.assertTrue(self.host.file('/home/vagrant/.vim/bundle/nerdcommenter').is_directory)

    def test_nerd_tree_plugin_is_installed(self):
        self.assertTrue(self.host.file('/home/vagrant/.vim/bundle/NERDTree').is_directory)

    def test_surround_plugin_is_installed(self):
        self.assertTrue(self.host.file('/home/vagrant/.vim/bundle/vim-surround').is_directory)

    def test_endwise_plugin_is_installed(self):
        self.assertTrue(self.host.file('/home/vagrant/.vim/bundle/vim-endwise').is_directory)

    def test_you_complete_me_plugin_is_installed(self):
        self.assertTrue(self.host.file('/home/vagrant/.vim/bundle/YouCompleteMe').is_directory)

    def test_airline_plugin_is_installed(self):
        self.assertTrue(self.host.file('/home/vagrant/.vim/bundle/vim-airline').is_directory)

class ChromeTests(unittest.TestCase):
    def setUp(self):
        self.host = testinfra.get_host(
            'paramiko://vagrant@localhost:2222',
            ssh_identity_file='.vagrant/machines/default/virtualbox/private_key')

    def test_chrome_is_installed(self):
        package = self.host.package('google-chrome-stable')
        self.assertTrue(package.is_installed)

    def test_libxss1_prerequisite_is_installed(self):
        package = self.host.package('libxss1')
        self.assertTrue(package.is_installed)

    def test_libappindicator1_prerequisite_is_installed(self):
        package = self.host.package('libappindicator1')
        self.assertTrue(package.is_installed)

    def test_libindicator7_prerequisite_is_installed(self):
        package = self.host.package('libindicator7')
        self.assertTrue(package.is_installed)
