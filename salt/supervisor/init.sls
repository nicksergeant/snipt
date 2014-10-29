python-pip:
  pkg.installed

supervisor:
  pip.installed

/etc/supervisord.conf:
  file.managed:
    - source: salt://supervisor/supervisord.conf
    - mode: 755

/etc/init.d/supervisord:
  file.managed:
    - source: salt://supervisor/supervisord.init.d
    - mode: 755

/var/log/supervisor:
  file.directory

/etc/supervisor:
  file.directory

/etc/supervisor/conf.d:
  file.directory

supervisord:
  service.running:
    - require:
      - file: /etc/init.d/supervisord
      - file: /var/log/supervisor
    - watch:
      - file: /etc/supervisord.conf
      - file: /etc/supervisor/conf.d/*
  cmd.run:
    - name: update-rc.d supervisord defaults
