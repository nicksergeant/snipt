deploy:
	git push heroku

sass:
	sass --sourcemap=none --watch -t compressed --scss media/css/style.scss:media/css/style.css

.PHONY: deploy sass
