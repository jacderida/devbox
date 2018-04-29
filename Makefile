SHELL := /bin/bash
USERNAME := $(shell whoami)

check-nerdfonts:
ifndef DEVBOX_NERDFONTS_SHARED_FOLDER
	@echo "WARNING: The DEVBOX_NERDFONTS_SHARED_FOLDER environment variable is undefined. \
		Provisioning will take a long time without this. See the documentation."
endif

virtualenv:
	( \
		source /usr/local/bin/virtualenvwrapper.sh; \
		if [ ! -d "$$WORKON_HOME/devbox" ]; then \
			mkvirtualenv devbox; \
		fi; \
		workon devbox; \
		pip install paramiko; \
		pip install testinfra; \
	)

clean-ubuntu:
	@vagrant destroy ubuntu -f

ubuntu-up: virtualenv
	@ANSIBLE_SKIP_TAGS='gui' vagrant up ubuntu --provision

ubuntu-gui-up: check-nerdfonts
	@DEVBOX_GUI=true vagrant up ubuntu

ubuntu-tests:
	@rm -f .vagrant/ssh-config
	@vagrant ssh-config ubuntu > .vagrant/ssh-config
	# Unfortunately the virtualenv activation doesn't persist across targets (or perhaps a shell session),
	# so the full path to the testinfra executable needs to be specified.
	@$$WORKON_HOME/devbox/bin/testinfra -v --ssh-config=.vagrant/ssh-config --hosts=ubuntu tests.py

ubuntu: ubuntu-up ubuntu-tests

ubuntu-gui: ubuntu-gui-up ubuntu-tests

clean-debian:
	@vagrant destroy debian -f

debian-up:
	@ANSIBLE_SKIP_TAGS='gui' vagrant up debian --provision

debian-gui-up: check-nerdfonts
	@DEVBOX_GUI=true vagrant up debian --provision

debian-gui-up-corporate: check-nerdfonts
	@DEVBOX_GUI=true vagrant up debian --provision

debian-tests:
	@rm -f .vagrant/ssh-config
	@vagrant ssh-config debian > .vagrant/ssh-config
	# Unfortunately the virtualenv activation doesn't persist across targets (or perhaps a shell session),
	# so the full path to the testinfra executable needs to be specified.
	@$$WORKON_HOME/devbox/bin/testinfra -v --ssh-config=.vagrant/ssh-config --hosts=debian tests.py

debian: debian-up debian-tests

debian-gui: debian-gui-up debian-tests

clean-fedora:
	@vagrant destroy fedora -f

fedora-up: virtualenv
	@ANSIBLE_SKIP_TAGS='gui' vagrant up fedora --provision

fedora-gui-up: check-nerdfonts
	@DEVBOX_GUI=true vagrant up fedora --provision

bare-metal:
	ansible-playbook -i inventory playbook.yml --extra-vars "dev_user=${USERNAME}"

clean: clean-ubuntu clean-debian clean-fedora
