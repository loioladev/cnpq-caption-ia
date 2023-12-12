# Regularizando sua rede neural

## Como a regularização reduz o *overfitting*

Quando implementamos a regularização, os pesos tendem a diminuir em toda a rede. É como se estivéssemos "zerando" os pesos de alguns nós ocultos.

Pense em um gráfico da função de ativação *tah*. Os pesos seriam jogados para a reta linear no meio da função.

## Regularização dropout

Outra regularização poderosa se chama droupout. Se o seu modelo está sofrendo com *overfitting*, você pode usar essa regularização para que, em cada camada da rede neural, ele escolha alguns nós para "desligar" naquela iteração, o que os leva a não atualizarem seus pesos de acordo com o treinamento. 