from django.test import TestCase
from .income_classifier.random_forest import RFClassifier
import inspect
from .registry import Register
from rest_framework.test import APIClient


class MLTests(TestCase):

    def test_predict_view(self):
        client = APIClient()
        input_data = {
            "age": 37,
            "workclass": "Private",
            "fnlwgt": 34146,
            "education": "HS-grad",
            "education-num": 9,
            "marital-status": "Married-civ-spouse",
            "occupation": "Craft-repair",
            "relationship": "Husband",
            "race": "White",
            "sex": "Male",
            "capital-gain": 0,
            "capital-loss": 0,
            "hours-per-week": 68,
            "native-country": "United-States"
        }
        classifier_url = "/api/v1/income_classifier/predict"
        response = client.post(classifier_url, input_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["label"], "<=50K")
        self.assertTrue("request_id" in response.data)
        self.assertTrue("status" in response.data)

    def test_rf_algorithm(self):
        input_data = {
            "age": 37,
            "workclass": "Private",
            "fnlwgt": 34146,
            "education": "HS-grad",
            "education-num": 9,
            "marital-status": "Married-civ-spouse",
            "occupation": "Craft-repair",
            "relationship": "Husband",
            "race": "White",
            "sex": "Male",
            "capital-gain": 0,
            "capital-loss": 0,
            "hours-per-week": 68,
            "native-country": "United-States"
        }
        my_alg = RFClassifier()
        response = my_alg.predict(input_data)
        self.assertEqual('OK', response['status'])
        self.assertTrue('label' in response)
        self.assertEqual('<=50K', response['label'])

    def test_registry(self):
        registry = Register()
        self.assertEqual(len(registry.endpoints), 0)
        endpoint_name = "income_classifier"
        algorithm_object = RFClassifier()
        algorithm_name = "random forest"
        status = "production"
        version = "0.0.1"
        owner = "Karan"
        description = "Random Forest with simple pre- and post-processing"
        code = inspect.getsource(RFClassifier)
        # add to registry
        registry.add_algorithm(endpoint_name, algorithm_object, algorithm_name, status, version, owner,
                 description, code)
        # there should be one endpoint available
        self.assertEqual(len(registry.endpoints), 1)