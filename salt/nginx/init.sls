nginx-extras:
  pkg:
    - installed

nginx:
  service:
    - running
    - enable: True
    - require:
      - pkg: nginx-extras
    - watch:
      - file: /etc/nginx/nginx.conf
      - file: /etc/nginx/sites-enabled/*

/etc/nginx/sites-available:
  file.directory:
    - mode: 755
    - require:
      - pkg: nginx-extras

/etc/nginx/sites-enabled:
  file.directory:
    - mode: 755
    - require:
      - pkg: nginx-extras

{% if pillar.env_name != 'vagrant' %}

/etc/certs:
  file.directory:
    - mode: 644
    - require:
      - pkg: nginx-extras

{% endif %}

/etc/nginx/nginx.conf:
  file.managed:
    - source: salt://nginx/nginx.conf
    - mode: 400
    - template: jinja
    - require:
      - pkg: nginx-extras
        
/etc/nginx/sites-enabled/default:
  file.absent
