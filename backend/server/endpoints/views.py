from django.shortcuts import render
from rest_framework import viewsets, exceptions
from .serializers import *
import json
import datetime
from django.db.models import F
from numpy.random import rand
from rest_framework import views, status
from rest_framework.response import Response
from ml.registry import Register
from server.wsgi import registry


class PredictView(views.APIView):
    def post(self, request, endpoint_name, format=None):
        print(request)
        algorithm_status = self.request.query_params.get("status", "production")
        algorithm_version = self.request.query_params.get("version")

        algs = MLAlgorithm.objects.filter(parent_endpoint__name=endpoint_name, status__status=algorithm_status, status__active=True)

        if algorithm_version is not None:
            algs = algs.filter(version = algorithm_version)

        if len(algs) == 0:
            return Response(
                {"status": "Error", "message": "ML algorithm is not available"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if len(algs) != 1 and algorithm_status != "ab_testing":
            return Response(
                {"status": "Error", "message": "ML algorithm selection is ambiguous. Please specify algorithm version."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        alg_index = 0
        if algorithm_status == "ab_testing":
            alg_index = 0 if rand() < 0.5 else 1

        print(registry.endpoints)
        for i in range(len(algs)):
            print(algs[i].id)
        algorithm_object = registry.endpoints[algs[alg_index].id]
        prediction = algorithm_object.predict(request.data)

        label = prediction["label"] if "label" in prediction else "error"
        ml_request = MLRequest(
            input_data=json.dumps(request.data),
            full_response=prediction,
            response=label,
            feedback="",
            parent_mlalgorithm=algs[alg_index],
        )
        ml_request.save()

        prediction["request_id"] = ml_request.id

        return Response(prediction)


class EndpointView(viewsets.ModelViewSet):
    serializer_class = EndpointSerializer
    queryset = Endpoint.objects.order_by('-created_at')
    #ordering_fields = ['created_at']


class MLAlgorithmView(viewsets.ModelViewSet):
    serializer_class = MLAlgorithmSerializer
    queryset = MLAlgorithm.objects.order_by('-created_at')
    #


class MLAlgorithmStatusView(viewsets.ModelViewSet):
    serializer_class = MLAlgorithmStatusSerializer
    queryset = MLAlgorithmStatus.objects.order_by('-created_at')
    #ordering_fields = ['created_at']

    def deactivate_other_statuses(self, instance):
        old_statuses = MLAlgorithmStatus.objects.filter(parent_mlalgorithm=instance.parent_mlalgorithm,
                                                        created_at__lt=instance.created_at,
                                                        active=True)
        for i in range(len(old_statuses)):
            old_statuses[i].active = False
        MLAlgorithmStatus.objects.bulk_update(old_statuses, ["active"])

    def perform_create(self, serializer):
        try:
            instance = serializer.save(active=True)
            # set active=False for other statuses
            self.deactivate_other_statuses(instance)

        except Exception as e:
            raise exceptions.APIException(str(e))


class MLRequestView(viewsets.ModelViewSet):
    serializer_class = MLRequestSerializer
    queryset = MLRequest.objects.order_by('-created_at')
    #ordering_fields = ['created_at']


class ABTestView(viewsets.ModelViewSet):
    serializer_class = ABTestSerializer
    queryset = ABTest.objects.all()

    def perform_create(self, serializer):
        instance = serializer.save()

        status_1 = MLAlgorithmStatus(parent_mlalgorithm=instance.parent_mlalgorithm_1,
                                     status="ab_testing", created_by=instance.created_by,
                                     active=True)
        status_1.save()
        status_2 = MLAlgorithmStatus(parent_mlalgorithm=instance.parent_mlalgorithm_2,
                                     status="ab_testing", created_by=instance.created_by,
                                     active=True)
        status_2.save()
        status_1.deactivate_other_statuses()
        status_2.deactivate_other_statuses()


class StopABTestView(views.APIView):
    def post(self, request, ab_test_id, format=None):

        try:
            ab_test = ABTest.objects.get(pk=ab_test_id)

            if ab_test.ended_at is not None:
                return Response({"message": "AB Test already finished."})

            date_now = datetime.datetime.now()
            # alg #1 accuracy
            all_responses_1 = MLRequest.objects.filter(parent_mlalgorithm=ab_test.parent_mlalgorithm_1, created_at__gt = ab_test.created_at, created_at__lt = date_now).count()
            correct_responses_1 = MLRequest.objects.filter(parent_mlalgorithm=ab_test.parent_mlalgorithm_1, created_at__gt = ab_test.created_at, created_at__lt = date_now, response=F('feedback')).count()
            accuracy_1 = correct_responses_1 / float(all_responses_1)
            print(all_responses_1, correct_responses_1, accuracy_1)

            # alg #2 accuracy
            all_responses_2 = MLRequest.objects.filter(parent_mlalgorithm=ab_test.parent_mlalgorithm_2, created_at__gt = ab_test.created_at, created_at__lt = date_now).count()
            correct_responses_2 = MLRequest.objects.filter(parent_mlalgorithm=ab_test.parent_mlalgorithm_2, created_at__gt = ab_test.created_at, created_at__lt = date_now, response=F('feedback')).count()
            accuracy_2 = correct_responses_2 / float(all_responses_2)
            print(all_responses_2, correct_responses_2, accuracy_2)

            # select algorithm with higher accuracy
            alg_id_1, alg_id_2 = ab_test.parent_mlalgorithm_1, ab_test.parent_mlalgorithm_2
            # swap
            if accuracy_1 < accuracy_2:
                alg_id_1, alg_id_2 = alg_id_2, alg_id_1

            status_1 = MLAlgorithmStatus(status = "production",
                            created_by=ab_test.created_by,
                            parent_mlalgorithm = alg_id_1,
                            active=True)
            status_1.save()
            status_1.deactivate_other_statuses()
            # update status for second algorithm
            status_2 = MLAlgorithmStatus(status = "testing",
                            created_by=ab_test.created_by,
                            parent_mlalgorithm = alg_id_2,
                            active=True)
            status_2.save()
            status_2.deactivate_other_statuses()


            summary = "Algorithm #1 accuracy: {}, Algorithm #2 accuracy: {}".format(accuracy_1, accuracy_2)
            ab_test.ended_at = date_now
            ab_test.summary = summary
            ab_test.save()

        except Exception as e:
            return Response({"status": "Error", "message": str(e)},
                            status=status.HTTP_400_BAD_REQUEST
            )
        return Response({"message": "AB Test finished.", "summary": summary})