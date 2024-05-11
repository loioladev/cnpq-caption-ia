# Overfitting

A maneira óbvia de detectar overfitting é mantendo o controle da precisão nos dados de teste conforme nossos treinos da rede. Se percebermos que a precisão nos dados de teste não está mais melhorando, devemos parar de treinar.

Até agora, usamos o training_data e test_data e ignoramos o validation_data nos treinamentos da rede. Em vez de usar o test_data para evitar overfitting, usaremos o validation_data. Para fazer isso, usaremos praticamente a mesma estratégia descrita acima para o test_data. Ou seja, calcularemos a precisão da classificação nos dados de validação no final de cada época. Quando a precisão da classificação nos dados de validação estiver saturada, paramos de treinar. Essa estratégia é chamada de parada antecipada (Early-Stopping). 

Por que usar o validation_data para evitar overfitting, em vez de test_data? Na verdade, isso faz parte de uma estratégia mais geral, que é usar o validation_data para avaliar diferentes opções de avaliação de hiperparâmetros, como o número de épocas para treinamento, a taxa de aprendizado, a melhor arquitetura de rede e assim por diante.

Para entender o porquê, considere que, ao definir os hiperparâmetros, é provável que tentemos muitas opções diferentes para os hiperparâmetros. Se definirmos os hiperparâmetros com base nas avaliações do test_data, será possível acabarmos super adequando nossos hiperparâmetros ao test_data. Ou seja, podemos acabar encontrando hiperparâmetros que se encaixam em peculiaridades particulares dos dados de teste, mas onde o desempenho da rede não se generalizará para outros conjuntos de dados. Protegemos contra isso descobrindo os hiperparâmetros usando o validation_data.

Felizmente, existem outras técnicas que podem reduzir o overfitting, mesmo quando temos uma rede fixa e dados de treinamento fixos. Estas técnicas são conhecidas como técnicas de regularização.
