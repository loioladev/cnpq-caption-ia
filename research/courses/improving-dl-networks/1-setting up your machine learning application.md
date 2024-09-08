# Configurando a aplicação de ML

## Train / Dev / Test sets

O conjunto de dados para treinamento da rede neural pode ser definido como o conjunto de treinamento (train set). O conjunto de validação (dev set) pode ser usado para holdin cross validation ou outros ajustes para melhorar o modelo, e o conjunto de teste serve para testar o seu modelo final.

Não é necessário fazer distribuições tão grandes entre os conjuntos quando a quantidade de dados é grande. Se você tem 1.000.000 de dados, bastam 10.000 em cada conjunto de dev e teste, ou seja, menos de 5% dos dados para esses dois conjuntos.

Não é necessário ter um conjunto de teste. 

## Bias / Variance

Um alto bias pode ser *underfitting* para os dados. Uma variância alta pode dar overfitting os dados. Por isso, devemos achar um balanço.

![Bias / variance](./high%20variance%20and%20bias.png)

Vamos supor que você tem um erro de 1% no conjunto de treinamento e um erro de 11% no conjunto de desenvolvimento. Dessa forma, é possível supor que você está tendo uma alta variância. 

Agora vamos supor que o seu conjunto de treinamento atingiu um erro de 15% e 16% no conjunto de desenvolvimento. Isso pode indicar um alto viés (bias).

Agora, vamos supor que você tem 15% de erro no conjunto de treinamento e 30% no conjunto de desenvolvimento. Assim, isso pode indicar que você tem uma alta variância e viés.

## Receita básica para ML

Se estiver com um alto viés, tente utilizar uma rede maior ou treinar o modelo por mais tempo, pois envolve o conjunto de treinamento.

Se estiver com uma variância alta, tente utilizar mais dados ou regularizar o modelo, pois isso estará relacionado ao conjunto de desenvolvimento.



