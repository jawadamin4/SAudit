from django.db import models
from audit_universe.models import AuditUniverse
from risk_assessment_setup.models import RiskOwner, TypeOfRisk, ResponseStrategy, TypeOfControl, ControlFrequency, ControlOwner, StrategicImportanceList, Function, MajorProcess, SubProcess

class RiskAssessment(models.Model):
    audit_universe = models.ForeignKey(AuditUniverse, on_delete=models.SET_NULL, null=True, blank=False)
    company = models.CharField(max_length=100, null=True, blank=False)
    country = models.CharField(max_length=100, null=True, blank=False)
    region = models.CharField(max_length=100, null=True, blank=False)
    city = models.CharField(max_length=100, null=True, blank=False)
    branch = models.CharField(max_length=100, null=True, blank=False)
    division = models.CharField(max_length=100, null=True, blank=False)
    department = models.CharField(max_length=100, null=True, blank=False)
    function = models.ForeignKey(Function, on_delete=models.SET_NULL, null=True, blank=False)
    major_process = models.ForeignKey(MajorProcess, on_delete=models.SET_NULL, null=True, blank=False)
    sub_process = models.ForeignKey(SubProcess, on_delete=models.SET_NULL, null=True, blank=False)
    risk_details = models.TextField(null=True, blank=False)
    risk_owner = models.ForeignKey(RiskOwner, on_delete=models.SET_NULL, null=True, blank=True)
    type_of_risk = models.ManyToManyField(TypeOfRisk, null=True, blank=True)
    impact = models.CharField(max_length=100, null=True, blank=False,
                              choices=[('Very Low', 'Very Low'), ('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High'),
                                       ('Critical', 'Critical')])
    likelihood = models.CharField(max_length=100, null=True, blank=False,
                                  choices=[('Rare', 'Rare'), ('Unlikely', 'Unlikely'), ('Likely', 'Likely'),
                                           ('Possible', 'Possible'), ('Certain', 'Certain')])
    risk_score = models.CharField(max_length=100, null=True, blank=True)
    overall_inherent_risk_rating = models.CharField(max_length=100, null=True, blank=True)
    response_strategy = models.ForeignKey(ResponseStrategy, on_delete=models.SET_NULL, null=True, blank=True)
    response_action = models.TextField(null=True, blank=True)
    type_of_control = models.ForeignKey(TypeOfControl, on_delete=models.SET_NULL, null=True, blank=True)
    control_frequency = models.ForeignKey(ControlFrequency, on_delete=models.SET_NULL, null=True, blank=True)
    control_owner = models.ForeignKey(ControlOwner, on_delete=models.SET_NULL, null=True, blank=True)
    control_design = models.CharField(max_length=100, null=True, blank=True, choices=[('Very Strong', 'Very Strong'), ('Strong', 'Strong'), ('Medium', 'Medium'), ('Weak', 'Weak'), ('Very Weak', 'Very Weak')])
    effectiveness = models.CharField(max_length=100, null=True, blank=True, choices=[('Highly Effective', 'Highly Effective'), ('Effective', 'Effective'), ('Moderately Effective', 'Moderately Effective'), ('Partially Effective', 'Partially Effective'), ('Ineffective', 'Ineffective')])
    control_score = models.CharField(max_length=100, null=True, blank=True)
    overall_control_rating = models.CharField(max_length=100, null=True, blank=True)
    residual_score_total = models.CharField(max_length=100, null=True, blank=True)
    residual_score = models.IntegerField(default=0, null=True, blank=True)
    residual_risk_rating = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.company = self.audit_universe.company
        self.country = self.audit_universe.country
        self.region = self.audit_universe.region
        self.city = self.audit_universe.city
        self.branch = self.audit_universe.branch
        self.division = self.audit_universe.division
        self.department = self.audit_universe.department
        likelihood_values = {'Very Low': 1, 'Low': 2, 'Medium': 3, 'High': 4, 'Critical': 5}
        likelihood_value = likelihood_values.get(self.likelihood, 0)
        impact_values = {'Rare': 1, 'Unlikely': 2, 'Likely': 3, 'Possible': 4, 'Certain': 5}
        impact_value = impact_values.get(self.impact, 0)
        risk_score = likelihood_value + impact_value
        self.risk_score = str(risk_score)
        if risk_score == 0:
            self.overall_inherent_risk_rating = 'None'
        elif risk_score <= 3:
            self.overall_inherent_risk_rating = 'Low'
        elif risk_score <= 6:
            self.overall_inherent_risk_rating = 'Medium'
        else:
            self.overall_inherent_risk_rating = 'High'
        control_design_values = {'Very Weak': 1, 'Weak': 2, 'Medium': 3, 'Strong': 4, 'Very Strong': 5}
        effectiveness_values = {'Ineffective': 1, 'Partially Effective': 2, 'Moderately Effective': 3, 'Effective': 4, 'Highly Effective': 5}
        control_design_value = control_design_values.get(self.control_design, 0)
        effectiveness_value = effectiveness_values.get(self.effectiveness, 0)
        control_score = control_design_value + effectiveness_value
        self.control_score = str(control_score)
        if control_score == 0:
            self.overall_control_rating = 'None'
        elif control_score <= 3:
            self.overall_control_rating = 'Low'
        elif control_score <= 6:
            self.overall_control_rating = 'Medium'
        else:
            self.overall_control_rating = 'High'
        residual_score = risk_score - control_score
        self.residual_score = str(residual_score)
        if risk_score == 0 & control_score == 0:
            self.residual_risk_rating = 'None'
        elif residual_score < 0:
            self.residual_risk_rating = 'Low'
        elif residual_score == 0:
            self.residual_risk_rating = 'Medium'
        else:
            self.residual_risk_rating = 'High'
        self.residual_score_total = 5
        super().save(*args, **kwargs)

    def __str__(self):
        return 'RA{:03d}'.format(self.id)
    
    def __str__(self):
        return f'{self.risk_details}'
    
    class Meta:
        verbose_name = "Risk"
        verbose_name_plural = "Risk"
        unique_together = ('audit_universe', 'function', 'major_process', 'sub_process', 'risk_details')

class StrategicImportance(models.Model):
    audit_universe = models.ForeignKey(AuditUniverse, on_delete=models.SET_NULL, null=True, blank=False)    
    company = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    branch = models.CharField(max_length=100, null=True, blank=True)
    division = models.CharField(max_length=100, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    strategic_importance = models.CharField(max_length=100, null=True, blank=False, choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')])
    strategic_importance_score = models.IntegerField(default=0, null=True, blank=True) # auto
    strategic_objective = models.TextField(max_length=100, null=True, blank=True)
    strategic_importance_in_next_1_to_5_years = models.ManyToManyField(StrategicImportanceList, blank=True)

    def save(self, *args, **kwargs):
        self.company = self.audit_universe.company
        self.country = self.audit_universe.country
        self.region = self.audit_universe.region
        self.city = self.audit_universe.city
        self.branch = self.audit_universe.branch
        self.division = self.audit_universe.division
        self.department = self.audit_universe.department
        if self.strategic_importance == 'Low':
            self.strategic_importance_score = 1
        elif self.strategic_importance == 'Medium':
            self.strategic_importance_score = 2
        elif self.strategic_importance == 'High':
            self.strategic_importance_score = 3
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Strategic Importance"
        verbose_name_plural = "Strategic Importance"
        unique_together = ('audit_universe', 'strategic_objective')