def test_cmake_package_is_installed(host):
    assert host.package('cmake').is_installed

def test_curl_package_is_installed(host):
    assert host.package('curl').is_installed

def test_dos2unix_package_is_installed(host):
    assert host.package('dos2unix').is_installed

def test_flac_package_is_installed(host):
    assert host.package('flac').is_installed

def test_git_package_is_installed(host):
    assert host.package('git').is_installed

def test_htop_package_is_installed(host):
    assert host.package('htop').is_installed

def test_mpc_package_is_installed(host):
    assert host.package('mpc').is_installed

def test_mpd_package_is_installed(host):
    assert host.package('mpd').is_installed

def test_mpdscribble_dev_package_is_installed(host):
    assert host.package('mpdscribble').is_installed

def test_ncmpcpp_package_is_installed(host):
    assert host.package('ncmpcpp').is_installed

def test_ncurses_dev_package_is_installed(host):
    assert host.package('libncurses5-dev').is_installed

def test_python_dev_package_is_installed(host):
    assert host.package('python-dev').is_installed

def test_python_dev_package_is_installed(host):
    assert host.package('python-dev').is_installed

def test_silversearcher_ag_package_is_installed(host):
    assert host.package('silversearcher-ag').is_installed

def test_subversion_package_is_installed(host):
    assert host.package('subversion').is_installed

def test_terminator_package_is_installed(host):
    assert host.package('terminator').is_installed

def test_tree_package_is_installed(host):
    assert host.package('tree').is_installed

def test_unzip_package_is_installed(host):
    assert host.package('unzip').is_installed

def test_dotfiles_cloned(host):
    user = host.user().name
    assert host.file("/home/{0}/dev/dotfiles".format(user)).is_directory

def test_vimrc_hard_linked(host):
    user = host.user().name
    hard_link_file = host.file("/home/{0}/.vimrc".format(user))
    dotfiles_file = host.file("/home/{0}/dev/dotfiles/vim/.vimrc".format(user))
    assert hard_link_file.is_file
    assert hard_link_file.size == dotfiles_file.size

def test_gvimrc_hard_linked(host):
    user = host.user().name
    hard_link_file = host.file("/home/{0}/.gvimrc".format(user))
    dotfiles_file = host.file('/home/{0}/dev/dotfiles/vim/.gvimrc'.format(user))
    assert hard_link_file.is_file
    assert hard_link_file.size == dotfiles_file.size

def test_gitconfig_hard_linked(host):
    user = host.user().name
    hard_link_file = host.file("/home/{0}/.gitconfig".format(user))
    dotfiles_file = host.file("/home/{0}/dev/dotfiles/git/.gitconfig".format(user))
    assert hard_link_file.is_file
    assert hard_link_file.size == dotfiles_file.size

def test_bashrc_hard_linked(host):
    user = host.user().name
    hard_link_file = host.file("/home/{0}/.bashrc".format(user))
    dotfiles_file = host.file("/home/{0}/dev/dotfiles/bash/.bashrc".format(user))
    assert hard_link_file.is_file
    assert hard_link_file.size == dotfiles_file.size

def test_zshrc_hard_linked(host):
    user = host.user().name
    hard_link_file = host.file("/home/{0}/.zshrc".format(user))
    dotfiles_file = host.file("/home/{0}/dev/dotfiles/zsh/.zshrc".format(user))
    assert hard_link_file.is_file
    assert hard_link_file.size == dotfiles_file.size

def test_bash_aliases_hard_linked(host):
    user = host.user().name
    hard_link_file = host.file("/home/{0}/.aliases".format(user))
    dotfiles_file = host.file("/home/{0}/dev/dotfiles/bash/.bash_aliases".format(user))
    assert hard_link_file.is_file
    assert hard_link_file.size == dotfiles_file.size

def test_bash_profile_hard_linked(host):
    user = host.user().name
    hard_link_file = host.file("/home/{0}/.bash_profile".format(user))
    dotfiles_file = host.file("/home/{0}/dev/dotfiles/bash/.bash_profile".format(user))
    assert hard_link_file.is_file
    assert hard_link_file.size == dotfiles_file.size

def test_profile_hard_linked(host):
    user = host.user().name
    hard_link_file = host.file("/home/{0}/.profile".format(user))
    dotfiles_file = host.file("/home/{0}/dev/dotfiles/bash/.profile".format(user))
    assert hard_link_file.is_file
    assert hard_link_file.size == dotfiles_file.size

