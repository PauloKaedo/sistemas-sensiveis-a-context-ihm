from behave import given, when, then
from futureArmorsBDD import *

@when("existir soldados com patente")
def when_soldados_com_patente(context):
    assert context.patent_soldiers != None

@then("soldados devem receber traje")
def then_soldados_recebem_armadura(context):
    select_armor(context.patent_soldiers, context.armor_storage, context.equipped_soldiers)
    