# Guia de estudo: como o gerador foi construído

Este guia acompanha o projeto desde a entrada Markdown até ao site HTML publicado. Foi escrito para quem está a aprender Python e ainda não tem muita experiência com a linguagem. Não é necessário dominar todos os detalhes à primeira leitura: siga as etapas na ordem, experimente os comandos e volte aos ficheiros enquanto lê.

## 1. O que é um site estático?

Um site estático é um conjunto de ficheiros prontos, normalmente HTML, CSS, imagens e outros recursos. O servidor entrega esses ficheiros ao navegador sem executar código Python para cada visita.

Neste projeto, o Python é usado **antes** da publicação para criar os HTML. Depois da geração, a pasta `docs/` contém os ficheiros que o GitHub Pages pode servir diretamente.

O percurso geral é:

```text
ficheiros Markdown em content/
             |
             v
       gerador Python  <--- template.html
             |          <--- ficheiros em static/
             v
     páginas HTML em docs/
             |
             v
       servidor local ou GitHub Pages
```

## 2. Preparar o projeto

É necessário Python 3.10 ou superior. Esta versão mínima é necessária porque o projeto usa `match`/`case` em `src/textnode.py`. Não são necessárias dependências externas.

Abra um terminal na pasta principal do repositório. Os scripts usam caminhos relativos, como `content`, `static` e `docs`, por isso devem ser executados a partir dessa pasta.

Para confirmar a versão do Python:

```bash
python3 --version
```

Para executar os testes:

```bash
bash test.sh
```

Os testes ajudam a verificar que uma alteração no parser não quebra comportamentos que já estão cobertos.

## 3. Conhecer as pastas

### `content/`: os textos

Cada ficheiro `.md` representa uma página. A estrutura de pastas é repetida na saída. Por exemplo:

```text
content/blog/glorfindel/index.md
```

torna-se:

```text
docs/blog/glorfindel/index.html
```

As páginas começam com um título `# Título`. Esse título é utilizado no conteúdo da página e na etiqueta `<title>` do template.

### `static/`: os recursos

Aqui ficam recursos que não precisam de ser convertidos, como o CSS, imagens e favicon. O gerador copia-os sem alterar o conteúdo:

```text
static/index.css       -> docs/index.css
static/dwarf.png       -> docs/dwarf.png
static/images/x.png    -> docs/images/x.png
```

### `template.html`: a moldura comum

O template define a estrutura HTML que todas as páginas partilham. Tem dois marcadores substituídos durante a geração:

```html
<title>{{ Title }}</title>
...
<article>{{ Content }}</article>
```

Assim, a página pode ter conteúdo diferente sem duplicar todo o cabeçalho HTML.

### `src/`: o gerador e as suas peças

O código está dividido em módulos pequenos. Cada módulo trata de uma parte da conversão, em vez de tentar fazer tudo numa única função.

## 4. Seguir uma frase: de Markdown a HTML

Considere este Markdown:

```markdown
Aqui está **uma frase importante** e uma [ligação](https://example.com).
```

O projeto trata essa frase em várias etapas:

1. `text_to_textnodes.py` começa por criar um nó de texto simples.
2. `split_nodes_delimiter.py` identifica o texto entre `**` e converte-o num nó `BOLD`.
3. `split_nodes.py` e `markdown_extract.py` identificam a ligação e guardam o texto e o URL.
4. `textnode.py` converte os tipos de nó para etiquetas HTML (`<b>` e `<a>`).
5. Os nós são reunidos e o resultado passa a ser HTML:

   ```html
   Aqui está <b>uma frase importante</b> e uma <a href="https://example.com">ligação</a>.
   ```

Um **nó** é aqui um objeto Python que representa uma parte do conteúdo. Por exemplo, um nó pode representar texto normal, texto em negrito, uma ligação, ou um elemento HTML com vários elementos filhos.

## 5. Seguir uma página: dos blocos à árvore HTML

Uma página é composta por blocos maiores, como parágrafos, títulos ou listas. A conversão acontece em camadas:

### 5.1. Separar blocos

`src/markdown_blocks.py` divide o texto pelas linhas em branco. Cada parte não vazia torna-se um bloco.

### 5.2. Identificar o tipo do bloco

`src/blocktype.py` define os tipos de bloco e decide se cada bloco é:

- Título (`#` até `######`).
- Código cercado por três acentos graves.
- Citação, com linhas iniciadas por `>`.
- Lista não ordenada, com linhas iniciadas por `- `.
- Lista ordenada, com itens como `1. ` e `2. `.
- Parágrafo, se não corresponder aos tipos anteriores.

### 5.3. Converter cada bloco

`src/markdown_to_html.py` transforma os blocos reconhecidos em elementos HTML. Alguns exemplos:

| Markdown | HTML produzido |
|---|---|
| `## Introdução` | `<h2>Introdução</h2>` |
| `Um parágrafo.` | `<p>Um parágrafo.</p>` |
| `- Um item` | `<ul><li>Um item</li></ul>` |
| `> Uma citação` | `<blockquote>Uma citação</blockquote>` |

Para o texto dentro de parágrafos e itens, o conversor também utiliza a etapa de nós de texto descrita anteriormente.

### 5.4. Criar e renderizar nós HTML

