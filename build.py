#!/usr/bin/env python3
"""Gera o site estático do Bíblia Vívida em docs/ (PT, EN, ES).

Uso:  python3 build.py
Edite CONFIG abaixo e rode de novo. Campos vazios aparecem destacados em amarelo
no site, de propósito, para não irem ao ar sem preenchimento.
"""
from pathlib import Path
import html

# ---------------------------------------------------------------------------
# Preencha antes de publicar
# ---------------------------------------------------------------------------
CONFIG = {
    "dominio": "vividbible.app",  # domínio principal (sem https://); bibliavivida.com abre em PT
    "email": "",            # ex.: suporte@bibliavivida.app
    "empresa": "",          # razão social de quem publica o app (titular da conta Apple)
    "cnpj": "",             # CNPJ da empresa
    "cidade_foro": "",      # ex.: São Paulo/SP
    "app_store_url": "",    # link da App Store quando o app for aprovado
}
ATUALIZADO = {"pt": "15 de novembro de 2026", "en": "November 15, 2026", "es": "15 de noviembre de 2026"}

ROOT = Path(__file__).parent / "docs"

PAGINAS = {  # chave interna -> nome de arquivo por idioma
    "home": {"pt": "index.html", "en": "index.html", "es": "index.html"},
    "suporte": {"pt": "suporte.html", "en": "support.html", "es": "soporte.html"},
    "privacidade": {"pt": "privacidade.html", "en": "privacy.html", "es": "privacidad.html"},
    "termos": {"pt": "termos.html", "en": "terms.html", "es": "terminos.html"},
}
LANG_ATTR = {"pt": "pt-BR", "en": "en", "es": "es"}
NOME = {"pt": "Bíblia Vívida", "en": "Vivid Bible", "es": "Bíblia Vívida"}


def P(chave, lang):
    """Valor do CONFIG ou marcador visível de pendência."""
    v = CONFIG.get(chave, "").strip()
    if v:
        return html.escape(v)
    rotulo = {
        "pt": {"dominio": "DOMÍNIO", "email": "E-MAIL DE SUPORTE", "empresa": "RAZÃO SOCIAL", "cnpj": "CNPJ", "cidade_foro": "CIDADE DO FORO"},
        "en": {"dominio": "DOMAIN", "email": "SUPPORT EMAIL", "empresa": "LEGAL ENTITY", "cnpj": "CNPJ", "cidade_foro": "VENUE CITY"},
        "es": {"dominio": "DOMINIO", "email": "CORREO DE SOPORTE", "empresa": "RAZÓN SOCIAL", "cnpj": "CNPJ", "cidade_foro": "CIUDAD DEL FORO"},
    }[lang].get(chave, chave.upper())
    return f'<mark class="pendente">[{rotulo}]</mark>'


def EMAIL(lang):
    v = CONFIG["email"].strip()
    if v:
        e = html.escape(v)
        return f'<a href="mailto:{e}">{e}</a>'
    return P("email", lang)


# ---------------------------------------------------------------------------
# Textos de interface
# ---------------------------------------------------------------------------
UI = {
    "pt": {
        "nav": {"home": "Início", "suporte": "Suporte", "privacidade": "Privacidade", "termos": "Termos"},
        "pular": "Pular para o conteúdo",
        "rodape": "Feito com cuidado para quem quer entender a Bíblia de perto.",
        "atualizado": "Última atualização",
        "em_breve": "Em breve na App Store",
        "baixar": "Baixar na App Store",
    },
    "en": {
        "nav": {"home": "Home", "suporte": "Support", "privacidade": "Privacy", "termos": "Terms"},
        "pular": "Skip to content",
        "rodape": "Made with care for anyone who wants to understand the Bible up close.",
        "atualizado": "Last updated",
        "em_breve": "Coming soon to the App Store",
        "baixar": "Download on the App Store",
    },
    "es": {
        "nav": {"home": "Inicio", "suporte": "Soporte", "privacidade": "Privacidad", "termos": "Términos"},
        "pular": "Saltar al contenido",
        "rodape": "Hecho con cuidado para quien quiere entender la Biblia de cerca.",
        "atualizado": "Última actualización",
        "em_breve": "Próximamente en la App Store",
        "baixar": "Descargar en la App Store",
    },
}

ICONES = {
    "livro": '<svg viewBox="0 0 24 24"><path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5z"/><path d="M4 20.5A2.5 2.5 0 0 0 6.5 23H20v-5"/></svg>',
    "som": '<svg viewBox="0 0 24 24"><path d="M11 5 6 9H3v6h3l5 4z"/><path d="M15.5 8.5a5 5 0 0 1 0 7"/><path d="M18.5 5.5a9 9 0 0 1 0 13"/></svg>',
    "video": '<svg viewBox="0 0 24 24"><rect x="3" y="5" width="13" height="14" rx="2"/><path d="m16 10 5-3v10l-5-3z"/></svg>',
    "marcador": '<svg viewBox="0 0 24 24"><path d="M6 3h12v18l-6-4-6 4z"/></svg>',
    "diario": '<svg viewBox="0 0 24 24"><path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/></svg>',
    "sino": '<svg viewBox="0 0 24 24"><path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/></svg>',
}


LIVROS = {
    "pt": ["Gênesis", "Êxodo", "Salmos", "Provérbios", "Isaías", "Mateus", "João", "Atos", "Romanos", "Hebreus", "Tiago", "Apocalipse"],
    "en": ["Genesis", "Exodus", "Psalms", "Proverbs", "Isaiah", "Matthew", "John", "Acts", "Romans", "Hebrews", "James", "Revelation"],
    "es": ["Génesis", "Éxodo", "Salmos", "Proverbios", "Isaías", "Mateo", "Juan", "Hechos", "Romanos", "Hebreos", "Santiago", "Apocalipsis"],
}

