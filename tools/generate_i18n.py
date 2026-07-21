from pathlib import Path
from html import escape


ROOT = Path(__file__).resolve().parents[1]
BASE = "https://getelia.app"
LANGS = ["en", "uk", "de", "ru"]
LOCALES = {"en": "en_US", "uk": "uk_UA", "de": "de_DE", "ru": "ru_RU"}
LANG_LABELS = {"en": "EN", "uk": "UA", "de": "DE", "ru": "RU"}
URL_PREFIXES = {"en": "", "uk": "ua", "de": "de", "ru": "ru"}


def url(lang, route=""):
    route = route.strip("/")
    prefix = URL_PREFIXES[lang]
    prefix = f"{prefix}/" if prefix else ""
    path = f"{prefix}{route}/" if route else prefix
    return f"{BASE}/{path}".replace("//", "/").replace("https:/", "https://")


def href(lang, route="", current_lang=None, current_route=""):
    route = route.strip("/")
    if current_lang is None:
        prefix = URL_PREFIXES[lang]
        prefix = f"{prefix}/" if prefix else ""
        return f"{prefix}{route}/index.html" if route else f"{prefix}index.html"
    target = out_path(lang, route)
    source_dir = out_path(current_lang, current_route).parent
    return Path.relative_to if False else relpath(target, source_dir)


def relpath(target, source_dir):
    return Path(__import__("os").path.relpath(target, source_dir)).as_posix()


def asset(path, current_lang, current_route=""):
    target = ROOT / path.strip("/")
    source_dir = out_path(current_lang, current_route).parent
    return relpath(target, source_dir)


def out_path(lang, route=""):
    route = route.strip("/")
    prefix = URL_PREFIXES[lang]
    if not prefix:
      return ROOT / (route or "") / "index.html"
    return ROOT / prefix / (route or "") / "index.html"

def alternates(route):
    links = [f'  <link rel="alternate" hreflang="{lang}" href="{url(lang, route)}" />' for lang in LANGS]
    links.append(f'  <link rel="alternate" hreflang="x-default" href="{url("en", route)}" />')
    return "\n".join(links)


def og_locales(lang):
    lines = [f'  <meta property="og:locale" content="{LOCALES[lang]}" />']
    lines.extend(f'  <meta property="og:locale:alternate" content="{LOCALES[x]}" />' for x in LANGS if x != lang)
    return "\n".join(lines)


def lang_switch(lang, route, label):
    links = []
    for x in LANGS:
        current = ' aria-current="true"' if x == lang else ""
        links.append(f'<a href="{href(x, route, lang, route)}"{current} hreflang="{x}" lang="{x}">{LANG_LABELS[x]}</a>')
    return f'<nav class="lang-switch" aria-label="{escape(label)}">{"".join(links)}</nav>'


def head(lang, route, title, description, icon="svg", image=None, extra=""):
    icon_link = f'  <link rel="icon" href="{asset("assets/img/favicon.svg", lang, route)}" type="image/svg+xml" />'
    if icon == "contractions":
        icon_link = '\n'.join([
            f'  <link rel="icon" type="image/png" href="{asset("assets/img/favicon-contractions.png", lang, route)}" />',
            f'  <link rel="apple-touch-icon" href="{asset("assets/img/apple-touch-icon-contractions.png", lang, route)}" />',
        ])
    image_tags = ""
    if image:
        image_tags = f"""
  <meta property="og:image" content="{image}" />
  <meta property="og:image:width" content="1024" />
  <meta property="og:image:height" content="500" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:image" content="{image}" />"""
    return f"""<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(description)}" />
  <meta name="theme-color" content="#FFF8F5" media="(prefers-color-scheme: light)" />
  <meta name="theme-color" content="#171316" media="(prefers-color-scheme: dark)" />
{icon_link}
  <link rel="stylesheet" href="{asset('assets/css/styles.css', lang, route)}" />
  <link rel="canonical" href="{url(lang, route)}" />
{alternates(route)}

  <meta property="og:type" content="website" />
  <meta property="og:title" content="{escape(title)}" />
  <meta property="og:description" content="{escape(description)}" />
  <meta property="og:url" content="{url(lang, route)}" />
{og_locales(lang)}{image_tags}
{extra}</head>"""


def header(lang, route, nav, aria):
    def nav_href(link):
        if link.startswith("#"):
            return link
        if link.startswith("home#"):
            return href(lang, "", lang, route) + link.removeprefix("home")
        return href(lang, link, lang, route)
    nav_html = "\n        ".join(f'<a href="{nav_href(link)}">{escape(text)}</a>' for text, link in nav)
    return f"""<header class="site-header">
    <div class="container">
      <a class="brand" href="{href(lang, "", lang, route)}" aria-label="Elia home">
        <img class="brand__mark" src="{asset("assets/img/favicon.svg", lang, route)}" alt="" />
        <span class="brand__name">Elia</span>
      </a>
      <nav class="nav" aria-label="Primary">
        {nav_html}
      </nav>
      {lang_switch(lang, route, aria)}
    </div>
  </header>"""


def footer(lang, links, note, route=""):
    links_html = "\n        ".join(f'<a href="{href(lang, link, lang, route)}">{escape(text)}</a>' if not link.startswith("mailto:") and not link.startswith("#") else f'<a href="{link}">{escape(text)}</a>' for text, link in links)
    return f"""<footer class="site-footer">
    <div class="container">
      <a class="brand" href="{href(lang, "", lang, route)}" aria-label="Elia home">
        <img class="brand__mark" src="{asset("assets/img/favicon.svg", lang, route)}" alt="" />
        <span class="brand__name">Elia</span>
      </a>
      <div class="foot-links">
        {links_html}
      </div>
      <small>{escape(note)} © <span id="year">2026</span> Elia.</small>
    </div>
  </footer>

  <script>document.getElementById('year').textContent = new Date().getFullYear();</script>"""


