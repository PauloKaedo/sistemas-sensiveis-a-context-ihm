from behave import given, when, then
from futureArmorsBDD import *

@when("um soldado foi reconhecido")
def when_soldado_indentificado(context):
    assert context.reconhecido is True

@then("deve ser alocado a patente {id_patente}")
def then_soldado_alocado(context, id_patente):
    context.soldados_patente = {}

    id = secrets.token_hex(nbytes=4).upper()
    context.alistado, context.soldados_patente[id] = indentify_patent(context.soldados_reconhecidos, id_patente)
    assert context.alistado is True
    