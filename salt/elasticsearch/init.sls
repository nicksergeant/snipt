elasticsearch-file:
  file.managed:
    - name: /tmp/elasticsearch-1.3.4.deb
    - source: https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.3.4.deb
    - unless: test -d /usr/local/elasticsearch/bin
    - source_hash: sha1=6a4b6a12825f141245bb581c76052464d17de874

elasticsearch-install:
  cmd:
    - cwd: /tmp
    - names:
      - dpkg -i elasticsearch-1.3.4.deb
    - unless: test -d /usr/local/elasticsearch/bin
    - run
    - require:
      - file: elasticsearch-file

elasticsearch:
  service:
    - running
    - enable: True
    - reload: True
    - require:
      - file: elasticsearch-file