# ---------------------------------------------------------------------------
# Conteúdo: página inicial
# ---------------------------------------------------------------------------
def home(lang):
    T = {
        "pt": dict(
            title="Bíblia Vívida — Histórias que você vê. Lições que você leva.",
            desc="Microlições bíblicas para ler em poucos minutos: a cena, o versículo, o que levar e como praticar. Em português, inglês e espanhol.",
            assinatura="Histórias que você vê. Lições que você leva.",
            lead="Microlições bíblicas para ler em poucos minutos: a cena, o versículo revelado, o que levar e como praticar. Em português, inglês e espanhol.",
            como="Como funciona",
            selo="Para iPhone",
            r_como="Como funciona", t_como="Uma ideia por vez, do texto para a vida.",
            i_como="Cada cartão percorre o mesmo caminho curto. Você entende a passagem, vê o versículo e sai com algo concreto para viver hoje.",
            passos=[("A cena", "O contexto da passagem em poucas linhas: quem, onde e o que estava em jogo."),
                    ("Revelar", "O versículo aparece no momento certo, com a referência completa."),
                    ("Levar", "O princípio que atravessa os séculos, sem exagero e sem fórmula pronta."),
                    ("Praticar", "Um passo simples para colocar a ideia em prática ainda hoje.")],
            r_telas="O aplicativo", t_telas="Limpo, calmo e feito para ler.",
            i_telas="Texto em primeiro plano, tamanho de fonte ajustável e nada competindo com a leitura.",
            telas=[("print-leitor.jpg", "Leitor com revelação do versículo"), ("print-salmos.jpg", "Livros e jornadas temáticas"),
                   ("print-video.jpg", "Histórias para ver e ouvir"), ("print-scanner.jpg", "Da página para a vida")],
            r_rec="Recursos", t_rec="Tudo o que ajuda a ler, lembrar e praticar.",
            recursos=[("livro", "Bíblia offline", "Consulte os 66 livros em português, inglês e espanhol, mesmo sem internet."),
                      ("som", "Ouça", "Escute cartões e livros em sequência, no seu ritmo."),
                      ("video", "Histórias animadas", "Episódios curtos que mostram a cena antes da lição."),
                      ("marcador", "Coleções e salvos", "Guarde passagens e monte coleções para voltar depois."),
                      ("diario", "Diário e histórico", "Escreva reflexões e acompanhe o que você já leu."),
                      ("sino", "Lembretes", "Escolha o horário e receba um convite discreto para ler.")],
            r_vid="Histórias para ver", t_vid="A cena antes da lição.",
            i_vid="Episódios curtos em animação 3D contam passagens bíblicas com fidelidade ao texto e linguagem de hoje. Você assiste, entende o contexto e leva a lição com você.",
            nota_vid="Representação artística criada com auxílio de inteligência artificial. O texto bíblico citado é identificado em cada episódio.",
            t_fim="Comece pela próxima página.",
            i_fim="Alguns minutos por dia, uma ideia por vez.",
        ),
        "en": dict(
            title="Vivid Bible — Short Bible lessons for everyday life",
            desc="Bible micro-lessons you can read in a few minutes: the scene, the verse, the takeaway and a practice. In English, Portuguese and Spanish.",
            assinatura="",
            lead="Bible micro-lessons you can read in a few minutes: the scene, the revealed verse, the takeaway and a simple practice. In English, Portuguese and Spanish.",
            como="How it works",
            selo="For iPhone",
            r_como="How it works", t_como="One idea at a time, from the page to your life.",
            i_como="Every card follows the same short path. You understand the passage, see the verse and leave with something concrete to live today.",
            passos=[("The scene", "The context of the passage in a few lines: who, where and what was at stake."),
                    ("Reveal", "The verse appears at the right moment, with its full reference."),
                    ("Take away", "The principle that crosses the centuries, without hype or ready-made formulas."),
                    ("Practice", "One simple step to put the idea into practice today.")],
            r_telas="The app", t_telas="Clean, calm and made for reading.",
            i_telas="Text comes first, font size is adjustable and nothing competes with your reading.",
            telas=[("print-leitor.jpg", "Reader with verse reveal"), ("print-salmos.jpg", "Books and themed journeys"),
                   ("print-video.jpg", "Stories to watch and hear"), ("print-scanner.jpg", "From the page to life")],
            r_rec="Features", t_rec="Everything that helps you read, remember and practice.",
            recursos=[("livro", "Offline Bible", "Browse all 66 books in English, Portuguese and Spanish, even without internet."),
                      ("som", "Listen", "Hear cards and books in sequence, at your own pace."),
                      ("video", "Animated stories", "Short episodes that show the scene before the lesson."),
                      ("marcador", "Collections and saved", "Save passages and build collections to come back to."),
                      ("diario", "Journal and history", "Write reflections and keep track of what you have read."),
                      ("sino", "Reminders", "Pick a time and get a gentle invitation to read.")],
            r_vid="Stories to watch", t_vid="The scene before the lesson.",
            i_vid="Short 3D-animated episodes tell Bible passages faithfully, in today's language. You watch, understand the context and carry the lesson with you.",
            nota_vid="Artistic representation created with the help of artificial intelligence. The Bible text quoted is identified in each episode.",
            t_fim="Start with the next page.",
            i_fim="A few minutes a day, one idea at a time.",
        ),
        "es": dict(
            title="Bíblia Vívida — Microlecciones bíblicas para la vida diaria",
            desc="Microlecciones bíblicas para leer en pocos minutos: la escena, el versículo, lo que te llevas y cómo practicarlo. En español, portugués e inglés.",
            assinatura="",
            lead="Microlecciones bíblicas para leer en pocos minutos: la escena, el versículo revelado, lo que te llevas y cómo practicarlo. En español, portugués e inglés.",
            como="Cómo funciona",
            selo="Para iPhone",
            r_como="Cómo funciona", t_como="Una idea a la vez, del texto a la vida.",
            i_como="Cada tarjeta recorre el mismo camino corto. Entiendes el pasaje, ves el versículo y sales con algo concreto para vivir hoy.",
            passos=[("La escena", "El contexto del pasaje en pocas líneas: quién, dónde y qué estaba en juego."),
                    ("Revelar", "El versículo aparece en el momento justo, con su referencia completa."),
                    ("Llevar", "El principio que atraviesa los siglos, sin exageraciones ni fórmulas hechas."),
                    ("Practicar", "Un paso sencillo para poner la idea en práctica hoy mismo.")],
            r_telas="La aplicación", t_telas="Limpia, serena y hecha para leer.",
            i_telas="El texto en primer plano, tamaño de letra ajustable y nada que compita con la lectura.",
            telas=[("print-leitor.jpg", "Lector con revelación del versículo"), ("print-salmos.jpg", "Libros y recorridos temáticos"),
                   ("print-video.jpg", "Historias para ver y escuchar"), ("print-scanner.jpg", "De la página a la vida")],
            r_rec="Funciones", t_rec="Todo lo que te ayuda a leer, recordar y practicar.",
            recursos=[("livro", "Biblia sin conexión", "Consulta los 66 libros en español, portugués e inglés, incluso sin internet."),
                      ("som", "Escucha", "Oye tarjetas y libros en secuencia, a tu ritmo."),
                      ("video", "Historias animadas", "Episodios cortos que muestran la escena antes de la lección."),
                      ("marcador", "Colecciones y guardados", "Guarda pasajes y arma colecciones para volver después."),
                      ("diario", "Diario e historial", "Escribe reflexiones y sigue lo que ya leíste."),
                      ("sino", "Recordatorios", "Elige la hora y recibe una invitación discreta a leer.")],
            r_vid="Historias para ver", t_vid="La escena antes de la lección.",
            i_vid="Episodios cortos en animación 3D cuentan pasajes bíblicos con fidelidad al texto y lenguaje de hoy. Miras, entiendes el contexto y te llevas la lección.",
            nota_vid="Representación artística creada con ayuda de inteligencia artificial. El texto bíblico citado se identifica en cada episodio.",
            t_fim="Empieza por la próxima página.",
            i_fim="Unos minutos al día, una idea a la vez.",
        ),
    }[lang]
    u = UI[lang]

    if CONFIG["app_store_url"].strip():
        cta = f'<a class="botao" href="{html.escape(CONFIG["app_store_url"])}">{u["baixar"]}</a>'
    else:
        cta = f'<span class="botao" aria-disabled="true">{u["em_breve"]}</span>'

    assin = f'<p class="assinatura">{T["assinatura"]}</p>' if T["assinatura"] else ""
    passos = "".join(f'<div class="passo"><h3>{a}</h3><p>{b}</p></div>' for a, b in T["passos"])
    telas = "".join(
        f'<div class="tela"><figure><div class="aparelho"><img src="../assets/img/{img}" alt="{cap}" width="440" height="956" loading="lazy"></div>'
        f'<figcaption>{cap}</figcaption></figure></div>' for img, cap in T["telas"])
    recursos = "".join(
        f'<div class="recurso"><div class="icone" aria-hidden="true">{ICONES[ic]}</div><h3>{a}</h3><p>{b}</p></div>'
        for ic, a, b in T["recursos"])

    p_esq = "".join(f'<div class="passo"><span class="num">{i}</span><h3>{a}</h3><p>{b}</p></div>' for i, (a, b) in enumerate(T["passos"][:2], 1))
    p_dir = "".join(f'<div class="passo"><span class="num">{i}</span><h3>{a}</h3><p>{b}</p></div>' for i, (a, b) in enumerate(T["passos"][2:], 3))
    rec = T["recursos"]
    bento = (
        f'<div class="bloco grande escuro-b"><div class="icone" aria-hidden="true">{ICONES[rec[0][0]]}</div><h3>{rec[0][1]}</h3><p>{rec[0][2]}</p>'
        f'<div class="livros" aria-hidden="true">' + "".join(f"<span>{n}</span>" for n in LIVROS[lang]) + '</div></div>'
        + "".join(f'<div class="bloco"><div class="icone" aria-hidden="true">{ICONES[ic]}</div><h3>{a}</h3><p>{b}</p></div>' for ic, a, b in rec[1:])
    )

    corpo = f"""
<section class="heroi" aria-labelledby="h-heroi">
  <div class="wrap">
    <img class="simbolo revela" src="../assets/img/simbolo.png" alt="" width="640" height="640">
    <h1 id="h-heroi" class="revela">{NOME[lang]}</h1>
    {assin}
    <p class="lead revela">{T["lead"]}</p>
    <div class="ctas revela">{cta}<a class="botao secundario" href="#como">{T["como"]}</a></div>
    <p class="selo">{T["selo"]}</p>
  </div>
  <div class="palco" aria-hidden="true">
    <div class="aparelho lado"><img src="../assets/img/print-salmos.jpg" alt="" width="440" height="956"></div>
    <div class="aparelho centro"><img src="../assets/img/print-leitor.jpg" alt="" width="440" height="956"></div>
    <div class="aparelho lado"><img src="../assets/img/print-video.jpg" alt="" width="440" height="956"></div>
  </div>
</section>

<section id="como" aria-labelledby="h-como">
  <div class="wrap">
    <div class="cabeca-secao">
      <p class="rotulo">{T["r_como"]}</p>
      <h2 class="titulo-secao" id="h-como">{T["t_como"]}</h2>
      <p class="intro">{T["i_como"]}</p>
    </div>
    <div class="orbita">
      <div class="coluna">{p_esq}</div>
      <div class="aparelho"><img src="../assets/img/print-leitor.jpg" alt="{T["telas"][0][1]}" width="440" height="956" loading="lazy"></div>
      <div class="coluna">{p_dir}</div>
    </div>
  </div>
</section>

<section class="escuro" aria-labelledby="h-telas">
  <div class="wrap">
    <div class="cabeca-secao">
      <p class="rotulo">{T["r_telas"]}</p>
      <h2 class="titulo-secao" id="h-telas">{T["t_telas"]}</h2>
      <p class="intro">{T["i_telas"]}</p>
    </div>
  </div>
  <div class="telas" tabindex="0" role="region" aria-label="{T["r_telas"]}">{telas}</div>
</section>

<section aria-labelledby="h-rec">
  <div class="wrap">
    <div class="cabeca-secao">
      <p class="rotulo">{T["r_rec"]}</p>
      <h2 class="titulo-secao" id="h-rec">{T["t_rec"]}</h2>
    </div>
    <div class="bento">{bento}</div>
  </div>
</section>

<section class="marfim" aria-labelledby="h-vid">
  <div class="wrap videos">
    <div class="aparelho"><img src="../assets/img/print-video.jpg" alt="" width="440" height="956" loading="lazy"></div>
    <div>
      <p class="rotulo">{T["r_vid"]}</p>
      <h2 class="titulo-secao" id="h-vid">{T["t_vid"]}</h2>
      <p class="intro">{T["i_vid"]}</p>
      <p class="nota">{T["nota_vid"]}</p>
    </div>
  </div>
</section>

<section class="escuro chamada" aria-labelledby="h-fim">
  <div class="wrap">
    <img class="simbolo-peq" src="../assets/img/simbolo.png" alt="" width="140" height="140">
    <h2 class="titulo-secao" id="h-fim">{T["t_fim"]}</h2>
    <p class="intro">{T["i_fim"]}</p>
    <div class="ctas">{cta}</div>
  </div>
</section>
"""
    return T["title"], T["desc"], corpo


