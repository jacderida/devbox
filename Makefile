SHELL := /bin/bash
USERNAME := $(shell whoami)

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

ubuntu-up: export ANSIBLE_SKIP_TAGS := gui
ubuntu-up: export DEVBOX_GUI := false
ubuntu-up: export DEVBOX_BARE_METAL_MODE := false
ubuntu-up:
	vagrant up ubuntu --provision

ubuntu-gui-up: export DEVBOX_GUI := true
ubuntu-gui-up: export DEVBOX_BARE_METAL_MODE := false
ubuntu-gui-up:
	vagrant up ubuntu --provision

ubuntu-gui-up-corporate: export DEVBOX_CORPORATE_MODE := true
ubuntu-gui-up-corporate: export DEVBOX_GUI := true
ubuntu-gui-up-corporate: export DEVBOX_BARE_METAL_MODE := false
ubuntu-gui-up-corporate:
	vagrant up ubuntu --provision

ubuntu-tests:
	@rm -f .vagrant/ssh-config
	@vagrant ssh-config ubuntu > .vagrant/ssh-config
	# Unfortunately the virtualenv activation doesn't persist across targets (or perhaps a shell session),
	# so the full path to the testinfra executable needs to be specified.
	@$$WORKON_HOME/devbox/bin/testinfra -v --ssh-config=.vagrant/ssh-config --hosts=ubuntu tests.py

debian-up: export ANSIBLE_SKIP_TAGS := gui
debian-up: export DEVBOX_GUI := false
debian-up: export DEVBOX_BARE_METAL_MODE := false
debian-up:
	vagrant up debian --provision

debian-gui-up: export DEVBOX_GUI := true
debian-gui-up: export DEVBOX_BARE_METAL_MODE := false
debian-gui-up:
	vagrant up debian --provision

debian-gui-up-corporate: export DEVBOX_CORPORATE_MODE := true
debian-gui-up-corporate: export DEVBOX_GUI := true
debian-gui-up-corporate: export DEVBOX_BARE_METAL_MODE := false
debian-gui-up-corporate:
	vagrant up debian --provision

debian-tests:
	@rm -f .vagrant/ssh-config
	@vagrant ssh-config debian > .vagrant/ssh-config
	# Unfortunately the virtualenv activation doesn't persist across targets (or perhaps a shell session),
	# so the full path to the testinfra executable needs to be specified.
	@$$WORKON_HOME/devbox/bin/testinfra -v --ssh-config=.vagrant/ssh-config --hosts=debian tests.py

fedora-up: export ANSIBLE_SKIP_TAGS := gui
fedora-up: export DEVBOX_GUI := false
fedora-up: export DEVBOX_BARE_METAL_MODE := false
fedora-up:
	vagrant up fedora --provision

fedora-gui-up: export DEVBOX_GUI := true
fedora-gui-up: export DEVBOX_BARE_METAL_MODE := false
fedora-gui-up:
	vagrant up fedora --provision

fedora-gui-up-corporate: export DEVBOX_CORPORATE_MODE := true
fedora-gui-up-corporate: export DEVBOX_GUI := true
fedora-gui-up-corporate: export DEVBOX_BARE_METAL_MODE := false
fedora-gui-up-corporate:
	vagrant up fedora --provision

bare-metal: export DEVBOX_BARE_METAL_MODE := true
bare-metal:
	ansible-playbook -i inventory playbook.yml --extra-vars "dev_user=${USERNAME}"

clean-ubuntu:
	@vagrant destroy ubuntu -f

clean-fedora:
	@vagrant destroy fedora -f

clean-debian:
	@vagrant destroy debian -f

clean: clean-ubuntu clean-debian clean-fedora
