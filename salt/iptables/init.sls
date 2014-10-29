/etc/iptables.up.rules:
  file.managed:
    - source: salt://iptables/iptables.up.rules
    - template: jinja
    - require:
      - pkg: iptables

flush-iptables:
  cmd.run:
    - names:
      - /sbin/iptables -F
      - /sbin/iptables-restore < /etc/iptables.up.rules
    - watch:
      - file: /etc/iptables.up.rules
    - require:
      - pkg: iptables

/etc/network/if-pre-up.d/iptables:
  file.managed:
    - mode: 644
    - source: salt://iptables/iptables-restore.sh
    - require:
      - pkg: iptables
  cmd.run:
    - name: chmod +x /etc/network/if-pre-up.d/iptables
    - require:
      - pkg: iptables
