# Reducao-astrometrica
Esse é um projeto do Centro Espacial ITA que visa fazer todo o caminho desde a observação prática de trajetórias de satélites até a visão computacional e cálculos correspondentes para determinação da trajetória dos satélites fotografados.

# Como utilizar os códigos

## Programar_Observacao.py
Esse é literalmente só rodar. Erros que podem ocorrer geralmente estão ligados à falta de módulos do python ou à versão do Selenium. 

A saída te entrega um arquivo .zip contendo uma planilha do Excel com as observações programadas "observacoes.xlsx" e as fotos da trajetória estimada pelo Heavens Above de cada satélite escolhido na observação. O .zip é salvo no mesmo diretório do código.

## astrometric_reduction.ipynb
Como é um notebook, dá para ir passo a passo, entendendo o que acontece.

Precisará mudar o path para o arquivo de imagem (ou nomear sua imagem como está no código). Depois disso, é só rodar tudo. O ideal é rodar uma célula por vez, acompanhando o desenvolvimento das funções.

Ao rodar tudo, teremos determinado as coordenadas desejadas (RA e dec) para input no código gauss_method.ipynb. 

## gauss_method.ipynb
Alterado o input das coordenadas e do tempo de observação no código, é só rodar e, ao fim, você terá os elementos orbitais da órbita do satélite correspondente.
