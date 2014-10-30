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
	@cat media/js/src/account.js|jsmin > media/js/src/account.min.js
	@cat media/js/src/snipts.js|jsmin > media/js/src/snipts.min.js
	@cat media/js/src/search.js|jsmin > media/js/src/search.min.js
	@cat media/js/src/jobs.js|jsmin > media/js/src/jobs.min.js
	@cat media/js/src/application.js|jsmin > media/js/src/application.min.js
	@cat media/js/src/modules/site.js|jsmin > media/js/src/modules/site.min.js
	@cat media/js/src/modules/snipt.js|jsmin > media/js/src/modules/snipt.min.js
	@cat media/js/src/pro.js|jsmin > media/js/src/pro.min.js
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
	/Users/Nick/.virtualenvs/snipt/bin/python manage.py collectstatic --noinput

db:
	@echo Creating database user snipt:
	@sudo -H -u postgres bash -c 'createuser snipt -P'
	@sudo -H -u postgres bash -c 'createdb snipt -O snipt'

deploy:
	@ssh vagrant@localhost -p 2222 -i ~/.vagrant.d/insecure_private_key 'cd /var/www/snipt; git pull;'
	@ssh vagrant@localhost -p 2222 -i ~/.vagrant.d/insecure_private_key 'cd /var/www/snipt; make assets;'
	@ssh vagrant@localhost -p 2222 -i ~/.vagrant.d/insecure_private_key 'cd /var/www/snipt; /var/www/.virtualenvs/snipt/bin/python manage.py migrate'
	@ssh vagrant@localhost -p 2222 -i ~/.vagrant.d/insecure_private_key 'sudo supervisorctl restart snipt'

deploy-heroku:
	@git push heroku

salt-vagrant:
	@scp -q -P 2222 -i ~/.vagrant.d/insecure_private_key -r ./salt/ vagrant@localhost:salt
	@scp -q -P 2222 -i ~/.vagrant.d/insecure_private_key -r ./pillar/ vagrant@localhost:pillar
	@ssh vagrant@localhost -p 2222 -i ~/.vagrant.d/insecure_private_key 'sudo rm -rf /srv'
	@ssh vagrant@localhost -p 2222 -i ~/.vagrant.d/insecure_private_key 'sudo mkdir /srv'
	@ssh vagrant@localhost -p 2222 -i ~/.vagrant.d/insecure_private_key 'sudo mv ~/salt /srv/salt'
	@ssh vagrant@localhost -p 2222 -i ~/.vagrant.d/insecure_private_key 'sudo mv ~/pillar /srv/pillar'
	@ssh vagrant@localhost -p 2222 -i ~/.vagrant.d/insecure_private_key 'sudo salt-call --local state.highstate'

vagrant:
	@vagrant up --provider=vmware_fusion
	@ssh vagrant@localhost -p 2222 -i ~/.vagrant.d/insecure_private_key 'sudo apt-get update'
	@ssh vagrant@localhost -p 2222 -i ~/.vagrant.d/insecure_private_key 'sudo apt-get install -y software-properties-common python-software-properties'
	@ssh vagrant@localhost -p 2222 -i ~/.vagrant.d/insecure_private_key 'sudo add-apt-repository -y ppa:saltstack/salt'
	@ssh vagrant@localhost -p 2222 -i ~/.vagrant.d/insecure_private_key 'sudo apt-get update'
	@ssh vagrant@localhost -p 2222 -i ~/.vagrant.d/insecure_private_key 'sudo apt-get install -y salt-minion'
	@scp -q -P 2222 -i ~/.vagrant.d/insecure_private_key -r ./salt/ vagrant@localhost:salt
	@scp -q -P 2222 -i ~/.vagrant.d/insecure_private_key -r ./pillar/ vagrant@localhost:pillar
	@ssh vagrant@localhost -p 2222 -i ~/.vagrant.d/insecure_private_key 'sudo rm -rf /srv'
	@ssh vagrant@localhost -p 2222 -i ~/.vagrant.d/insecure_private_key 'sudo mkdir /srv'
	@ssh vagrant@localhost -p 2222 -i ~/.vagrant.d/insecure_private_key 'sudo mv ~/salt /srv/salt'
	@ssh vagrant@localhost -p 2222 -i ~/.vagrant.d/insecure_private_key 'sudo mv ~/pillar /srv/pillar'
	@ssh vagrant@localhost -p 2222 -i ~/.vagrant.d/insecure_private_key 'sudo salt-call --local state.highstate'
	@ssh vagrant@localhost -p 2222 -i ~/.vagrant.d/insecure_private_key 'cd /var/www/snipt; make db'
	@ssh vagrant@localhost -p 2222 -i ~/.vagrant.d/insecure_private_key 'cd /var/www/snipt; /var/www/.virtualenvs/snipt/bin/python manage.py syncdb'
	@ssh vagrant@localhost -p 2222 -i ~/.vagrant.d/insecure_private_key 'cd /var/www/snipt; /var/www/.virtualenvs/snipt/bin/python manage.py migrate'
	@ssh vagrant@localhost -p 2222 -i ~/.vagrant.d/insecure_private_key 'cd /var/www/snipt; /var/www/.virtualenvs/snipt/bin/python manage.py backfill_api_keys'

.PHONY: assets, \
				db, \
				deploy, \
				deploy-heroku, \
				salt-vagrant, \
				vagrant
