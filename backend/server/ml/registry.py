from .income_classifier.random_forest import RFClassifier
from endpoints.models import *


class Register:

    def __init__(self):
        self.endpoints = {}

    def add_algorithm(self, endpoint_name, algorithm_object, algorithm_name, status, version, owner,
                 description, code):

        endpoint, _ = Endpoint.objects.get_or_create(name=endpoint_name, owner=owner)

        database_object, algo_created = MLAlgorithm.objects.get_or_create(parent_endpoint=endpoint,
                                                                    version=version, code=code,
                                                                    owner=owner, description=description, name=algorithm_name)

        if algo_created:
            status_object, _ = MLAlgorithmStatus.objects.get_or_create(parent_mlalgorithm=database_object,
                                                                       created_by=owner, status=status,
                                                                       active=True)
        self.endpoints[database_object.id] = algorithm_object