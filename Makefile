SHELL := /bin/bash

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

clean:
	@vagrant destroy -f

ubuntu-up: check-nerdfonts clean virtualenv
	@vagrant up ubuntu --provision

ubuntu-gui-up: check-nerdfonts clean virtualenv
	@DEVBOX_GUI=true vagrant up ubuntu

ubuntu-tests:
	@rm -f .vagrant/ssh-config
	@vagrant ssh-config ubuntu > .vagrant/ssh-config
	# Unfortunately the virtualenv activation doesn't persist across targets (or perhaps a shell session),
	# so the full path to the testinfra executable needs to be specified.
	@$$WORKON_HOME/devbox/bin/testinfra -v --ssh-config=.vagrant/ssh-config --hosts=ubuntu tests.py

ubuntu: ubuntu-up ubuntu-tests

ubuntu-gui: ubuntu-gui-up ubuntu-tests
