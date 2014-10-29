deploy-group:
  group.present:
    - name: deploy

wheel-group:
  group.present:
    - name: wheel

{% for user in pillar.users %}

{{ user.name }}:
  user.present:
    - name: {{ user.name }}
    - home: /home/{{ user.name }}
    - groups: {{ user.groups }}
    - require:
      {% for group in user.groups %}
      - group: {{ group }}
      {% endfor %}
      - pkg: fish
    - shell: /usr/bin/fish
  ssh_auth.present:
    - user: {{ user.name }}
    {% if user.name != 'vagrant' and user.name != 'deploy' %}
    - source: salt://users/{{ user.name }}.pub
    {% endif %}
    - makedirs: True

{% endfor %}

{% if pillar.env_name != 'vagrant' %}

deploy-authorized-keys:
  file.managed:
    - name: /home/deploy/.ssh/authorized_keys
    - user: deploy
    - group: deploy
    - mode: 600
    - source: salt://users/deploy.authorized_keys
    - makedirs: True
    - require:
      - user: deploy

deploy-known-hosts:
  file.managed:
    - name: /home/deploy/.ssh/known_hosts
    - user: deploy
    - group: deploy
    - mode: 700
    - source: salt://users/known_hosts
    - makedirs: True

{% endif %}

/etc/sudoers:
  file.managed:
    - source: salt://users/sudoers
    - mode: 440
