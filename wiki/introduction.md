
# Introduction

## Contributing

There are 3 main branches on project: master, stage, dev. Every commit to dev is auto-doployed to dev server, as well as stage to stage server and master reserved for production.    

**Once a project is in production the master branch must always be stable. It should always be safe to deploy the master branch to production at any given time.**  
For every ticket(feature) separate branch must be created. Branches may only contain lowercase letters and hyphens. Also, make sure that branch name is prefixed with ticket number.  

## Configs

For now, there are 3 possible setups of project:
- local  
- development (dev server)  
- stage (stage server)  

Every possible setup has separated `docker-compose*.yaml` and `start*.sh`(api) files.  

Each setup has own api config in `conf.py`:
| Setup | Env |
| --- | --- |
| local | development |
| dev | development_server |
| stage | stage |
