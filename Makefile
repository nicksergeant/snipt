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
	@cat media/js/src/jobs.js > media/js/src/jobs.min.js
	@cat media/js/src/application.js > media/js/src/application.min.js
	@cat media/js/src/team.js > media/js/src/team.min.js
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
		media/js/src/jobs.min.js \
		media/js/src/team.min.js \
		media/js/libs/codemirror.js \
		media/js/libs/highlight.js \
		> media/js/snipt-all.min.js
	@cat media/js/libs/highlight.js \
		media/js/src/pro.js \
		> media/js/pro-all.min.js

deploy:
	git push heroku heroku:master

sass:
	sass --sourcemap=none --watch -t compressed --scss media/css/style.scss:media/css/style.css

.PHONY: deploy sass