T = {
 "en": {
  "lang": "Language", "note": "Not a medical device.",
  "home": {
   "title": "Elia — calm, private apps for your family's first days",
   "description": "Elia is a small family of calm, private, offline-first apps for pregnancy, birth, and the early days with your baby. No account. No ads. No cloud.",
   "nav": [("Apps", "#apps"), ("Philosophy", "#philosophy"), ("Story", "#story")],
   "hero": ["Elia", "Calm companions for birth and beyond.", "A small family of private, offline-first apps for pregnancy, birth, and the early days with your baby. No account. No ads. No cloud.", "See the apps", "Why Elia"],
   "apps_head": ["The apps", "Two apps for two moments.", "Each does one thing calmly, and gets out of your way."],
   "coming": "Coming soon", "learn": "Learn more",
   "contr_card": ["Elia Contractions", "A calm companion for birth. Time contractions clearly, stay present, and share a simple summary with your care team."],
   "feed_card": ["Elia Feeding", "A calm, private feeding log for the first days with your baby. Tap what just happened — Elia remembers the rest."],
   "promise": ["The promise", "The interface should reduce stress, not add to it.", "Elia is warm, quiet, and trustworthy — like a calm midwife and a supportive partner, not like hospital software. Every Elia app follows the same principles."],
   "chips": ["No account", "No ads", "No subscriptions", "No cloud sync", "No analytics", "Offline-first", "Local-only by default", "No judgement"],
   "story": ["Our story", "Elia was born in a delivery room.", "During labor, a partner reached for a contraction app. It lagged. The main button never made it clear whether tracking had started. Useful features were locked behind a subscription. After three contractions it said to go to the hospital — where the family already was.", "The app added stress. Elia is the answer to that moment: the companion we wished we had.", "Their baby was born that evening. Elia was born the same day — and grew into a small family of apps for the quiet, tired, important days that follow."],
  },
 },
 "uk": {
  "lang": "Мова", "note": "Не є медичним виробом.",
  "home": {
   "title": "Elia — спокійні приватні застосунки для перших сімейних днів",
   "description": "Elia — невелика родина спокійних приватних застосунків для вагітності, пологів і перших днів з малюком. Без акаунта, реклами й хмарної синхронізації.",
   "nav": [("Застосунки", "#apps"), ("Філософія", "#philosophy"), ("Історія", "#story")],
   "hero": ["Elia", "Спокійні помічники для пологів і днів після них.", "Невелика родина приватних offline-first застосунків для вагітності, пологів і перших днів з малюком. Без акаунта. Без реклами. Без хмарної синхронізації.", "Переглянути застосунки", "Чому Elia"],
   "apps_head": ["Застосунки", "Два застосунки для двох моментів.", "Кожен спокійно робить одну справу і не заважає."],
   "coming": "Незабаром", "learn": "Докладніше",
   "contr_card": ["Elia Contractions", "Спокійний помічник для пологів. Чітко фіксуйте перейми, залишайтеся поруч із моментом і діліться простим підсумком із командою догляду."],
   "feed_card": ["Elia Feeding", "Спокійний приватний журнал годувань для перших днів із малюком. Натисніть те, що щойно сталося — Elia запам'ятає решту."],
   "promise": ["Обіцянка", "Інтерфейс має зменшувати стрес, а не додавати його.", "Elia тепла, тиха й надійна — як спокійна акушерка і підтримуючий партнер, а не як лікарняна система. Усі застосунки Elia дотримуються тих самих принципів."],
   "chips": ["Без акаунта", "Без реклами", "Без підписок", "Без хмарної синхронізації", "Без аналітики", "Offline-first", "Локально за замовчуванням", "Без осуду"],
   "story": ["Наша історія", "Elia народилася у пологовій кімнаті.", "Під час пологів партнер відкрив застосунок для перейм. Він гальмував. Головна кнопка не давала зрозуміти, чи запис уже почався. Корисні функції були за підпискою. Після трьох перейм застосунок сказав їхати до лікарні — де сім'я вже була.", "Застосунок додав стресу. Elia — відповідь на той момент: помічник, якого нам тоді бракувало.", "Їхній малюк народився того вечора. Elia народилася того ж дня — і виросла в невелику родину застосунків для тихих, втомлених і важливих днів після."],
  },
 },
 "de": {
  "lang": "Sprache", "note": "Kein Medizinprodukt.",
  "home": {
   "title": "Elia — ruhige, private Apps für die ersten Tage als Familie",
   "description": "Elia ist eine kleine Familie ruhiger, privater Offline-first-Apps für Schwangerschaft, Geburt und die ersten Tage mit deinem Baby. Kein Konto. Keine Werbung. Keine Cloud.",
   "nav": [("Apps", "#apps"), ("Philosophie", "#philosophy"), ("Geschichte", "#story")],
   "hero": ["Elia", "Ruhige Begleiter für Geburt und die Zeit danach.", "Eine kleine Familie privater Offline-first-Apps für Schwangerschaft, Geburt und die ersten Tage mit deinem Baby. Kein Konto. Keine Werbung. Keine Cloud.", "Apps ansehen", "Warum Elia"],
   "apps_head": ["Die Apps", "Zwei Apps für zwei Momente.", "Jede tut ruhig eine Sache und tritt dann in den Hintergrund."],
   "coming": "Demnächst", "learn": "Mehr erfahren",
   "contr_card": ["Elia Contractions", "Ein ruhiger Begleiter für die Geburt. Wehen klar erfassen, präsent bleiben und bei Bedarf eine einfache Zusammenfassung teilen."],
   "feed_card": ["Elia Feeding", "Ein ruhiges, privates Still- und Fütterungsprotokoll für die ersten Tage mit deinem Baby. Tippe, was gerade passiert ist — Elia merkt sich den Rest."],
   "promise": ["Das Versprechen", "Die Oberfläche soll Stress reduzieren, nicht erhöhen.", "Elia ist warm, leise und vertrauenswürdig — eher wie eine ruhige Hebamme und ein unterstützender Partner als wie Krankenhaussoftware. Jede Elia-App folgt denselben Prinzipien."],
   "chips": ["Kein Konto", "Keine Werbung", "Keine Abos", "Keine Cloud-Synchronisierung", "Keine Analyse", "Offline-first", "Standardmäßig lokal", "Kein Urteil"],
   "story": ["Unsere Geschichte", "Elia entstand in einem Kreißsaal.", "Während der Geburt griff ein Partner zu einer Wehen-App. Sie reagierte träge. Der Hauptknopf machte nie klar, ob die Aufzeichnung begonnen hatte. Nützliche Funktionen lagen hinter einem Abo. Nach drei Wehen sagte sie, man solle ins Krankenhaus fahren — wo die Familie bereits war.", "Die App machte den Moment stressiger. Elia ist die Antwort darauf: der Begleiter, den wir uns gewünscht hätten.", "Das Baby wurde an diesem Abend geboren. Elia entstand am selben Tag — und wuchs zu einer kleinen App-Familie für die leisen, müden und wichtigen Tage danach."],
  },
 },
 "ru": {
  "lang": "Язык", "note": "Не является медицинским изделием.",
  "home": {
   "title": "Elia — спокойные приватные приложения для первых семейных дней",
   "description": "Elia — небольшая семья спокойных приватных приложений для беременности, родов и первых дней с малышом. Без аккаунта, рекламы и облачной синхронизации.",
   "nav": [("Приложения", "#apps"), ("Философия", "#philosophy"), ("История", "#story")],
   "hero": ["Elia", "Спокойные помощники для родов и дней после.", "Небольшая семья приватных offline-first приложений для беременности, родов и первых дней с малышом. Без аккаунта. Без рекламы. Без облачной синхронизации.", "Посмотреть приложения", "Почему Elia"],
   "apps_head": ["Приложения", "Два приложения для двух моментов.", "Каждое спокойно делает одну вещь и не мешает."],
   "coming": "Скоро", "learn": "Подробнее",
   "contr_card": ["Elia Contractions", "Спокойный помощник для родов. Четко фиксируйте схватки, оставайтесь в моменте и делитесь простым итогом с командой ухода."],
   "feed_card": ["Elia Feeding", "Спокойный приватный журнал кормлений для первых дней с малышом. Нажмите то, что только что произошло — Elia запомнит остальное."],
   "promise": ["Обещание", "Интерфейс должен снижать стресс, а не добавлять его.", "Elia теплая, тихая и надежная — как спокойная акушерка и поддерживающий партнер, а не как больничная система. Все приложения Elia следуют одним принципам."],
   "chips": ["Без аккаунта", "Без рекламы", "Без подписок", "Без облачной синхронизации", "Без аналитики", "Offline-first", "Локально по умолчанию", "Без осуждения"],
   "story": ["Наша история", "Elia родилась в родильной комнате.", "Во время родов партнер открыл приложение для схваток. Оно тормозило. Главная кнопка не давала понять, началась ли запись. Полезные функции были за подпиской. После трех схваток приложение сказало ехать в больницу — где семья уже была.", "Приложение добавило стресса. Elia — ответ на тот момент: помощник, которого нам тогда не хватало.", "Их малыш родился тем вечером. Elia родилась в тот же день — и выросла в небольшую семью приложений для тихих, уставших и важных дней после."],
  },
 },
}


