from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class TransporteurRequisMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        entreprise = getattr(self.request.user, 'entreprise', None)
        return entreprise is not None and entreprise.type_entreprise == 'transporteur'

class ChargeurRequisMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        entreprise = getattr(self.request.user, 'entreprise', None)
        return entreprise is not None and entreprise.type_entreprise == 'chargeur'