# ---------------------------------------------------------------------------
# Conteúdo: suporte
# ---------------------------------------------------------------------------
def suporte(lang):
    E = EMAIL(lang)
    T = {
        "pt": dict(
            title="Suporte", sub="Respostas rápidas e um jeito fácil de falar com a gente.",
            faq_t="Perguntas frequentes",
            faq=[
                ("Preciso de internet para usar o app?", "Não para ler. A consulta à Bíblia e os cartões já baixados funcionam offline. Vídeos e alguns recursos opcionais precisam de conexão."),
                ("Como mudo o tamanho do texto?", "No leitor, toque em <strong>Aa</strong> no topo da tela e escolha o tamanho mais confortável. A preferência fica salva."),
                ("Como ativo ou desativo os lembretes?", "Abra <strong>Ajustes › Lembretes</strong> e escolha o horário. Você também pode desligar as notificações do app em <strong>Ajustes do iPhone › Notificações</strong>."),
                ("Como assino o Pro?", "Toque em qualquer conteúdo marcado como Pro e siga as instruções. O pagamento é feito pela sua conta Apple, e o preço aparece antes da confirmação."),
                ("Como cancelo a assinatura?", "As assinaturas são gerenciadas pela Apple. No iPhone, abra <strong>Ajustes › [seu nome] › Assinaturas</strong>, escolha Bíblia Vívida e toque em Cancelar. O acesso continua até o fim do período já pago."),
                ("Troquei de iPhone. Como recupero o Pro?", "Entre com o mesmo Apple ID, abra o app e toque em <strong>Restaurar compras</strong> na tela do Pro ou em Ajustes."),
                ("Quero um reembolso.", "Reembolsos de compras feitas pela App Store são analisados pela Apple. Solicite em <a href=\"https://reportaproblem.apple.com\">reportaproblem.apple.com</a>."),
                ("Onde ficam minhas anotações e salvos?", "No seu aparelho. Se você apagar o app sem ter ativado uma cópia de segurança, essas informações são removidas junto."),
                ("Como apago meus dados?", "Apagar o app remove os dados locais. Se você criou uma conta, use <strong>Ajustes › Conta › Excluir conta</strong> ou escreva para nós. Detalhes na <a href=\"privacidade.html\">Política de Privacidade</a>."),
                ("Encontrei um erro no texto ou uma informação imprecisa.", "Obrigado por avisar. Escreva para nós com o nome do livro e do cartão ou mande um print da tela."),
            ],
            contato_t="Fale com a gente",
            contato=f"Escreva para {E}. Conte o modelo do iPhone, a versão do iOS e, se possível, mande um print da tela. Respondemos em português, inglês ou espanhol.",
        ),
        "en": dict(
            title="Support", sub="Quick answers and an easy way to reach us.",
            faq_t="Frequently asked questions",
            faq=[
                ("Do I need internet to use the app?", "Not for reading. The Bible and the cards already downloaded work offline. Videos and some optional features need a connection."),
                ("How do I change the text size?", "In the reader, tap <strong>Aa</strong> at the top of the screen and choose a comfortable size. Your choice is saved."),
                ("How do I turn reminders on or off?", "Open <strong>Settings › Reminders</strong> and pick a time. You can also turn off the app's notifications in <strong>iPhone Settings › Notifications</strong>."),
                ("How do I subscribe to Pro?", "Tap any content marked Pro and follow the steps. Payment is handled by your Apple account, and the price is shown before you confirm."),
                ("How do I cancel my subscription?", "Subscriptions are managed by Apple. On your iPhone, open <strong>Settings › [your name] › Subscriptions</strong>, choose Vivid Bible and tap Cancel. Access continues until the end of the period you already paid for."),
                ("I got a new iPhone. How do I get Pro back?", "Sign in with the same Apple ID, open the app and tap <strong>Restore purchases</strong> on the Pro screen or in Settings."),
                ("I would like a refund.", "Refunds for App Store purchases are handled by Apple. Request one at <a href=\"https://reportaproblem.apple.com\">reportaproblem.apple.com</a>."),
                ("Where are my notes and saved items stored?", "On your device. If you delete the app without having turned on a backup, this information is removed with it."),
                ("How do I delete my data?", "Deleting the app removes local data. If you created an account, go to <strong>Settings › Account › Delete account</strong> or write to us. See the <a href=\"privacy.html\">Privacy Policy</a> for details."),
                ("I found a mistake or an inaccurate statement.", "Thank you for letting us know. Write to us with the book and card name, or send a screenshot."),
            ],
            contato_t="Contact us",
            contato=f"Email {E}. Tell us your iPhone model and iOS version and, if possible, attach a screenshot. We answer in English, Portuguese or Spanish.",
        ),
        "es": dict(
            title="Soporte", sub="Respuestas rápidas y una forma fácil de escribirnos.",
            faq_t="Preguntas frecuentes",
            faq=[
                ("¿Necesito internet para usar la app?", "No para leer. La Biblia y las tarjetas ya descargadas funcionan sin conexión. Los videos y algunas funciones opcionales necesitan conexión."),
                ("¿Cómo cambio el tamaño del texto?", "En el lector, toca <strong>Aa</strong> en la parte superior y elige el tamaño más cómodo. La preferencia se guarda."),
                ("¿Cómo activo o desactivo los recordatorios?", "Abre <strong>Ajustes › Recordatorios</strong> y elige la hora. También puedes desactivar las notificaciones en <strong>Ajustes del iPhone › Notificaciones</strong>."),
                ("¿Cómo me suscribo a Pro?", "Toca cualquier contenido marcado como Pro y sigue los pasos. El pago se hace con tu cuenta de Apple y el precio aparece antes de confirmar."),
                ("¿Cómo cancelo la suscripción?", "Las suscripciones las gestiona Apple. En el iPhone, abre <strong>Ajustes › [tu nombre] › Suscripciones</strong>, elige Bíblia Vívida y toca Cancelar. El acceso continúa hasta el final del período ya pagado."),
                ("Cambié de iPhone. ¿Cómo recupero Pro?", "Inicia sesión con el mismo Apple ID, abre la app y toca <strong>Restaurar compras</strong> en la pantalla Pro o en Ajustes."),
                ("Quiero un reembolso.", "Los reembolsos de compras en la App Store los gestiona Apple. Solicítalo en <a href=\"https://reportaproblem.apple.com\">reportaproblem.apple.com</a>."),
                ("¿Dónde se guardan mis notas y guardados?", "En tu dispositivo. Si borras la app sin haber activado una copia de seguridad, esa información se elimina con ella."),
                ("¿Cómo borro mis datos?", "Borrar la app elimina los datos locales. Si creaste una cuenta, ve a <strong>Ajustes › Cuenta › Eliminar cuenta</strong> o escríbenos. Más detalles en la <a href=\"privacidad.html\">Política de Privacidad</a>."),
                ("Encontré un error o una información imprecisa.", "Gracias por avisarnos. Escríbenos con el nombre del libro y de la tarjeta, o envía una captura de pantalla."),
            ],
            contato_t="Escríbenos",
            contato=f"Escribe a {E}. Cuéntanos el modelo de iPhone y la versión de iOS y, si puedes, adjunta una captura de pantalla. Respondemos en español, portugués o inglés.",
        ),
    }[lang]
    faq = "".join(f"<details><summary>{q}</summary><div><p>{a}</p></div></details>" for q, a in T["faq"])
    corpo = f"""
<header class="cabecalho-pagina"><div class="wrap"><h1>{T["title"]}</h1><p>{T["sub"]}</p></div></header>
<div class="texto">
  <h2 style="margin-top:0">{T["faq_t"]}</h2>
  <div class="faq">{faq}</div>
  <div class="contato"><h2>{T["contato_t"]}</h2><p style="margin:0">{T["contato"]}</p></div>
</div>
"""
    return f'{T["title"]} — {NOME[lang]}', T["sub"], corpo