def test_profile_hard_linked(host):
    user = host.user().name
    hard_link_file = host.file("/home/{0}/.profile".format(user))
    dotfiles_file = host.file("/home/{0}/dev/dotfiles/bash/.profile".format(user))
    assert hard_link_file.is_file
    assert hard_link_file.size == dotfiles_file.size

def test_i3_config_hard_linked(host):
    user = host.user().name
    hard_link_file = host.file("/home/{0}/.i3/config".format(user))
    dotfiles_file = host.file("/home/{0}/dev/dotfiles/i3/config".format(user))
    assert hard_link_file.is_file
    assert hard_link_file.size == dotfiles_file.size

def test_vim_version_8_is_installed(host):
    assert host.run("vim --version | grep '^VIM' | awk '{ print $5 }'").stdout.strip() == '8.0'

def test_gitgutter_plugin_is_installed(host):
    user = host.user().name
    assert host.file("/home/{0}/.vim/bundle/vim-gitgutter".format(user)).is_directory

def test_ctrlp_plugin_is_installed(host):
    user = host.user().name
    assert host.file("/home/{0}/.vim/bundle/ctrlp.vim".format(user)).is_directory

def test_vundle_plugin_is_installed(host):
    user = host.user().name
    assert host.file("/home/{0}/.vim/bundle/Vundle.vim".format(user)).is_directory

def test_tabular_plugin_is_installed(host):
    user = host.user().name
    assert host.file("/home/{0}/.vim/bundle/tabular".format(user)).is_directory

def test_gruvbox_plugin_is_installed(host):
    user = host.user().name
    assert host.file("/home/{0}/.vim/bundle/gruvbox".format(user)).is_directory

def test_indent_guides_plugin_is_installed(host):
    user = host.user().name
    assert host.file("/home/{0}/.vim/bundle/vim-indent-guides".format(user)).is_directory

def test_rainbow_plugin_is_installed(host):
    user = host.user().name
    assert host.file("/home/{0}/.vim/bundle/rainbow".format(user)).is_directory

def test_ansible_plugin_is_installed(host):
    user = host.user().name
    assert host.file("/home/{0}/.vim/bundle/ansible-vim".format(user)).is_directory

def test_delimit_mate_plugin_is_installed(host):
    user = host.user().name
    assert host.file("/home/{0}/.vim/bundle/delimitMate".format(user)).is_directory

def test_devicons_plugin_is_installed(host):
    user = host.user().name
    assert host.file("/home/{0}/.vim/bundle/vim-devicons".format(user)).is_directory

def test_nerd_commenter_plugin_is_installed(host):
    user = host.user().name
    assert host.file("/home/{0}/.vim/bundle/nerdcommenter".format(user)).is_directory

def test_nerd_tree_plugin_is_installed(host):
    user = host.user().name
    assert host.file("/home/{0}/.vim/bundle/NERDTree".format(user)).is_directory

def test_surround_plugin_is_installed(host):
    user = host.user().name
    assert host.file("/home/{0}/.vim/bundle/vim-surround".format(user)).is_directory

def test_endwise_plugin_is_installed(host):
    user = host.user().name
    assert host.file("/home/{0}/.vim/bundle/vim-endwise".format(user)).is_directory

def test_you_complete_me_plugin_is_installed(host):
    user = host.user().name
    assert host.file("/home/{0}/.vim/bundle/YouCompleteMe".format(user)).is_directory

def test_airline_plugin_is_installed(host):
    user = host.user().name
    assert host.file("/home/{0}/.vim/bundle/vim-airline".format(user)).is_directory

def test_chrome_is_installed(host):
    assert host.package('google-chrome-stable').is_installed

def test_libxss1_prerequisite_is_installed(host):
    assert host.package('libxss1').is_installed

def test_libappindicator1_prerequisite_is_installed(host):
    assert host.package('libappindicator1').is_installed

def test_libindicator7_prerequisite_is_installed(host):
    assert host.package('libindicator7').is_installed

def test_zsh_is_installed(host):
    assert host.package('zsh').is_installed

def test_pam_configuration_allows_no_password_for_change_shell(host):
    assert host.file('/etc/pam.d/chsh').contains('auth sufficient pam_shells.so')

def test_zsh_syntax_highlighting_plugin_is_installed(host):
    user = host.user().name
    assert host.file('/home/{0}/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting'.format(user)).is_directory
