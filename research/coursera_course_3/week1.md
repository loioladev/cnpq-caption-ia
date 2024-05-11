## Introduction to Machine Learning Strategy

### Orthogonalization | Ortogonalização

Ortogonalização é um método que, dado uma certa quantidade de "botões" para modificar uma imagem, cada botão é único e não interfere na mudança de outros botões. Porém, imagine que tais botões agora não são únicos, e alteram todos os outros botões de formas diferentes. Agora, como isso se relaciona com Machine Learning?

Em um projeto de machine learning, devemos seguir os quatro tópicos a seguir:

- O conjunto de treinamento deve ter uma performance boa, que pode ser comparada com a análise de nível humano. Caso não esteja assim, pode-se tentar uma rede maior, um algoritmo de otimização diferente...

- O conjunto de desenvolvimento deve ter uma performance boa na função de custo. Caso não esteja assim, pode-se tentar a regularização, um conjunto de treinamento maior...

- O conjunto de teste deve ter uma performance boa na função de custo. Caso não esteja assim, pode-se tentar aumentar o conjunto de desenvolvimento...

- O modelo perfoma bem no mundo real. Caso não esteja assim, pode-se tentar mudar o conjunto de desenvolvimento, a função de custo...


O autor também comenta que a técnica de *early stopping* não é tão utilizado por ele, visto que, ao utilizá-la, ele perde um pouco do controle ortogonal sobre o conjunto de treinamento e desenvolvimento.

## Setting Up your Goal

### Single Number Evaluation Metric

Quando os times começam um novo projeto de ML, o autor recomenda que se escolha uma métrica única real para a validação do problema. Um exemplo dado é avaliar o modelo a partir da precisão e do recall. Se em dois treinamentos as métricas se saíram diferentes (uma melhor do que a outra em cada treinamento), fica dificil se basear nelas para definir o melhor modelo. Assim, ao escolher uma métrica única, como o F1 Score ("média" entre precisão e recall), você consegue escolher mais facilmente qual o melhor modelo.

Assim, um bom conjunto de desenvolvimento e uma única métrica de avaliação podem melhorar a eficiência do time em realizar decisões.

### Satisficing and Optimizing Metric

Às vezes, é complicado definir apenas uma métrica para a avaliação do modelo. Assim, suponha que você tenha N métricas. Escolha uma para ser a métrica de otimização, que deve possuir o maior/menor valor de acordo com o problema, e as outras são métricas satisfatórias, que podem variar os resultados. Um exemplo dado é acurácia e tempo de execução. Escolhendo acurácia como métrica de otimização, podemos chegar na fórmula do custo $acurácia -  0.5xtempo de execução$, para definir uma métrica.

### Train/Dev/Test Distributions

Escolha um conjunto de desenvolvimento e teste que reflita os dados que você espera conseguir no futuro e considere importante de performar bem, ou seja, utilize a mesma distribuição de dados nos dois conjuntos.

### Size of Dev and Test Sets

Define o tamanho do seu conjunto de teste para ser grande o suficiente para dar uma alta confiança na performance geral do seu modelo.

## Comparing to Human Level Performance

### Por quê a comparação de nível humano?

Bayes optimal error: é o melhor erro possível, onde não é possível uma função superar esse limite. Em imagens que possuem muito barulho ou estão muito desfocadas, onde não é possível reconhecer se é a imagem é um gato ou não, uma acurácia de 100% não necessariamente é o nível perfeito.

Quando um algoritmo supera uma classificação humana, talvez o espaço disponível para melhorar seja pequeno ou dificil de alcançar.

Quando o modelo de ML é pior que a classificação de humanos, você pode
- Adquirar dados rotulados por humanos
- Ganhar conhecimento de uma análise manual dos erros
- Melhor análise do bias e da variância.

### Avoidable Bias

Ao comparar o valor do erro com o erro humano, talvez o algoritmo esteja próximo de atingir o limite de Bayes. 

O *avoidable bias* é uma certa quantia de erro que você não consegue diminuir sem necessariamente ter um overfitting no modelo.
