#!/usr/bin/env python3
"""Genera las fichas de los 118 elementos y la tabla índice, en inglés y en español.

    python3 tools/elements.py [ruta al repositorio de la app]

Lee los mismos datos que la app (Element.json, Isotopes.json y
Localizable.strings del repositorio PeriodicTable), así que cada cifra de la
web es la que el estudiante ve en la app. Solo publica los datos gratuitos:
lo que la app reserva a Pro (punto crítico, propiedades eléctricas, medidas
magnéticas, CID y RTECS, isótopos radiactivos) no sale aquí.

Escribe:
  elements/<nombre>/index.html   y   es/elementos/<nombre>/index.html
  elements/index.html            y   es/elementos/index.html   (tabla índice)
  assets/site.css                     (estilo compartido de estas páginas)
  sitemap.xml                         (todas las páginas del sitio)
"""
import html
import json
import os
import re
import sys
import unicodedata
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_REPO = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(ROOT), 'PeriodicTable')
DB = os.path.join(APP_REPO, 'Tabla Periodica', 'Database')
LOC = os.path.join(APP_REPO, 'Tabla Periodica', 'Localizable')
SITE = 'https://periodictable.echandia.app'
APPSTORE = 'https://apps.apple.com/app/id1455103430'
TODAY = date.today().isoformat()
e = html.escape

FAMILY = {1: 'ae', 2: 'am', 3: 'tm', 4: 'pt', 5: 'md', 6: 'nm', 7: 'hl', 8: 'ng', 9: 'ln', 10: 'ac', 11: 'ac'}
FAMILY_BY_NAME = {'Alkali Metal': 'am', 'Alkaline Earth Metal': 'ae', 'Transition Metal': 'tm', 'Poor Metal': 'pt',
                  'Metalloid': 'md', 'Nonmetal': 'nm', 'Halogen': 'hl', 'Noble Gas': 'ng', 'Lanthanide': 'ln',
                  'Actinoid': 'ac', 'SuperActinoid': 'ac'}
SUP = str.maketrans('0123456789+-−', '⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁻')

APPLE = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M16.37 12.6c-.02-2.3 1.88-3.4 1.96-3.46-1.07-1.56-2.73-1.77-3.32-1.8-1.41-.14-2.76.83-3.47.83-.72 0-1.82-.81-2.99-.79-1.54.02-2.96.9-3.75 2.27-1.6 2.78-.41 6.89 1.15 9.14.76 1.1 1.67 2.34 2.86 2.3 1.15-.05 1.58-.74 2.97-.74 1.38 0 1.77.74 2.98.72 1.24-.02 2.02-1.12 2.77-2.23.87-1.28 1.23-2.52 1.25-2.58-.03-.01-2.39-.92-2.41-3.66zM14.1 5.86c.63-.77 1.06-1.83.94-2.89-.91.04-2.02.61-2.67 1.37-.58.67-1.09 1.76-.96 2.8 1.02.08 2.06-.51 2.69-1.28z"/></svg>')

