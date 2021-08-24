from behave import given, when, then
from futureArmorsBDD import *

@when("existir soldados equipados")
def when_soldados_equipados(context):
    assert context.equipped_soldiers != None

@then("soldados devem missões e instrucoes")
def then_soldados_recebem_missoes(context):
    provide_armor(context.equipped_soldiers)
    