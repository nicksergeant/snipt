nginx:
  pkg:
    - installed
  service:
    - running
    - enable: True
    - watch:
      - file: /etc/nginx/nginx.conf
      - file: /etc/nginx/sites-enabled/*

/etc/nginx/sites-available:
  file.directory:
    - mode: 755
    - require:
      - pkg: nginx

/etc/nginx/sites-enabled:
  file.directory:
    - mode: 755
    - require:
      - pkg: nginx

/etc/nginx/nginx.conf:
  file.managed:
    - source: salt://nginx/nginx.conf
    - mode: 400
    - template: jinja
    - require:
      - pkg: nginx
        
/etc/nginx/sites-enabled/default:
  file.absent
