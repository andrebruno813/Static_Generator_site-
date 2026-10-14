# Tolkien Fan Club — gerador de site estático

Este repositório contém um pequeno gerador de sites estáticos escrito em Python. O conteúdo das páginas é escrito em Markdown, convertido para HTML pelo programa e combinado com um template. O resultado final fica na pasta `docs/` e pode ser servido localmente ou publicado com GitHub Pages.

O site de exemplo é dedicado ao universo de Tolkien. O código do gerador, no entanto, é separado do conteúdo, por isso pode ser adaptado para outro site.

Para uma explicação didática do código e da sua construção passo a passo, consulte [GUIA_DE_ESTUDO.md](./GUIA_DE_ESTUDO.md).

## Requisitos

- Python 3.10 ou superior.
- Git para publicar o projeto no GitHub.
- Não são necessárias bibliotecas externas: o gerador usa módulos incluídos no Python.

## Estrutura do projeto

```text
content/        Páginas escritas em Markdown
static/         CSS, imagens e outros ficheiros estáticos
template.html   Estrutura HTML comum às páginas
src/            Gerador, conversores e testes automatizados
docs/           Site HTML gerado; é a pasta publicada pelo GitHub Pages
build.sh        Gera o site com o caminho-base do repositório no Pages
main.sh         Gera o site para pré-visualização local e inicia um servidor
test.sh         Executa os testes
```

O conteúdo está organizado por diretórios. Por exemplo, `content/blog/glorfindel/index.md` é transformado em `docs/blog/glorfindel/index.html`. O ficheiro `static/index.css` é copiado para `docs/index.css`, e as imagens mantêm os seus subdiretórios.

> `docs/` é uma pasta gerada. O programa apaga o seu conteúdo anterior antes de voltar a criá-lo. Faça as alterações nas pastas `content/`, `static/` ou no `template.html`, e não edite diretamente os HTML de `docs/`.

## Escrever ou alterar páginas

Cada página é um ficheiro `.md` dentro de `content/` e deve começar com um título de nível 1 (`#`), usado também como título do separador do navegador:

```markdown
# Título da página

Um parágrafo normal. Pode escrever **negrito**, _itálico_ ou `código`.

## Um subtítulo

- Primeiro item
- Segundo item

[Voltar à página inicial](/)
```

O gerador reconhece:

- Títulos de `#` a `######`.
- Parágrafos separados por uma linha em branco.
- **Negrito** com `**texto**`, _itálico_ com `_texto_` e código em linha com `` `texto` ``.
- Blocos de código delimitados por três acentos graves.
- Citações começadas por `>`.
- Listas não ordenadas começadas por `- ` e listas ordenadas como `1. `.
- Ligações em `[texto](URL)` e imagens em `![descrição](URL)`.

Para adicionar uma página, crie a pasta correspondente em `content/` e coloque nela um `index.md`. Por exemplo, `content/about/index.md` será publicado como `docs/about/index.html`. Para incluir uma ligação para a nova página, edite o Markdown da página que deve apontar para ela.

## Adicionar imagens, CSS e favicon

Coloque os ficheiros estáticos dentro de `static/`. O gerador copia essa pasta recursivamente para `docs/`.

- Uma imagem guardada em `static/images/mapa.png` pode ser usada no Markdown como `![Mapa](/images/mapa.png)`.
- O CSS principal está em `static/index.css`.
- O favicon atual está em `static/dwarf.png`. A referência está no `<head>` de `template.html`; o gerador copia a imagem e ajusta o caminho durante a geração.

## Pré-visualizar no computador

Na raiz do repositório, execute:

```bash
bash main.sh
```

O script gera as páginas com caminhos locais e inicia um servidor HTTP na porta `8888`. Abra <http://localhost:8888> no navegador. Mantenha o terminal aberto enquanto consulta o site; para parar o servidor, prima `Ctrl+C`.

Sempre que alterar conteúdo, template ou ficheiros estáticos, pare o servidor se necessário, volte a executar `bash main.sh` e atualize a página no navegador.

Também pode executar os passos separadamente:

```bash
python3 src/main.py
cd docs
python3 -m http.server 8888
```

## Gerar para GitHub Pages

Este projeto está preparado para o repositório `andrebruno813/Static_Generator_site-`. O script `build.sh` passa o caminho-base `/Static_Generator_site-/` ao gerador, necessário para que CSS, imagens, favicon e ligações funcionem num site de projeto do GitHub Pages.

Na raiz do repositório:

```bash
bash build.sh
```

Confirme que a pasta `docs/` foi atualizada. Se estiver a usar Git, envie as alterações, por exemplo:

```bash
git add content static template.html build.sh docs
git commit -m "Update website"
git push origin main
```

Depois configure o GitHub Pages no repositório:

1. Abra **Settings → Pages**.
2. Em **Build and deployment**, escolha **Deploy from a branch**.
3. Escolha a branch `main` e a pasta `/docs`.
4. Clique em **Save**.
5. Aguarde a conclusão da publicação. O GitHub apresenta o URL e o estado da publicação nessa página.

O URL esperado para este repositório é <https://andrebruno813.github.io/Static_Generator_site-/>.

> O GitHub Pages publica os ficheiros que estão em `docs/`; não executa este gerador Python. Por isso, gere o site com `bash build.sh` antes de enviar alterações ao GitHub.

## Executar os testes

Na raiz do repositório:

```bash
bash test.sh
```

O comando executado pelo script é `python3 -m unittest discover -s src`. Os testes verificam as partes do conversor Markdown, a construção de nós HTML e a geração das páginas.

## Como funciona, resumidamente

1. `src/main.py` limpa e recria a pasta `docs/`.
2. Os ficheiros de `static/` são copiados para `docs/`.
3. O gerador procura recursivamente ficheiros `.md` em `content/`.
4. O Markdown é separado em blocos e convertido em nós HTML.
5. O primeiro título `# ` da página é usado como título.
6. O HTML resultante substitui `{{ Title }}` e `{{ Content }}` em `template.html`.
7. O HTML é escrito em `docs/`, preservando a estrutura de diretórios do conteúdo.
8. Para GitHub Pages, os caminhos absolutos do template e do conteúdo recebem o prefixo do repositório.

Para conhecer em detalhe a responsabilidade de cada módulo e seguir o fluxo com exemplos, consulte [GUIA_DE_ESTUDO.md](./GUIA_DE_ESTUDO.md).