# ---------------------------------------------------------------------------
# Conteúdo: política de privacidade
# ---------------------------------------------------------------------------
def privacidade(lang):
    E, EMP, CNPJ = EMAIL(lang), P("empresa", lang), P("cnpj", lang)
    secoes = {
        "pt": [
            ("Quem somos", f"""<p>O aplicativo {NOME[lang]} (“app”) é oferecido por {EMP}, CNPJ {CNPJ} (“nós”). Somos responsáveis pelo tratamento dos dados pessoais descritos nesta política, nos termos da Lei Geral de Proteção de Dados (Lei 13.709/2018, “LGPD”).</p>"""),
            ("Resumo", """<ul>
<li>Você pode ler, ouvir, salvar e anotar sem criar conta. Esses dados ficam no seu aparelho.</li>
<li>Pagamentos são processados pela Apple. Nunca recebemos o número do seu cartão.</li>
<li>Recursos que enviam dados para a nuvem são opcionais e só funcionam com a sua ação ou consentimento.</li>
<li>Não vendemos seus dados pessoais.</li>
</ul>"""),
            ("Dados que ficam no seu aparelho", """<p>Progresso de leitura, cartões salvos, coleções, histórico, diário, conquistas, preferências (idioma, tamanho de fonte, horário dos lembretes) e passagens registradas pelo scanner são guardados localmente no iPhone. Não temos acesso a essas informações enquanto você não ativar uma cópia na nuvem.</p>"""),
            ("Assinatura e compras", """<p>A assinatura Pro é vendida pela App Store. A Apple processa o pagamento e nos informa apenas o status da compra. Usamos o serviço RevenueCat para validar assinaturas; ele recebe um identificador anônimo gerado pelo app e os dados da transação fornecidos pela Apple (produto, data, validade, país da loja). Base legal: execução de contrato.</p>"""),
            ("Lembretes e notificações", """<p>Os lembretes de leitura são agendados no próprio aparelho. Se você ativar recursos de comunidade, poderemos enviar notificações sobre interações com o seu conteúdo; para isso, guardamos um token de notificação do aparelho. Você pode desligar notificações a qualquer momento nos Ajustes do iPhone.</p>"""),
            ("Câmera e fotos", """<p>O scanner usa a câmera ou a galeria apenas quando você toca para fotografar ou escolher uma imagem. A foto serve para identificar a referência bíblica e não é enviada para nós, a menos que você ative o reconhecimento de texto por um serviço externo, descrito abaixo.</p>"""),
            ("Conta, cópia na nuvem e comunidade (opcionais)", """<p>Quando esses recursos estiverem disponíveis e você decidir usá-los, trataremos: e-mail ou identificador de login (incluindo “Iniciar sessão com a Apple”), nome de exibição, foto de perfil e capa, a cópia dos seus dados de leitura, e o que você publicar em grupos ou jornadas compartilhadas. Conteúdos publicados ficam visíveis para os participantes escolhidos e podem ser moderados e denunciados. Base legal: execução de contrato e consentimento. Os dados ficam armazenados no provedor de banco de dados descrito na seção “Prestadores de serviço”.</p>"""),
            ("Recursos de inteligência artificial (opcionais)", """<p>Recursos como reescrita de texto, geração de imagem ou leitura de texto em fotos (OCR) só funcionam depois do seu consentimento explícito. O conteúdo que você enviar é processado por um provedor de IA apenas para gerar a resposta e não é usado por nós para treinar modelos. Há limites de uso, e você pode desativar o recurso a qualquer momento.</p>"""),
            ("Novidades por e-mail", """<p>Se você pedir para receber novidades, guardaremos seu e-mail para esse fim. Cada mensagem tem um link para cancelar o recebimento. Base legal: consentimento.</p>"""),
            ("Métricas de uso e relatórios de erro", """<p><mark class="pendente">[CONFIRMAR COM O DESENVOLVIMENTO: o app usa algum serviço de métricas ou de relatório de falhas? Se sim, nomear o serviço, os dados coletados e se são vinculados à pessoa. Se não, escrever: “O app não usa ferramentas de métricas de terceiros nem publicidade.”]</mark></p>"""),
            ("Prestadores de serviço", """<p>Compartilhamos dados somente com fornecedores necessários para o funcionamento do app, que os tratam conforme nossas instruções:</p>
<ul>
<li><strong>Apple</strong>: distribuição do app, pagamentos, login com a Apple e entrega de notificações.</li>
<li><strong>RevenueCat</strong>: validação de assinaturas.</li>
<li><strong>Supabase</strong>: banco de dados e armazenamento de conta, cópia na nuvem e comunidade, quando ativados.</li>
<li><strong>Provedor de IA</strong> <mark class="pendente">[NOME]</mark>: somente se você ativar recursos de IA.</li>
</ul>
<p>Também podemos compartilhar dados quando exigido por lei ou ordem de autoridade competente.</p>"""),
            ("Transferência internacional", """<p>Alguns fornecedores armazenam dados fora do Brasil, inclusive nos Estados Unidos. Nesses casos, adotamos as salvaguardas previstas na LGPD, como cláusulas contratuais.</p>"""),
            ("Por quanto tempo guardamos", """<p>Dados locais permanecem no aparelho até você apagá-los ou remover o app. Dados de conta são mantidos enquanto a conta existir. Ao excluir a conta, apagamos ou anonimizamos os dados em até 30 dias, exceto o que precisarmos guardar para cumprir obrigações legais.</p>"""),
            ("Seus direitos", f"""<p>Você pode pedir confirmação de tratamento, acesso, correção, portabilidade, anonimização ou eliminação dos seus dados, informações sobre compartilhamento e revogação do consentimento. A exclusão da conta pode ser feita no próprio app, em <strong>Ajustes › Conta › Excluir conta</strong>. Para os demais pedidos, escreva para {E}. Você também pode apresentar reclamação à Autoridade Nacional de Proteção de Dados (ANPD).</p>"""),
            ("Crianças", """<p>O app não é direcionado a crianças menores de 13 anos e não coleta intencionalmente dados delas. Recursos de conta e comunidade exigem idade mínima de 13 anos ou autorização do responsável, conforme a lei aplicável.</p>"""),
            ("Segurança", """<p>Usamos conexões criptografadas, controle de acesso e outras medidas razoáveis para proteger seus dados. Nenhum sistema é totalmente imune a falhas; se ocorrer um incidente relevante, avisaremos você e as autoridades conforme a lei.</p>"""),
            ("Alterações", """<p>Podemos atualizar esta política. A data no topo indica a versão vigente. Mudanças relevantes serão avisadas no app.</p>"""),
            ("Contato e encarregado", f"""<p>Encarregado pelo tratamento de dados: <mark class="pendente">[NOME DO ENCARREGADO]</mark>. Contato: {E}.</p>"""),
        ],
        "en": [
            ("Who we are", f"""<p>The {NOME[lang]} app (the “app”) is provided by {EMP}, Brazilian company registration (CNPJ) {CNPJ} (“we”, “us”). We are the controller of the personal data described in this policy under Brazil’s General Data Protection Law (LGPD) and other applicable laws.</p>"""),
            ("Summary", """<ul>
<li>You can read, listen, save and take notes without an account. That data stays on your device.</li>
<li>Payments are processed by Apple. We never receive your card number.</li>
<li>Features that send data to the cloud are optional and only work with your action or consent.</li>
<li>We do not sell your personal data.</li>
</ul>"""),
            ("Data that stays on your device", """<p>Reading progress, saved cards, collections, history, journal, achievements, preferences (language, font size, reminder time) and passages recorded with the scanner are stored locally on your iPhone. We cannot access this information unless you turn on a cloud backup.</p>"""),
            ("Subscription and purchases", """<p>The Pro subscription is sold through the App Store. Apple processes the payment and only tells us the purchase status. We use RevenueCat to validate subscriptions; it receives an anonymous identifier generated by the app and the transaction data provided by Apple (product, date, expiry, store country). Legal basis: performance of a contract.</p>"""),
            ("Reminders and notifications", """<p>Reading reminders are scheduled on the device itself. If you turn on community features, we may send notifications about interactions with your content; to do so we store a device notification token. You can turn notifications off at any time in iPhone Settings.</p>"""),
            ("Camera and photos", """<p>The scanner uses the camera or photo library only when you tap to take or choose a picture. The photo is used to identify the Bible reference and is not sent to us, unless you turn on text recognition by an external service, described below.</p>"""),
            ("Account, cloud backup and community (optional)", """<p>When these features are available and you choose to use them, we process: email or sign-in identifier (including Sign in with Apple), display name, profile and cover photos, the copy of your reading data, and what you post in groups or shared journeys. Posted content is visible to the participants you choose and may be moderated and reported. Legal basis: performance of a contract and consent. The data is stored with the database provider listed under “Service providers”.</p>"""),
            ("Artificial intelligence features (optional)", """<p>Features such as text rewriting, image generation or reading text in photos (OCR) only work after your explicit consent. The content you send is processed by an AI provider solely to produce the result and is not used by us to train models. Usage limits apply, and you can turn the feature off at any time.</p>"""),
            ("News by email", """<p>If you ask to receive news, we keep your email for that purpose. Every message has an unsubscribe link. Legal basis: consent.</p>"""),
            ("Usage analytics and crash reports", """<p><mark class="pendente">[CONFIRM WITH DEVELOPMENT: does the app use any analytics or crash-reporting service? If yes, name it, the data collected and whether it is linked to the person. If not, write: “The app does not use third-party analytics or advertising.”]</mark></p>"""),
            ("Service providers", """<p>We only share data with vendors needed to run the app, who process it on our instructions:</p>
<ul>
<li><strong>Apple</strong>: app distribution, payments, Sign in with Apple and notification delivery.</li>
<li><strong>RevenueCat</strong>: subscription validation.</li>
<li><strong>Supabase</strong>: database and storage for account, cloud backup and community, when turned on.</li>
<li><strong>AI provider</strong> <mark class="pendente">[NAME]</mark>: only if you turn on AI features.</li>
</ul>
<p>We may also share data when required by law or by order of a competent authority.</p>"""),
            ("International transfers", """<p>Some vendors store data outside Brazil, including in the United States. In those cases we use the safeguards provided by law, such as contractual clauses.</p>"""),
            ("How long we keep data", """<p>Local data stays on the device until you delete it or remove the app. Account data is kept while the account exists. When you delete your account, we delete or anonymize the data within 30 days, except what we must keep to meet legal obligations.</p>"""),
            ("Your rights", f"""<p>You may request confirmation of processing, access, correction, portability, anonymization or deletion of your data, information about sharing, and withdrawal of consent. Depending on where you live (for example in the EU, UK or California), you may have similar rights under local law. You can delete your account in the app under <strong>Settings › Account › Delete account</strong>. For other requests, email {E}. You may also complain to your data protection authority.</p>"""),
            ("Children", """<p>The app is not directed to children under 13 and does not knowingly collect their data. Account and community features require a minimum age of 13 or parental consent, as required by applicable law.</p>"""),
            ("Security", """<p>We use encrypted connections, access controls and other reasonable measures to protect your data. No system is completely immune to failures; if a relevant incident occurs, we will notify you and the authorities as required by law.</p>"""),
            ("Changes", """<p>We may update this policy. The date at the top shows the current version. Relevant changes will be announced in the app.</p>"""),
            ("Contact and data protection officer", f"""<p>Data protection officer: <mark class="pendente">[DPO NAME]</mark>. Contact: {E}.</p>"""),
        ],
        "es": [
            ("Quiénes somos", f"""<p>La aplicación {NOME[lang]} (la “app”) es ofrecida por {EMP}, registro de empresa brasileño (CNPJ) {CNPJ} (“nosotros”). Somos responsables del tratamiento de los datos personales descritos en esta política, conforme a la Ley General de Protección de Datos de Brasil (LGPD) y demás leyes aplicables.</p>"""),
            ("Resumen", """<ul>
<li>Puedes leer, escuchar, guardar y tomar notas sin crear una cuenta. Esos datos quedan en tu dispositivo.</li>
<li>Los pagos los procesa Apple. Nunca recibimos el número de tu tarjeta.</li>
<li>Las funciones que envían datos a la nube son opcionales y solo funcionan con tu acción o consentimiento.</li>
<li>No vendemos tus datos personales.</li>
</ul>"""),
            ("Datos que quedan en tu dispositivo", """<p>El progreso de lectura, tarjetas guardadas, colecciones, historial, diario, logros, preferencias (idioma, tamaño de letra, hora de recordatorios) y pasajes registrados con el escáner se guardan localmente en el iPhone. No tenemos acceso a esa información a menos que actives una copia en la nube.</p>"""),
            ("Suscripción y compras", """<p>La suscripción Pro se vende a través de la App Store. Apple procesa el pago y solo nos informa el estado de la compra. Usamos RevenueCat para validar suscripciones; recibe un identificador anónimo generado por la app y los datos de la transacción proporcionados por Apple (producto, fecha, vencimiento, país de la tienda). Base legal: ejecución de contrato.</p>"""),
            ("Recordatorios y notificaciones", """<p>Los recordatorios de lectura se programan en el propio dispositivo. Si activas funciones de comunidad, podemos enviarte notificaciones sobre interacciones con tu contenido; para ello guardamos un token de notificación del dispositivo. Puedes desactivar las notificaciones en cualquier momento en los Ajustes del iPhone.</p>"""),
            ("Cámara y fotos", """<p>El escáner usa la cámara o la galería solo cuando tocas para tomar o elegir una imagen. La foto sirve para identificar la referencia bíblica y no se nos envía, salvo que actives el reconocimiento de texto por un servicio externo, descrito abajo.</p>"""),
            ("Cuenta, copia en la nube y comunidad (opcionales)", """<p>Cuando estas funciones estén disponibles y decidas usarlas, trataremos: correo o identificador de inicio de sesión (incluido “Iniciar sesión con Apple”), nombre visible, foto de perfil y portada, la copia de tus datos de lectura y lo que publiques en grupos o recorridos compartidos. El contenido publicado es visible para los participantes que elijas y puede ser moderado y denunciado. Base legal: ejecución de contrato y consentimiento. Los datos se almacenan en el proveedor de base de datos indicado en “Proveedores de servicios”.</p>"""),
            ("Funciones de inteligencia artificial (opcionales)", """<p>Funciones como reescritura de texto, generación de imágenes o lectura de texto en fotos (OCR) solo funcionan después de tu consentimiento explícito. El contenido que envíes lo procesa un proveedor de IA únicamente para generar el resultado y no lo usamos para entrenar modelos. Hay límites de uso y puedes desactivar la función en cualquier momento.</p>"""),
            ("Novedades por correo", """<p>Si pides recibir novedades, guardaremos tu correo con ese fin. Cada mensaje incluye un enlace para darte de baja. Base legal: consentimiento.</p>"""),
            ("Métricas de uso e informes de errores", """<p><mark class="pendente">[CONFIRMAR CON DESARROLLO: ¿la app usa algún servicio de métricas o de informes de fallos? Si sí, nombrarlo, indicar los datos recogidos y si se vinculan a la persona. Si no, escribir: “La app no usa herramientas de métricas de terceros ni publicidad.”]</mark></p>"""),
            ("Proveedores de servicios", """<p>Solo compartimos datos con proveedores necesarios para el funcionamiento de la app, que los tratan según nuestras instrucciones:</p>
<ul>
<li><strong>Apple</strong>: distribución de la app, pagos, inicio de sesión con Apple y envío de notificaciones.</li>
<li><strong>RevenueCat</strong>: validación de suscripciones.</li>
<li><strong>Supabase</strong>: base de datos y almacenamiento de cuenta, copia en la nube y comunidad, cuando se activan.</li>
<li><strong>Proveedor de IA</strong> <mark class="pendente">[NOMBRE]</mark>: solo si activas funciones de IA.</li>
</ul>
<p>También podemos compartir datos cuando lo exija la ley o una autoridad competente.</p>"""),
            ("Transferencias internacionales", """<p>Algunos proveedores almacenan datos fuera de Brasil, incluso en Estados Unidos. En esos casos adoptamos las salvaguardas previstas por la ley, como cláusulas contractuales.</p>"""),
            ("Cuánto tiempo guardamos los datos", """<p>Los datos locales permanecen en el dispositivo hasta que los borres o elimines la app. Los datos de cuenta se conservan mientras la cuenta exista. Al eliminar la cuenta, borramos o anonimizamos los datos en un plazo de 30 días, salvo lo que debamos conservar para cumplir obligaciones legales.</p>"""),
            ("Tus derechos", f"""<p>Puedes solicitar confirmación del tratamiento, acceso, corrección, portabilidad, anonimización o eliminación de tus datos, información sobre su uso compartido y la revocación del consentimiento. Según dónde vivas, puedes tener derechos similares bajo la ley local. Puedes eliminar tu cuenta en la app, en <strong>Ajustes › Cuenta › Eliminar cuenta</strong>. Para otras solicitudes, escribe a {E}. También puedes presentar una reclamación ante tu autoridad de protección de datos.</p>"""),
            ("Niños", """<p>La app no está dirigida a menores de 13 años y no recoge intencionalmente sus datos. Las funciones de cuenta y comunidad exigen una edad mínima de 13 años o autorización de los padres, según la ley aplicable.</p>"""),
            ("Seguridad", """<p>Usamos conexiones cifradas, control de acceso y otras medidas razonables para proteger tus datos. Ningún sistema es totalmente inmune a fallos; si ocurre un incidente relevante, te avisaremos a ti y a las autoridades conforme a la ley.</p>"""),
            ("Cambios", """<p>Podemos actualizar esta política. La fecha en la parte superior indica la versión vigente. Los cambios relevantes se anunciarán en la app.</p>"""),
            ("Contacto y delegado de protección de datos", f"""<p>Delegado de protección de datos: <mark class="pendente">[NOMBRE DEL DELEGADO]</mark>. Contacto: {E}.</p>"""),
        ],
    }[lang]
    titulo = {"pt": "Política de Privacidade", "en": "Privacy Policy", "es": "Política de Privacidad"}[lang]
    sumario_t = {"pt": "Nesta página", "en": "On this page", "es": "En esta página"}[lang]
    return _documento(lang, titulo, secoes, sumario_t)