# ------------------------------------------------------------------ textos
U = {
    'en': dict(
        home='Periodic Table', home_url='/', idx_url='/elements/', idx_name='Elements', other='Español',
        skip='Skip to content', crumbs='Breadcrumb', store_small='Download on the',
        title='{name} ({sym}): atomic mass, electron configuration and properties',
        desc='{name} ({sym}), element {z}: atomic mass {mass} u, electron configuration {conf}, {cat_l}. Melting and boiling point, density, electronegativity and natural isotopes, checked against PubChem, IUPAC, NIST and the IAEA.',
        h1='{name} ({sym})',
        lead='{name} is {a_cat} with atomic number {z}, in period {period}{group_part} of the periodic table. Its atomic mass is {mass} u and its electron configuration is {conf}.',
        group_part=' and group {group}', f_block_part=', in the f-block',
        state={'solid': 'Solid at 25 °C.', 'liquid': 'Liquid at 25 °C.', 'gas': 'Gas at 25 °C.'},
        key='Key facts', atomic='Atomic properties', physical='Physical and thermal properties',
        ident='Identification and history', isotopes='Natural isotopes', iso_cols=('Isotope', 'Mass (u)', 'Abundance'),
        no_iso='{name} has no stable isotopes: every isotope is radioactive.',
        unknown='---', unknown_note='A dash (---) means there is no reliable published measurement. The app never makes one up.',
        predicted_note='No visible amount of {name} has ever been made: its physical properties here are theoretical estimates, not measurements.',
        sources='Data checked against PubChem (NIH), IUPAC, the NIST Atomic Spectra Database and the IAEA (NUBASE and AME), the same data you see in the app.',
        app_h='See {name} in the app',
        app_p='Orbital diagram with Hund’s rule, emission spectrum, shell model, every isotope, a real photo, and comparison with any other element. Free, no ads, works offline.',
        prev='Previous', next='Next', all='All 118 elements', calcs='Molar mass calculator', calcs_url='/molar-mass-calculator/',
        made_by='Created by', made='Made with <span role="img" aria-label="love">&#x2665;&#xFE0E;</span> in Peru <span aria-hidden="true">🇵🇪</span>',
        privacy=('Privacy', '/privacidad/#en'), support=('Support', '/soporte/#en'),
        labels=dict(z='Atomic number', mass='Atomic mass', cat='Category', period='Period', group='Group', block='Block',
                    conf='Electron configuration', shells='Electrons per shell', en='Electronegativity (Pauling)',
                    ox='Oxidation states', ox_note='common in bold', melt='Melting point', boil='Boiling point',
                    dens='Density', ion='First ionization energy', aff='Electron affinity', r_at='Atomic radius',
                    r_cov='Covalent radius', r_vdw='Van der Waals radius', ioncharge='Common ions', molvol='Molar volume',
                    hfus='Heat of fusion', hvap='Heat of vaporization', cp='Specific heat', k='Thermal conductivity',
                    alpha='Thermal expansion', mohs='Mohs hardness', young='Young’s modulus', crystal='Crystal structure',
                    magnetic='Magnetic type', state='State at 25 °C', cas='CAS number', latin='Latin name',
                    discovered='Discovered by', named='Named by', protons='Protons, neutrons, electrons'),
        states={'solid': 'Solid', 'liquid': 'Liquid', 'gas': 'Gas'}, f_block='f-block, no group number',
        idx_title='Periodic table of elements: properties of all 118 elements',
        idx_desc='Interactive periodic table with a page for each of the 118 elements: atomic mass, electron configuration, melting and boiling point, density, electronegativity and isotopes.',
        idx_h1='The periodic table of elements',
        idx_lead='Tap an element to see its atomic mass, electron configuration, melting and boiling point, density, electronegativity and natural isotopes. The same data as in the app.',
        idx_list='All elements by atomic number', idx_app_h='Every element, in depth, in the app',
    ),
    'es': dict(
        home='Tabla Periódica', home_url='/es/', idx_url='/es/elementos/', idx_name='Elementos', other='English',
        skip='Ir al contenido', crumbs='Ruta', store_small='Descárgala en el',
        title='{name} ({sym}): masa atómica, configuración electrónica y propiedades',
        desc='{name} ({sym}), elemento {z}: masa atómica {mass} u, configuración electrónica {conf}, {cat_l}. Punto de fusión y ebullición, densidad, electronegatividad e isótopos naturales, contrastados con PubChem, IUPAC, NIST y el OIEA.',
        h1='{name} ({sym})',
        lead='El {name_l} es un {cat_l} de número atómico {z}, en el periodo {period}{group_part} de la tabla periódica. Su masa atómica es {mass} u y su configuración electrónica, {conf}.',
        group_part=' y el grupo {group}', f_block_part=', en el bloque f',
        state={'solid': 'Sólido a 25 °C.', 'liquid': 'Líquido a 25 °C.', 'gas': 'Gas a 25 °C.'},
        key='Datos clave', atomic='Propiedades atómicas', physical='Propiedades físicas y térmicas',
        ident='Identificación e historia', isotopes='Isótopos naturales', iso_cols=('Isótopo', 'Masa (u)', 'Abundancia'),
        no_iso='El {name_l} no tiene isótopos estables: todos sus isótopos son radiactivos.',
        unknown='---', unknown_note='Un guion (---) significa que no hay una medición publicada fiable. La app nunca se la inventa.',
        predicted_note='Nunca se ha obtenido una cantidad visible de {name_l}: sus propiedades físicas aquí son estimaciones teóricas, no mediciones.',
        sources='Datos contrastados con PubChem (NIH), la IUPAC, la base de espectros atómicos del NIST y el OIEA (NUBASE y AME): los mismos que ves en la app.',
        app_h='Mira el {name_l} en la app',
        app_p='Diagrama de orbitales con la regla de Hund, espectro de emisión, modelo de capas, todos sus isótopos, una fotografía real y la comparación con cualquier otro elemento. Gratis, sin anuncios y sin conexión.',
        prev='Anterior', next='Siguiente', all='Los 118 elementos', calcs='Calculadora de masa molar', calcs_url='/es/calculadora-masa-molar/',
        made_by='Creada por', made='Hecha con <span role="img" aria-label="amor">&#x2665;&#xFE0E;</span> en Perú <span aria-hidden="true">🇵🇪</span>',
        privacy=('Privacidad', '/privacidad/#es'), support=('Soporte', '/soporte/#es'),
        labels=dict(z='Número atómico', mass='Masa atómica', cat='Categoría', period='Periodo', group='Grupo', block='Bloque',
                    conf='Configuración electrónica', shells='Electrones por capa', en='Electronegatividad (Pauling)',
                    ox='Estados de oxidación', ox_note='los comunes en negrita', melt='Punto de fusión', boil='Punto de ebullición',
                    dens='Densidad', ion='Primera energía de ionización', aff='Afinidad electrónica', r_at='Radio atómico',
                    r_cov='Radio covalente', r_vdw='Radio de Van der Waals', ioncharge='Iones comunes', molvol='Volumen molar',
                    hfus='Calor de fusión', hvap='Calor de vaporización', cp='Calor específico', k='Conductividad térmica',
                    alpha='Dilatación térmica', mohs='Dureza de Mohs', young='Módulo de Young', crystal='Estructura cristalina',
                    magnetic='Tipo magnético', state='Estado a 25 °C', cas='Número CAS', latin='Nombre en latín',
                    discovered='Descubierto por', named='Nombrado por', protons='Protones, neutrones, electrones'),
        states={'solid': 'Sólido', 'liquid': 'Líquido', 'gas': 'Gas'}, f_block='bloque f, sin número de grupo',
        idx_title='Tabla periódica de los elementos: propiedades de los 118 elementos',
        idx_desc='Tabla periódica interactiva con una ficha para cada uno de los 118 elementos: masa atómica, configuración electrónica, punto de fusión y ebullición, densidad, electronegatividad e isótopos.',
        idx_h1='La tabla periódica de los elementos',
        idx_lead='Toca un elemento para ver su masa atómica, configuración electrónica, punto de fusión y ebullición, densidad, electronegatividad e isótopos naturales. Los mismos datos que en la app.',
        idx_list='Todos los elementos por número atómico', idx_app_h='Cada elemento, a fondo, en la app',
    ),
}

