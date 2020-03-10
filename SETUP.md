1) Copy `.env.yaml.example` to `.env.yaml`
2) Generate key
3) Run `gcloud functions deploy hello_flask --runtime python37 --trigger-http --allow-unauthenticated --env-vars-file .env.yaml`