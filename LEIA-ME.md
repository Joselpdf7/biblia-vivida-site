# Site do Bíblia Vívida

Site estático em PT, EN e ES: página inicial, Suporte, Política de Privacidade e Termos de Uso.

- Gerar: `python3 build.py`. O comando regrava a pasta `docs/` e informa quantas pendências ainda existem.
- Ver localmente: `python3 -m http.server 8765 -d docs` e abrir http://localhost:8765
- Publicar: o GitHub Pages publica a pasta `docs/` da branch `main` a cada push (https://joselpdf7.github.io/biblia-vivida-site/). Rode `python3 build.py` antes de commitar.

## Site no ar (Cloudflare Pages, projeto `vividbible`)
- https://vividbible.app: domínio principal, abre no idioma do navegador (padrão: inglês)
- https://bibliavivida.com: abre sempre em português
- `www.` dos dois domínios também funciona. Os registros DNS são CNAMEs para `vividbible.pages.dev`.
- Para atualizar o site:

  ```bash
  python3 build.py && npx wrangler@3.114.0 pages deploy docs --project-name vividbible --branch main
  ```

  O Cloudflare não está ligado ao GitHub; o push só atualiza o GitHub Pages.

## URLs para a App Store Connect
- Support URL: https://vividbible.app/en/support (PT: https://vividbible.app/pt/suporte · ES: https://vividbible.app/es/soporte)
- Privacy Policy URL: https://vividbible.app/en/privacy (PT: https://vividbible.app/pt/privacidade · ES: https://vividbible.app/es/privacidad)
- Marketing URL: https://vividbible.app

## Pendências antes de publicar (aparecem em amarelo no site)
1. Preencher `CONFIG` em `build.py`: domínio, e-mail de suporte, razão social, CNPJ, cidade do foro e, depois, o link da App Store.
2. Política de Privacidade:
   - confirmar com o desenvolvimento se o app usa métricas ou relatório de falhas;
   - nomear o provedor de IA, se houver;
   - indicar o encarregado de dados (DPO).
3. Ajustar a política ao escopo real da versão 1. Se conta, comunidade e IA ficarem para depois, as seções "opcionais" podem continuar, porque estão redigidas como "quando disponíveis".
4. Revisão jurídica dos Termos e da Política. São um rascunho técnico, não um parecer.
5. Assinatura em inglês e espanhol: o kit de marca diz que a versão inglesa ainda não foi aprovada, por isso EN e ES aparecem sem assinatura. O nome usado em ES ("Bíblia Vívida") também precisa ser confirmado.
6. Os prints do app são da rodada de 15/11/2026 no navegador e estão em português. Trocar por capturas da versão final, em cada idioma, quando houver build.

## Referências de layout (Mobbin)
- Superpower e Jeton: navegação em pílula e herói central com o aparelho.
- Monarch: passos distribuídos em volta do aparelho.
- Fluz e PamPam: títulos com serifa e grade de recursos.

As cores, o logo e o símbolo vêm do kit de marca aprovado (`identidade/kit-estilo` no OneDrive).
