# Underground Videos

## Sitema para combate de a pirataria usando Marca D'água Digital Invisível
 
## Tecnologias
- Django
- ffmpeg
- lsb

## Como funciona?
- Pré-processamento: O vídeo é dividido em segmentos (quadros) e seu áudio é salvo temporariamente utilizando a biblioteca FFmpeg.
- Inserção da marca d'água: Com base no segmento escolhido, é realizado o processo de esteganografia no quadro.
- Pós-processamento: Os segmentos são recombinados e o áudio é reintroduzido, utilizando novamente a biblioteca FFmpeg, formando um novo vídeo. Assim, obtemos o vídeo com os dados ocultos em seu interior.
- Extração da marca d'água: Para extrair os dados, a ```função decode_video()``` é utilizada. O vídeo é novamente segmentado e, em cada segmento, a ```função decode_image()``` decodifica os dados ocultos."