APP = {
 "en": {
  "common": {"overview": "Overview", "support": "Support", "privacy": "Privacy", "all": "All apps", "back": "← All Elia apps", "what": "What it is", "does": "What it does", "promise": "The promise", "why": "Why it exists", "still": "Still need help?", "read": "We read every message."},
  "contractions": {
   "title": "Elia Contractions — a calm companion for birth", "desc": "Elia Contractions is a calm, offline-first contraction companion for families during labor. Time contractions clearly, stay present, and share a simple summary.", "tag": "A calm companion for birth.",
   "sub": "A contraction companion for families during labor, built around one belief: during labor, the interface should reduce stress, not add to it.",
   "head": ["What it is", "Just enough, exactly when it matters."], "left": "Elia Contractions helps you", "right": "What it is not",
   "yes": ["Record contractions with one clear tap.", "Review timing and intervals at a glance.", "Stay focused during a contraction.", "Stay present between them.", "Keep a simple, honest history.", "Share a clear summary with your care team, if useful."],
   "no": ["A medical device or diagnostic tool.", "A replacement for doctors or midwives.", "A pregnancy or baby tracker.", "A subscription trap.", "An advertising surface.", "Something that tells you what to do."],
   "story": ["Why it exists", "Born from a real birth.", "It began in a hospital room, during labor. Things moved quickly, and soon the contractions left almost no pause in between.", "The partner reached for a contraction app. The one they found lagged. The main button never made it clear whether tracking had started or stopped. Useful features were locked behind a subscription. After a few contractions, it told the family to leave for the hospital — where they already were, under care.", "The app added stress. Elia is the answer to that moment.", "Their baby was born that evening. Elia was born the same day."],
   "principles": ["Calm, private, and yours.", ["Offline-first", "Local-only", "No account", "No ads", "No subscription for core", "No analytics"], "Elia Contractions is not a medical device and does not provide medical advice or diagnosis. It never tells you when to go to the hospital. Always follow the guidance of your doctors and midwives."],
  },
  "feeding": {
   "title": "Elia Feeding — a calm feeding log for the first days", "desc": "Elia Feeding is a calm, private newborn feeding and care log for the first days with your baby. No account. No cloud. No judgement.", "tag": "Remember just enough.",
   "sub": "A calm, private feeding log for the first days with your baby. No account. No cloud. No judgement. Just the last feed, the next action, and a simple history.",
   "pull": ["Open the app. Tap the thing that just happened. Elia remembers.", "Most baby trackers help you measure everything. Elia helps you remember just enough."],
   "head": ["What it does", "Fast, obvious logging — one hand, low attention."], "left": "In the app", "right": "Deliberately not included",
   "yes": ["Breastfeeding timer with Left / Right side.", "Bottle feeding log, with optional amount.", "Simple diaper log: wet, dirty, or both.", "A home screen showing the current state and last useful context.", "A quiet history you can edit or delete.", "Share or export as plain text."],
   "no": ["Accounts, cloud, or multi-parent sync.", "Growth charts and analytics.", "Feeding targets, streaks, or warnings.", "Medical recommendations.", "Sleep, medication, or pumping inventory.", "Ads or billing."],
   "principles": ["Calm, private, and yours.", "No goals, warnings, or pressure. Elia remembers what you log — nothing more.", ["No account", "No ads", "No subscriptions", "No backend", "No cloud sync", "No analytics", "Offline-first", "No judgement"], "Elia Feeding is a calm memory aid, not a medical tool. It does not give medical advice and does not define what is normal. For anything about your baby's health, talk to your pediatrician or midwife."],
  },
 },
 "uk": {
  "common": {"overview": "Огляд", "support": "Підтримка", "privacy": "Приватність", "all": "Усі застосунки", "back": "← Усі застосунки Elia", "what": "Що це", "does": "Що робить", "promise": "Обіцянка", "why": "Навіщо існує", "still": "Потрібна допомога?", "read": "Ми читаємо кожне повідомлення."},
  "contractions": {
   "title": "Elia Contractions — спокійний помічник для пологів", "desc": "Elia Contractions — спокійний offline-first помічник для сімей під час пологів. Чітко фіксуйте перейми, залишайтеся поруч із моментом і діліться простим підсумком.", "tag": "Спокійний помічник для пологів.",
   "sub": "Помічник для сімей під час пологів, створений навколо однієї думки: під час пологів інтерфейс має зменшувати стрес, а не додавати його.",
   "head": ["Що це", "Рівно стільки, скільки потрібно, саме тоді, коли важливо."], "left": "Elia Contractions допомагає", "right": "Чим це не є",
   "yes": ["Записувати перейми одним зрозумілим натисканням.", "Бачити тривалість і інтервали з першого погляду.", "Залишатися зосередженими під час перейми.", "Бути присутніми між ними.", "Мати просту й чесну історію.", "Ділитися зрозумілим підсумком із командою догляду, якщо це корисно."],
   "no": ["Медичний виріб або діагностичний інструмент.", "Заміна лікаря чи акушерки.", "Трекер вагітності або дитини.", "Пастка з підпискою.", "Місце для реклами.", "Щось, що каже вам, що робити."],
   "story": ["Навіщо існує", "Народжена з реальних пологів.", "Усе почалося в лікарняній кімнаті, під час пологів. Події рухалися швидко, і невдовзі між переймами майже не залишалося пауз.", "Партнер відкрив застосунок для перейм. Він гальмував. Головна кнопка не давала зрозуміти, чи запис почався або зупинився. Корисні функції були за підпискою. Після кількох перейм застосунок сказав їхати до лікарні — де сім'я вже була під наглядом.", "Застосунок додав стресу. Elia — відповідь на той момент.", "Їхній малюк народився того вечора. Elia народилася того ж дня."],
   "principles": ["Спокійна, приватна і ваша.", ["Offline-first", "Локально", "Без акаунта", "Без реклами", "Основне без підписки", "Без аналітики"], "Elia Contractions не є медичним виробом і не надає медичних порад чи діагнозів. Вона ніколи не каже, коли їхати до лікарні. Завжди дотримуйтеся рекомендацій лікарів і акушерок."],
  },
  "feeding": {
   "title": "Elia Feeding — спокійний журнал годувань для перших днів", "desc": "Elia Feeding — спокійний приватний журнал годувань і догляду за новонародженим у перші дні. Без акаунта, хмарної синхронізації й осуду.", "tag": "Пам'ятати рівно стільки, скільки потрібно.",
   "sub": "Спокійний приватний журнал годувань для перших днів із малюком. Без акаунта. Без хмарної синхронізації. Без осуду. Тільки останнє годування, наступна дія і проста історія.",
   "pull": ["Відкрийте застосунок. Натисніть те, що щойно сталося. Elia запам'ятає.", "Більшість дитячих трекерів допомагають вимірювати все. Elia допомагає пам'ятати рівно стільки, скільки потрібно."],
   "head": ["Що робить", "Швидке й очевидне логування — однією рукою, з мінімумом уваги."], "left": "У застосунку", "right": "Навмисно не включено",
   "yes": ["Таймер грудного годування з лівим / правим боком.", "Журнал годування з пляшечки, з необов'язковою кількістю.", "Простий журнал підгузків: мокрий, брудний або обидва.", "Головний екран із поточним станом і останнім корисним контекстом.", "Тиха історія, яку можна редагувати або видаляти.", "Поділитися або експортувати як звичайний текст."],
   "no": ["Акаунти, хмара або синхронізація між батьками.", "Графіки росту й аналітика.", "Цілі годування, серії або попередження.", "Медичні рекомендації.", "Сон, ліки або облік зціджування.", "Реклама або оплата."],
   "principles": ["Спокійна, приватна і ваша.", "Без цілей, попереджень і тиску. Elia пам'ятає те, що ви записали — і нічого більше.", ["Без акаунта", "Без реклами", "Без підписок", "Без бекенду", "Без хмарної синхронізації", "Без аналітики", "Offline-first", "Без осуду"], "Elia Feeding — спокійна пам'ятка, а не медичний інструмент. Вона не дає медичних порад і не визначає, що є нормою. Щодо здоров'я малюка звертайтеся до педіатра або акушерки."],
  },
 },
 "de": {
  "common": {"overview": "Überblick", "support": "Support", "privacy": "Datenschutz", "all": "Alle Apps", "back": "← Alle Elia-Apps", "what": "Was es ist", "does": "Was es tut", "promise": "Versprechen", "why": "Warum es existiert", "still": "Brauchst du Hilfe?", "read": "Wir lesen jede Nachricht."},
  "contractions": {
   "title": "Elia Contractions — ein ruhiger Begleiter für die Geburt", "desc": "Elia Contractions ist ein ruhiger Offline-first-Begleiter für Familien während der Geburt. Wehen klar erfassen, präsent bleiben und eine einfache Zusammenfassung teilen.", "tag": "Ein ruhiger Begleiter für die Geburt.",
   "sub": "Ein Wehenbegleiter für Familien während der Geburt, gebaut um eine Überzeugung: Während der Geburt soll die Oberfläche Stress reduzieren, nicht erhöhen.",
   "head": ["Was es ist", "Gerade genug, genau dann, wenn es zählt."], "left": "Elia Contractions hilft dir", "right": "Was es nicht ist",
   "yes": ["Wehen mit einem klaren Tippen erfassen.", "Dauer und Abstände auf einen Blick prüfen.", "Während einer Wehe fokussiert bleiben.", "Zwischen den Wehen präsent bleiben.", "Eine einfache, ehrliche Historie behalten.", "Bei Bedarf eine klare Zusammenfassung mit dem Betreuungsteam teilen."],
   "no": ["Ein Medizinprodukt oder Diagnosewerkzeug.", "Ein Ersatz für Ärztinnen, Ärzte oder Hebammen.", "Ein Schwangerschafts- oder Babytracker.", "Eine Abo-Falle.", "Eine Werbefläche.", "Etwas, das dir sagt, was du tun sollst."],
   "story": ["Warum es existiert", "Aus einer echten Geburt entstanden.", "Es begann in einem Krankenhauszimmer während der Geburt. Alles ging schnell, und bald blieb zwischen den Wehen kaum noch Pause.", "Der Partner öffnete eine Wehen-App. Sie reagierte träge. Der Hauptknopf machte nicht klar, ob die Aufzeichnung gestartet oder gestoppt war. Nützliche Funktionen lagen hinter einem Abo. Nach ein paar Wehen sagte die App, man solle ins Krankenhaus fahren — wo die Familie bereits betreut wurde.", "Die App machte den Moment stressiger. Elia ist die Antwort darauf.", "Das Baby wurde an diesem Abend geboren. Elia entstand am selben Tag."],
   "principles": ["Ruhig, privat und dein.", ["Offline-first", "Nur lokal", "Kein Konto", "Keine Werbung", "Kernfunktionen ohne Abo", "Keine Analyse"], "Elia Contractions ist kein Medizinprodukt und gibt keine medizinische Beratung oder Diagnose. Sie sagt dir nie, wann du ins Krankenhaus fahren sollst. Folge immer den Empfehlungen deiner Ärztinnen, Ärzte und Hebammen."],
  },
  "feeding": {
   "title": "Elia Feeding — ein ruhiges Fütterungsprotokoll für die ersten Tage", "desc": "Elia Feeding ist ein ruhiges, privates Protokoll für Füttern und Pflege in den ersten Tagen mit deinem Baby. Kein Konto. Keine Cloud. Kein Urteil.", "tag": "Gerade genug merken.",
   "sub": "Ein ruhiges, privates Fütterungsprotokoll für die ersten Tage mit deinem Baby. Kein Konto. Keine Cloud. Kein Urteil. Nur die letzte Mahlzeit, die nächste Aktion und eine einfache Historie.",
   "pull": ["App öffnen. Antippen, was gerade passiert ist. Elia merkt es sich.", "Die meisten Babytracker helfen, alles zu messen. Elia hilft, gerade genug im Kopf zu behalten."],
   "head": ["Was es tut", "Schnelles, klares Protokollieren — mit einer Hand, wenig Aufmerksamkeit."], "left": "In der App", "right": "Bewusst nicht enthalten",
   "yes": ["Still-Timer mit linker / rechter Seite.", "Fläschchen-Protokoll mit optionaler Menge.", "Einfaches Windelprotokoll: nass, schmutzig oder beides.", "Startseite mit aktuellem Zustand und dem letzten nützlichen Kontext.", "Eine ruhige Historie, die du bearbeiten oder löschen kannst.", "Teilen oder Export als Klartext."],
   "no": ["Konten, Cloud oder Synchronisierung zwischen Eltern.", "Wachstumskurven und Analysen.", "Fütterungsziele, Serien oder Warnungen.", "Medizinische Empfehlungen.", "Schlaf, Medikamente oder Pumpvorräte.", "Werbung oder Bezahlung."],
   "principles": ["Ruhig, privat und dein.", "Keine Ziele, Warnungen oder Druck. Elia merkt sich, was du einträgst — mehr nicht.", ["Kein Konto", "Keine Werbung", "Keine Abos", "Kein Backend", "Keine Cloud-Synchronisierung", "Keine Analyse", "Offline-first", "Kein Urteil"], "Elia Feeding ist eine ruhige Gedächtnisstütze, kein medizinisches Werkzeug. Sie gibt keine medizinischen Ratschläge und definiert nicht, was normal ist. Wenn es um die Gesundheit deines Babys geht, sprich mit Kinderarzt, Kinderärztin oder Hebamme."],
  },
 },
 "ru": {
  "common": {"overview": "Обзор", "support": "Поддержка", "privacy": "Приватность", "all": "Все приложения", "back": "← Все приложения Elia", "what": "Что это", "does": "Что делает", "promise": "Обещание", "why": "Зачем существует", "still": "Нужна помощь?", "read": "Мы читаем каждое сообщение."},
  "contractions": {
   "title": "Elia Contractions — спокойный помощник для родов", "desc": "Elia Contractions — спокойный offline-first помощник для семей во время родов. Четко фиксируйте схватки, оставайтесь в моменте и делитесь простым итогом.", "tag": "Спокойный помощник для родов.",
   "sub": "Помощник для семей во время родов, построенный вокруг одной мысли: во время родов интерфейс должен снижать стресс, а не добавлять его.",
   "head": ["Что это", "Ровно столько, сколько нужно, именно когда важно."], "left": "Elia Contractions помогает", "right": "Чем это не является",
   "yes": ["Записывать схватки одним понятным нажатием.", "Быстро видеть длительность и интервалы.", "Сохранять фокус во время схватки.", "Оставаться в моменте между ними.", "Вести простую и честную историю.", "Делиться понятным итогом с командой ухода, если это полезно."],
   "no": ["Медицинское изделие или диагностический инструмент.", "Замена врачу или акушерке.", "Трекер беременности или ребенка.", "Ловушка с подпиской.", "Рекламная площадка.", "Что-то, что говорит вам, что делать."],
   "story": ["Зачем существует", "Родилось из настоящих родов.", "Все началось в больничной палате, во время родов. События шли быстро, и вскоре между схватками почти не оставалось пауз.", "Партнер открыл приложение для схваток. Оно тормозило. Главная кнопка не давала понять, началась запись или остановилась. Полезные функции были за подпиской. После нескольких схваток приложение сказало ехать в больницу — где семья уже была под присмотром.", "Приложение добавило стресса. Elia — ответ на тот момент.", "Их малыш родился тем вечером. Elia родилась в тот же день."],
   "principles": ["Спокойная, приватная и ваша.", ["Offline-first", "Локально", "Без аккаунта", "Без рекламы", "Основное без подписки", "Без аналитики"], "Elia Contractions не является медицинским изделием и не дает медицинских советов или диагнозов. Она никогда не говорит, когда ехать в больницу. Всегда следуйте рекомендациям врачей и акушерок."],
  },
  "feeding": {
   "title": "Elia Feeding — спокойный журнал кормлений для первых дней", "desc": "Elia Feeding — спокойный приватный журнал кормлений и ухода за новорожденным в первые дни. Без аккаунта, облачной синхронизации и осуждения.", "tag": "Помнить ровно столько, сколько нужно.",
   "sub": "Спокойный приватный журнал кормлений для первых дней с малышом. Без аккаунта. Без облачной синхронизации. Без осуждения. Только последнее кормление, следующее действие и простая история.",
   "pull": ["Откройте приложение. Нажмите то, что только что произошло. Elia запомнит.", "Большинство детских трекеров помогают измерять все. Elia помогает помнить ровно столько, сколько нужно."],
   "head": ["Что делает", "Быстрая и очевидная запись — одной рукой, с минимумом внимания."], "left": "В приложении", "right": "Намеренно не включено",
   "yes": ["Таймер грудного кормления с левой / правой стороной.", "Журнал кормления из бутылочки, с необязательным количеством.", "Простой журнал подгузников: мокрый, грязный или оба.", "Главный экран с текущим состоянием и последним полезным контекстом.", "Тихая история, которую можно редактировать или удалять.", "Поделиться или экспортировать обычным текстом."],
   "no": ["Аккаунты, облако или синхронизация между родителями.", "Графики роста и аналитика.", "Цели кормления, серии или предупреждения.", "Медицинские рекомендации.", "Сон, лекарства или учет сцеживания.", "Реклама или оплата."],
   "principles": ["Спокойная, приватная и ваша.", "Без целей, предупреждений и давления. Elia помнит то, что вы записали — и ничего больше.", ["Без аккаунта", "Без рекламы", "Без подписок", "Без бэкенда", "Без облачной синхронизации", "Без аналитики", "Offline-first", "Без осуждения"], "Elia Feeding — спокойная памятка, а не медицинский инструмент. Она не дает медицинских советов и не определяет, что нормально. По вопросам здоровья малыша обращайтесь к педиатру или акушерке."],
  },
 },
}


