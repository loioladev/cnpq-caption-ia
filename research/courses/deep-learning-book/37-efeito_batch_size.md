# O Efeito do Batch Size no Treinamento de Redes Neurais Artificiais

Tamanho do lote (Batch Size) é um termo usado em aprendizado de máquina e refere-se ao número de exemplos de treinamento usados em uma iteração. O Batch Size pode ser uma das três opções:

-**batch mode**: onde o tamanho do lote é igual ao conjunto de dados total, tornando os valores de iteração e épocas equivalentes.
-**mini-batch mode**: onde o tamanho do lote é maior que um, mas menor que o tamanho total do conjunto de dados. Geralmente, um número que pode ser dividido no tamanho total do conjunto de dados.
-**stochastic mode**: onde o tamanho do lote é igual a um. Portanto, o gradiente e os parâmetros da rede neural são atualizados após cada amostra.

A métrica em que nos concentraremos é o gap de generalização, que é definido como a diferença entre o valor do tempo de treinamento e o valor do tempo de teste. 

Por um lado, usar um lote igual a todo o conjunto de dados garante a convergência para o ótimo global da função objetivo. No entanto, isso é à custa de uma convergência empírica mais lenta para esse ótimo. Por outro lado, o uso de tamanhos menores de lotes mostrou empiricamente uma convergência mais rápida para soluções “boas”. Isso é intuitivamente explicado pelo fato de que tamanhos de lote menores permitem que o modelo “inicie o aprendizado antes de ver todos os dados”. A desvantagem de usar um tamanho de lote menor é que não há garantia que o modelo vai convergir para o ótimo global. Ele irá saltar em torno do ótimo global, dependendo da relação entre o tamanho do lote e o tamanho do conjunto de dados. 

A razão para uma melhor generalização é vagamente atribuída à existência de “ruído” no treinamento de pequeno tamanho de lote. Como os sistemas de redes neurais são extremamente propensos a ajustes excessivos (overfitting), a ideia é que a visualização de vários tamanhos de lote pequenos, cada lote sendo uma representação “ruidosa” de todo o conjunto de dados, causará uma espécie de dinâmica de “tug-and-pull”. Essa dinâmica evita que a rede neural se ajuste excessivamente no conjunto de treinamento e, portanto, tenha um desempenho ruim no conjunto de testes.

## Efeito do Tamanho de lote

Tamanhos maiores de lotes levam a uma precisão menor nos dados de teste.