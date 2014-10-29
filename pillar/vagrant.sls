env_name: vagrant
hostname: local.snipt.net
deploy_user: vagrant

users:
  -
    name: vagrant
    groups:
      - deploy
      - wheel

ssh:
    port: 22
