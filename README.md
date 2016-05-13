# Lattes Mining
Extrator de dados do Lattes para a disciplina Dados Abertos Conectados - IC/UFAL 2015.2
Professor responsável: Ig Bittencourt [http://igbittencourt.com/]

Este projeto tem o objetivo de extrair dados de currículos Lattes de autores de contribuições científicas. Visto que, atualmente, o sistema de consulta de currículos Lattes possui uma verificação captcha para a visualização e download do currículo, o script de coleta dos dados precisa de um humano para validar cada um dos captchas apresentados. Apesar de muitas melhorias terem sido feitas ao algoritmo com o propósito de diminuir o número de captchas apresentados, esta continua sendo uma tarefa árdua, ainda mais quando há uma quantidade elevada de currículos a serem coletados.

#### Instruções

######Coleta de currículos:

Script: `lattes_mining.py`

Um arquivo CSV `authors.csv` (no diretório atual) deve possuir uma lista com nomes de autores e títulos de contribuições, nessa ordem, onde cada contribuição possui uma linha no arquivo. Para cada nome de autor buscado três reações podem surgir:

1. Nenhum currículo foi encontrado com a string de busca (nome do autor) no Lattes, então o nome desse autor e o título de sua contribuição (nesta ordem) são adicionados a um arquivo CSV `not_found.csv` (no diretório atual) que conterá todos os autores que estão na mesma situação;

2. Um ou mais currículos foram encontrados com a string de busca (nome do autor), mas o título da contribuição não pode ser encontrado no currículo do autor, então o nome desse autor e o título de sua contribuição (nesta ordem) são adicionados a um arquivo CSV `error.csv` (no diretório atual) que conterá todas as contribuições que estão na mesma situação;

3. O currículo do autor foi encontrado e o título de sua contribução estava em seu currículo, então o download do currículo é efetuado para o diretório `data/` (partindo do diretório atual) e o nome do autor e o título de sua contribuição são adicionados a um arquivo CSV `downloaded.csv` (no diretório atual) que conterá todos os autores na mesma situação. Eventualmente, o currículo desse autor pode ter sido baixado anteriormente por outra contribuição, e, nesse caso, a requisição para o download do currículo não é efetuada, mas o nome/título da contribuição do autor são adicionados ao arquivo da mesma forma -- dessa forma, é possível economizar memória e diminuir a carga de verificações captcha necessárias para finalizar a extração.

Observação: sempre que o nome de um autor e o título de sua contribuição são adicionados a um arquivo, estas informações são removidas da primeira linha do arquivo que contém a lista de autores a serem extraídos -- dessa forma, é possível pausar o processo de extração a qualquer momento.

Ao usar o script `lattes_mining.py` é possível definir um prefixo para o nome dos arquivos passando esse prefixo como argumento. Ao rodar com `lattes_mining.py wie`, por exemplo, fará com que o arquivo `wie_authors.csv` seja buscado em vez do arquivo `authors.csv` (padrão, quando nenhum argumento é passado). Da mesma forma, os arquivos `wie_not_found.csv`, `wie_error.csv` e `wie_downloaded.csv` serão usados em vez dos arquivos `not_found.csv`, `error.csv` e `downloaded.csv` (padrões quando nenhum argumento é passado). O diretório de armazenamento dos arquivos `.zip` baixados (`data/`, partindo do diretório atual) não é alterado ao usar prefixos.

É necessário possuir Python 2 com a biblioteca Selenium instalada e Firefox para rodar o script de coleta de currículos.