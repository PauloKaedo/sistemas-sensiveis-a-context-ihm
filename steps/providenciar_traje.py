from behave import given, when, then
from futureArmorsBDD import *

@when("existir soldados equipados")
def when_soldados_equipados(context):
    assert context.soldados_equipados != {}

@then("soldados devem ser alocados missões e receber instrucoes")
def then_soldados_recebem_missoes(context):
    context.em_missão = {}

    id = secrets.token_hex(nbytes=4).upper()
    context.recebeu_instrucoes, context.em_missão[id] =  provide_armor(context.soldados_equipados)

    assert context.equipado is True
    