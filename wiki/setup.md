
# Setup

## Local
- Build the project: `docker-compose -f docker-compose-local.yaml up -d --build`  
::: tip
After each build, all data will be erased and automatically generated again with seeding.
:::

## Dev
- Build the project: `docker-compose -f docker-compose-dev.yaml up -d --build`  
:::warning
After each commit, all data will be erased and automatically generated again with seeding.
:::

## Stage
- Build the project: `docker-compose -f docker-compose-stage.yaml up -d --build`
- Create default admin: `docker-compose -f docker-compose-stage.yaml exec api flask create:account -u admin -p admin`  
:::tip
After each start `flask migrate` will be called automatically
:::

## New environment
- Init new start script for API (f.e. `cp api/scripts/start-stage.sh api/scripts/start-prod.sh`)  
- Init new docker-compose file (f.e. `cp docker-compose-stage.yaml docker-compose-prod.yaml`)  
- Rename containers to fit environment
- Set `command` for api in docker-compose (f.e. `bash scripts/start-prod.sh`)  
- Set new `FLASK_ENV` value in docker-compose file (f.e. `production`)  
- Create new config for environment in `api/conf.py` wuth the same name, as value of FLASK_ENV. F.e.
  ```python
  configs.production = deepcopy(configs.stage)
  ```
- Create new .env file for frontend with the name of environment (f.e. `cp frontend/.env.stage frontend/.env.prod`)  
- Set `API_BASE_URL` in the new environment file
- Create new script in `package.json` for starting frontend  
  ```
  "prod": "cp .env.prod .env && webpack-dev-server --inline --progress --hot --host 0.0.0.0 --port 60602 --config build/webpack.dev.conf.js"
  ```
- Set `command` for web in docker-compose (f.e. `npm run prod`)

Default ports (from stage):
| Port | Instance |
| --- | --- |
| 60799 | PostgreSQL (recommended to hide) |
| 60700 | Wiki |
| 60701 | API |
| 60702 | Web |
