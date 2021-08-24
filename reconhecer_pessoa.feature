Feature: reconhecer um soldado pela foto

Scenario: Um soldado chega a base e deve ser reconhecido por uma camera

Given o ambiente de reconhecimento foi preparado com sucesso
When a foto C:/Users/Java/Desktop/future_armors/faces/jack1.jpg for capturada
Then um soldado deve ser conhecido