EXTRA_CSS = '''
/* element pages */
.crumbs { margin: 28px 0 0; font-size: .92rem; color: var(--muted); }
.crumbs a { color: var(--muted); }
.el-hero { display: grid; gap: 28px; align-items: center; padding: 20px 0 0; }
@media (min-width: 760px) { .el-hero { grid-template-columns: auto 1fr; gap: 48px; padding-top: 36px; } }
.el-hero h1 { font-size: clamp(2.3rem, 6vw, 3.6rem); letter-spacing: -.03em; font-weight: 750; }
.el-hero .lead { margin-bottom: 18px; }
.big-cell { position: relative; width: 220px; height: 236px; border-radius: 18px; background: var(--surface);
  border: 1px solid var(--line); box-shadow: inset 0 -10px 0 var(--c); padding: 18px 20px; color: var(--title); }
.big-cell .z { font-size: 1.3rem; font-weight: 600; color: var(--muted); }
.big-cell .sym { display: block; font-size: 5.4rem; font-weight: 750; line-height: 1; letter-spacing: -.03em; margin-top: 6px; }
.big-cell .nm { display: block; font-size: 1.15rem; font-weight: 650; margin-top: 10px; }
.big-cell .ms { display: block; font-size: .95rem; color: var(--muted); font-variant-numeric: tabular-nums; }
.props { display: grid; gap: 18px; margin-top: 28px; }
@media (min-width: 860px) { .props { grid-template-columns: 1fr 1fr; } }
.props section { background: var(--surface); border: 1px solid var(--line); border-radius: 18px; overflow: hidden; }
.props h2 { font-size: 1.15rem; letter-spacing: -.01em; padding: 18px 20px 6px; }
.props table { width: 100%; border-collapse: collapse; font-variant-numeric: tabular-nums; }
.props th, .props td { padding: 11px 20px; text-align: left; vertical-align: top; border-top: 1px solid var(--line); font-size: .97rem; }
.props th { font-weight: 500; color: var(--muted); width: 46%; }
.props td { color: var(--title); font-weight: 600; }
.props td small { display: block; font-weight: 450; color: var(--muted); }
.props .wide { grid-column: 1 / -1; }
.notes { margin-top: 18px; color: var(--muted); font-size: .95rem; max-width: 52rem; }
.notes p { margin: 6px 0; }
.pager { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 28px; padding: 0; list-style: none; }
.pager a { display: inline-flex; align-items: center; gap: 8px; min-height: 44px; padding: 0 18px; border-radius: 999px;
  background: var(--surface); border: 1px solid var(--line); text-decoration: none; font-weight: 600; }
.app-cta { margin-top: var(--space); display: grid; gap: 24px; align-items: center; padding: 28px; border-radius: 20px;
  background: var(--surface); border: 1px solid var(--line); }
@media (min-width: 760px) { .app-cta { grid-template-columns: 1fr auto; } }
.app-cta h2 { font-size: 1.6rem; }
.app-cta p { color: var(--muted); margin: 8px 0 0; }
/* index table */
.ptable-wrap { overflow-x: auto; margin: 28px -16px 0; padding: 0 16px 12px; }
.ptable { display: grid; grid-template-columns: repeat(18, minmax(54px, 1fr)); gap: 4px; min-width: 1040px; }
.ptable a { position: relative; aspect-ratio: 1 / 1.18; border-radius: 6px; background: var(--surface); border: 1px solid var(--line);
  box-shadow: inset 0 -4px 0 var(--c); text-decoration: none; color: var(--title); padding: 4px 5px;
  display: flex; flex-direction: column; justify-content: center; align-items: center; padding-top: 14px; }
.ptable a:hover { border-color: var(--title); }
.ptable small { position: absolute; top: 3px; left: 5px; font-size: .62rem; color: var(--muted); }
.ptable b { font-size: 1.1rem; line-height: 1; }
.ptable span { font-size: .55rem; color: var(--muted); margin-top: 3px; max-width: 100%; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.ptable .gap { grid-column: span 1; }
.ellist { columns: 2; column-gap: 32px; margin: 18px 0 0; padding: 0; list-style: none; font-size: .95rem; }
@media (min-width: 760px) { .ellist { columns: 4; } }
.ellist li { break-inside: avoid; margin: 0 0 6px; }
'''


