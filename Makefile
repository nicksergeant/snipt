pm = /var/www/.virtualenvs/snipt/bin/python /var/www/snipt/manage.py
ssh-server-deploy = ssh deploy@69.164.221.98 -p 55555
ssh-server-root = ssh root@69.164.221.98
ssh-vagrant = ssh vagrant@localhost -p 2222 -i ~/.vagrant.d/insecure_private_key

assets:
	@cat media/css/bootstrap.min.css \
		media/css/blog-themes/pro-adams/style.css \
		media/css/highlightjs-themes/tomorrow.css \
		media/css/themes.css \
		> media/css/pro.css
	@cat media/css/bootstrap.min.css \
		media/css/style.css \
		media/css/themes.css \
		media/css/chosen.css \
		media/css/codemirror.css \
		media/css/codemirror-themes/ambiance.css \
		media/css/codemirror-themes/blackboard.css \
		media/css/codemirror-themes/cobalt.css \
		media/css/codemirror-themes/eclipse.css \
		media/css/codemirror-themes/elegant.css \
		media/css/codemirror-themes/erlang-dark.css \
		media/css/codemirror-themes/lesser-dark.css \
		media/css/codemirror-themes/monokai.css \
		media/css/codemirror-themes/neat.css \
		media/css/codemirror-themes/night.css \
		media/css/codemirror-themes/rubyblue.css \
		media/css/codemirror-themes/solarized.css \
		media/css/codemirror-themes/twilight.css \
		media/css/codemirror-themes/vibrant-ink.css \
		media/css/codemirror-themes/xq-dark.css \
		media/css/highlightjs-themes/tomorrow.css \
		media/css/blog-themes/default/style.css \
		> media/css/snipt.css
	@cat media/js/src/account.js > media/js/src/account.min.js
	@cat media/js/src/snipts.js > media/js/src/snipts.min.js
	@cat media/js/src/search.js > media/js/src/search.min.js
	@cat media/js/src/jobs.js > media/js/src/jobs.min.js
	@cat media/js/src/application.js > media/js/src/application.min.js
	@cat media/js/src/modules/site.js > media/js/src/modules/site.min.js
	@cat media/js/src/modules/snipt.js > media/js/src/modules/snipt.min.js
	@cat media/js/src/pro.js > media/js/src/pro.min.js
	@cat media/js/libs/jquery.min.js \
		media/js/libs/jquery-ui.min.js \
		media/js/libs/angular.min.js \
		media/js/libs/angular-route.min.js \
		media/js/libs/underscore.js \
		media/js/libs/json2.js \
		media/js/libs/backbone.js \
		media/js/libs/bootstrap.min.js \
		media/js/plugins/jquery.hotkeys.js \
		media/js/plugins/jquery.infieldlabel.js \
		media/js/plugins/jquery.chosen.js \
		media/js/src/application.min.js \
		media/js/src/modules/site.min.js \
		media/js/src/modules/snipt.min.js \
		media/js/src/account.min.js \
		media/js/src/snipts.min.js \
		media/js/src/search.min.js \
		media/js/src/jobs.min.js \
		media/js/libs/codemirror.js \
		media/js/libs/highlight.js \
		> media/js/snipt-all.min.js
	@cat media/js/libs/highlight.js \
		media/js/src/pro.js \
		> media/js/pro-all.min.js

db:
	@echo Creating database user snipt:
	@sudo -u postgres bash -c 'createuser snipt -P'
	@sudo -u postgres bash -c 'createdb snipt -O snipt'

deploy:
	@$(ssh-server-deploy) 'cd /var/www/snipt; git pull;'
	@$(ssh-server-deploy) 'cd /var/www/snipt; make assets;'
	@$(ssh-server-deploy) '$(pm) collectstatic --noinput'
	@$(ssh-server-deploy) '$(pm) migrate'
	@$(ssh-server-deploy) 'sudo supervisorctl restart snipt'

deploy-heroku:
	@git push heroku

