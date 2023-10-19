# Minibatch

porque usamos Mini-Batches? Digamos que você tenha cerca de 1 bilhão de dados de treinamento. Se você decidir usar o conjunto completo de treinamento em cada época, você precisará de muita memória RAM e armazenamento para processar esses dados

Portanto, usamos um subconjunto de dados de treinamento (chamamos de “Mini-Batch”) de cada vez em cada época. Isso nos permitirá manter os dois objetivos: ajustar dados suficientes na memória do computador e manter a filosofia de vetorização ao mesmo tempo. Uma coisa importante sobre o Mini-Batch é que, é melhor escolher o tamanho do Mini-Batch como múltiplo de 2 e os valores comuns são: 64, 128, 256 e 512.

Portanto, a utilização do Mini-Batch (principalmente na descida do gradiente) é introduzida como um trade-off entre {atualizações rápidas do modelo, eficiência de memória}.

O caminho a percorrer é, portanto, usar alguns valores aceitáveis ​​(mas não necessariamente ideais) para os outros hiperparâmetros, e então testar vários tamanhos diferentes de Mini-Lotes, escalando η como fizemos no exemplo acima. Plote a precisão da validação em relação ao tempo (como em tempo real decorrido, não em época!) e escolha o tamanho do Mini-Lote que forneça a melhoria mais rápida no desempenho. 
