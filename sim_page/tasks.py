from __future__ import print_function
from __future__ import absolute_import
from subprocess import Popen, PIPE

from django.utils import timezone
from sim_page.models import SimCard
from sim_page.celeryapp import app
from celery.task import periodic_task
from celery.schedules import crontab


@app.task(time_limit=240)
def check_balance(sim_card_id):
    sim_card = SimCard.objects.get(id=sim_card_id)

    try:
        call = Popen(['python', '/home/celery/_ChkSIM_one.py', '{}'.format(int(sim_card_id))],
                     stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = call.communicate()

    except:
        print('Communication error')

    try:
        output = float(output)

    except ValueError:
        sim_card.balance_renewal_in_progress = False
        sim_card.save()

        print('Undefined data received for {0}: {1}'.format(sim_card.name, output))

        return output

    if isinstance(output, float):
        sim_card.balance = output
        sim_card.last_update = timezone.now()

        print("Sim {0} with number {1} balance {2} successfully updated".format(sim_card.sim_number, sim_card.name,
                                                                                sim_card.balance))

    sim_card.balance_renewal_in_progress = False
    sim_card.save()

    print('Task finished')

    return str(sim_card.sim_number), str(sim_card.name), str(output)


def update_group(all_id):

    for sim in all_id:
        check_balance(sim.id)


@periodic_task(run_every=crontab(minute=0, hour=4))
def update_all_integration():
    all_id = SimCard.objects.filter(owner_id='3')

    update_group(all_id)

    return len(all_id)


@periodic_task(run_every=crontab(minute=0, hour=5))
def update_all_alpha():
    all_id = SimCard.objects.filter(owner_id='4')

    update_group(all_id)

    return len(all_id)


@periodic_task(run_every=crontab(minute=0, hour=8))
def update_all_power_manage():
    all_id = SimCard.objects.filter(owner_id='2')

    update_group(all_id)

    return len(all_id)


@periodic_task(run_every=crontab(minute=0, hour=6))
def update_all_power_master():
    all_id = SimCard.objects.filter(owner_id='1')

    update_group(all_id)

    return len(all_id)
