# Introdução às Redes Neurais Convolucionais

Essas redes usam uma arquitetura especial que é particularmente bem adaptada para classificar imagens. O uso dessa arquitetura torna as redes convolucionais rápidas de treinar. Isso, por sua vez, nos ajuda a treinar redes profundas de muitas camadas, que são muito boas na classificação de imagens. Hoje, redes neurais convolucionais ou alguma variante próxima são usadas na maioria das redes neurais para reconhecimento de imagem.

## Definição

Uma Rede Neural Convolucional (ConvNet / Convolutional Neural Network / CNN) é um algoritmo de Aprendizado Profundo que pode captar uma imagem de entrada, atribuir importância (pesos e vieses que podem ser aprendidos) a vários aspectos / objetos da imagem e ser capaz de diferenciar um do outro. O pré-processamento exigido em uma ConvNet é muito menor em comparação com outros algoritmos de classificação. Enquanto nos métodos primitivos os filtros são feitos à mão, com treinamento suficiente, as ConvNets têm a capacidade de aprender esses filtros / características.

## Por que usar ConvNets e não rede feed-forward?

Uma ConvNet é capaz de capturar com sucesso as dependências espaciais e temporais em uma imagem através da aplicação de filtros relevantes. A arquitetura executa um melhor ajuste ao conjunto de dados da imagem devido à redução no número de parâmetros envolvidos e à capacidade de reutilização dos pesos. Em outras palavras, a rede pode ser treinada para entender melhor a sofisticação da imagem.

Você pode imaginar como a computação ficaria intensiva assim que as imagens atingissem dimensões, digamos, 8K (7680 × 4320). A função da ConvNet é reduzir as imagens para uma forma mais fácil de processar, sem perder recursos que são críticos para obter uma boa previsão. Isso é importante quando queremos projetar uma arquitetura que não seja apenas boa em recursos de aprendizado, mas que também seja escalável para conjuntos de dados massivos.


