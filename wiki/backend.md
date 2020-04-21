---
sidebar: auto
---

# Backend

## Backend role

Backend is responsible for:  
- Authorization  
- Separating accounts rights
- Providing CRUD for accounts, companies, products, orders, etc.

## Technologies

**Languages**  
Python 3.6

**Databases**  
PostgreSQL  
Redis

**Base frameworks**  
Flask

**RESTful**  
flask-restplus

**Database libs**  
flask-sqlalchemy  
sqlalchemy-filters

**Debug&Profiling**  
ProfilerMiddleware(Flask/Werkzeug default)

## Architecture

### Entry point
App lifecycle starts with `app.py`. There is an import of app factory ([docs](http://flask.pocoo.org/docs/1.0/patterns/appfactories/)). Then we are getting the name of the configuration from env and creating an app with that configuration name. 

### Parts
All application parts that related to the working code are stored in src.  
**`commands`** - custom commands, that integrated into Flask. F.e. flask create:account.  
**`endpoints`** - all application endpoints are here. Flask-restplus is used for API, so, this part consists of namespaces for simple navigation, beautiful swagger docs, and a good understanding of API structure.  
**`layers`** - (DEPRECATED!!!) was created as part of policies system, but replaced with validators due to time consuming development.  
**`models`** - SQLAlchemy models. All models are imported in `__init__.py` for simplified usage.  
**`plugins`** - all flask additional libraries inits are here, also attach(app) function in `__init__.py` for centralized attaching of inited libraries.  
**`policies`** - (DEPRECATED!!!) another try to create policies system, replaced with validators  
**`reports`** - reporting system (supporting web and csv formats)  
**`seeders`** - seeding database with test data  
**`serializers`** - part of `flask-restplus` library, defining fields with parameters for accepting data from endpoints and (de)serializing models  
**`tasks`** - background Celery tasks (only setup, not used yet)  
**`validators`** - validating data before going to controller


### Specifics

**Endpoints**  
Endpoints are separated on namespaces. All endpoints are automatically documented with `flask-restplus`. Namespaces also separated in swagger docs.  
**Serializers**  
Serializing models are containing flask-restplus models for correct handling/validating API requests and marshalling.
There can be several models, depends on request types and access rights.
All models must be registered in one of namespaces.
Also here is a standard mask for fields, that can be changed in `X-Fields` header in request.  
**Models**  
Python supports multiple inheritance, so, mixins are used in this setup (`mixins` folder in `models`)

## API

### General

For now there is only JSON RESTful API. Some parts are implemented separately (not following REST) to support additional functionality.
API separated on 5 parts: Catalog, Minor, Orders, Organization, Reports, Storefront.
Available actions/info vary depending on roles. 

**Organization**: part that responsible for actions related to people management. Getting and modifying accounts, companies, campaings, relations private data. Most of methods are require token.  
**Catalog**: methods, related to products management (attributes, types, variants, etc.)  
**Orders**: orders management (notes and events included)

### Marshalling

There are multiple marshalling models for working with flask-restplus.
One database model has multiple marshalling models for different types of request (creation, updating, getting).
All endpoints, that returns model, has X-Fields header as parameter, that allows to add or filter model fields.

### Relations

All parent models must include childs as field, but don't include that by default in mask.
In one-to-one relations child can be included by default, depends on the situation.
Many-to-many relations are absent by default, they must be enabled manualy with X-Fields mask.
Child can't include parent model due to recursion. But parent id must be included.

### Filtering

All endpoints, that returns a list of models, must to support filtering.
By default it's sqlalchemy-filters, easy to apply and highly customizable.

## Style Guide

- Python annotations are used where it possible, especially in `modules`  
  ```python
    def generate_hash(row:str) -> str:
        conf = configs[str(os.environ.get('FLASK_ENV'))]
        return hashlib.sha256(
            (row+str(conf['SECRET'])).encode('utf-8')
        ).hexdigest()
  ```
- Any custom logic must be implemented in modules folder  
- A functional approach is preferred. Classes are used if necessary (models, extending plugins with inheritance, etc.)  
- Comments. Comments everywhere  
- Single quote for strings  
  ```python
  # Nope
  a = "asd"
  
  # Yes
  a = 'asd'
  ```
- The order of decorators should correspond to the order of request processing (security -> receiving -> processing -> response). Only custom decorators are allowed to be placed in needed places (such as authorization)  
  ```python
    # Bad
    @require_level(2)
    @organization.doc(security='apiKey')
    @organization.marshal_with(models.Account.model_get_private)
    @organization.response(200, 'Account model list')
    @organization.response(401, 'Not authorized')
    @organization.response(403, 'Not permitted')
    @require_token
    def get(self):
        # ...
    
    # Good
    @organization.doc(security='apiKey')
    @organization.response(200, 'Account model list')
    @organization.response(401, 'Not authorized')
    @organization.response(403, 'Not permitted')
    @organization.marshal_with(models.Account.model_get_private)
    @require_token
    @require_level(2)
    def get(self):
        # ...
  ```


## Debugging & Profiling
Debug mode is already enabled in local `development` environment (see `conf.py`).  
To enable Flask profiling, change conf `'PROFILE': False` to `True`. After each API request, there will be cProfile output in terminal about request.
:::danger
**DANGER!**
Enabled profiling may cause performance problems. (x2-3 slower)
:::
