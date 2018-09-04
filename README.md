# gae_slackbot

```
pip install flask
pip freeze > requirements.txt

gcloud app deploy
gcloud app deploy -v [vername]
gcloud app deploy -v att-seq2seq
```

```:app.yaml
runtime: python
env: flex
service: slackbot
entrypoint: python main.py

runtime_config:
  python_version: 3

env_variables:
  API_TOKEN: 'YOUR_API_TOKEN'

resources:
  cpu: 2
  memory_gb: 2.3

manual_scaling:
  instances: 1
```

standard環境では，app.yamlで，library sslが必要だったが，flexible環境では不要

