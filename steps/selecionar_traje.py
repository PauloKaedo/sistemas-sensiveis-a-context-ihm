from behave import given, when, then
from futureArmorsBDD import *

@when("existir soldados com patente")
def when_soldados_com_patente(context):
    assert context.soldados_patente != {}

@then("soldados devem receber traje")
def then_soldados_recebem_armadura(context):
    context.soldados_equipados = {}
    
    id = secrets.token_hex(nbytes=4).upper()
    context.equipado, context.soldados_equipados[id] = select_armor(context.soldados_patente, context.armor_storage)
    assert context.equipado is True
    