# ------------------------------------------------------------------ datos
def load_strings(lang):
    s = open(os.path.join(LOC, f'{lang}.lproj', 'Localizable.strings'), encoding='utf-8').read()
    return {k.replace('\\"', '"'): v.replace('\\"', '"')
            for k, v in re.findall(r'^"((?:[^"\\]|\\.)*)"\s*=\s*"((?:[^"\\]|\\.)*)";', s, re.M)}


def slug(name):
    n = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', n).strip('-')


def known(v):
    return v not in (-1, '-1', '', None, '---')


def num(v):
    """Un número tal como lo guarda la app, sin ceros de más."""
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return str(v)


def rich(s):
    """'3×10^{-7}' → '3×10⁻⁷', 'Fe^{3+}' → 'Fe³⁺'."""
    return re.sub(r'\^\{([^}]*)\}', lambda m: m.group(1).translate(SUP), str(s))


def sci(v):
    """1.18e-05 → '1.18 × 10⁻⁵'."""
    m, ex = f'{v:.3g}'.split('e') if 'e' in f'{v:.3g}' else (f'{v:.3g}', None)
    return f'{m} × 10{str(int(ex)).translate(SUP)}' if ex else m


ORDER = 'spdf'


def configuration(raw):
    """Reordena la configuración como la app: por n y luego por l ('[Ar] 3d⁶ 4s²')."""
    parts = raw.split()
    core = [p for p in parts if p.startswith('[')]
    subs = []
    for p in parts:
        m = re.match(r'(\d+)([spdf])\^\{(\d+)\}', p)
        if m:
            subs.append((int(m.group(1)), ORDER.index(m.group(2)), f'{m.group(1)}{m.group(2)}{m.group(3).translate(SUP)}'))
    if not subs:
        return rich(raw)
    subs.sort()
    return ' '.join(core + [s[2] for s in subs])


def state(el):
    melt, boil = el['absoluteMeltingPoint'], el['absoluteBoilingPoint']
    if known(boil) and boil < 298.15:
        return 'gas'
    if known(melt) and melt > 298.15:
        return 'solid'
    if known(melt) and known(boil):
        return 'liquid'
    return None