# ---------------------------------------------------------------------------
# Conteúdo: termos de uso
# ---------------------------------------------------------------------------
def termos(lang):
    E, EMP, CNPJ, FORO = EMAIL(lang), P("empresa", lang), P("cnpj", lang), P("cidade_foro", lang)
    priv = PAGINAS["privacidade"][lang]
    secoes = {
        "pt": [
            ("Aceitação", f"""<p>Estes Termos de Uso regulam o uso do aplicativo {NOME[lang]} (“app”), oferecido por {EMP}, CNPJ {CNPJ} (“nós”). Ao usar o app, você concorda com estes termos e com a <a href="{priv}">Política de Privacidade</a>. Se não concordar, não use o app.</p>"""),
            ("O que o app oferece", """<p>O app oferece microlições bíblicas, consulta ao texto bíblico, áudio, vídeos, ferramentas de estudo pessoal e, quando disponíveis, recursos de conta, comunidade e inteligência artificial. Podemos alterar, incluir ou retirar funcionalidades para melhorar o serviço.</p>"""),
            ("Conteúdo bíblico e interpretações", """<p>Buscamos separar com clareza o texto bíblico, a interpretação e a informação histórica. As lições refletem uma leitura cristã ampla e não representam a posição oficial de nenhuma igreja ou denominação. Os vídeos são representações artísticas criadas com auxílio de inteligência artificial e podem conter paráfrases, sempre identificadas.</p>
<p>Traduções bíblicas de terceiros são usadas conforme suas licenças, indicadas no próprio app. Exemplo: Bíblia Livre (BLIVRE), © 2018 Diego Santos, Mario Sérgio e Marco Teles, licença Creative Commons Atribuição 4.0 Brasil.</p>
<p>O conteúdo do app tem finalidade de estudo e reflexão e não substitui aconselhamento pastoral, psicológico, médico ou jurídico.</p>"""),
            ("Assinatura Pro", """<ul>
<li>Parte do conteúdo exige a assinatura Pro, vendida pela App Store e cobrada na sua conta Apple na confirmação da compra.</li>
<li>A assinatura renova automaticamente pelo mesmo período e preço, salvo se for cancelada até 24 horas antes do fim do período vigente.</li>
<li>Você gerencia e cancela a assinatura em <strong>Ajustes do iPhone › [seu nome] › Assinaturas</strong>. O cancelamento vale a partir do período seguinte; o acesso continua até o fim do período pago.</li>
<li>Se houver período de teste gratuito, a parte não utilizada é perdida quando você assina.</li>
<li>Preços aparecem na loja antes da compra e podem variar por país. Reembolsos seguem as regras da Apple.</li>
</ul>"""),
            ("Conta e comunidade", """<p>Se você criar uma conta, mantenha seus dados de acesso seguros e informe dados verdadeiros. Em grupos, jornadas compartilhadas e demais áreas sociais, você se compromete a não publicar conteúdo ilegal, ofensivo, discriminatório, enganoso, sexual, violento, spam ou que viole direitos de terceiros. Podemos remover conteúdos e suspender contas que descumpram estas regras. Use a opção de denúncia para nos avisar. Você continua dono do que publica e nos autoriza a exibir esse conteúdo dentro do app para os participantes escolhidos.</p>"""),
            ("Uso permitido", """<p>O app é para uso pessoal e não comercial. Não é permitido copiar, revender, extrair conteúdo em massa, fazer engenharia reversa, contornar a assinatura ou usar o app para fins ilegais.</p>"""),
            ("Propriedade intelectual", """<p>Marca, logotipo, textos originais, ilustrações, vídeos, áudios e o software do app pertencem a nós ou a nossos licenciadores e são protegidos por lei. O uso do app não transfere esses direitos a você.</p>"""),
            ("Isenções e responsabilidade", """<p>O app é oferecido “no estado em que se encontra”. Trabalhamos para que funcione bem, mas não garantimos que estará livre de erros ou disponível o tempo todo. Na medida permitida pela lei, não nos responsabilizamos por danos indiretos decorrentes do uso do app. Nada nestes termos limita direitos garantidos pelo Código de Defesa do Consumidor.</p>"""),
            ("Encerramento", """<p>Você pode parar de usar o app e excluir sua conta a qualquer momento. Podemos encerrar o acesso de quem violar estes termos.</p>"""),
            ("Termos da Apple", """<p>Para apps baixados pela App Store, também se aplica o Contrato de Licença de Usuário Final padrão da Apple. A Apple não é responsável pelo app nem pelo seu suporte.</p>"""),
            ("Lei aplicável e alterações", f"""<p>Estes termos são regidos pelas leis do Brasil. Fica eleito o foro da comarca de {FORO}, ressalvado o direito do consumidor de propor ação no foro do seu domicílio. Podemos atualizar estes termos; mudanças relevantes serão avisadas no app.</p>"""),
            ("Contato", f"""<p>Dúvidas sobre estes termos: {E}.</p>"""),
        ],
        "en": [
            ("Acceptance", f"""<p>These Terms of Use govern your use of the {NOME[lang]} app (the “app”), provided by {EMP}, Brazilian company registration (CNPJ) {CNPJ} (“we”, “us”). By using the app you agree to these terms and to the <a href="{priv}">Privacy Policy</a>. If you do not agree, do not use the app.</p>"""),
            ("What the app offers", """<p>The app offers Bible micro-lessons, access to the Bible text, audio, videos, personal study tools and, when available, account, community and artificial intelligence features. We may change, add or remove features to improve the service.</p>"""),
            ("Bible content and interpretation", """<p>We aim to clearly separate the Bible text, interpretation and historical information. Lessons reflect a broad Christian reading and do not represent the official position of any church or denomination. Videos are artistic representations created with the help of artificial intelligence and may contain paraphrases, which are always identified.</p>
<p>Third-party Bible translations are used under their licenses, which are shown in the app. Example: Bíblia Livre (BLIVRE), © 2018 Diego Santos, Mario Sérgio and Marco Teles, Creative Commons Attribution 4.0 Brazil license.</p>
<p>App content is meant for study and reflection and does not replace pastoral, psychological, medical or legal advice.</p>"""),
            ("Pro subscription", """<ul>
<li>Some content requires the Pro subscription, sold through the App Store and charged to your Apple account when you confirm the purchase.</li>
<li>The subscription renews automatically for the same period and price unless cancelled at least 24 hours before the end of the current period.</li>
<li>You manage and cancel it in <strong>iPhone Settings › [your name] › Subscriptions</strong>. Cancellation applies from the next period; access continues until the end of the paid period.</li>
<li>If a free trial is offered, any unused portion is forfeited when you subscribe.</li>
<li>Prices are shown in the store before purchase and may vary by country. Refunds follow Apple’s rules.</li>
</ul>"""),
            ("Account and community", """<p>If you create an account, keep your sign-in details secure and provide accurate information. In groups, shared journeys and other social areas, you agree not to post content that is illegal, offensive, discriminatory, misleading, sexual, violent, spam or that infringes the rights of others. We may remove content and suspend accounts that break these rules. Use the report option to let us know. You keep ownership of what you post and allow us to display it in the app to the participants you choose.</p>"""),
            ("Permitted use", """<p>The app is for personal, non-commercial use. You may not copy, resell, bulk-extract content, reverse engineer, bypass the subscription or use the app for unlawful purposes.</p>"""),
            ("Intellectual property", """<p>The brand, logo, original texts, illustrations, videos, audio and software belong to us or our licensors and are protected by law. Using the app does not transfer these rights to you.</p>"""),
            ("Disclaimers and liability", """<p>The app is provided “as is”. We work to keep it running well but do not guarantee it will be error-free or always available. To the extent permitted by law, we are not liable for indirect damages arising from use of the app. Nothing in these terms limits rights you have under consumer protection law.</p>"""),
            ("Termination", """<p>You may stop using the app and delete your account at any time. We may terminate access for anyone who breaches these terms.</p>"""),
            ("Apple terms", """<p>For apps downloaded from the App Store, Apple’s standard Licensed Application End User License Agreement also applies. Apple is not responsible for the app or its support.</p>"""),
            ("Governing law and changes", f"""<p>These terms are governed by the laws of Brazil, with venue in {FORO}, without prejudice to any mandatory consumer rights in your country of residence. We may update these terms; relevant changes will be announced in the app.</p>"""),
            ("Contact", f"""<p>Questions about these terms: {E}.</p>"""),
        ],
        "es": [
            ("Aceptación", f"""<p>Estos Términos de Uso regulan el uso de la app {NOME[lang]} (la “app”), ofrecida por {EMP}, registro de empresa brasileño (CNPJ) {CNPJ} (“nosotros”). Al usar la app aceptas estos términos y la <a href="{priv}">Política de Privacidad</a>. Si no estás de acuerdo, no uses la app.</p>"""),
            ("Qué ofrece la app", """<p>La app ofrece microlecciones bíblicas, consulta del texto bíblico, audio, videos, herramientas de estudio personal y, cuando estén disponibles, funciones de cuenta, comunidad e inteligencia artificial. Podemos cambiar, añadir o retirar funciones para mejorar el servicio.</p>"""),
            ("Contenido bíblico e interpretación", """<p>Buscamos separar con claridad el texto bíblico, la interpretación y la información histórica. Las lecciones reflejan una lectura cristiana amplia y no representan la posición oficial de ninguna iglesia o denominación. Los videos son representaciones artísticas creadas con ayuda de inteligencia artificial y pueden contener paráfrasis, siempre identificadas.</p>
<p>Las traducciones bíblicas de terceros se usan conforme a sus licencias, indicadas en la app. Ejemplo: Bíblia Livre (BLIVRE), © 2018 Diego Santos, Mario Sérgio y Marco Teles, licencia Creative Commons Atribución 4.0 Brasil.</p>
<p>El contenido de la app es para estudio y reflexión y no sustituye el consejo pastoral, psicológico, médico o jurídico.</p>"""),
            ("Suscripción Pro", """<ul>
<li>Parte del contenido requiere la suscripción Pro, vendida a través de la App Store y cobrada en tu cuenta de Apple al confirmar la compra.</li>
<li>La suscripción se renueva automáticamente por el mismo período y precio, salvo que se cancele al menos 24 horas antes del final del período vigente.</li>
<li>La gestionas y cancelas en <strong>Ajustes del iPhone › [tu nombre] › Suscripciones</strong>. La cancelación aplica desde el período siguiente; el acceso continúa hasta el final del período pagado.</li>
<li>Si se ofrece una prueba gratuita, la parte no utilizada se pierde al suscribirte.</li>
<li>Los precios se muestran en la tienda antes de la compra y pueden variar por país. Los reembolsos siguen las reglas de Apple.</li>
</ul>"""),
            ("Cuenta y comunidad", """<p>Si creas una cuenta, mantén seguros tus datos de acceso e informa datos verdaderos. En grupos, recorridos compartidos y demás áreas sociales, te comprometes a no publicar contenido ilegal, ofensivo, discriminatorio, engañoso, sexual, violento, spam o que viole derechos de terceros. Podemos retirar contenidos y suspender cuentas que incumplan estas reglas. Usa la opción de denuncia para avisarnos. Sigues siendo dueño de lo que publicas y nos autorizas a mostrarlo en la app a los participantes que elijas.</p>"""),
            ("Uso permitido", """<p>La app es para uso personal y no comercial. No está permitido copiar, revender, extraer contenido de forma masiva, hacer ingeniería inversa, eludir la suscripción ni usar la app con fines ilegales.</p>"""),
            ("Propiedad intelectual", """<p>La marca, el logotipo, los textos originales, ilustraciones, videos, audios y el software nos pertenecen a nosotros o a nuestros licenciantes y están protegidos por la ley. El uso de la app no te transfiere esos derechos.</p>"""),
            ("Exenciones y responsabilidad", """<p>La app se ofrece “tal cual”. Trabajamos para que funcione bien, pero no garantizamos que esté libre de errores ni disponible en todo momento. En la medida permitida por la ley, no somos responsables de daños indirectos derivados del uso de la app. Nada en estos términos limita los derechos que te otorga la ley de protección al consumidor.</p>"""),
            ("Terminación", """<p>Puedes dejar de usar la app y eliminar tu cuenta en cualquier momento. Podemos cancelar el acceso de quien incumpla estos términos.</p>"""),
            ("Términos de Apple", """<p>Para apps descargadas desde la App Store, también se aplica el Contrato de Licencia de Usuario Final estándar de Apple. Apple no es responsable de la app ni de su soporte.</p>"""),
            ("Ley aplicable y cambios", f"""<p>Estos términos se rigen por las leyes de Brasil, con foro en {FORO}, sin perjuicio de los derechos imperativos del consumidor en tu país de residencia. Podemos actualizar estos términos; los cambios relevantes se anunciarán en la app.</p>"""),
            ("Contacto", f"""<p>Dudas sobre estos términos: {E}.</p>"""),
        ],
    }[lang]
    titulo = {"pt": "Termos de Uso", "en": "Terms of Use", "es": "Términos de Uso"}[lang]
    sumario_t = {"pt": "Nesta página", "en": "On this page", "es": "En esta página"}[lang]
    return _documento(lang, titulo, secoes, sumario_t)