`src/htmlnode.py` contém a estrutura base para representar elementos HTML, os seus atributos e os seus filhos. `src/leafnode.py` trata de elementos folha, sem filhos; `src/parentnode.py` trata de elementos que contêm outros elementos.

O método `to_html()` percorre essa estrutura e junta as etiquetas e o conteúdo. É assim que várias peças pequenas se transformam numa página completa.

## 6. Como uma página é montada

`src/main.py` coordena a geração. Para cada ficheiro Markdown encontrado em `content/`, a função `generate_page()`:

1. Lê o Markdown.
2. Lê `template.html`.
3. Chama `markdown_to_html_node()` para criar a árvore HTML do conteúdo.
4. Chama `extract_title()` para encontrar a primeira linha que começa por `# `.
5. Substitui `{{ Title }}` e `{{ Content }}` no template.
6. Ajusta os caminhos que começam por `/`, quando é fornecido um caminho-base.
7. Cria as pastas de destino necessárias.
8. Escreve a página HTML.

`generate_pages_recursive()` percorre `content/` e replica os diretórios encontrados em `docs/`. A função `copy_fyles_recursive()` copia os ficheiros estáticos para a saída.

Antes dessas operações, `main()` apaga a pasta de saída anterior e cria-a novamente. Isto evita deixar páginas antigas publicadas depois de o conteúdo de origem ser removido. Também significa que alterações manuais dentro de `docs/` serão perdidas na próxima geração.

## 7. Os dois modos de gerar o site

### Pré-visualização local: `main.sh`

Execute na raiz do repositório:

```bash
bash main.sh
```

O script chama o gerador sem caminho-base, inicia um servidor local na porta `8888` e serve a pasta `docs/`. Abra <http://localhost:8888>. O terminal tem de ficar aberto enquanto o servidor estiver a funcionar; prima `Ctrl+C` para o parar.

### GitHub Pages: `build.sh`

Execute:

```bash
bash build.sh
```

Este script passa `/Static_Generator_site-/` ao gerador. O prefixo é necessário porque o site está num **repositório de projeto**. O domínio contém o nome do utilizador e o caminho do repositório:

```text
https://andrebruno813.github.io/Static_Generator_site-/
```

Sem o prefixo, um caminho como `/index.css` apontaria para a raiz do domínio (`andrebruno813.github.io/index.css`), em vez de apontar para o diretório do projeto. O gerador ajusta atributos `href` e `src` que começam por `/`, para que apontem para o caminho correto.

## 8. Publicar com GitHub Pages

O GitHub Pages não executa `src/main.py`. Neste projeto, publica os ficheiros HTML já gerados na pasta `docs/`.

1. Faça as alterações em `content/`, `static/` ou `template.html`.
2. Na raiz do repositório, gere a versão para produção:

   ```bash
   bash build.sh
   ```

3. Envie as fontes e a saída gerada para o GitHub:

   ```bash
   git add content static template.html build.sh docs
   git commit -m "Update website"
   git push origin main
   ```

4. No repositório GitHub, abra **Settings → Pages**.
5. Selecione **Deploy from a branch**, escolha `main` e `/docs`, e guarde.
6. Aguarde o estado de publicação e abra o URL apresentado em **Settings → Pages**. Para este repositório, o endereço esperado é <https://andrebruno813.github.io/Static_Generator_site-/>.

Se o HTML, CSS, as imagens ou o favicon não refletirem as alterações, confirme primeiro que executou `bash build.sh` e que enviou a pasta `docs/`. O navegador também pode guardar recursos antigos em cache; experimente uma atualização forçada ou uma janela privada.

## 9. Executar os testes e experimentar

O comando:

```bash
bash test.sh
```

executa a biblioteca de testes incluída no Python (`unittest`) e procura testes dentro de `src/`. Os ficheiros `test_*.py` verificam componentes individuais e, em conjunto, partes do fluxo de geração.

Um exercício curto para observar uma alteração:

1. Edite `content/index.md` e acrescente uma lista com dois itens.
2. Execute `bash main.sh`.
3. Abra <http://localhost:8888> e verifique a lista.
4. Abra `docs/index.html` num editor e encontre as etiquetas `<ul>` e `<li>`.
5. Execute `bash test.sh`.

## 10. Glossário curto

- **Markdown:** texto simples com marcas como `#`, `**` e `-` para indicar estrutura e formatação.
- **HTML:** linguagem de marcação que o navegador usa para apresentar uma página.
- **CSS:** regras visuais, como cores, margens e tipos de letra.
- **Template:** modelo com estrutura comum e espaços reservados para conteúdo variável.
- **Nó:** objeto que representa um pedaço de texto ou um elemento numa árvore.
- **Caminho-base:** prefixo de URL usado para servir corretamente os recursos num subdiretório, como o caminho do repositório no GitHub Pages.
- **Gerador estático:** programa que cria os ficheiros de um site antes de estes serem servidos aos visitantes.

## 11. Limites atuais do parser

Este projeto é um exercício de implementação, não um parser completo de Markdown. Use a sintaxe listada no [README](./README.md). Em particular, não assuma suporte para tabelas Markdown ou listas aninhadas. Os títulos das páginas devem ter um título de nível 1 (`# `), porque o gerador usa esse título e gera um erro se não o encontrar.

Ao estudar, pode adicionar uma funcionalidade de cada vez: primeiro escreva um teste para o comportamento esperado, depois implemente a conversão e, por fim, execute `bash test.sh`.
