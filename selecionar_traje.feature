Feature: Verificando se o sistema consegue atribuir traje ao soldado

Scenario: Um soldado reconhecido precisa receber uma traje

Given o ambiente de reconhecimento foi preparado com sucesso
When a foto C:/Users/Java/Desktop/future_armors/faces/jack1.jpg for capturada
Then um soldado deve ser reconhecido
When um soldado foi reconhecido
Then deve ser alocado a patente
When existir soldados com patente
Then soldados devem receber traje