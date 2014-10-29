env_name: production
hostname: snipt.net
deploy_user: deploy

users:
  -
    name: deploy
    groups:
      - deploy
      - wheel
  -
    name: nick
    groups:
      - deploy
      - wheel

ssh:
    port: 55555
