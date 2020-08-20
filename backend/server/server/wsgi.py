"""
WSGI config for server project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
application = get_wsgi_application()
import inspect
from ml.registry import Register
from ml.income_classifier.random_forest import RFClassifier
from ml.income_classifier.irandom_forest import RFClassifier as RFC

try:
    registry = Register() # create ML registry
    # Random Forest classifier
    rf = RFClassifier()
    # add to ML registry
    registry.add_algorithm(endpoint_name="income_classifier",
                            algorithm_object=rf,
                            algorithm_name="random forest",
                            status="production",
                            version="0.0.1",
                            owner="Karan",
                            description="Random Forest with simple pre- and post-processing",
                            code=inspect.getsource(RFClassifier))

    rfi = RFC()
    registry.add_algorithm(endpoint_name="income_classifier",
                            algorithm_object=rfi,
                            algorithm_name="random forest",
                            status="production",
                            version="0.0.2",
                            owner="Karan",
                            description="Random Forest with simple pre- and post-processing",
                            code=inspect.getsource(RFC))

except Exception as e:
    print("Exception while loading the algorithms to the registry,", str(e))