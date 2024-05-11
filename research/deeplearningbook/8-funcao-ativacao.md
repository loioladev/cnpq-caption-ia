# Função de Ativação

## Introdução

Vamos supor uma rede neural qualquer. Gostaríamos que a rede aprendesse pesos e bias para que a saída da rede classifique corretamente o dígito. Para ver como a aprendizagem pode funcionar, suponha que façamos uma pequena alteração em algum peso (ou bias) na rede, para que essa alteração modifique a saída da rede. Entretanto, essa mudança pode mudar completamente o comportamento da rede, como visto em Perceptrons, que podem mudar a saída binária.

Podemos superar esse problema através da introdução de um componente matemático em nosso neurônio artificial, chamado função de ativação. As funções de ativação permitem que pequenas mudanças nos pesos e bias causem apenas uma pequena alteração no output, definindo se o neurônio deve ser ativado ou não.

A função de ativação é a transformação não linear que fazemos ao longo do sinal de entrada. As funções de ativação tornam possível a propagação posterior desde que os gradientes sejam fornecidos juntamente com o erro para atualizar os pesos e bias. Sem a função não linear diferenciável, isso não seria possível.

## Tipos de Funções de Ativação

### Binary Step Function

A primeira coisa que vem à nossa mente quando temos uma função de ativação seria um classificador baseado em limiar (threshold), ou seja, se o neurônio deve ou não ser ativado. Se o valor Y estiver acima de um valor de limite determinado, ative o neurônio senão deixa desativado.

$$
f(x) = 1, x >= 0\\
f(x) = 0, x < 0
$$

Além disso, o gradiente da função de etapa é zero. Isso faz com que a função de etapa não seja tão útil durante o backpropagation quando os gradientes das funções de ativação são enviados para cálculos de erro para melhorar e otimizar os resultados.

### Linear Function

Uma simples função linear de forma $f(x) = ax$. A derivada de uma função linear é constante, isto é, não depende do valor de entrada x. Isso significa que toda vez que fazemos backpropagation, o gradiente seria o mesmo. E este é um grande problema, não estamos realmente melhorando o erro, já que o gradiente é praticamente o mesmo.

### Sigmóide

A função sigmóide tem a forma $f(x) = 1 / (1 + e ^ -x)$. Esta é uma função suave e é continuamente diferenciável. A função varia de 0 a 1 tendo um formato S. A função essencialmente tenta empurrar os valores de Y para os extremos. Esta é uma qualidade muito desejável quando tentamos classificar os valores para uma classe específica. Um problema dessa função é que os valores variam apenas de 0 a 1. 

### Tanh

É apenas uma versão escalonada da função sigmóide, de forma $tahn(x) = 2sigmoides(2x) - 1$, e varia de -1 a 1.

### ReLU

A função ReLU é a unidade linear rectificada. É definida como $f(x) = max(0, x)$. ReLU é a função de ativação mais amplamente utilizada ao projetar redes neurais atualmente. Primeiramente, a função ReLU é não linear, o que significa que podemos facilmente copiar os erros para trás e ter várias camadas de neurônios ativados pela função ReLU.

A principal vantagem de usar a função ReLU sobre outras funções de ativação é que ela não ativa todos os neurônios ao mesmo tempo.

### Softmax

A função softmax também é um tipo de função sigmóide, mas é útil quando tentamos lidar com problemas de classificação. A função softmax transforma as saídas para cada classe para valores entre 0 e 1 e também divide pela soma das saídas. Isso essencialmente dá a probabilidade de a entrada estar em uma determinada classe. 

A função softmax é idealmente usada na camada de saída do classificador, onde realmente estamos tentando gerar as probabilidades para definir a classe de cada entrada.

