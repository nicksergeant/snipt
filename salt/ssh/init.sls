openssh-server:
  pkg:
    - installed

/etc/ssh/sshd_config:
  file.managed:
    - user: root
    - group: root
    - mode: 644
    - source: salt://ssh/sshd_config
    - template: jinja

ssh:
  service:
    - running
    - watch:
      - file: /etc/ssh/sshd_config
      - file: /etc/network/if-pre-up.d/iptables
    - require:
      - pkg: openssh-server