SUPPORT = {
 "en": {
  "contractions": [
   ("Is my data private?", "Yes. Elia Contractions has no account and no backend. Your contraction times, history, and settings stay on your device. See the privacy policy for details."),
   ("Does it work offline?", "Yes. Recording contractions never needs an internet connection. The app is built to be reliable in a delivery room, not dependent on a signal."),
   ("Does it tell me when to go to the hospital?", "No. Elia does not diagnose or give medical directives. It shows your contractions clearly so you can share them with your care team. Always follow the guidance of your doctors and midwives."),
   ("Can I correct a mistake?", "Yes. You can edit or delete entries calmly. Nothing is permanent by accident."),
   ("How do I share a summary with my midwife or doctor?", "You can export or share your session as plain text using your device's share options. You choose where it goes; Elia never sends it anywhere on its own."),
   ("Is there a subscription?", "The core experience is not a subscription trap. Elia will never lock essential labor features behind a paywall or show ads."),
  ],
  "feeding": [
   ("Is my data private?", "Yes. Elia Feeding has no account, no backend, and no cloud. Your entries and settings stay on your device. See the privacy policy for details."),
   ("Does it work offline?", "Yes. Logging a feed, bottle, or diaper never needs an internet connection."),
   ("Does it tell me if my baby is feeding enough?", "No. Elia does not set targets, warnings, or judgements, and does not define what is normal. It simply remembers what you log. For anything about your baby's health, talk to your pediatrician or midwife."),
   ("Can I edit or delete an entry?", "Yes. You can edit or delete any entry. Nothing is permanent by accident."),
   ("Can two parents share the same log?", "Not in the current version. Elia Feeding is local-only by design, so there is no cloud sync between devices. Everything lives on the one device you log on."),
   ("How do I move my log somewhere else?", "You can export or share it as plain text using your device's share options. You choose the destination; Elia never sends it anywhere on its own."),
   ("Are there ads or subscriptions?", "No ads, no subscriptions, no billing. Elia Feeding is a calm memory aid, not a monetization funnel."),
  ],
 },
 "uk": {
  "contractions": [("Чи мої дані приватні?", "Так. В Elia Contractions немає акаунта й бекенду. Часи перейм, історія та налаштування залишаються на вашому пристрої. Докладніше — у політиці приватності."), ("Чи працює без інтернету?", "Так. Запис перейм ніколи не потребує інтернету. Застосунок створений, щоб бути надійним у пологовій кімнаті, а не залежати від сигналу."), ("Чи каже застосунок, коли їхати до лікарні?", "Ні. Elia не діагностує і не дає медичних вказівок. Вона чітко показує ваші перейми, щоб ви могли поділитися ними з командою догляду. Завжди дотримуйтеся рекомендацій лікарів і акушерок."), ("Чи можна виправити помилку?", "Так. Ви можете спокійно редагувати або видаляти записи. Нічого не стає постійним випадково."), ("Як поділитися підсумком з акушеркою або лікарем?", "Ви можете експортувати або поділитися сесією як звичайним текстом через системні опції пристрою. Ви самі обираєте місце призначення; Elia нічого не надсилає самостійно."), ("Чи є підписка?", "Основний досвід не є пасткою з підпискою. Elia ніколи не закриє важливі для пологів функції за paywall і не показуватиме рекламу.")],
  "feeding": [("Чи мої дані приватні?", "Так. В Elia Feeding немає акаунта, бекенду й хмарної синхронізації. Ваші записи та налаштування залишаються на пристрої. Докладніше — у політиці приватності."), ("Чи працює без інтернету?", "Так. Запис годування, пляшечки або підгузка ніколи не потребує інтернету."), ("Чи каже застосунок, чи достатньо їсть мій малюк?", "Ні. Elia не ставить цілей, попереджень або оцінок і не визначає, що є нормою. Вона просто пам'ятає те, що ви записали. Щодо здоров'я малюка звертайтеся до педіатра або акушерки."), ("Чи можна редагувати або видалити запис?", "Так. Ви можете редагувати або видаляти будь-який запис. Нічого не стає постійним випадково."), ("Чи можуть двоє батьків вести один журнал?", "Не в поточній версії. Elia Feeding за задумом локальна, тому хмарної синхронізації між пристроями немає. Усе живе на одному пристрої."), ("Як перенести журнал кудись іще?", "Ви можете експортувати або поділитися ним як звичайним текстом через системні опції пристрою. Ви самі обираєте місце призначення; Elia нічого не надсилає самостійно."), ("Чи є реклама або підписки?", "Ні реклами, ні підписок, ні оплати. Elia Feeding — спокійна пам'ятка, а не воронка монетизації.")],
 },
 "de": {
  "contractions": [("Sind meine Daten privat?", "Ja. Elia Contractions hat kein Konto und kein Backend. Wehenzeiten, Historie und Einstellungen bleiben auf deinem Gerät. Details stehen in der Datenschutzerklärung."), ("Funktioniert es offline?", "Ja. Wehen zu erfassen braucht nie eine Internetverbindung. Die App soll im Kreißsaal verlässlich sein, nicht vom Empfang abhängen."), ("Sagt die App mir, wann ich ins Krankenhaus fahren soll?", "Nein. Elia diagnostiziert nicht und gibt keine medizinischen Anweisungen. Sie zeigt deine Wehen klar, damit du sie mit deinem Betreuungsteam teilen kannst. Folge immer den Empfehlungen deiner Ärztinnen, Ärzte und Hebammen."), ("Kann ich einen Fehler korrigieren?", "Ja. Du kannst Einträge ruhig bearbeiten oder löschen. Nichts ist aus Versehen endgültig."), ("Wie teile ich eine Zusammenfassung mit Hebamme oder Arzt?", "Du kannst deine Sitzung als Klartext über die Teilen-Funktionen deines Geräts exportieren. Du wählst das Ziel; Elia sendet nie von selbst etwas."), ("Gibt es ein Abo?", "Die Kernfunktionen sind keine Abo-Falle. Elia wird wichtige Geburtsfunktionen nie hinter einer Paywall verstecken oder Werbung zeigen.")],
  "feeding": [("Sind meine Daten privat?", "Ja. Elia Feeding hat kein Konto, kein Backend und keine Cloud. Deine Einträge und Einstellungen bleiben auf deinem Gerät. Details stehen in der Datenschutzerklärung."), ("Funktioniert es offline?", "Ja. Füttern, Fläschchen oder Windeln zu protokollieren braucht nie Internet."), ("Sagt die App, ob mein Baby genug trinkt?", "Nein. Elia setzt keine Ziele, Warnungen oder Urteile und definiert nicht, was normal ist. Sie merkt sich nur, was du einträgst. Wenn es um die Gesundheit deines Babys geht, sprich mit Kinderarzt, Kinderärztin oder Hebamme."), ("Kann ich einen Eintrag bearbeiten oder löschen?", "Ja. Du kannst jeden Eintrag bearbeiten oder löschen. Nichts ist aus Versehen endgültig."), ("Können zwei Eltern dasselbe Protokoll teilen?", "In der aktuellen Version nicht. Elia Feeding ist bewusst lokal, daher gibt es keine Cloud-Synchronisierung zwischen Geräten. Alles bleibt auf dem Gerät, auf dem du protokollierst."), ("Wie verschiebe ich mein Protokoll woandershin?", "Du kannst es als Klartext über die Teilen-Funktionen deines Geräts exportieren. Du wählst das Ziel; Elia sendet nie von selbst etwas."), ("Gibt es Werbung oder Abos?", "Keine Werbung, keine Abos, keine Bezahlung. Elia Feeding ist eine ruhige Gedächtnisstütze, kein Monetarisierungstrichter.")],
 },
 "ru": {
  "contractions": [("Мои данные приватны?", "Да. В Elia Contractions нет аккаунта и бэкенда. Время схваток, история и настройки остаются на вашем устройстве. Подробности — в политике приватности."), ("Работает ли без интернета?", "Да. Для записи схваток интернет не нужен. Приложение сделано так, чтобы быть надежным в родильной комнате, а не зависеть от сигнала."), ("Говорит ли приложение, когда ехать в больницу?", "Нет. Elia не ставит диагнозы и не дает медицинских указаний. Она ясно показывает схватки, чтобы вы могли поделиться ими с командой ухода. Всегда следуйте рекомендациям врачей и акушерок."), ("Можно исправить ошибку?", "Да. Вы можете спокойно редактировать или удалять записи. Ничто не становится постоянным случайно."), ("Как поделиться итогом с акушеркой или врачом?", "Вы можете экспортировать или отправить сессию обычным текстом через системные функции устройства. Вы сами выбираете адресата; Elia ничего не отправляет сама."), ("Есть ли подписка?", "Основной опыт не является ловушкой с подпиской. Elia никогда не закроет важные для родов функции за paywall и не будет показывать рекламу.")],
  "feeding": [("Мои данные приватны?", "Да. В Elia Feeding нет аккаунта, бэкенда и облачной синхронизации. Ваши записи и настройки остаются на устройстве. Подробности — в политике приватности."), ("Работает ли без интернета?", "Да. Для записи кормления, бутылочки или подгузника интернет не нужен."), ("Говорит ли приложение, достаточно ли ест мой малыш?", "Нет. Elia не ставит целей, предупреждений или оценок и не определяет, что нормально. Она просто помнит то, что вы записали. По вопросам здоровья малыша обращайтесь к педиатру или акушерке."), ("Можно редактировать или удалить запись?", "Да. Вы можете редактировать или удалить любую запись. Ничто не становится постоянным случайно."), ("Могут ли двое родителей вести один журнал?", "Не в текущей версии. Elia Feeding по задумке локальная, поэтому облачной синхронизации между устройствами нет. Все хранится на одном устройстве."), ("Как перенести журнал куда-то еще?", "Вы можете экспортировать или отправить его обычным текстом через системные функции устройства. Вы сами выбираете адресата; Elia ничего не отправляет сама."), ("Есть ли реклама или подписки?", "Нет рекламы, подписок и оплаты. Elia Feeding — спокойная памятка, а не воронка монетизации.")],
 },
}


