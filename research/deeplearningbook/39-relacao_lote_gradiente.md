# Relação Entre o Tamanho do Lote e o Cálculo do Gradiente

Uma hipótese pode ser que as amostras de treinamento no mesmo lote interfiram (competem) com o gradiente um do outro. Uma amostra deseja mover os pesos do modelo em uma direção, enquanto outra amostra deseja mover os pesos na direção oposta. Portanto, seus gradientes tendem a ser cancelados e você obtém um pequeno gradiente geral. Talvez, se as amostras forem divididas em dois lotes, a concorrência será reduzida, pois o modelo poderá encontrar pesos que satisfarão as duas amostras, se forem feitas em sequência. Em outras palavras, a otimização sequencial de amostras é mais fácil do que a otimização simultânea em espaços de parâmetros complexos e de alta dimensão.

Ao realizar os experimentos, descobriu-se que tamanhos de lotes maiores produzem etapas de gradiente maiores do que tamanhos de lotes menores para o mesmo número de amostras vistas.

Ao contrário da nossa hipótese, a norma gradiente média aumenta com o tamanho do lote! Esperávamos que os gradientes fossem menores para um tamanho de lote maior devido à competição entre as amostras de dados. Em vez disso, o que encontramos é que tamanhos maiores de lotes fazem etapas de gradiente maiores do que tamanhos de lote menores para o mesmo número de amostras vistas.

Além disso, para a mesma distância média da norma euclidiana dos pesos iniciais do modelo, tamanhos de lote maiores têm maior variância na distância.
