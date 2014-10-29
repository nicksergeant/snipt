fish:
  pkgrepo.managed:
    - ppa: fish-shell/release-2
    - require_in:
      - pkg: fish
  pkg.latest:
    - name: fish
    - refresh: True

/etc/z.fish:
  file.managed:
    - source: salt://fish/z.fish
    - mode: 755

{% for user in pillar.users %}

fish-{{ user.name }}:
  file.managed:
    - name: /home/{{ user.name }}/.config/fish/config.fish
    - user: {{ user.name }}
    - source: salt://fish/config.fish
    - makedirs: True
    - require:
      - user: {{ user.name }}

fish-{{ user.name }}-virtualenv:
  file.managed:
    - name: /home/{{ user.name }}/.config/fish/virtualenv.fish
    - user: {{ user.name }}
    - source: salt://fish/virtualenv.fish
    - makedirs: True
    - require:
      - user: {{ user.name }}

{% endfor %}
