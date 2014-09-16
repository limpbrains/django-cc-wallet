from time import sleep

from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, FormView
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404

from django import forms
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse, reverse_lazy

from wallet.models import ProxyWallet
from cc.models import Wallet
from cc.tasks import process_withdraw_transacions


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)


class Wallets(LoginRequiredMixin, ListView):
    template_name = 'wallet/list.html'

    def get_queryset(self):
        return ProxyWallet.objects.filter(user=self.request.user)

wallets = Wallets.as_view()


class CreateWallet(LoginRequiredMixin, CreateView):
    model = Wallet
    fields = ['currency', 'label']
    template_name = 'wallet/create.html'
    success_url = reverse_lazy('wallet_list')

    def form_valid(self, form):
        response = super(CreateWallet, self).form_valid(form)
        ProxyWallet.objects.create(
            user=self.request.user,
            wallet=self.object
        )
        return response

create = CreateWallet.as_view()


class WalletDetail(LoginRequiredMixin, DetailView):
    model = ProxyWallet
    template_name = 'wallet/detail.html'

    def get_queryset(self):
        qs = super(WalletDetail, self).get_queryset()
        return qs.filter(user=self.request.user)

detail = WalletDetail.as_view()


class Withdraw(LoginRequiredMixin, FormView):
    template_name = 'wallet/withdraw.html'

    def get_form_class(self):
        class WithdrawForm(forms.Form):
            address = forms.CharField()
            amount = forms.DecimalField()
            execute = forms.BooleanField(required=False)

        return WithdrawForm

    def form_valid(self, form):
        px = get_object_or_404(ProxyWallet, user=self.request.user, **self.kwargs)
        self.px = px
        try:
            px.wallet.withdraw(form.cleaned_data['address'], form.cleaned_data['amount'])
        except ValueError, e:
            form.add_error(None, e)
            return self.form_invalid(form)

        if form.cleaned_data['execute']:
            process_withdraw_transacions.delay(ticker=px.wallet.currency.ticker)
            sleep(0.2)

        return super(Withdraw, self).form_valid(form)

    def get_success_url(self):
        return reverse('wallet_detail', kwargs={'pk': self.px.pk})

withdraw = Withdraw.as_view()
