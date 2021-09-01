from behave import given, when, then
from futureArmorsBDD import *

@given("o ambiente de reconhecimento foi preparado com sucesso")
def given_ambiente_preparado(context):
    context.configData, context.patent_soldiers, context.equipped_soldiers, context.recognized_soldiers, context.armor_storage = start()
    context.soldados_reconhecidos = {}
    assert context.configData != None

@when("a foto {foto_soldado} for capturada")
def when_foto_capturada(context, foto_soldado):
    pessoa = simule_enlistment(foto_soldado)
    context.reconhecido, context.soldado = recognitize_person(pessoa, context.configData)

    assert True

@then("um soldado deve ser reconhecido")
def then_soldado_reconhecido(context):
    id = secrets.token_hex(nbytes=4).upper()
    context.soldados_reconhecidos[id] = context.soldado
    assert context.reconhecido is True