salt-server:
	@scp -q -P 55555 settings_local_server.py deploy@69.164.221.98:/var/www/snipt/settings_local.py
	@scp -q -P 55555 -r ./salt/ deploy@69.164.221.98:salt
	@scp -q -P 55555 -r ./pillar/ deploy@69.164.221.98:pillar
	@$(ssh-server-deploy) 'sudo rm -rf /srv'
	@$(ssh-server-deploy) 'sudo mkdir /srv'
	@$(ssh-server-deploy) 'sudo mv ~/salt /srv/salt'
	@$(ssh-server-deploy) 'sudo mv ~/pillar /srv/pillar'
	@$(ssh-server-deploy) 'sudo salt-call --local state.highstate'

salt-vagrant:
	@scp -q -P 2222 -i ~/.vagrant.d/insecure_private_key -r ./salt/ vagrant@localhost:salt
	@scp -q -P 2222 -i ~/.vagrant.d/insecure_private_key -r ./pillar/ vagrant@localhost:pillar
	@$(ssh-vagrant) 'sudo rm -rf /srv'
	@$(ssh-vagrant) 'sudo mkdir /srv'
	@$(ssh-vagrant) 'sudo mv ~/salt /srv/salt'
	@$(ssh-vagrant) 'sudo mv ~/pillar /srv/pillar'
	@$(ssh-vagrant) 'sudo salt-call --local state.highstate'

server:
	@$(ssh-server-root) 'sudo apt-get update'
	@$(ssh-server-root) 'sudo apt-get -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" upgrade'
	@$(ssh-server-root) 'sudo apt-get install -y software-properties-common python-software-properties'
	@$(ssh-server-root) 'sudo add-apt-repository -y ppa:saltstack/salt'
	@$(ssh-server-root) 'sudo apt-get update'
	@$(ssh-server-root) 'sudo apt-get install -y salt-minion'
	@scp -q -r ./salt/ root@69.164.221.98:salt
	@scp -q -r ./pillar/ root@69.164.221.98:pillar
	@$(ssh-server-root) 'sudo rm -rf /srv'
	@$(ssh-server-root) 'sudo mkdir /srv'
	@$(ssh-server-root) 'sudo mv ~/salt /srv/salt'
	@$(ssh-server-root) 'sudo mv ~/pillar /srv/pillar'
	@$(ssh-server-root) 'sudo salt-call --local state.highstate'

server-init:
	@$(ssh-server-deploy) 'cd /var/www/snipt; make db;'
	@$(ssh-server-deploy) '$(pm) syncdb --noinput;'
	@$(ssh-server-deploy) '$(pm) migrate;'
	@$(ssh-server-deploy) '$(pm) backfill_api_keys;'
	@$(ssh-server-deploy) '$(pm) rebuild_index --noinput;'

vagrant:
	@vagrant up --provider=vmware_fusion
	@$(ssh-vagrant) 'sudo apt-get update'
	@$(ssh-vagrant) 'sudo apt-get -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" upgrade'
	@$(ssh-vagrant) 'sudo apt-get install -y software-properties-common python-software-properties'
	@$(ssh-vagrant) 'sudo add-apt-repository -y ppa:saltstack/salt'
	@$(ssh-vagrant) 'sudo apt-get update'
	@$(ssh-vagrant) 'sudo apt-get install -y salt-minion'
	@scp -q -P 2222 -i ~/.vagrant.d/insecure_private_key -r ./salt/ vagrant@localhost:salt
	@scp -q -P 2222 -i ~/.vagrant.d/insecure_private_key -r ./pillar/ vagrant@localhost:pillar
	@$(ssh-vagrant) 'sudo rm -rf /srv'
	@$(ssh-vagrant) 'sudo mkdir /srv'
	@$(ssh-vagrant) 'sudo mv ~/salt /srv/salt'
	@$(ssh-vagrant) 'sudo mv ~/pillar /srv/pillar'
	@$(ssh-vagrant) 'sudo salt-call --local state.highstate'
	@vagrant ssh -c 'cd /var/www/snipt; make db;'
	@vagrant ssh -c '$(pm) syncdb;'
	@$(ssh-vagrant) '$(pm) migrate;'
	@$(ssh-vagrant) '$(pm) backfill_api_keys;'
	@$(ssh-vagrant) '$(pm) rebuild_index --noinput;'

.PHONY: assets, \
	db, \
	deploy, \
	deploy-heroku, \
	provision-server, \
	provision-vagrant, \
	salt-server, \
	salt-vagrant, \
	server-init, \
	server, \
	vagrant
