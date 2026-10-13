#!/usr/bin/env python3
"""Genera es/index.html (landing en español) a partir de index.html (inglés).

    python3 tools/landing_es.py

Copia la página inglesa y traduce cada texto: las dos comparten diseño y
estructura. Si cambias un texto en inglés, añade aquí su traducción; el
script falla si algún texto inglés no encuentra su par.
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'index.html')
OUT = os.path.join(ROOT, 'es', 'index.html')
SITE = 'https://periodictable.echandia.app'

FAQ = [
    ('¿Tabla Periódica es gratis?',
     'Sí. La app se descarga gratis y no tiene anuncios. La tabla, los datos básicos de cada elemento, 10 tablas de consulta, 28 listas, las 147 reacciones, el glosario, la práctica de cuestionarios y las once calculadoras en su modo básico son gratis. Pro es opcional: un pago único, o un plan mensual o anual.'),
    ('¿Funciona sin conexión?',
     'Sí. Todos los datos van dentro de la app, así que funciona en clase, en el laboratorio o en modo avión. Solo hace falta conexión para comprar o restaurar Pro y para abrir enlaces externos.'),
    ('¿De dónde salen los datos?',
     'Los datos de los elementos están contrastados con PubChem (NIH) y la IUPAC, las configuraciones electrónicas con la base de espectros atómicos del NIST y los isótopos con el OIEA (NUBASE y AME). Un valor sin una medición publicada fiable aparece como desconocido (---), nunca inventado.'),
    ('¿En qué dispositivos funciona?',
     'En iPhone y iPad con iOS 16 o posterior, en Mac con chip de Apple y en Apple Watch, con su propia app que funciona sin el iPhone.'),
    ('¿Qué calculadoras de química incluye?',
     'Once: masa molar y composición, fórmula empírica, nomenclatura inorgánica y orgánica (IUPAC), ajuste de ecuaciones (también redox) con ΔH°, ΔS°, ΔG° y K, disoluciones, gases, propiedades coligativas, equilibrio químico con tabla ICE, pH y tampones, pilas electroquímicas y estadística analítica.'),
    ('¿La app recoge algún dato?',
     'No. No hay cuentas, anuncios, rastreadores ni analíticas. Tus favoritos, notas y progreso se quedan en tu dispositivo.'),
]

# Pares inglés → español, en orden (los textos largos antes que los cortos).
T = [
    # cabecera
    ('<html lang="en">', '<html lang="es">'),
    ('<title>Periodic Table and Chemistry App for iPhone, iPad and Mac</title>',
     '<title>Tabla Periódica y Química: app para iPhone, iPad y Mac</title>'),
    ('content="Free periodic table app with data checked against PubChem, IUPAC and NIST, eleven chemistry calculators, 22 reference tables and quizzes. No ads, works offline."',
     'content="App gratis de tabla periódica con datos contrastados con PubChem, IUPAC y NIST, once calculadoras de química, 22 tablas y cuestionarios. Sin anuncios y sin conexión."'),
    (f'<link rel="canonical" href="{SITE}/">', f'<link rel="canonical" href="{SITE}/es/">'),
    ('<meta property="og:site_name" content="Periodic Table and Chemistry">',
     '<meta property="og:site_name" content="Tabla Periódica y Química">'),
    (f'<meta property="og:url" content="{SITE}/">', f'<meta property="og:url" content="{SITE}/es/">'),
    ('<meta property="og:title" content="Periodic Table and Chemistry: data you can trust">',
     '<meta property="og:title" content="Tabla Periódica y Química: datos en los que puedes confiar">'),
    ('content="The periodic table with data checked against PubChem, IUPAC and NIST, eleven lab calculators, 22 reference tables and quizzes. Free, no ads, works offline."',
     'content="La tabla periódica con datos contrastados con PubChem, IUPAC y NIST, once calculadoras de laboratorio, 22 tablas y cuestionarios. Gratis, sin anuncios y sin conexión."'),
    (f'{SITE}/og.jpg', f'{SITE}/og-es.jpg'),
    ('content="Periodic Table and Chemistry on iPad and iPhone: the full periodic table and the copper element page"',
     'content="Tabla Periódica y Química en iPad y iPhone: la tabla periódica completa y la ficha del cobre"'),
    ('<meta property="og:type" content="website">', '<meta property="og:type" content="website">\n<meta property="og:locale" content="es_MX">'),
    ('href="icon.png"', 'href="../icon.png"'),
    ('src="icon.png"', 'src="../icon.png"'),
    ('src="capturas/en/', 'src="../capturas/es/'),
    ('<a class="skip" href="#main">Skip to content</a>', '<a class="skip" href="#main">Ir al contenido</a>'),
    ('alt="">Periodic Table</a>', 'alt="">Tabla Periódica</a>'),
    ('<a class="langlink" href="es/" hreflang="es" lang="es">Español</a>',
     '<a class="langlink" href="../" hreflang="en" lang="en">English</a>'),
    ('data-section="en" lang="en" aria-labelledby="en-title"', 'data-section="es" lang="es" aria-labelledby="es-title"'),
    ('id="en-title"', 'id="es-title"'), ('id="en-shots"', 'id="es-shots"'), ('href="#en-shots"', 'href="#es-shots"'),
    ('id="en-ipad"', 'id="es-ipad"'),
    # portada
    ('The periodic table with data you can trust.</h1>', 'La tabla periódica con datos en los que puedes confiar.</h1>'),
    ('All 118 elements and the 22 tables from the back of your chemistry textbook, plus eleven lab calculators and quizzes. Data checked against PubChem, IUPAC, NIST and the IAEA. No ads, no account, and it works offline.',
     'Los 118 elementos y las 22 tablas del apéndice de tu libro de química, con once calculadoras de laboratorio y cuestionarios. Datos contrastados con PubChem, IUPAC, NIST y el OIEA. Sin anuncios, sin cuenta y sin conexión.'),
    ('<small>Download on the</small>', '<small>Descárgala en el</small>'),
    ('See what it can do</a>', 'Ver qué puedes hacer</a>'),
    ('For iPhone, iPad, Mac and Apple Watch · in 20 languages', 'Para iPhone, iPad, Mac y Apple Watch · en 20 idiomas'),
    ('alt="The app on iPad: the full periodic table"', 'alt="La app en el iPad: la tabla periódica completa"'),
    ('alt="The app on iPhone: the copper page"', 'alt="La app en el iPhone: la ficha del cobre"'),
    # galerías
    ('Look up, calculate, compare and practice.', 'Consulta, calcula, compara y practica.'),
    ('Everything you need for chemistry class, in your pocket.', 'Todo lo que necesitas para la clase de química, en el bolsillo.'),
    ('aria-label="Previous"', 'aria-label="Anterior"'), ('aria-label="Next"', 'aria-label="Siguiente"'),
    ('App features on iPhone. Scroll horizontally to see all 12.', 'Funciones de la app en el iPhone. Desplázate en horizontal para ver las 12.'),
    ('The app on iPad. Scroll horizontally to see all 10.', 'La app en el iPad. Desplázate en horizontal para ver las 10.'),
    ('alt="In the app: Balancing methane combustion, with half-reactions and thermodynamics"',
     'alt="En la app: ajuste de la combustión del metano, con semirreacciones y termodinámica"'),
    ('alt="In the app: Balancing an equation with half-reactions and thermodynamics"',
     'alt="En la app: ajuste de una ecuación con semirreacciones y termodinámica"'),
    ('alt="In the app: pH of 0.1 M acetic acid"', 'alt="En la app: pH del ácido acético 0.1 M"'),
    ('alt="In the app: ', 'alt="En la app: '),
    ('Iron orbitals and atomic properties', 'Orbitales y propiedades atómicas del hierro'),
    ('Balancing with thermodynamics', 'Ajuste con termodinámica'),
    ('Solutions calculator', 'Calculadora de disoluciones'),
    ('Search by symbol', 'Búsqueda por símbolo'),
    ('Home in dark mode', 'Inicio en modo oscuro'),
    ('The full table', 'La tabla completa'), ('The copper page', 'La ficha del cobre'),
    ('Iron orbitals', 'Orbitales del hierro'), ('Gold versus copper', 'Oro frente a cobre'),
    ('pH and buffers', 'pH y tampones'), ('Quizzes by topic', 'Cuestionarios por temas'),
    ('Practice by topic', 'Práctica por temas'),
    ('Chemical reactions', 'Reacciones químicas'), ('Glossary', 'Glosario'),
    ('Instant search', 'Búsqueda al instante'), ('Dark mode', 'Modo oscuro'),
    ('More room on iPad.', 'Más espacio en el iPad.'),
    ('The same app in landscape, with the whole table, element pages and tools using every inch of the screen.',
     'La misma app en horizontal: la tabla entera, las fichas y las herramientas aprovechan toda la pantalla.'),
    # funciones
    ('Everything you need for class.', 'Todo lo que necesitas para clase.'),
    ('The whole appendix of your chemistry textbook, always two taps away: from electron configuration to Student’s t.',
     'El apéndice entero del libro de química, siempre a dos toques: de la configuración electrónica a la t de Student.'),
    ('Search the way you think', 'Busca como piensas'),
    ('By name, symbol, atomic number, Latin or English name, CAS number or family.',
     'Por nombre, símbolo, número atómico, nombre en latín o en inglés, número CAS o familia.'),
    ('A page for every element', 'La ficha de cada elemento'),
    ('Over 70 properties, from safety (NFPA 704) to isotopes, emission spectra and real photos of 97 elements. Touch and hold any value to copy it.',
     'Más de 70 propiedades, de la seguridad (NFPA 704) a los isótopos, el espectro de emisión y fotografías reales de 97 elementos. Mantén pulsado un dato para copiarlo.'),
    ('Configuration and orbitals', 'Configuración y orbitales'),
    ('Orbital diagram with Hund’s rule, unpaired electrons and ground-state term. If the real configuration breaks Madelung’s rule, it tells you.',
     'Diagrama de orbitales con la regla de Hund, electrones desapareados y término fundamental. Si la configuración real se sale de la regla de Madelung, te lo dice.'),
    ('Compare and spot trends', 'Compara y descubre tendencias'),
    ('Two or three elements side by side, 38 sortable lists, a trends chart and a heat map on the table.',
     'Dos o tres elementos lado a lado, 38 listas ordenables, gráfica de tendencias y mapa de calor en la tabla.'),
    ('Eleven lab calculators', 'Once calculadoras de laboratorio'),
    ('Molar mass, empirical formula, IUPAC nomenclature, equation balancing (redox too), solutions, gases, colligative properties, equilibrium, pH, cells and statistics.',
     'Masa molar, fórmula empírica, nomenclatura IUPAC, ajuste de ecuaciones (también redox), disoluciones, gases, propiedades coligativas, equilibrio, pH, pilas y estadística.'),
    ('Quizzes built from the data', 'Cuestionarios que salen de los datos'),
    ('Eight topics and three levels. Every answer shows the value behind it, with a link to where it lives.',
     'Ocho temas y tres niveles. Cada respuesta enseña el dato que la sostiene, con un enlace a donde vive.'),
    ('Reactions with thermodynamics', 'Reacciones con termodinámica'),
    ('147 reactions with their conditions, oxidation states, and ΔH°, ΔS°, ΔG° and K at 25 °C, ready to balance in one tap. Plus a 173-term glossary.',
     '147 reacciones con sus condiciones, estados de oxidación y ΔH°, ΔS°, ΔG° y K a 25 °C, listas para ajustar con un toque. Y un glosario de 173 términos.'),
    ('22 reference tables', '22 tablas de consulta'),
    ('Solubility, reduction potentials, acids and bases, Ksp, thermodynamic data, ionization energies and critical values of t, F, Q and Grubbs.',
     'Solubilidad, potenciales de reducción, ácidos y bases, Ksp, datos termodinámicos, energías de ionización y valores críticos de t, F, Q y Grubbs.'),
    # confianza
    ('<h2>Data you can trust.</h2>', '<h2>Datos en los que puedes confiar.</h2>'),
    ('Every value is checked against public reference sources, and the sources are listed in the app itself, under More › Data sources. Take the iron page, for example:',
     'Cada dato está contrastado con fuentes públicas de referencia, y las fuentes están en la propia app, en Más › Fuentes de datos. Por ejemplo, la ficha del hierro:'),
    ('Iron<small>Transition metal</small>', 'Hierro<small>Metal de transición</small>'),
    ('<caption class="vh">Iron</caption>', '<caption class="vh">Hierro</caption>'),
    ('>Atomic mass</th>', '>Masa atómica</th>'),
    ('>Electron configuration</th>', '>Configuración electrónica</th>'),
    ('>Electronegativity (Pauling)</th>', '>Electronegatividad (Pauling)</th>'),
    ('>Stable isotopes</th>', '>Isótopos estables</th>'),
    ('checked against NIST', 'contrastada con NIST'), ('IAEA · NUBASE', 'OIEA · NUBASE'),
    ('And when a value doesn’t exist, the app doesn’t make one up.', 'Y cuando un dato no existe, la app no se lo inventa.'),
    ('Anything without a reliable measurement is shown as unknown. An honest gap beats a made-up number.',
     'Lo que no tiene una medida fiable aparece como desconocido. Mejor un hueco honesto que un número inventado.'),
    ('Hypothetical elements are clearly marked: their data are predictions, not measurements.',
     'Los elementos hipotéticos aparecen marcados: sus datos son predicciones, no mediciones.'),
    ('Oxidation states are split into common, rare and predicted.', 'Los estados de oxidación separan los comunes, los raros y los predichos.'),
    ('<a href="soporte/#en-sources">See all data sources →</a>', '<a href="../soporte/#es-datos">Ver todas las fuentes de datos →</a>'),
    # planes
    ('Free, with no ads and no data collection.', 'Gratis, sin anuncios y sin recoger datos.'),
    ('What you need every day is free. Pro is a one-time purchase that’s yours forever, no subscription; if you prefer, there are also monthly and yearly plans. All three unlock the same thing on every device with your Apple Account.',
     'Lo que necesitas a diario es gratis. Pro se paga una vez y es tuyo para siempre, sin suscripción; si lo prefieres, también hay plan mensual y anual. Los tres desbloquean lo mismo en todos tus dispositivos con tu cuenta de Apple.'),
    ('<h3>Free</h3>', '<h3>Gratis</h3>'), ('For studying every day.', 'Para estudiar a diario.'),
    ('The table, search and each element’s core data', 'La tabla, la búsqueda y los datos básicos de cada elemento'),
    ('10 reference tables and 28 lists', '10 tablas de consulta y 28 listas'),
    ('All 147 reactions and the glossary', 'Las 147 reacciones y el glosario'),
    ('Unlimited quiz practice', 'Práctica de cuestionarios sin límite'),
    ('All eleven calculators in their basic modes', 'Las once calculadoras en su modo básico'),
    ('Apple Watch, widgets and three themes', 'Apple Watch, widgets y tres temas'),
    ('One payment, forever. Or monthly or yearly.', 'Un solo pago, para siempre. O mensual o anual.'),
    ('The other 12 tables and 10 lists', 'Las otras 12 tablas y 10 listas'),
    ('Advanced data: magnetic and electrical properties, the critical point and every radioactive isotope',
     'Datos avanzados: propiedades magnéticas y eléctricas, punto crítico y todos los isótopos radiactivos'),
    ('Timed exams, spaced review and stats', 'Examen cronometrado, repaso espaciado y estadísticas'),
    ('Advanced calculator modes: stoichiometry, gas mixtures, buffers, the Nernst equation, confidence intervals and outlier tests',
     'Modos avanzados de las calculadoras: estequiometría, mezclas de gases, tampones, ecuación de Nernst, intervalos de confianza y valores anómalos'),
    ('PDF export and ten more themes', 'Exportar a PDF y diez temas más'),
    ('Used it back in 2019? It’s back, rebuilt from scratch, and if you bought Premium it’s still yours: it comes back when you open the app or under More › Restore purchases.',
     '¿La usabas en 2019? Vuelve reconstruida desde cero, y si compraste Premium sigue siendo tuyo: se recupera al abrir la app o en Más › Restaurar compras.'),
    ('What you save stays on your device.', 'Lo que guardas se queda en tu dispositivo.'),
    ('No accounts or sign-up', 'Sin cuentas ni registro'), ('No ads or tracking', 'Sin anuncios ni rastreo'),
    ('No third-party analytics', 'Sin analíticas de terceros'),
    ('Suitable for students of any age', 'Apta para estudiantes de cualquier edad'),
    ('<a href="privacidad/#en">Read the privacy policy →</a>', '<a href="../privacidad/#es">Leer la política de privacidad →</a>'),
    # dispositivos
    ('Made for your Apple devices.', 'Hecha para tus dispositivos Apple.'),
    ('A native app on every screen, using the system features you already know.',
     'Una app nativa en cada pantalla, que usa las funciones del sistema que ya conoces.'),
    ('alt="Apple Watch: element list"', 'alt="Apple Watch: lista de elementos"'),
    ('alt="Apple Watch: gold element page"', 'alt="Apple Watch: ficha del oro"'),
    ('All 124 elements on your wrist, independent of your iPhone.', 'Los 124 elementos en la muñeca, sin depender del iPhone.'),
    ('Element of the day, also on the Lock Screen, plus your favorites.', 'Elemento del día, también en la pantalla de bloqueo, y tus favoritos.'),
    ('<dt>Siri, Shortcuts and Spotlight</dt>', '<dt>Siri, Atajos y Spotlight</dt>'),
    ('“Molar mass in Periodic Table”, or find an element from system search.',
     '«Masa molar en Tabla Periódica», o encuentra un elemento desde la búsqueda del sistema.'),
    ('<dt>Your units</dt>', '<dt>Tus unidades</dt>'),
    ('Kelvin or Celsius, kJ/mol or eV, and MPa, bar or atm.', 'Kelvin o grados Celsius, kJ/mol o eV, y MPa, bar o atm.'),
    ('<dt>Thirteen themes</dt>', '<dt>Trece temas</dt>'),
    ('Named after scientists. Lavoisier, Curie and Dalton, designed for color blindness, are free.',
     'Con nombre de científico. Lavoisier, Curie y Dalton, pensado para el daltonismo, son gratis.'),
    ('<dt>Accessible</dt>', '<dt>Accesible</dt>'),
    ('VoiceOver, larger text, Dark Mode and a shape for each family if you can’t tell the colors apart. 20 languages.',
     'VoiceOver, texto grande, modo oscuro y una forma para cada familia si no distingues los colores. 20 idiomas.'),
    # cierre
    ('<h2>Questions.</h2>', '<h2>Preguntas.</h2>'),
    ('Start studying with data you can trust.', 'Empieza a estudiar con datos fiables.'),
    ('Free on the App Store for iPhone, iPad, Mac and Apple Watch.', 'Gratis en el App Store para iPhone, iPad, Mac y Apple Watch.'),
    # pie
    ('<p>Created by Josue Echandia', '<p>Creada por Josue Echandia'),
    ('<p>Made with <span role="img" aria-label="love">&#x2665;&#xFE0E;</span> in Peru <span aria-hidden="true">🇵🇪</span></p>',
     '<p>Hecha con <span role="img" aria-label="amor">&#x2665;&#xFE0E;</span> en Perú <span aria-hidden="true">🇵🇪</span></p>'),
    ('<a href="privacidad/#en">Privacy</a>', '<a href="../privacidad/#es">Privacidad</a>'),
    ('<a href="soporte/#en">Support</a>', '<a href="../soporte/#es">Soporte</a>'),
]

FAQ_EN = re.compile(r'<dl class="devlist faq">.*?</dl>', re.S)
LD = re.compile(r'<script type="application/ld\+json">.*?</script>', re.S)


def main():
    s = open(SRC, encoding='utf-8').read()
    for en, es in T:
        if en not in s:
            raise SystemExit(f'Falta en index.html (¿cambió el texto inglés?): {en[:80]}')
        s = s.replace(en, es)
    s = FAQ_EN.sub('<dl class="devlist faq">' + ''.join(f'<div><dt>{q}</dt><dd>{a}</dd></div>' for q, a in FAQ) + '</dl>', s)
    ld = json.loads(LD.search(s).group(0).split('>', 1)[1].rsplit('<', 1)[0])
    app = ld[0]
    app.update({
        'name': 'Tabla Periódica y Química', 'alternateName': 'Periodic Table and Chemistry',
        'url': f'{SITE}/es/', 'image': f'{SITE}/og-es.jpg',
        'screenshot': [u.replace('/capturas/en/', '/capturas/es/') for u in app['screenshot']],
        'description': 'La tabla periódica con datos contrastados con PubChem, IUPAC, NIST y el OIEA, once calculadoras de química, 22 tablas de consulta, 147 reacciones y cuestionarios. Sin anuncios, funciona sin conexión y no recoge datos.',
        'operatingSystem': 'iOS 16.0 o posterior, iPadOS, macOS (chip de Apple), watchOS',
        'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'MXN'},
    })
    ld[1]['mainEntity'] = [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in FAQ]
    s = LD.sub(lambda _: '<script type="application/ld+json">\n' + json.dumps(ld, ensure_ascii=False, indent=1) + '\n</script>', s)
    # Lo que no se haya traducido y siga en inglés en el texto visible salta aquí.
    for leftover in ['Download on the', 'Periodic Table</a>', 'In the app', 'Skip to content']:
        if leftover in s:
            raise SystemExit(f'Queda en inglés: {leftover}')
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, 'w', encoding='utf-8').write(s)
    print('escrito', os.path.relpath(OUT, ROOT))


if __name__ == '__main__':
    main()
