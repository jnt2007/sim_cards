from django.shortcuts import render, redirect
from sim_page.models import SimCard
from sim_page.tasks import check_balance


# from django.views.decorators.cache import cache_page

# Create your views here.


# @cache_page(60 * 5)
def power_master(request, errors=None):
    sims_power_master = SimCard.objects.order_by('appointment').filter(owner_id='1')
    context = {
        'sim_cards': sims_power_master,
        'errors': errors,
    }
    return render(request, u'sim_page/PowerMaster.html', context)


def power_manage(request, errors=None):
    sims_power_manage = SimCard.objects.order_by('sim_number').filter(owner_id='2')
    context = {
        'sim_cards': sims_power_manage,
        'errors': errors,
    }
    return render(request, u'sim_page/PowerManage.html', context)


def alpha(request, errors=None):
    sims_alpha = SimCard.objects.order_by('sim_number').filter(owner_id='4')
    context = {
        'sim_cards': sims_alpha,
        'errors': errors,
    }
    return render(request, u'sim_page/Alpha.html', context)


def dev(request, errors=None):
    sims_dev = SimCard.objects.order_by('sim_number').filter(owner_id='3')
    context = {
        'sim_cards': sims_dev,
        'errors': errors,
    }
    return render(request, u'sim_page/Dev.html', context)


def save_info(request):
    errors = []
    if request.method == 'POST':
        if not request.POST.get('appointment', ''):
            errors.append('Appointment field shoudn`t be empty')
        if not request.POST.get('comment', ''):
            errors.append('Comment field shoudn`t be empty')
        if not errors:
            SimCard.objects.filter(id=request.GET['sim_id']). \
                update(appointment=u'{}'.format((request.POST.get('appointment', ))))
            SimCard.objects.filter(id=request.GET['sim_id']). \
                update(comment=u'{}'.format((request.POST.get('comment', ))))

    if int(request.GET['owner_id']) == 1:
        return power_master(request=request, errors=errors)
    elif request.GET['owner_id'] == u'2':
        return power_manage(request=request, errors=errors)
    elif request.GET['owner_id'] == u'3':
        return dev(request=request, errors=errors)
    elif request.GET['owner_id'] == u'4':
        return alpha(request=request, errors=errors)


def schedule_balance_renewal(request):
    sim_card_id = int(request.GET['sim_id'])

    if not sim_card_id:
        return 'error, sim id is empty'

    sim_card = SimCard.objects.get(id=sim_card_id)
    if not sim_card:
        return 'error, sim card with this id not found'

    if sim_card.balance_renewal_in_progress:
        return 'updating balance for this sim in progress'

    check_balance.delay(sim_card_id)

    sim_card.balance_renewal_in_progress = True

    sim_card.save()

    if int(request.GET['owner_id']) == 1:
        return redirect('/pmaster/')
    elif request.GET['owner_id'] == u'2':
        return redirect('/pmanage/')
    elif request.GET['owner_id'] == u'3':
        return redirect('/dev/')
    elif request.GET['owner_id'] == u'4':
        return redirect('/alpha/')
