# Configurando o problema de otimização

## Normalizar entradas

A primeira etapa é zerar a média, ou seja, é realizar a média de todos os dados e, após isso, remover esse valor de cada dado individualmente. A segunda etapa é normalizar as variâncias, que é o processo de realizar a média do quadrado de todos os elementos, e depois dividir todos os dados por esse valor. Dessa forma, você terá a seguinte distribuição:

![Normalizing inputs](./normalizing%20inputs.png)

Lembrando que é importante salvar os valores das normalizações para reutilizá-los no conjunto de teste. Esse processo de normalização ajuda na função de custo, como visto abaixo:

![Normalizing inputs visualization](./normalizing%20inputs%20visualization.png)

## Gradientes explodindo ou sumindo

Esse problema ocorre quando as derivadas ou as funções se tornam exponencialmente grandes ou pequenas. Uma maneira parcial de contornar esse problema é como os pesos são iniciados nas redes neurais. 

## Inicialização de pesos

Para cada função de ativação existe uma inicialização de pesos especificos que ameniza a explosão dos gradientes. para a ReLu, temos a função $rand * sqrt(2 / n)$. Pesquisar mais sobre essas inicializações.

## Verificação do Gradiente

Esse é um método para verificar se o processo de backpropagation está correto. Como não faremos isso manualmente, já que o Pytorch faz isso automaticamente, irei pular essa parte.