def ul(items, cls):
    return f'<ul class="{cls}">' + "".join(f"<li>{escape(x)}</li>" for x in items) + "</ul>"


def chips(items):
    return '<div class="chips">' + "".join(f'<span class="chip">{escape(x)}</span>' for x in items) + "</div>"


def home(lang):
    t = T[lang]["home"]
    body = f"""<!DOCTYPE html>
<html lang="{lang}">
{head(lang, "", t["title"], t["description"])}
<body>
  {header(lang, "", t["nav"], T[lang]["lang"])}

  <main>
    <section class="hero">
      <div class="container">
        <h1 class="hero__wordmark">{escape(t["hero"][0])}</h1>
        <p class="hero__tagline">{escape(t["hero"][1])}</p>
        <p class="hero__sub lead">{escape(t["hero"][2])}</p>
        <div class="btn-row">
          <a class="btn btn--primary" href="#apps">{escape(t["hero"][3])}</a>
          <a class="btn btn--ghost" href="#philosophy">{escape(t["hero"][4])}</a>
        </div>
      </div>
    </section>

    <section id="apps">
      <div class="container">
        <div class="section-head"><span class="eyebrow">{escape(t["apps_head"][0])}</span><h2>{escape(t["apps_head"][1])}</h2><p class="lead">{escape(t["apps_head"][2])}</p></div>
        <div class="apps">
          <a class="app-card" href="{href(lang, "apps/contractions", lang, "")}" data-accent="rose">
            <div class="app-card__top"><span class="app-icon is-image" aria-hidden="true"><img src="{asset("assets/img/icon-contractions.png", lang, "")}" alt="" width="256" height="256" /></span><div><div class="app-card__title">{escape(t["contr_card"][0])}</div><span class="tag"><span class="tag__dot"></span>{escape(t["coming"])}</span></div></div>
            <p class="app-card__one">{escape(t["contr_card"][1])}</p><div class="app-card__foot"><span class="app-card__cta">{escape(t["learn"])} <span class="arrow">→</span></span></div>
          </a>
          <a class="app-card" href="{href(lang, "apps/feeding", lang, "")}" data-accent="honey">
            <div class="app-card__top"><span class="app-icon" aria-hidden="true">{bottle_svg()}</span><div><div class="app-card__title">{escape(t["feed_card"][0])}</div><span class="tag"><span class="tag__dot"></span>{escape(t["coming"])}</span></div></div>
            <p class="app-card__one">{escape(t["feed_card"][1])}</p><div class="app-card__foot"><span class="app-card__cta">{escape(t["learn"])} <span class="arrow">→</span></span></div>
          </a>
        </div>
      </div>
    </section>

    <section id="philosophy" class="tint">
      <div class="container"><div class="section-head"><span class="eyebrow">{escape(t["promise"][0])}</span><h2>{escape(t["promise"][1])}</h2><p class="lead">{escape(t["promise"][2])}</p></div>{chips(t["chips"])}</div>
    </section>

    <section id="story">
      <div class="container"><div class="section-head"><span class="eyebrow">{escape(t["story"][0])}</span><h2>{escape(t["story"][1])}</h2></div><div class="story"><p class="pull">{escape(t["story"][2])}</p><p>{escape(t["story"][3])}</p><p>{escape(t["story"][4])}</p></div></div>
    </section>
  </main>

  {footer(lang, [("Contractions", "apps/contractions"), ("Feeding", "apps/feeding"), (t["nav"][1][0], "#philosophy"), ("Contact", "mailto:hello@getelia.app")], T[lang]["note"], "")}
</body>
</html>
"""
    write(lang, "", body)


