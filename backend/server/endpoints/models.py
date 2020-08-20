from django.db import models


class Endpoint(models.Model):
    owner = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    name = models.CharField(max_length=120)


class MLAlgorithm(models.Model):
    name = models.CharField(max_length=100, default='')
    code = models.CharField(max_length=1000)
    description = models.CharField(max_length=4000)
    owner = models.CharField(max_length=100)
    parent_endpoint = models.ForeignKey(Endpoint, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    version = models.CharField(max_length=100)


class MLAlgorithmStatus(models.Model):
    status = models.CharField(max_length=100)
    active = models.BooleanField()
    created_by = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    parent_mlalgorithm = models.ForeignKey(MLAlgorithm, related_name='status', on_delete=models.CASCADE)

    def deactivate_other_statuses(self):
        old_statuses = MLAlgorithmStatus.objects.filter(parent_mlalgorithm=self.parent_mlalgorithm,
                                                        created_at__lt=self.created_at,
                                                        active=True)
        for i in range(len(old_statuses)):
            old_statuses[i].active = False
        MLAlgorithmStatus.objects.bulk_update(old_statuses, ["active"])

class MLRequest(models.Model):
    response = models.CharField(max_length=1000)
    feedback = models.CharField(max_length=1000, blank=True, null=True)
    input_data = models.CharField(max_length=1000)
    full_response = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    parent_mlalgorithm = models.ForeignKey(MLAlgorithm, related_name='requests', on_delete=models.CASCADE)


class ABTest(models.Model):
    title = models.CharField(max_length=100)
    created_by = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    summary = models.CharField(max_length=500)
    parent_mlalgorithm_1 = models.ForeignKey(MLAlgorithm, on_delete=models.CASCADE, related_name='parent_mlalgorithm_1')
    parent_mlalgorithm_2 = models.ForeignKey(MLAlgorithm, on_delete=models.CASCADE, related_name='parent_mlalgorithm_2')