def kelvin(v):
    c = round(v - 273.15, 2)
    c = int(c) if c == int(c) else c
    return f'{num(v)} K', f'{c} °C'.replace('-', '−')


def shells(cap):
    vals = [int(x[1:]) for x in cap.split('-') if x[1:].isdigit()]
    while vals and vals[-1] == 0:
        vals.pop()
    return ', '.join(map(str, vals))


def oxidation(el):
    st = sorted(el.get('oxidationStates') or [], key=lambda o: o['v'])
    if not st:
        return None
    fmt = lambda v: ('+' if v > 0 else '') + str(v).replace('-', '−')
    return ', '.join((f'<b>{fmt(o["v"])}</b>' if o.get('rank') == 0 else fmt(o['v'])) for o in st)


def natural_isotopes(iso, z, sym):
    out = []
    for i in iso.get(str(z), []):
        if 'ab' in i and known(i['ab']):
            out.append((f'<sup>{i["a"]}</sup>{sym}', f'{i["m"]:.6f}'.rstrip('0').rstrip('.'), f'{num(i["ab"])} %'))
    return out


# ------------------------------------------------------------------ html
def shell_page(lang, *, title, desc, path, alt_paths, body, ld, css_href, og):
    u = U[lang]
    other = 'es' if lang == 'en' else 'en'
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="color-scheme" content="light">
<link rel="canonical" href="{SITE}{path}">
<link rel="alternate" hreflang="en" href="{SITE}{alt_paths['en']}">
<link rel="alternate" hreflang="es" href="{SITE}{alt_paths['es']}">
<link rel="alternate" hreflang="x-default" href="{SITE}{alt_paths['en']}">
<meta name="apple-itunes-app" content="app-id=1455103430">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{SITE}/{og}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/icon.png">
<link rel="apple-touch-icon" href="/icon.png">
<link rel="stylesheet" href="{css_href}">
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=1)}
</script>
</head>
<body>
<a class="skip" href="#main">{e(u["skip"])}</a>
<div class="wrap">
<header class="site">
<a class="brand" href="{u["home_url"]}"><img src="/icon.png" width="32" height="32" alt="">{e(u["home"])}</a>
<a class="langlink" href="{alt_paths[other]}" hreflang="{other}" lang="{other}">{u["other"]}</a>
</header>
{body}
<footer>
<div class="maker">
<p>{u["made_by"]} Josue Echandia · <a href="mailto:josue@echandia.app">josue@echandia.app</a></p>
<p>{u["made"]}</p>
</div>
<nav aria-label="Legal">
<a href="{u["privacy"][1]}">{u["privacy"][0]}</a>
<a href="{u["support"][1]}">{u["support"][0]}</a>
</nav>
</footer>
</div>
</body>
</html>
'''


def store_button(lang):
    return f'<a class="store" href="{APPSTORE}">{APPLE}<span><small>{e(U[lang]["store_small"])}</small><b>App Store</b></span></a>'


def table(rows):
    return '<table>' + ''.join(f'<tr><th scope="row">{e(k)}</th><td>{v}</td></tr>' for k, v in rows) + '</table>'


def element_page(el, lang, ctx):
    u, Lb, L = U[lang], U[lang]['labels'], ctx['L'][lang]
    z, sym = el['atomicNumber'], el['shortName']
    name = ctx['name'][lang][z]
    name_l = name.lower() if lang == 'es' else name
    cat = L.get(el['category'], el['category'])
    fam = FAMILY_BY_NAME.get(el['category'], 'tm')
    mass = num(el['atomWeigth'])
    conf = configuration(el['electronicConfiguration'])
    unk = f'<span title="{e(u["unknown_note"])}">{u["unknown"]}</span>'
    # Lantánidos y actínidos: sin número de grupo (los datos de la app traen
    # valores sueltos, como el 16 del lutecio). "Bloque f" solo si lo es.
    f_block = el['block'] == 'f'
    no_group = el['category'] in ('Lanthanide', 'Actinoid')
    group = None if no_group or not known(el['groupNumber']) or el['groupNumber'] < 1 else el['groupNumber']
    if lang == 'en':
        a_cat = ('an ' if cat[0].lower() in 'aeiou' else 'a ') + cat.lower()
    else:
        a_cat = cat.lower()
    group_part = u['group_part'].format(group=group) if group else (u['f_block_part'] if f_block else '')
    lead = u['lead'].format(name=name, name_l=name_l, a_cat=a_cat, cat_l=cat.lower(), z=z, period=el['periodNumber'],
                            group_part=group_part, mass=mass, conf=conf)
    st = state(el)
    if st and z < 100:
        lead += ' ' + u['state'][st]

    def val(v, unit=''):
        return f'{e(num(v))}{(" " + unit) if unit else ""}' if known(v) else unk

    def temp(v):
        if not known(v):
            return unk
        k, c = kelvin(v)
        return f'{k}<small>{c}</small>'

    dens_unit = 'g/L' if st == 'gas' else 'g/cm³'
    ox = oxidation(el)
    key_rows = [
        (Lb['z'], str(z)), (Lb['mass'], f'{mass} u'), (Lb['cat'], e(cat)), (Lb['period'], str(el['periodNumber'])),
        (Lb['group'], str(group) if group else (e(u['f_block']) if f_block else unk)), (Lb['block'], e(el['block'] or '---')),
        (Lb['conf'], conf), (Lb['shells'], shells(el['electronicCap']) or unk),
        (Lb['en'], val(el['reativityElectronegativity'])),
        (Lb['ox'], f'{ox}<small>{e(Lb["ox_note"])}</small>' if ox else unk),
        (Lb['state'], e(u['states'][st]) if st and z < 100 else unk),
        (Lb['melt'], temp(el['absoluteMeltingPoint'])), (Lb['boil'], temp(el['absoluteBoilingPoint'])),
        (Lb['dens'], val(el['atomDensity'], dens_unit)),
    ]
    atomic_rows = [
        (Lb['ion'], val(el['ionizationPotencialAnAtom'], 'eV')),
        (Lb['aff'], val(el['reativityElectronAffinity'], 'kJ/mol')),
        (Lb['r_at'], val(el['radiusAtomic'], 'pm')), (Lb['r_cov'], val(el['radiusCovalent'], 'pm')),
        (Lb['r_vdw'], val(el['radioVanDerWalls'], 'pm')),
        (Lb['ioncharge'], e(rich(el['ionCharge'])) if known(el['ionCharge']) else unk),
        (Lb['protons'], f'{el["protonsNumber"]}, {el["neutronsNumber"]}, {el["electronsNumber"]}'),
    ]
    alpha = el['thermalExpansion']
    crystal = L.get(el['crystalStructure'], el['crystalStructure']) if known(el['crystalStructure']) else ''
    if crystal:
        crystal = crystal[0] + crystal[1:].lower()          # la app lo guarda con mayúsculas de título
    magnetic = L.get(el['magneticType'], el['magneticType']) if known(el['magneticType']) else ''
    phys_rows = [
        (Lb['molvol'], val(el['atomMolarVolume'], 'cm³/mol')),
        (Lb['hfus'], val(el['heatofFusion'], 'kJ/mol')), (Lb['hvap'], val(el['heatofVaporization'], 'kJ/mol')),
        (Lb['cp'], val(el['specificHeat'], 'J/(kg·K)')), (Lb['k'], val(el['thermalConductivity'], 'W/(m·K)')),
        (Lb['alpha'], f'{sci(alpha)} K⁻¹' if known(alpha) and isinstance(alpha, (int, float)) else unk),
        (Lb['mohs'], val(el['mohsHardness'])), (Lb['young'], val(el['youngModulus'], 'GPa')),
        (Lb['crystal'], e(crystal) if crystal else unk), (Lb['magnetic'], e(magnetic) if magnetic else unk),
    ]
    disc = L.get(el['discoverPerson'], el['discoverPerson']) if el['discoverYear'] == -1 else \
        ' · '.join(x for x in (el['discoverPerson'], str(el['discoverYear'])) if known(x))
    named = ' · '.join(x for x in (el['namedPerson'], str(el['namedYear'])) if known(x))
    ident_rows = [
        (Lb['cas'], e(el['casNumber']) if known(el['casNumber']) else unk),
        (Lb['latin'], e(el['latinName']) if known(el['latinName']) else unk),
        (Lb['discovered'], e(disc) if disc else unk), (Lb['named'], e(named) if named else unk),
    ]
    iso = natural_isotopes(ctx['iso'], z, sym)
    if iso:
        iso_html = ('<table><tr>' + ''.join(f'<th scope="col">{e(c)}</th>' for c in u['iso_cols']) + '</tr>' +
                    ''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>' for a, b, c in iso) + '</table>')
    else:
        iso_html = f'<p class="note" style="padding:0 20px 16px">{e(u["no_iso"].format(name=name, name_l=name_l))}</p>'

    paths = {l: element_path(l, z, ctx) for l in ('en', 'es')}
    prev_z, next_z = (z - 1 if z > 1 else None), (z + 1 if z < 118 else None)
    pager = []
    if prev_z:
        pager.append(f'<li><a href="{element_path(lang, prev_z, ctx)}" rel="prev">← {e(u["prev"])}: {e(ctx["name"][lang][prev_z])}</a></li>')
    if next_z:
        pager.append(f'<li><a href="{element_path(lang, next_z, ctx)}" rel="next">{e(u["next"])}: {e(ctx["name"][lang][next_z])} →</a></li>')
    pager.append(f'<li><a href="{u["idx_url"]}">{e(u["all"])}</a></li>')
    pager.append(f'<li><a href="{u["calcs_url"]}">{e(u["calcs"])}</a></li>')
    notes = [u['sources'], u['unknown_note']]
    if z >= 100:
        notes.insert(0, u['predicted_note'].format(name=name, name_l=name_l))

    body = f'''<nav class="crumbs" aria-label="{u["crumbs"]}"><a href="{u["home_url"]}">{e(u["home"])}</a> › <a href="{u["idx_url"]}">{e(u["idx_name"])}</a> › <span aria-current="page">{e(name)}</span></nav>
