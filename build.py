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
    "email": "support@vividbible.app",  # encaminha (Cloudflare Email Routing) para a caixa da equipe
    "responsavel": "Fabricio Silva",  # titular (pessoa física) da conta Apple Developer
    "app_store_url": "",    # link da App Store quando o app for aprovado
}
ATUALIZADO = {"pt": "15 de novembro de 2026", "en": "November 15, 2026", "es": "15 de noviembre de 2026"}

ROOT = Path(__file__).parent / "docs"

PAGINAS = {  # chave interna -> nome de arquivo por idioma
    "home": {"pt": "index.html", "en": "index.html", "es": "index.html"},
    "suporte": {"pt": "suporte.html", "en": "support.html", "es": "soporte.html"},
    "privacidade": {"pt": "privacidade.html", "en": "privacy.html", "es": "privacidad.html"},
}
LANG_ATTR = {"pt": "pt-BR", "en": "en", "es": "es"}
NOME = {"pt": "Bíblia Vívida", "en": "Vivid Bible", "es": "Biblia Vívida"}
EULA = "https://www.apple.com/legal/internet-services/itunes/dev/stdeula/"


def P(chave, lang):
    """Valor do CONFIG ou marcador visível de pendência."""
    v = CONFIG.get(chave, "").strip()
    if v:
        return html.escape(v)
    rotulo = {
        "pt": {"dominio": "DOMÍNIO", "email": "E-MAIL DE SUPORTE", "responsavel": "NOME DO RESPONSÁVEL"},
        "en": {"dominio": "DOMAIN", "email": "SUPPORT EMAIL", "responsavel": "LEGAL NAME"},
        "es": {"dominio": "DOMINIO", "email": "CORREO DE SOPORTE", "responsavel": "NOMBRE DEL RESPONSABLE"},
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
        "nav": {"home": "Início", "suporte": "Suporte", "privacidade": "Privacidade", "termos": "Termos de uso"},
        "pular": "Pular para o conteúdo",
        "rodape": "Feito com cuidado para quem quer entender a Bíblia de perto.",
        "atualizado": "Última atualização",
        "em_breve": "Em breve na App Store",
        "baixar": "Baixar na App Store",
    },
    "en": {
        "nav": {"home": "Home", "suporte": "Support", "privacidade": "Privacy", "termos": "Terms of use"},
        "pular": "Skip to content",
        "rodape": "Made with care for anyone who wants to understand the Bible up close.",
        "atualizado": "Last updated",
        "em_breve": "Coming soon to the App Store",
        "baixar": "Download on the App Store",
    },
    "es": {
        "nav": {"home": "Inicio", "suporte": "Soporte", "privacidade": "Privacidad", "termos": "Términos de uso"},
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
                ("Onde ficam minhas anotações e salvos?", "No seu aparelho. O app não tem conta nem cópia na nuvem, então, se você apagar o app, essas informações são removidas junto."),
                ("Como apago meus dados?", "Apagar o app remove todos os dados guardados no aparelho. Para dúvidas sobre dados da assinatura, escreva para nós. Detalhes na <a href=\"privacidade.html\">Política de Privacidade</a>."),
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
                ("Where are my notes and saved items stored?", "On your device. The app has no account or cloud backup, so if you delete the app, this information is removed with it."),
                ("How do I delete my data?", "Deleting the app removes all data stored on the device. For questions about subscription data, write to us. See the <a href=\"privacy.html\">Privacy Policy</a> for details."),
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
                ("¿Dónde se guardan mis notas y guardados?", "En tu dispositivo. La app no tiene cuenta ni copia en la nube, así que, si borras la app, esa información se elimina con ella."),
                ("¿Cómo borro mis datos?", "Borrar la app elimina todos los datos guardados en el dispositivo. Para dudas sobre datos de la suscripción, escríbenos. Más detalles en la <a href=\"privacidad.html\">Política de Privacidad</a>."),
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
    E, RESP = EMAIL(lang), P("responsavel", lang)
    secoes = {
        "pt": [
            ("Quem somos", f"""<p>O aplicativo {NOME[lang]} (“app”) é desenvolvido e publicado por {RESP}, pessoa física, no Brasil (“nós”). Somos o controlador dos dados pessoais descritos nesta política, nos termos da Lei Geral de Proteção de Dados (Lei 13.709/2018, “LGPD”).</p>"""),
            ("Resumo", """<ul>
<li>O app não tem cadastro nem conta. Você lê, ouve, salva e anota sem informar nome ou e-mail.</li>
<li>O que você faz no app fica guardado no seu aparelho.</li>
<li>Pagamentos são processados pela Apple. Nunca recebemos o número do seu cartão.</li>
<li>O app não usa ferramentas de métricas, relatórios de falhas de terceiros nem publicidade.</li>
<li>Não vendemos dados pessoais.</li>
</ul>"""),
            ("Dados que ficam no seu aparelho", """<p>Progresso de leitura, cartões salvos, coleções, histórico, diário, conquistas, preferências (idioma, tamanho de fonte, horário dos lembretes) e passagens registradas pelo scanner são guardados apenas no iPhone. Essas informações não são enviadas para nós.</p>"""),
            ("Assinatura e compras", """<p>A assinatura Pro é vendida pela App Store. A Apple processa o pagamento e informa ao app apenas o status da compra. Usamos o serviço RevenueCat para validar assinaturas: ele recebe um identificador anônimo gerado pelo app e os dados da transação fornecidos pela Apple (produto, data, validade, país da loja). Nenhum nome, e-mail ou dado de cartão é compartilhado com ele. Base legal: execução de contrato.</p>"""),
            ("Lembretes", """<p>Os lembretes de leitura são agendados no próprio aparelho, com a sua permissão. Não enviamos notificações por servidor. Você pode desligá-las a qualquer momento nos Ajustes do iPhone.</p>"""),
            ("Câmera e fotos", """<p>O scanner usa a câmera ou a galeria apenas quando você toca para fotografar ou escolher uma imagem. A imagem serve para registrar a referência bíblica e não é enviada para nós nem para terceiros.</p>"""),
            ("Métricas e publicidade", """<p>O app não usa ferramentas de métricas de uso, de relatório de falhas de terceiros nem publicidade. Se você autorizou o compartilhamento de análises nos Ajustes do iPhone, a Apple pode fornecer aos desenvolvedores estatísticas agregadas e anônimas de uso e de falhas, conforme a política de privacidade da Apple.</p>"""),
            ("Prestadores de serviço", """<p>Compartilhamos dados somente com os fornecedores necessários para o funcionamento do app:</p>
<ul>
<li><strong>Apple</strong>: distribuição do app, pagamentos e assinaturas.</li>
<li><strong>RevenueCat</strong>: validação de assinaturas.</li>
</ul>
<p>Também podemos compartilhar dados quando exigido por lei ou ordem de autoridade competente.</p>"""),
            ("Transferência internacional", """<p>A Apple e o RevenueCat podem armazenar os dados de compra fora do Brasil, inclusive nos Estados Unidos, com as salvaguardas previstas na LGPD.</p>"""),
            ("Por quanto tempo guardamos", """<p>Os dados do app ficam no aparelho até você apagá-los ou remover o app. Os registros de assinatura são mantidos pela Apple e pelo RevenueCat enquanto forem necessários para a assinatura e para obrigações legais.</p>"""),
            ("Seus direitos", f"""<p>Você pode pedir confirmação de tratamento, acesso, correção, eliminação e informações sobre compartilhamento dos seus dados. Como o app não tem conta, a maior parte das informações está somente no seu aparelho, e apagar o app as remove. Para pedidos sobre dados de assinatura, escreva para {E}. Você também pode apresentar reclamação à Autoridade Nacional de Proteção de Dados (ANPD).</p>"""),
            ("Crianças", """<p>O app não é direcionado a crianças menores de 13 anos e não coleta intencionalmente dados pessoais delas.</p>"""),
            ("Segurança", """<p>As compras usam a infraestrutura da Apple, e a comunicação com o RevenueCat é criptografada. Os dados do app ficam protegidos pelos recursos de segurança do próprio iPhone.</p>"""),
            ("Alterações", """<p>Podemos atualizar esta política, por exemplo se novos recursos forem lançados. A data no topo indica a versão vigente, e mudanças relevantes serão avisadas no app.</p>"""),
            ("Contato", f"""<p>Controlador e responsável pelo atendimento a titulares: {RESP}. Contato: {E}.</p>"""),
        ],
        "en": [
            ("Who we are", f"""<p>The {NOME[lang]} app (the “app”) is developed and published by {RESP}, an individual developer based in Brazil (“we”, “us”). We are the controller of the personal data described in this policy under Brazil’s General Data Protection Law (LGPD) and other applicable laws.</p>"""),
            ("Summary", """<ul>
<li>The app has no sign-up or account. You can read, listen, save and take notes without giving a name or email.</li>
<li>What you do in the app is stored on your device.</li>
<li>Payments are processed by Apple. We never receive your card number.</li>
<li>The app does not use analytics tools, third-party crash reporting or advertising.</li>
<li>We do not sell personal data.</li>
</ul>"""),
            ("Data that stays on your device", """<p>Reading progress, saved cards, collections, history, journal, achievements, preferences (language, font size, reminder time) and passages recorded with the scanner are stored only on your iPhone. This information is not sent to us.</p>"""),
            ("Subscription and purchases", """<p>The Pro subscription is sold through the App Store. Apple processes the payment and only tells the app the purchase status. We use RevenueCat to validate subscriptions: it receives an anonymous identifier generated by the app and the transaction data provided by Apple (product, date, expiry, store country). No name, email or card data is shared with it. Legal basis: performance of a contract.</p>"""),
            ("Reminders", """<p>Reading reminders are scheduled on the device itself, with your permission. We do not send server notifications. You can turn them off at any time in iPhone Settings.</p>"""),
            ("Camera and photos", """<p>The scanner uses the camera or photo library only when you tap to take or choose a picture. The image is used to record the Bible reference and is not sent to us or to third parties.</p>"""),
            ("Analytics and advertising", """<p>The app does not use usage analytics, third-party crash reporting or advertising. If you allowed analytics sharing in iPhone Settings, Apple may provide developers with aggregated, anonymous usage and crash statistics, under Apple’s privacy policy.</p>"""),
            ("Service providers", """<p>We only share data with the vendors needed to run the app:</p>
<ul>
<li><strong>Apple</strong>: app distribution, payments and subscriptions.</li>
<li><strong>RevenueCat</strong>: subscription validation.</li>
</ul>
<p>We may also share data when required by law or by order of a competent authority.</p>"""),
            ("International transfers", """<p>Apple and RevenueCat may store purchase data outside Brazil, including in the United States, with the safeguards provided by law.</p>"""),
            ("How long we keep data", """<p>App data stays on the device until you delete it or remove the app. Subscription records are kept by Apple and RevenueCat as long as needed for the subscription and for legal obligations.</p>"""),
            ("Your rights", f"""<p>You may request confirmation of processing, access, correction, deletion and information about sharing of your data. Depending on where you live (for example in the EU, UK or California), you may have similar rights under local law. Because the app has no account, most information exists only on your device, and deleting the app removes it. For requests about subscription data, email {E}. You may also complain to your data protection authority.</p>"""),
            ("Children", """<p>The app is not directed to children under 13 and does not knowingly collect their personal data.</p>"""),
            ("Security", """<p>Purchases use Apple’s infrastructure, and communication with RevenueCat is encrypted. App data is protected by the iPhone’s own security features.</p>"""),
            ("Changes", """<p>We may update this policy, for example if new features are released. The date at the top shows the current version, and relevant changes will be announced in the app.</p>"""),
            ("Contact", f"""<p>Controller and contact for data requests: {RESP}. Email: {E}.</p>"""),
        ],
        "es": [
            ("Quiénes somos", f"""<p>La aplicación {NOME[lang]} (la “app”) es desarrollada y publicada por {RESP}, persona física con residencia en Brasil (“nosotros”). Somos responsables del tratamiento de los datos personales descritos en esta política, conforme a la Ley General de Protección de Datos de Brasil (LGPD) y demás leyes aplicables.</p>"""),
            ("Resumen", """<ul>
<li>La app no tiene registro ni cuenta. Puedes leer, escuchar, guardar y tomar notas sin dar tu nombre ni tu correo.</li>
<li>Lo que haces en la app se guarda en tu dispositivo.</li>
<li>Los pagos los procesa Apple. Nunca recibimos el número de tu tarjeta.</li>
<li>La app no usa herramientas de métricas, informes de fallos de terceros ni publicidad.</li>
<li>No vendemos datos personales.</li>
</ul>"""),
            ("Datos que quedan en tu dispositivo", """<p>El progreso de lectura, tarjetas guardadas, colecciones, historial, diario, logros, preferencias (idioma, tamaño de letra, hora de recordatorios) y pasajes registrados con el escáner se guardan solo en el iPhone. Esa información no se nos envía.</p>"""),
            ("Suscripción y compras", """<p>La suscripción Pro se vende a través de la App Store. Apple procesa el pago y solo informa a la app el estado de la compra. Usamos RevenueCat para validar suscripciones: recibe un identificador anónimo generado por la app y los datos de la transacción proporcionados por Apple (producto, fecha, vencimiento, país de la tienda). No se comparte con él ningún nombre, correo ni dato de tarjeta. Base legal: ejecución de contrato.</p>"""),
            ("Recordatorios", """<p>Los recordatorios de lectura se programan en el propio dispositivo, con tu permiso. No enviamos notificaciones desde un servidor. Puedes desactivarlas en cualquier momento en los Ajustes del iPhone.</p>"""),
            ("Cámara y fotos", """<p>El escáner usa la cámara o la galería solo cuando tocas para tomar o elegir una imagen. La imagen sirve para registrar la referencia bíblica y no se nos envía a nosotros ni a terceros.</p>"""),
            ("Métricas y publicidad", """<p>La app no usa métricas de uso, informes de fallos de terceros ni publicidad. Si autorizaste compartir análisis en los Ajustes del iPhone, Apple puede proporcionar a los desarrolladores estadísticas agregadas y anónimas de uso y de fallos, según la política de privacidad de Apple.</p>"""),
            ("Proveedores de servicios", """<p>Solo compartimos datos con los proveedores necesarios para el funcionamiento de la app:</p>
<ul>
<li><strong>Apple</strong>: distribución de la app, pagos y suscripciones.</li>
<li><strong>RevenueCat</strong>: validación de suscripciones.</li>
</ul>
<p>También podemos compartir datos cuando lo exija la ley o una autoridad competente.</p>"""),
            ("Transferencias internacionales", """<p>Apple y RevenueCat pueden almacenar los datos de compra fuera de Brasil, incluso en Estados Unidos, con las salvaguardas previstas por la ley.</p>"""),
            ("Cuánto tiempo guardamos los datos", """<p>Los datos de la app permanecen en el dispositivo hasta que los borres o elimines la app. Los registros de suscripción los conservan Apple y RevenueCat mientras sean necesarios para la suscripción y para obligaciones legales.</p>"""),
            ("Tus derechos", f"""<p>Puedes solicitar confirmación del tratamiento, acceso, corrección, eliminación e información sobre el uso compartido de tus datos. Según dónde vivas, puedes tener derechos similares bajo la ley local. Como la app no tiene cuenta, la mayor parte de la información está solo en tu dispositivo y borrar la app la elimina. Para solicitudes sobre datos de suscripción, escribe a {E}. También puedes presentar una reclamación ante tu autoridad de protección de datos.</p>"""),
            ("Niños", """<p>La app no está dirigida a menores de 13 años y no recoge intencionalmente sus datos personales.</p>"""),
            ("Seguridad", """<p>Las compras usan la infraestructura de Apple y la comunicación con RevenueCat está cifrada. Los datos de la app están protegidos por las funciones de seguridad del propio iPhone.</p>"""),
            ("Cambios", """<p>Podemos actualizar esta política, por ejemplo si se lanzan nuevas funciones. La fecha en la parte superior indica la versión vigente y los cambios relevantes se anunciarán en la app.</p>"""),
            ("Contacto", f"""<p>Responsable del tratamiento y contacto para solicitudes: {RESP}. Correo: {E}.</p>"""),
        ],
    }[lang]
    titulo = {"pt": "Política de Privacidade", "en": "Privacy Policy", "es": "Política de Privacidad"}[lang]
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
        for k in ("home", "suporte", "privacidade"))
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
    rod_links = "".join(f'<a href="{PAGINAS[k][lang]}">{u["nav"][k]}</a>' for k in ("suporte", "privacidade")) + f'<a href="{EULA}">{u["nav"]["termos"]}</a>'
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
        for chave, fn in (("home", home), ("suporte", suporte), ("privacidade", privacidade)):
            title, desc, corpo = fn(lang)
            (ROOT / lang / PAGINAS[chave][lang]).write_text(pagina(lang, chave, title, desc, corpo), encoding="utf-8")
    (ROOT / "index.html").write_text(RAIZ, encoding="utf-8")
    pend = sum(p.read_text(encoding="utf-8").count('class="pendente"') for p in ROOT.rglob("*.html"))
    redirects = "".join(f"/{l}/{f} {EULA} 301\n/{l}/{f.replace('.html', '')} {EULA} 301\n"
                        for l, f in (("pt", "termos.html"), ("en", "terms.html"), ("es", "terminos.html")))
    (ROOT / "_redirects").write_text(redirects, encoding="utf-8")
    for l, f in (("pt", "termos.html"), ("en", "terms.html"), ("es", "terminos.html")):
        (ROOT / l / f).unlink(missing_ok=True)
    print(f"Site gerado em {ROOT}  ·  {pend} marcações de pendência a preencher")
    if pend:
        raise SystemExit("ATENÇÃO: há campos pendentes (em amarelo). Preencha o CONFIG antes de enviar à Apple.")


if __name__ == "__main__":
    main()