def _documento(lang, titulo, secoes, sumario_t):
    itens = "".join(f'<li><a href="#s{i}">{t}</a></li>' for i, (t, _) in enumerate(secoes, 1))
    corpo_sec = "".join(f'<h2 id="s{i}">{i}. {t}</h2>{c}' for i, (t, c) in enumerate(secoes, 1))
    corpo = f"""
<header class="cabecalho-pagina"><div class="wrap"><h1>{titulo}</h1><p>{UI[lang]["atualizado"]}: {ATUALIZADO[lang]}</p></div></header>
<div class="texto">
  <nav class="sumario" aria-label="{sumario_t}"><p class="rotulo" style="margin-bottom:8px">{sumario_t}</p><ol>{itens}</ol></nav>
  {corpo_sec}
</div>
"""
    return f"{titulo} — {NOME[lang]}", titulo, corpo


# ---------------------------------------------------------------------------
# Moldura da página
# ---------------------------------------------------------------------------
def pagina(lang, chave, title, desc, corpo):
    u = UI[lang]
    cur_pg, cur_on, so_desk = ' aria-current="page"', ' aria-current="true"', ' class="so-desktop"'
    nav = "".join(
        f'<a href="{PAGINAS[k][lang]}"{cur_pg if k == chave else ""}'
        f'{so_desk if k == "home" else ""}>{u["nav"][k]}</a>'
        for k in ("home", "suporte", "privacidade", "termos"))
    idiomas = "".join(
        f'<a href="../{l}/{PAGINAS[chave][l]}" hreflang="{LANG_ATTR[l]}" lang="{LANG_ATTR[l]}"'
        f'{cur_on if l == lang else ""}>{l.upper()}</a>' for l in ("pt", "en", "es"))
    dom = CONFIG["dominio"].strip()
    alternates = canonical = ""
    if dom:
        canonical = f'<link rel="canonical" href="https://{dom}/{lang}/{PAGINAS[chave][lang]}">'
        alternates = "".join(
            f'<link rel="alternate" hreflang="{LANG_ATTR[l]}" href="https://{dom}/{l}/{PAGINAS[chave][l]}">'
            for l in ("pt", "en", "es"))
    rod_links = "".join(f'<a href="{PAGINAS[k][lang]}">{u["nav"][k]}</a>' for k in ("suporte", "privacidade", "termos"))
    return f"""<!doctype html>
<html lang="{LANG_ATTR[lang]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="theme-color" content="#123B46">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:image" content="{f"https://{dom}" if dom else ".."}/assets/img/avatar.png">
{canonical}{alternates}
<link rel="icon" type="image/png" href="../assets/img/favicon.png">
<link rel="apple-touch-icon" href="../assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Lora:ital,wght@0,500;0,600;0,700;1,500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../assets/style.css">
</head>
<body>
<a class="skip" href="#conteudo">{u["pular"]}</a>
<header class="topo">
  <div class="pilula">
    <a class="marca" href="{PAGINAS["home"][lang]}"><img src="../assets/img/avatar.png" alt="" width="36" height="36">{NOME[lang]}</a>
    <nav class="nav" aria-label="Menu">{nav}<span class="idiomas">{idiomas}</span></nav>
  </div>
</header>
<main id="conteudo">
{corpo}
</main>
<footer class="rodape">
  <div class="wrap">
    <div>© 2026 {NOME[lang]}. {u["rodape"]}</div>
    <nav aria-label="Links">{rod_links}</nav>
  </div>
</footer>
<script>
  (function () {{
    var t = document.querySelector(".topo");
    var f = function () {{ t.classList.toggle("rolou", window.scrollY > 8); }};
    f(); window.addEventListener("scroll", f, {{ passive: true }});
  }})();
</script>
</body>
</html>
"""


