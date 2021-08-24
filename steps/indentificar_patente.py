from behave import given, when, then
from futureArmorsBDD import *

@when("um soldado foi reconhecido")
def when_soldado_indentificado(context):
    assert context.reconhecido

@then("deve ser alocado a patente")
def then_soldado_alocado(context, id_patente):
    indentify_patent(context.recognized_soldiers, context.patent_soldiers, id_patente)
    