def bottle_svg():
    return """<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">
                <path d="M12 3h8M13 6h6l-1 2.5c2 1.2 3 3.2 3 5.5v11a3 3 0 0 1-3 3h-6a3 3 0 0 1-3-3V14c0-2.3 1-4.3 3-5.5L13 6z" />
                <path d="M10 15h12M10 20h12" />
              </svg>"""


def app_page(lang, app):
    c = APP[lang]["common"]
    a = APP[lang][app]
    route = f"apps/{app}"
    icon = "contractions" if app == "contractions" else "svg"
    image = f"{BASE}/assets/img/cover-contractions.png" if app == "contractions" else None
    extra = ""
    if app == "feeding":
        extra = """  <style>
    body { --accent: #C9976A; --accent-dark: #A9784C; --accent-light: #F3E3D1; }
    @media (prefers-color-scheme: dark) { body { --accent-light: #352A20; } }
  </style>
"""
    icon_html = f'<span class="app-icon is-image" aria-hidden="true" style="margin-top:24px;"><img src="{asset("assets/img/icon-contractions.png", lang, route)}" alt="" width="256" height="256" /></span>' if app == "contractions" else f'<span class="app-icon" aria-hidden="true" style="margin-top:24px;">{bottle_svg()}</span>'
    pre = ""
    if app == "feeding":
        pre = f"""<section id="promise" class="tint"><div class="container"><div class="story" style="margin-inline:auto; text-align:center;"><p class="pull">{escape(a["pull"][0])}</p><p class="lead">{escape(a["pull"][1])}</p></div></div></section>"""
    route_other = "apps/feeding" if app == "contractions" else "apps/contractions"
    other_name = "Feeding" if app == "contractions" else "Contractions"
    sublead = f'<p class="lead">{escape(a["principles"][1])}</p>' if app == "feeding" else ""
    body = f"""<!DOCTYPE html>
<html lang="{lang}">
{head(lang, route, a["title"], a["desc"], icon, image, extra)}
<body>
  {header(lang, route, [(c["overview"], "#what"), (c["support"], f"{route}/support"), (c["privacy"], f"{route}/privacy"), (c["all"], "")], T[lang]["lang"])}
  <main>
    <section class="hero app-hero"><div class="container"><a class="backlink" href="{href(lang, "", lang, route)}">{escape(c["back"])}</a>{icon_html}<h1>Elia {app.capitalize()}</h1><p class="hero__tagline">{escape(a["tag"])}</p><p class="hero__sub lead">{escape(a["sub"])}</p><div class="btn-row"><span class="tag"><span class="tag__dot"></span>{escape(T[lang]["home"]["coming"])}</span></div></div></section>
{pre}
    <section id="what"><div class="container"><div class="section-head"><span class="eyebrow">{escape(a["head"][0])}</span><h2>{escape(a["head"][1])}</h2></div><div class="grid-2"><div class="panel"><h3>{escape(a["left"])}</h3>{ul(a["yes"], "checklist")}</div><div class="panel"><h3>{escape(a["right"])}</h3>{ul(a["no"], "notlist")}</div></div></div></section>
{story_section(a) if app == "contractions" else ""}
    <section id="principles"><div class="container"><div class="section-head"><span class="eyebrow">{escape(c["promise"])}</span><h2>{escape(a["principles"][0])}</h2>{sublead}</div>{chips(a["principles"][2 if app == "feeding" else 1])}<div class="callout" style="margin-top:32px;">{escape(a["principles"][3 if app == "feeding" else 2])}</div></div></section>
  </main>
  {footer(lang, [(c["support"], f"{route}/support"), (c["privacy"], f"{route}/privacy"), (other_name, route_other), (c["all"], "")], T[lang]["note"], route)}
</body>
</html>
"""
    write(lang, route, body)