RAIZ = """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Bíblia Vívida · Vivid Bible</title>
<meta name="theme-color" content="#123B46">
<link rel="icon" type="image/png" href="assets/img/favicon.png">
<script>
  (function () {
    // bibliavivida.com abre sempre em português; nos demais, segue o idioma do navegador (padrão: inglês)
    if (/bibliavivida\./i.test(location.hostname)) { location.replace("pt/index.html"); return; }
    var l = (navigator.languages && navigator.languages[0] || navigator.language || "en").toLowerCase();
    var d = l.indexOf("pt") === 0 ? "pt" : l.indexOf("es") === 0 ? "es" : "en";
    location.replace(d + "/index.html");
  })();
</script>
<style>body{margin:0;min-height:100vh;display:grid;place-items:center;background:#123B46;color:#F5EBDD;font-family:-apple-system,system-ui,sans-serif}a{color:#E8B75A;margin:0 10px}</style>
</head>
<body>
<p><a href="pt/index.html">Português</a><a href="en/index.html">English</a><a href="es/index.html">Español</a></p>
</body>
</html>
"""


def main():
    for lang in ("pt", "en", "es"):
        (ROOT / lang).mkdir(parents=True, exist_ok=True)
        for chave, fn in (("home", home), ("suporte", suporte), ("privacidade", privacidade), ("termos", termos)):
            title, desc, corpo = fn(lang)
            (ROOT / lang / PAGINAS[chave][lang]).write_text(pagina(lang, chave, title, desc, corpo), encoding="utf-8")
    (ROOT / "index.html").write_text(RAIZ, encoding="utf-8")
    pend = sum(p.read_text(encoding="utf-8").count('class="pendente"') for p in ROOT.rglob("*.html"))
    print(f"Site gerado em {ROOT}  ·  {pend} marcações de pendência a preencher")


if __name__ == "__main__":
    main()
