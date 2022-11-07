"""
WSGI config for sc project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

'''
# Uncomment this and comment out the rest of the file when getting:
#    "RuntimeError: populate() isn't reentrant"
import os
def application(environ, start_response):
    if environ['mod_wsgi.process_group'] != '':
        import signal
        os.kill(os.getpid(), signal.SIGINT)
    return ["killed"]
'''

# imports
import os
import sys
import site
import six

# declare variables
django_project_name = ""
path_to_django_project_parent = ""
virtualenv_python3 = ""
python_3_version = ""
temp_path = None

# declare variables - anaconda
anaconda_base_bin_path = ""
conda_env_home_path = None
conda_env_activate_command = None
activate_code = None

# configure
anaconda_base_bin_path = "/apps/user/dich0001/miniconda3/bin"
django_project_name = "sc"
conda_env_folder_path = "/apps/user/dich0001/django/sc"
path_to_django_project_parent = "/apps/user/dich0001/django/sc"
conda_env_python3 = "conda_env"
python_3_version = "3.8"
conda_env_home_path = "{}/{}".format( conda_env_folder_path, conda_env_python3 )

# Add the app's directory to the PYTHONPATH
temp_path = "{}/{}".format( path_to_django_project_parent, django_project_name )
sys.path.append( temp_path )

# Set DJANGO_SETTINGS_MODULE
os.environ.setdefault( "DJANGO_SETTINGS_MODULE", "{}.settings".format( django_project_name ) )

# Activate your virtualenv - only support Python 3.

# Add the site-packages of the desired virtualenv
temp_path = conda_env_home_path + "/lib/python" + python_3_version + "/site-packages"
site.addsitedir( temp_path )

# Activate your conda env?
# command:
#conda_env_activate_command = "source {}/activate {}".format( anaconda_base_bin_path, conda_env_home_path )

# compile code
#activate_code = compile( conda_env_activate_command, "anaconda_doc", 'exec')

# run the code
#exec( activate_code, dict( __file__ = activate_this ) )

# import django stuff - it is installed in your virtualenv, so you must import
#     after activating virtualenv.
from django.core.wsgi import get_wsgi_application

# load django application
application = get_wsgi_application()