<main id="main">
<div class="el-hero">
<div class="big-cell" style="--c:var(--c-{fam})" aria-hidden="true"><span class="z">{z}</span><span class="sym">{e(sym)}</span><span class="nm">{e(name)}</span><span class="ms">{mass} u</span></div>
<div>
<h1>{e(u["h1"].format(name=name, sym=sym))}</h1>
<p class="lead">{lead}</p>
<div class="cta">{store_button(lang)}</div>
</div>
</div>
<div class="props">
<section><h2>{e(u["key"])}</h2>{table(key_rows)}</section>
<section><h2>{e(u["atomic"])}</h2>{table(atomic_rows)}</section>
<section><h2>{e(u["physical"])}</h2>{table(phys_rows)}</section>
<section><h2>{e(u["ident"])}</h2>{table(ident_rows)}</section>
<section class="wide"><h2>{e(u["isotopes"])}</h2>{iso_html}</section>
</div>
<div class="notes">{"".join(f"<p>{e(n)}</p>" for n in notes)}</div>
<ul class="pager">{"".join(pager)}</ul>
<div class="app-cta">
<div><h2>{e(u["app_h"].format(name=name, name_l=name_l))}</h2><p>{e(u["app_p"])}</p></div>
<div class="cta">{store_button(lang)}</div>
</div>
</main>'''
    title = u['title'].format(name=name, sym=sym)
    desc = u['desc'].format(name=name, sym=sym, z=z, mass=mass, conf=conf, cat_l=cat.lower())
    ld = [{'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': u['home'], 'item': SITE + u['home_url']},
        {'@type': 'ListItem', 'position': 2, 'name': u['idx_name'], 'item': SITE + u['idx_url']},
        {'@type': 'ListItem', 'position': 3, 'name': name, 'item': SITE + paths[lang]}]}]
    return shell_page(lang, title=title, desc=desc, path=paths[lang], alt_paths=paths, body=body, ld=ld,
                      css_href='/assets/site.css', og='og.jpg' if lang == 'en' else 'og-es.jpg')


def index_page(lang, ctx):
    u = U[lang]
    cells = {}
    for el in ctx['els']:
        cells[(el['positionY'], el['positionX'])] = el
    grid = []
    for y in range(1, 11):
        if y == 8:
            grid.append('<div class="gap" style="grid-column:1/-1;height:10px"></div>')
            continue
        for x in range(1, 19):
            el = cells.get((y, x))
            if not el:
                grid.append('<div class="gap" aria-hidden="true"></div>')
                continue
            z = el['atomicNumber']
            fam = FAMILY_BY_NAME.get(el['category'], 'tm')
            nm = ctx['name'][lang][z]
            grid.append(f'<a href="{element_path(lang, z, ctx)}" style="--c:var(--c-{fam})" aria-label="{e(nm)}, {z}">'
                        f'<small>{z}</small><b>{e(el["shortName"])}</b><span>{e(nm)}</span></a>')
    lst = ''.join(f'<li>{el["atomicNumber"]} · <a href="{element_path(lang, el["atomicNumber"], ctx)}">{e(ctx["name"][lang][el["atomicNumber"]])}</a> ({e(el["shortName"])})</li>'
                  for el in ctx['els'])
    body = f'''<nav class="crumbs" aria-label="{u["crumbs"]}"><a href="{u["home_url"]}">{e(u["home"])}</a> › <span aria-current="page">{e(u["idx_name"])}</span></nav>
