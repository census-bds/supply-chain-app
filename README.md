Using the django app for supply chain database models 

-- make sure you install this app under your django project settings -- by default this app is called as 'scip' 

# data migration scripts
exists in `scip/management` folder 

# api & swagger docs
REST API using `djangorestframework` library 

endpoint queries are defined in `views.py` and tied to endpoint urls in `scip/urls.py`

access API endpoints at `/api`
access swagger docs at `/api-docs` 

