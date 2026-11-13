# O Pomar do Pé de Laranja: livro de colorir para o Amazon KDP

Livro de colorir infantojuvenil com 30 páginas, personagens originais (frutas brasileiras) e 4 capítulos inspirados no folclore.

## Arquivos prontos

| Arquivo | O que é |
|---|---|
| `build/interior.pdf` | Miolo: 30 páginas, 8,5" × 11", preto e branco, sem sangria |
| `build/capa.pdf` | Capa completa (contracapa + lombada + frente), 17,318" × 11,25", com sangria de 0,125" |

## Estrutura do miolo

| Pág. | Conteúdo |
|---|---|
| 1 | Folha de rosto (para colorir) |
| 2 | Créditos / direitos autorais |
| 3 | "Este livro pertence a:" |
| 4 | Conheça a turma (texto) |
| 5–17 | 7 personagens em página inteira (ímpares). No verso de cada um: "Teste suas cores" ou "Rabisque aqui" |
| 18–25 | 4 capítulos: texto à esquerda, ilustração à direita |
| 26–27 | Epílogo + cena final |
| 28–30 | "Fim!", "Invente sua fruta!", "Meu desenho favorito" |

Nenhum desenho fica no verso de outro desenho, então a tinta da canetinha não estraga a próxima ilustração.

## Antes de publicar

1. Abra `src/config.py`, troque `[Nome do Autor]` pelo seu nome (ou pseudônimo) e gere de novo:
   ```bash
   cd src
   python3 book.py   # gera build/interior.html e build/capa.html
   node render.js    # gera os PDFs (precisa do Playwright + Chromium)
   ```
2. Se mudar o número de páginas, a lombada da capa é recalculada sozinha.

## Configurações no KDP (kdp.amazon.com → Criar → Livro de capa comum)

- **Idioma:** Português
- **Categoria:** Infantil → Atividades / Livros de colorir
- **ISBN:** use o ISBN gratuito do KDP
- **Tinta e papel:** Tinta preta e papel branco
- **Tamanho:** 8,5 x 11 pol. (21,59 x 27,94 cm)
- **Sangria:** **Sem sangria**
- **Acabamento da capa:** Fosco (recomendado para livro infantil)
- **Miolo:** enviar `build/interior.pdf`
- **Capa:** "Enviar uma capa que você já tem" → `build/capa.pdf`
  - O KDP coloca o código de barras sozinho no retângulo branco da contracapa
- **Conteúdo gerado por IA:** o KDP pergunta isso. As ilustrações e os textos foram criados com o Claude (IA), então responda **Sim** e informe o tipo de conteúdo (imagens e texto). É obrigatório.
- Use o **Visualizador on-line** do KDP para conferir tudo antes de publicar.

## Código

- `src/art.py`: personagens e elementos de cenário, desenhados como SVG vetorial
- `src/scenes.py`: ilustrações de página inteira
- `src/book.py`: textos, diagramação do miolo e da capa
- `src/config.py`: título, autor e ano
- `fonts/`: Fredoka e Nunito (SIL Open Font License, uso comercial permitido)