def story_section(a):
    s = a["story"]
    return f"""<section id="story" class="tint"><div class="container"><div class="section-head"><span class="eyebrow">{escape(s[0])}</span><h2>{escape(s[1])}</h2></div><div class="story"><p>{escape(s[2])}</p><p>{escape(s[3])}</p><p class="pull">{escape(s[4])}</p><p>{escape(s[5])}</p></div></div></section>"""


def support_page(lang, app):
    c = APP[lang]["common"]
    route = f"apps/{app}/support"
    app_name = f"Elia {app.capitalize()}"
    title = f"{c['support']} — {app_name}"
    desc = f"{c['support']} — {app_name}"
    extra = feeding_style() if app == "feeding" else ""
    faq = "".join(f'<details{" open" if i == 0 else ""}><summary>{escape(q)}</summary><p>{escape(a).replace("privacy policy", f"<a href=\"{href(lang, f"apps/{app}/privacy", lang, route)}\">privacy policy</a>").replace("політиці приватності", f"<a href=\"{href(lang, f"apps/{app}/privacy", lang, route)}\">політиці приватності</a>").replace("Datenschutzerklärung", f"<a href=\"{href(lang, f"apps/{app}/privacy", lang, route)}\">Datenschutzerklärung</a>").replace("политике приватности", f"<a href=\"{href(lang, f"apps/{app}/privacy", lang, route)}\">политике приватности</a>")}</p></details>' for i, (q, a) in enumerate(SUPPORT[lang][app]))
    body = f"""<!DOCTYPE html>
<html lang="{lang}">
{head(lang, route, title, desc, "svg", None, extra)}
<body>
  {header(lang, route, [(app.capitalize(), f"apps/{app}"), (c["privacy"], f"apps/{app}/privacy"), (c["promise"], "home#philosophy")], T[lang]["lang"])}
  <main><section class="hero doc-hero"><div class="container"><a class="backlink" href="{href(lang, f"apps/{app}", lang, route)}">← {app_name}</a><h1>{escape(c["support"])}</h1><p class="updated">{escape("We keep things simple. Here are the common questions." if lang == "en" else "Ми тримаємо все простим. Ось найчастіші запитання." if lang == "uk" else "Wir halten es einfach. Hier sind die häufigsten Fragen." if lang == "de" else "Мы держим все простым. Вот частые вопросы.")}</p></div></section><section><div class="container"><div class="faq">{faq}</div><div class="prose" style="margin-top:40px;"><h2>{escape(c["still"])}</h2><p>{escape("Write to us at" if lang == "en" else "Напишіть нам на" if lang == "uk" else "Schreib uns an" if lang == "de" else "Напишите нам на")} <a href="mailto:{app}@getelia.app?subject=Elia%20{app.capitalize()}%20support">{app}@getelia.app</a>. {escape(c["read"])}</p></div></div></section></main>
  {footer(lang, [(c["overview"], f"apps/{app}"), (c["privacy"], f"apps/{app}/privacy"), (c["all"], "")], T[lang]["note"], route)}
</body>
</html>
"""
    write(lang, route, body)


def privacy_page(lang, app):
    c = APP[lang]["common"]
    route = f"apps/{app}/privacy"
    app_name = f"Elia {app.capitalize()}"
    title = f"{c['privacy']} — {app_name}"
    desc = f"{c['privacy']} — {app_name}"
    extra = feeding_style() if app == "feeding" else ""
    text = privacy_text(lang, app)
    sections = "".join(f"<h2>{escape(h)}</h2><p>{escape(p)}</p>" if isinstance(p, str) else f"<h2>{escape(h)}</h2>{ul(p, '')}" for h, p in text["sections"])
    body = f"""<!DOCTYPE html>
<html lang="{lang}">
{head(lang, route, title, desc, "svg", None, extra)}
<body>
  {header(lang, route, [(app.capitalize(), f"apps/{app}"), (c["support"], f"apps/{app}/support"), (c["promise"], "home#philosophy")], T[lang]["lang"])}
  <main><section class="hero doc-hero"><div class="container"><a class="backlink" href="{href(lang, f"apps/{app}", lang, route)}">← {app_name}</a><h1>{escape(c["privacy"])}</h1><p class="updated">{app_name} · {escape(text["updated"])}</p></div></section><section><div class="container prose"><p>{escape(text["intro"])}</p>{sections}<h2>{escape(text["contact"])}</h2><p>{escape(text["question"])} <a href="mailto:{app}@getelia.app">{app}@getelia.app</a>.</p><div class="callout">{escape(text["callout"])}</div></div></section></main>
  {footer(lang, [(c["overview"], f"apps/{app}"), (c["support"], f"apps/{app}/support"), (c["all"], "")], T[lang]["note"], route)}
</body>
</html>
"""
    write(lang, route, body)


def feeding_style():
    return """  <style>
    body { --accent: #C9976A; --accent-dark: #A9784C; --accent-light: #F3E3D1; }
    @media (prefers-color-scheme: dark) { body { --accent-light: #352A20; } }
  </style>
"""


