python-virtualenv:
  pkg.installed

virtualenvwrapper:
  pip.installed

/var/www:
  file.directory:
    - user: {{ pillar.deploy_user }}
    - group: deploy
    - mode: 775
    - require:
      - user: {{ pillar.deploy_user }}
      - group: deploy

/var/www/.virtualenvs:
  file.directory:
    - user: {{ pillar.deploy_user }}
    - group: deploy
    - mode: 775
    - require:
      - group: deploy

{% if pillar.env_name != 'vagrant' %}

/var/www/snipt:
  file.directory:
    - user: {{ pillar.deploy_user }}
    - group: deploy
    - mode: 775
    - require:
      - group: deploy

  git.latest:
    - name: https://github.com/nicksergeant/snipt.git
    - target: /var/www/snipt
    - user: deploy

{% endif %}

/var/www/.virtualenvs/snipt:
  file.directory:
    - user: {{ pillar.deploy_user }}
    - group: deploy
    - mode: 775
    - require:
      - group: deploy
  virtualenv.managed:
    - system_site_packages: False
    - requirements: /var/www/snipt/requirements.txt

/home/{{ pillar.deploy_user }}/tmp:
  file.absent

/etc/supervisor/conf.d/snipt.conf:
  file.managed:
    - source: salt://application/snipt.supervisor.conf
    - template: jinja
    - makedirs: True
  cmd.run:
    - name: supervisorctl restart snipt

snipt-site:
  file.managed:
    - name: /etc/nginx/sites-available/snipt
    - source: salt://application/snipt.nginx.conf
    - template: jinja
    - group: deploy
    - mode: 755
    - require:
      - pkg: nginx-extras
      - group: deploy

enable-snipt-site:
  file.symlink:
    - name: /etc/nginx/sites-enabled/snipt
    - target: /etc/nginx/sites-available/snipt
    - force: false
    - require:
      - pkg: nginx-extras
  cmd.run:
    - name: service nginx restart
    - require:
      - pkg: nginx-extras