<main id="main">
<div class="block" style="margin-top:28px">
<h1 style="font-size:clamp(2.2rem,5vw,3.4rem);letter-spacing:-.03em">{e(u["idx_h1"])}</h1>
<p class="sub">{e(u["idx_lead"])}</p>
</div>
<div class="ptable-wrap"><div class="ptable">{"".join(grid)}</div></div>
<div class="block">
<h2>{e(u["idx_list"])}.</h2>
<ul class="ellist">{lst}</ul>
</div>
<div class="app-cta">
<div><h2>{e(u["idx_app_h"])}</h2><p>{e(u["app_p"])}</p></div>
<div class="cta">{store_button(lang)}</div>
</div>
</main>'''
    paths = {'en': U['en']['idx_url'], 'es': U['es']['idx_url']}
    ld = [{'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': u['home'], 'item': SITE + u['home_url']},
        {'@type': 'ListItem', 'position': 2, 'name': u['idx_name'], 'item': SITE + u['idx_url']}]}]
    return shell_page(lang, title=u['idx_title'], desc=u['idx_desc'], path=paths[lang], alt_paths=paths, body=body,
                      ld=ld, css_href='/assets/site.css', og='og.jpg' if lang == 'en' else 'og-es.jpg')


def element_path(lang, z, ctx):
    return (U[lang]['idx_url'] + ctx['slug'][lang][z] + '/')


def write(rel, text):
    out = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'w', encoding='utf-8').write(text)


def sitemap(ctx):
    """El sitemap entero: landings, calculadoras, elementos y páginas legales."""
    pairs = [('/', '/es/'), ('/molar-mass-calculator/', '/es/calculadora-masa-molar/'), ('/ph-calculator/', '/es/calculadora-ph/'),
             ('/balance-chemical-equations/', '/es/ajustar-ecuaciones/'), (U['en']['idx_url'], U['es']['idx_url'])]
    pairs += [(element_path('en', z, ctx), element_path('es', z, ctx)) for z in range(1, 119)]
    out = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for en, es in pairs:
        for loc in (en, es):
            out.append(f'  <url><loc>{SITE}{loc}</loc><lastmod>{TODAY}</lastmod>'
                       f'<xhtml:link rel="alternate" hreflang="en" href="{SITE}{en}"/>'
                       f'<xhtml:link rel="alternate" hreflang="es" href="{SITE}{es}"/>'
                       f'<xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{en}"/></url>')
    for p in ('/soporte/', '/privacidad/'):
        out.append(f'  <url><loc>{SITE}{p}</loc><lastmod>{TODAY}</lastmod></url>')
    out.append('</urlset>')
    write('sitemap.xml', '\n'.join(out) + '\n')


def main():
    els = [x for x in json.load(open(os.path.join(DB, 'Element.json'), encoding='utf-8')) if 1 <= x['atomicNumber'] <= 118]
    els.sort(key=lambda x: x['atomicNumber'])
    L = {'en': load_strings('en'), 'es': load_strings('es')}
    name = {'en': {x['atomicNumber']: x['englishName'] for x in els},
            'es': {x['atomicNumber']: L['es'].get(x['englishName'], x['englishName']) for x in els}}
    ctx = dict(els=els, L=L, name=name, iso=json.load(open(os.path.join(DB, 'Isotopes.json'), encoding='utf-8')),
               slug={l: {z: slug(n) for z, n in name[l].items()} for l in name})
    css = re.search(r'<style>(.*?)</style>', open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read(), re.S).group(1)
    write('assets/site.css', css + EXTRA_CSS)
    for el in els:
        for lang in ('en', 'es'):
            write(element_path(lang, el['atomicNumber'], ctx).strip('/') + '/index.html', element_page(el, lang, ctx))
    for lang in ('en', 'es'):
        write(U[lang]['idx_url'].strip('/') + '/index.html', index_page(lang, ctx))
    sitemap(ctx)
    print(f'{len(els) * 2} fichas, 2 índices, assets/site.css y sitemap.xml')


if __name__ == '__main__':
    main()