def privacy_text(lang, app):
    if lang == "en":
        intro = "Elia is built to be private by design. It has no account, no backend, and no tracking. This policy explains, in plain language, what that means."
        return {"updated": "Last updated 13 July 2026", "intro": intro, "contact": "Contact", "question": "Questions about privacy? Reach us at", "callout": APP[lang][app]["principles"][3 if app == "feeding" else 2], "sections": [
            ("The short version", ["No account and no sign-in.", "No data is collected by Elia.", "Your data is never sold or shared.", "Everything is stored locally on your device.", "Nothing is uploaded to any Elia server."]),
            ("What the app stores", "Stored locally on your device only: your entries, history derived from them, and settings."),
            ("Data leaving your device", "Data leaves your device only when you choose to export or share it, using your device's own share options. You pick the destination. Elia does not upload your log to any service of its own."),
            ("Backups", "Automatic cloud backup and device-to-device transfer of app data are disabled. Your log moves only through an export you start yourself."),
            ("Network and permissions", "Core use does not require registration or a connection. The app avoids unnecessary permissions and contains no advertising, analytics, or third-party tracking SDKs."),
            ("Deleting your data", "Deleting the app's data, or uninstalling the app, removes the local data from your device. Because nothing is stored elsewhere, that is all it takes."),
            ("Children", "Elia is intended as a tool for adults and caregivers. It does not knowingly collect data from anyone."),
        ]}
    data = {
      "uk": ("Оновлено 13 липня 2026", "Elia від початку створена приватною. У застосунку немає акаунта, бекенду й трекінгу. Ця політика простою мовою пояснює, що це означає.", "Контакт", "Питання щодо приватності? Напишіть нам на", [
        ("Коротко", ["Без акаунта і входу.", "Elia не збирає дані.", "Ваші дані ніколи не продаються і не передаються.", "Усе зберігається локально на вашому пристрої.", "Нічого не завантажується на сервери Elia."]),
        ("Що зберігає застосунок", "Лише локально на вашому пристрої: ваші записи, похідна від них історія та налаштування."),
        ("Коли дані залишають пристрій", "Дані залишають пристрій лише тоді, коли ви самі експортуєте або ділитеся ними через системні опції пристрою. Ви самі обираєте місце призначення."),
        ("Резервні копії", "Автоматичне хмарне резервне копіювання і перенесення даних між пристроями вимкнені. Журнал рухається лише через експорт, який ви запускаєте самі."),
        ("Мережа і дозволи", "Основне використання не потребує реєстрації або з'єднання. Застосунок уникає зайвих дозволів і не містить реклами, аналітики або стороннього трекінгу."),
        ("Видалення даних", "Видалення даних застосунку або деінсталяція прибирає локальні дані з пристрою. Оскільки нічого не зберігається деінде, цього достатньо."),
        ("Діти", "Elia призначена для дорослих і доглядальників. Вона свідомо не збирає дані ні про кого."),
      ]),
      "de": ("Zuletzt aktualisiert am 13. Juli 2026", "Elia ist von Anfang an privat gedacht. Es gibt kein Konto, kein Backend und kein Tracking. Diese Richtlinie erklärt in einfacher Sprache, was das bedeutet.", "Kontakt", "Fragen zum Datenschutz? Schreib uns an", [
        ("Kurzfassung", ["Kein Konto und keine Anmeldung.", "Elia sammelt keine Daten.", "Deine Daten werden nie verkauft oder geteilt.", "Alles wird lokal auf deinem Gerät gespeichert.", "Nichts wird auf Elia-Server hochgeladen."]),
        ("Was die App speichert", "Nur lokal auf deinem Gerät: deine Einträge, daraus abgeleitete Historie und Einstellungen."),
        ("Wenn Daten dein Gerät verlassen", "Daten verlassen dein Gerät nur, wenn du sie selbst über die Teilen-Funktionen deines Geräts exportierst oder teilst. Du wählst das Ziel."),
        ("Backups", "Automatische Cloud-Backups und Geräteübertragung von App-Daten sind deaktiviert. Dein Protokoll bewegt sich nur durch einen Export, den du selbst startest."),
        ("Netzwerk und Berechtigungen", "Die Kernnutzung braucht keine Registrierung und keine Verbindung. Die App vermeidet unnötige Berechtigungen und enthält keine Werbung, Analyse oder Tracking-SDKs."),
        ("Daten löschen", "Wenn du App-Daten löschst oder die App deinstallierst, werden die lokalen Daten vom Gerät entfernt. Da nichts anderswo gespeichert wird, reicht das aus."),
        ("Kinder", "Elia ist als Werkzeug für Erwachsene und Betreuungspersonen gedacht. Sie sammelt wissentlich keine Daten von irgendwem."),
      ]),
      "ru": ("Обновлено 13 июля 2026", "Elia изначально сделана приватной. В приложении нет аккаунта, бэкенда и трекинга. Эта политика простым языком объясняет, что это значит.", "Контакт", "Вопросы о приватности? Напишите нам на", [
        ("Коротко", ["Без аккаунта и входа.", "Elia не собирает данные.", "Ваши данные никогда не продаются и не передаются.", "Все хранится локально на вашем устройстве.", "Ничего не загружается на серверы Elia."]),
        ("Что хранит приложение", "Только локально на вашем устройстве: ваши записи, история на их основе и настройки."),
        ("Когда данные покидают устройство", "Данные покидают устройство только когда вы сами экспортируете или отправляете их через системные функции устройства. Вы сами выбираете адресата."),
        ("Резервные копии", "Автоматическое облачное резервное копирование и перенос данных между устройствами отключены. Журнал перемещается только через экспорт, который запускаете вы."),
        ("Сеть и разрешения", "Основное использование не требует регистрации или соединения. Приложение избегает лишних разрешений и не содержит рекламы, аналитики или стороннего трекинга."),
        ("Удаление данных", "Удаление данных приложения или деинсталляция убирает локальные данные с устройства. Поскольку ничего не хранится где-то еще, этого достаточно."),
        ("Дети", "Elia предназначена как инструмент для взрослых и людей, которые ухаживают за ребенком. Она сознательно не собирает данные ни о ком."),
      ]),
    }
    updated, intro, contact, question, sections = data[lang]
    return {"updated": updated, "intro": intro, "contact": contact, "question": question, "sections": sections, "callout": APP[lang][app]["principles"][3 if app == "feeding" else 2]}


def not_found(lang):
    route = ""
    title = {"en": "Page not found — Elia", "uk": "Сторінку не знайдено — Elia", "de": "Seite nicht gefunden — Elia", "ru": "Страница не найдена — Elia"}[lang]
    text = {"en": "Take a breath. This page doesn't exist — but the rest of Elia does.", "uk": "Зробіть вдих. Цієї сторінки немає — але решта Elia на місці.", "de": "Atme kurz durch. Diese Seite gibt es nicht — der Rest von Elia schon.", "ru": "Сделайте вдох. Этой страницы нет — но остальная Elia на месте."}[lang]
    btn = {"en": "Back to Elia", "uk": "Назад до Elia", "de": "Zurück zu Elia", "ru": "Назад к Elia"}[lang]
    body = f"""<!DOCTYPE html>
<html lang="{lang}">
{head(lang, "", title, text)}
<body><main><section class="hero"><div class="container"><img class="brand__mark" src="{asset("assets/img/favicon.svg", lang, route)}" alt="" style="width:40px;height:40px;border-radius:12px;margin:0 auto 24px;" /><h1 class="hero__wordmark" style="font-size:clamp(40px,9vw,72px);">{escape(title.split(" — ")[0])}</h1><p class="hero__sub lead">{escape(text)}</p><div class="btn-row"><a class="btn btn--primary" href="{href(lang, "", lang, route)}">{escape(btn)}</a></div></div></section></main></body></html>"""
    if lang == "en":
        (ROOT / "404.html").write_text(body, encoding="utf-8")


def sitemap():
    routes = ["", "apps/contractions", "apps/feeding", "apps/contractions/privacy", "apps/contractions/support", "apps/feeding/privacy", "apps/feeding/support"]
    urls = []
    for route in routes:
        for lang in LANGS:
            urls.append(f"""  <url>
    <loc>{url(lang, route)}</loc>
    <lastmod>2026-07-19</lastmod>
    <priority>{"1.0" if route == "" else "0.8" if route.count("/") == 1 else "0.3"}</priority>
  </url>""")
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n", encoding="utf-8")


def write(lang, route, body):
    path = out_path(lang, route)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


for lang in LANGS:
    home(lang)
    for app in ["contractions", "feeding"]:
        app_page(lang, app)
        privacy_page(lang, app)
        support_page(lang, app)
    not_found(lang)
sitemap()
