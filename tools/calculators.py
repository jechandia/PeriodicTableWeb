#!/usr/bin/env python3
"""Genera las páginas por calculadora, en inglés y en español.

    python3 tools/calculators.py

Usa la hoja de estilos de index.html (la misma identidad que la landing) y
escribe cada página en su carpeta. Las cifras de los ejemplos son las que
da la app (capturas de capturas/extras): si la app cambia, cámbialas aquí.
"""
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://periodictable.echandia.app'
APP = 'https://apps.apple.com/app/id1455103430'
e = html.escape

APPLE = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M16.37 12.6c-.02-2.3 1.88-3.4 1.96-3.46-1.07-1.56-2.73-1.77-3.32-1.8-1.41-.14-2.76.83-3.47.83-.72 0-1.82-.81-2.99-.79-1.54.02-2.96.9-3.75 2.27-1.6 2.78-.41 6.89 1.15 9.14.76 1.1 1.67 2.34 2.86 2.3 1.15-.05 1.58-.74 2.97-.74 1.38 0 1.77.74 2.98.72 1.24-.02 2.02-1.12 2.77-2.23.87-1.28 1.23-2.52 1.25-2.58-.03-.01-2.39-.92-2.41-3.66zM14.1 5.86c.63-.77 1.06-1.83.94-2.89-.91.04-2.02.61-2.67 1.37-.58.67-1.09 1.76-.96 2.8 1.02.08 2.06-.51 2.69-1.28z"/></svg>')

EXTRA_CSS = '''
/* calculator pages */
.crumbs { margin: 28px 0 0; font-size: .92rem; color: var(--muted); }
.crumbs a { color: var(--muted); }
.calc-hero { display: grid; gap: 32px; align-items: center; padding: 20px 0 0; }
@media (min-width: 860px) { .calc-hero { grid-template-columns: 1.15fr .85fr; gap: 56px; padding-top: 40px; } }
.calc-hero h1 { font-size: clamp(2.2rem, 5vw, 3.4rem); letter-spacing: -.03em; font-weight: 750; }
.calc-hero .phone { max-width: 300px; margin: 0 auto; }
.prose { max-width: 44rem; }
.prose p, .prose li { color: var(--ink); }
.prose h3 { margin-top: 28px; }
.steps { padding-left: 1.3em; }
.steps li { margin: .5em 0; }
.worked { width: 100%; max-width: 44rem; border-collapse: collapse; margin: 18px 0 8px; background: var(--surface);
  border: 1px solid var(--line); border-radius: 14px; overflow: hidden; font-variant-numeric: tabular-nums; }
.worked th, .worked td { padding: 12px 16px; text-align: left; border-top: 1px solid var(--line); }
.worked thead th { border-top: 0; color: var(--muted); font-weight: 500; font-size: .92rem; }
.worked tfoot td { font-weight: 700; color: var(--title); }
.worked td.n { text-align: right; white-space: nowrap; }
.worked th.n { text-align: right; }
.table-wrap { max-width: 44rem; overflow-x: auto; }
@media (max-width: 560px) { .worked th, .worked td { padding: 10px 6px; font-size: .86rem; } .worked th:first-child, .worked td:first-child { padding-left: 12px; } }
.note { color: var(--muted); font-size: .96rem; }
.wide-shot { margin-top: 28px; max-width: 900px; }
.related { display: flex; flex-wrap: wrap; gap: 10px; margin: 18px 0 0; padding: 0; list-style: none; }
.related a { display: inline-flex; align-items: center; min-height: 44px; padding: 0 18px; border-radius: 999px;
  background: var(--surface); border: 1px solid var(--line); text-decoration: none; font-weight: 600; }
'''

UI = {
    'en': dict(home='Periodic Table', home_url='/', crumbs_label='Breadcrumb', store_small='Download on the',
               more='More chemistry calculators', in_app='In the app', faq='Questions', skip='Skip to content',
               free_line='Free on the App Store for iPhone, iPad, Mac and Apple Watch.', cta_h='Try it on your iPhone.',
               made_by='Created by', made='Made with <span role="img" aria-label="love">&#x2665;&#xFE0E;</span> in Peru <span aria-hidden="true">🇵🇪</span>',
               privacy=('Privacy', '/privacidad/#en'), support=('Support', '/soporte/#en'), other_lang='Español', all_link='See everything the app does →'),
    'es': dict(home='Tabla Periódica', home_url='/es/', crumbs_label='Ruta', store_small='Descárgala en el',
               more='Más calculadoras de química', in_app='En la app', faq='Preguntas', skip='Ir al contenido',
               free_line='Gratis en el App Store para iPhone, iPad, Mac y Apple Watch.', cta_h='Pruébala en tu iPhone.',
               made_by='Creada por', made='Hecha con <span role="img" aria-label="amor">&#x2665;&#xFE0E;</span> en Perú <span aria-hidden="true">🇵🇪</span>',
               privacy=('Privacidad', '/privacidad/#es'), support=('Soporte', '/soporte/#es'), other_lang='English', all_link='Ver todo lo que hace la app →'),
}

# Cada calculadora: rutas por idioma y el contenido de cada página.
PAGES = {
    'molar': {
        'path': {'en': '/molar-mass-calculator/', 'es': '/es/calculadora-masa-molar/'},
        'shot': '14-masa-molar', 'ipad': None,
        'en': dict(
            title='Molar Mass Calculator: Formula to g/mol | Periodic Table app',
            desc='Calculate the molar mass of any chemical formula in g/mol, with the mass percent of each element. Handles parentheses, hydrates and ions. Free app for iPhone, iPad and Mac.',
            name='Molar mass calculator',
            h1='Molar mass calculator',
            lead='Type a chemical formula and get its molar mass in g/mol, with the share of each element. Parentheses, hydrates and ions included. Free in Periodic Table and Chemistry for iPhone, iPad and Mac.',
            alt='Molar mass of H2SO4 in the app: 98.072 g/mol with the mass percent of each element',
            ipad_alt='The molar mass calculator on iPad in landscape',
            how_h='How to calculate molar mass',
            how=['Count the atoms of each element in the formula. A subscript after parentheses multiplies everything inside: Ca(OH)₂ has 2 O and 2 H.',
                 'Multiply each count by the element’s standard atomic weight (in g/mol).',
                 'Add the products. The sum is the molar mass: the mass in grams of one mole of the substance.'],
            ex_h='Worked example: sulfuric acid, H₂SO₄',
            ex_cols=('Element', 'Atoms × atomic weight', 'g/mol', 'Mass %'),
            ex_rows=[('H', '2 × 1.008', '2.016', '2.06 %'), ('S', '1 × 32.06', '32.06', '32.69 %'), ('O', '4 × 15.999', '63.996', '65.25 %')],
            ex_total=('Molar mass of H₂SO₄', '98.072 g/mol'),
            ex_note='The mass percent of each element is its contribution divided by the molar mass: 63.996 / 98.072 = 65.25 % oxygen.',
            app_h='What the app does for you',
            app=['A chemistry keyboard with element symbols and subscripts, so H2SO4 becomes H₂SO₄ as you type.',
                 'Parentheses and brackets, like Ca(OH)₂ or K₄[Fe(CN)₆], hydrates like CuSO₄·5H₂O and ions like SO₄²⁻.',
                 'It tells Co (cobalt) from CO (carbon monoxide), and offers the other reading when a formula is ambiguous.',
                 'The composition by element, with each atom’s contribution and mass percent, and a history of your calculations.',
                 'Atomic weights checked against IUPAC and PubChem. Ask Siri: “Molar mass in Periodic Table”.'],
            faq=[('What is molar mass?', 'The mass of one mole of a substance, in grams per mole (g/mol). It has the same number as the relative formula mass: water, H₂O, is 18.015 g/mol.'),
                 ('Is the molar mass calculator free?', 'Yes. The molar mass and the composition by element are free in the app, with no ads and no account.'),
                 ('Does it work with hydrates and complex ions?', 'Yes: write CuSO4·5H2O, K4[Fe(CN)6] or SO4^2- and the app reads the coefficient, the brackets and the charge.')]),
        'es': dict(
            title='Calculadora de masa molar: de fórmula a g/mol | Tabla Periódica',
            desc='Calcula la masa molar de cualquier fórmula química en g/mol, con el porcentaje en masa de cada elemento. Con paréntesis, hidratos e iones. App gratis para iPhone, iPad y Mac.',
            name='Calculadora de masa molar',
            h1='Calculadora de masa molar',
            lead='Escribe una fórmula química y obtén su masa molar en g/mol, con la parte de cada elemento. Con paréntesis, hidratos e iones. Gratis en Tabla Periódica y Química para iPhone, iPad y Mac.',
            alt='Masa molar del H2SO4 en la app: 98.072 g/mol con el porcentaje en masa de cada elemento',
            ipad_alt='La calculadora de masa molar en el iPad en horizontal',
            how_h='Cómo se calcula la masa molar',
            how=['Cuenta los átomos de cada elemento de la fórmula. Un subíndice después de un paréntesis multiplica todo lo de dentro: Ca(OH)₂ tiene 2 O y 2 H.',
                 'Multiplica cada cantidad por el peso atómico estándar del elemento (en g/mol).',
                 'Suma los productos. El total es la masa molar: la masa en gramos de un mol de la sustancia.'],
            ex_h='Ejemplo resuelto: ácido sulfúrico, H₂SO₄',
            ex_cols=('Elemento', 'Átomos × peso atómico', 'g/mol', '% en masa'),
            ex_rows=[('H', '2 × 1.008', '2.016', '2.06 %'), ('S', '1 × 32.06', '32.06', '32.69 %'), ('O', '4 × 15.999', '63.996', '65.25 %')],
            ex_total=('Masa molar del H₂SO₄', '98.072 g/mol'),
            ex_note='El porcentaje en masa de cada elemento es su aporte dividido entre la masa molar: 63.996 / 98.072 = 65.25 % de oxígeno.',
            app_h='Lo que hace la app por ti',
            app=['Un teclado de química con los símbolos y los subíndices: H2SO4 se convierte en H₂SO₄ mientras escribes.',
                 'Paréntesis y corchetes, como Ca(OH)₂ o K₄[Fe(CN)₆], hidratos como CuSO₄·5H₂O e iones como SO₄²⁻.',
                 'Distingue Co (cobalto) de CO (monóxido de carbono) y te ofrece la otra lectura cuando la fórmula es ambigua.',
                 'La composición por elemento, con el aporte de cada átomo y su porcentaje en masa, y el historial de tus cálculos.',
                 'Pesos atómicos contrastados con la IUPAC y PubChem. Pídeselo a Siri: «Masa molar en Tabla Periódica».'],
            faq=[('¿Qué es la masa molar?', 'La masa de un mol de una sustancia, en gramos por mol (g/mol). Tiene el mismo número que la masa fórmula relativa: el agua, H₂O, tiene 18.015 g/mol.'),
                 ('¿La calculadora de masa molar es gratis?', 'Sí. La masa molar y la composición por elemento son gratis en la app, sin anuncios y sin cuenta.'),
                 ('¿Funciona con hidratos e iones complejos?', 'Sí: escribe CuSO4·5H2O, K4[Fe(CN)6] o SO4^2- y la app lee el coeficiente, los corchetes y la carga.')]),
    },
    'ph': {
        'path': {'en': '/ph-calculator/', 'es': '/es/calculadora-ph/'},
        'shot': '12-ph', 'ipad': None,
        'en': dict(
            title='pH Calculator for Strong and Weak Acids and Bases | Periodic Table app',
            desc='Calculate pH, pOH, [H⁺] and percent ionization for strong and weak acids and bases, with pKa values built in. Free chemistry app for iPhone, iPad and Mac.',
            name='pH calculator',
            h1='pH calculator',
            lead='Strong and weak acids and bases: choose the species, type the concentration and get pH, pOH, [H⁺], [OH⁻] and how much of it ionizes. Free in Periodic Table and Chemistry for iPhone, iPad and Mac.',
            alt='pH of 0.1 M acetic acid in the app: pH 2.88, pOH 11.12, 1.33 % ionized',
            how_h='How to calculate pH',
            how=['Strong acid: it ionizes completely, so [H⁺] equals its concentration times the H⁺ it releases. pH = −log[H⁺]. For 0.01 M HCl, pH = 2.00.',
                 'Weak acid: only part of it ionizes. With Ka = 10^(−pKa), solve x² / (C − x) = Ka for x = [H⁺].',
                 'Quick estimate for a weak acid: pH ≈ ½ (pKa − log C).',
                 'pOH = 14 − pH at 25 °C, because Kw = 1.0 × 10⁻¹⁴.'],
            ex_h='Worked example: 0.1 M acetic acid (pKa 4.74)',
            ex_cols=('Quantity', '', '', 'Value', ''),
            ex_rows=[('Quick estimate', '', '', 'pH ≈ ½ (4.74 + 1) = 2.87', ''), ('[H⁺]', '', '', '1.33 × 10⁻³ mol/L', ''),
                     ('[OH⁻]', '', '', '7.50 × 10⁻¹² mol/L', ''), ('pOH', '', '', '11.12', ''), ('Ionized', '', '', '1.33 %', '')],
            ex_total=('pH', '2.88'),
            ex_note='The quick estimate gives 2.87. The app solves the full charge balance, including the ionization of water, and gets 2.88: that is why a very dilute acid never goes past pH 7.',
            app_h='What the app does for you',
            app=['Strong and weak acids and bases, with the number of H⁺ or OH⁻ per formula (HCl 1, Ba(OH)₂ 2).',
                 'Pick a weak acid or base and its pKa comes from the app’s acids and bases table, or type your own pKa or pKb.',
                 'pH, pOH, [H⁺], [OH⁻] and percent ionization at once, and a history of your calculations.',
                 'With Pro: buffers, with the acid and base forms of the pair (Henderson–Hasselbalch).'],
            faq=[('What is pH?', 'pH = −log[H⁺], the negative logarithm of the hydrogen ion concentration in mol/L. At 25 °C, 7 is neutral, below 7 acidic, above 7 basic.'),
                 ('Is the pH calculator free?', 'Yes. Strong and weak acids and bases are free in the app. Buffers are part of Pro.'),
                 ('Why can’t a very dilute acid reach pH 7?', 'Because water itself ionizes and gives 1.0 × 10⁻⁷ mol/L of H⁺. The app includes it in the balance, so an acid, however dilute, stays below 7.')]),
        'es': dict(
            title='Calculadora de pH: ácidos y bases fuertes y débiles | Tabla Periódica',
            desc='Calcula pH, pOH, [H⁺] y porcentaje de ionización de ácidos y bases fuertes y débiles, con los pKa incluidos. App de química gratis para iPhone, iPad y Mac.',
            name='Calculadora de pH',
            h1='Calculadora de pH',
            lead='Ácidos y bases fuertes y débiles: elige la especie, escribe la concentración y obtén pH, pOH, [H⁺], [OH⁻] y cuánto se ioniza. Gratis en Tabla Periódica y Química para iPhone, iPad y Mac.',
            alt='pH del ácido acético 0.1 M en la app: pH 2.88, pOH 11.12, 1.33 % ionizado',
            how_h='Cómo se calcula el pH',
            how=['Ácido fuerte: se ioniza por completo, así que [H⁺] es su concentración por los H⁺ que libera. pH = −log[H⁺]. Para HCl 0.01 M, pH = 2.00.',
                 'Ácido débil: solo se ioniza una parte. Con Ka = 10^(−pKa), resuelve x² / (C − x) = Ka para x = [H⁺].',
                 'Estimación rápida para un ácido débil: pH ≈ ½ (pKa − log C).',
                 'pOH = 14 − pH a 25 °C, porque Kw = 1.0 × 10⁻¹⁴.'],
            ex_h='Ejemplo resuelto: ácido acético 0.1 M (pKa 4.74)',
            ex_cols=('Magnitud', '', '', 'Valor', ''),
            ex_rows=[('Estimación rápida', '', '', 'pH ≈ ½ (4.74 + 1) = 2.87', ''), ('[H⁺]', '', '', '1.33 × 10⁻³ mol/L', ''),
                     ('[OH⁻]', '', '', '7.50 × 10⁻¹² mol/L', ''), ('pOH', '', '', '11.12', ''), ('Ionizado', '', '', '1.33 %', '')],
            ex_total=('pH', '2.88'),
            ex_note='La estimación rápida da 2.87. La app resuelve el balance de cargas completo, con la autoionización del agua, y da 2.88: por eso un ácido muy diluido nunca pasa de pH 7.',
            app_h='Lo que hace la app por ti',
            app=['Ácidos y bases fuertes y débiles, con los H⁺ u OH⁻ por fórmula (HCl 1, Ba(OH)₂ 2).',
                 'Elige un ácido o una base débil y su pKa sale de la tabla de ácidos y bases de la app, o escribe tu propio pKa o pKb.',
                 'pH, pOH, [H⁺], [OH⁻] y porcentaje de ionización a la vez, y el historial de tus cálculos.',
                 'Con Pro: tampones, con la forma ácida y la básica del par (Henderson-Hasselbalch).'],
            faq=[('¿Qué es el pH?', 'pH = −log[H⁺], el logaritmo negativo de la concentración de iones hidrógeno en mol/L. A 25 °C, 7 es neutro, por debajo es ácido y por encima, básico.'),
                 ('¿La calculadora de pH es gratis?', 'Sí. Los ácidos y bases fuertes y débiles son gratis en la app. Los tampones son parte de Pro.'),
                 ('¿Por qué un ácido muy diluido no llega a pH 7?', 'Porque el agua también se ioniza y aporta 1.0 × 10⁻⁷ mol/L de H⁺. La app lo incluye en el balance, así que un ácido, por diluido que esté, se queda por debajo de 7.')]),
    },
    'equations': {
        'path': {'en': '/balance-chemical-equations/', 'es': '/es/ajustar-ecuaciones/'},
        'shot': '11-ajuste-termodinamica', 'ipad': '11-ajuste-termodinamica',
        'en': dict(
            title='Chemical Equation Balancer with Redox and ΔH° | Periodic Table app',
            desc='Balance chemical equations, including redox by the half-reaction method, and see ΔH°, ΔS°, ΔG° and K at 25 °C. Free chemistry app for iPhone, iPad and Mac.',
            name='Chemical equation balancer',
            h1='Chemical equation balancer',
            lead='Write the reactants and products and the app balances the equation, checks the atoms on each side, finds what is oxidized and reduced and, for known reactions, gives ΔH°, ΔS°, ΔG° and K. Free in Periodic Table and Chemistry.',
            alt='Balancing CH4 + O2 → CO2 + H2O in the app, with oxidation numbers and the half-reaction method',
            ipad_alt='The equation balancer on iPad in landscape, with thermodynamics at 25 °C',
            how_h='How to balance a chemical equation',
            how=['Write the unbalanced equation with correct formulas: CH₄ + O₂ → CO₂ + H₂O.',
                 'Balance the elements that appear in only one compound on each side first. Carbon: 1 = 1.',
                 'Then hydrogen: 4 H on the left needs 2 H₂O on the right.',
                 'Leave elements that appear alone for last. Oxygen: the right now has 2 + 2 = 4 O, so the left needs 2 O₂.',
                 'Check every element: C 1 = 1, H 4 = 4, O 4 = 4.'],
            ex_h='Worked example: combustion of methane',
            ex_cols=('Step', '', '', 'Result', ''),
            ex_rows=[('Balanced', '', '', 'CH₄ + 2 O₂ → CO₂ + 2 H₂O', ''), ('Atoms on each side', '', '', 'C 1 = 1 · H 4 = 4 · O 4 = 4', ''),
                     ('Oxidized', '', '', 'C: −4 → +4 (CH₄ → CO₂)', ''), ('Reduced', '', '', 'O: 0 → −2 (O₂ → CO₂)', ''),
                     ('ΔS° at 25 °C', '', '', '−5.3 J/(mol·K)', '')],
            ex_total=('ΔH° at 25 °C', '−802.6 kJ/mol'),
            ex_note='Thermodynamics uses the physical states from the app’s reaction catalog (here, water as a gas). CH₄ is the reducing agent and O₂ the oxidizing agent.',
            app_h='What the app does for you',
            app=['Balances any equation you type, and shows the atoms on each side so you can check it.',
                 'Redox by the ion-electron (half-reaction) method, in acidic or basic medium, with oxidation numbers, oxidizing and reducing agents.',
                 'ΔH°, ΔS°, ΔG° and K at 25 °C when the reaction is in the catalog of 147 reactions, which also opens in the balancer with one tap.',
                 'With Pro: stoichiometry, with the limiting reactant and the yield.'],
            faq=[('Is the equation balancer free?', 'Yes. Balancing, redox by the half-reaction method and the thermodynamics of catalog reactions are free. Stoichiometry (limiting reactant and yield) is part of Pro.'),
                 ('Can it balance ionic redox equations?', 'Yes. Write the ionic skeleton and choose acidic or basic medium: the app adds H⁺, OH⁻ and H₂O by the ion-electron method.'),
                 ('Where do ΔH° and ΔS° come from?', 'From standard thermodynamic data at 25 °C for each species, in the physical states listed in the app’s reaction catalog.')]),
        'es': dict(
            title='Ajustar ecuaciones químicas, con redox y ΔH° | Tabla Periódica',
            desc='Ajusta (balancea) ecuaciones químicas, también redox por el método del ion-electrón, y ve ΔH°, ΔS°, ΔG° y K a 25 °C. App de química gratis para iPhone, iPad y Mac.',
            name='Ajustar ecuaciones químicas',
            h1='Ajustar ecuaciones químicas',
            lead='Escribe los reactivos y los productos y la app ajusta (balancea) la ecuación, comprueba los átomos de cada lado, encuentra qué se oxida y qué se reduce y, en las reacciones conocidas, da ΔH°, ΔS°, ΔG° y K. Gratis en Tabla Periódica y Química.',
            alt='Ajuste de CH4 + O2 → CO2 + H2O en la app, con números de oxidación y el método del ion-electrón',
            ipad_alt='El ajustador de ecuaciones en el iPad en horizontal, con la termodinámica a 25 °C',
            how_h='Cómo se ajusta una ecuación química',
            how=['Escribe la ecuación sin ajustar con las fórmulas correctas: CH₄ + O₂ → CO₂ + H₂O.',
                 'Ajusta primero los elementos que aparecen en un solo compuesto de cada lado. Carbono: 1 = 1.',
                 'Luego el hidrógeno: 4 H a la izquierda piden 2 H₂O a la derecha.',
                 'Deja para el final los elementos que van solos. Oxígeno: a la derecha hay 2 + 2 = 4 O, así que a la izquierda hacen falta 2 O₂.',
                 'Comprueba cada elemento: C 1 = 1, H 4 = 4, O 4 = 4.'],
            ex_h='Ejemplo resuelto: combustión del metano',
            ex_cols=('Paso', '', '', 'Resultado', ''),
            ex_rows=[('Ajustada', '', '', 'CH₄ + 2 O₂ → CO₂ + 2 H₂O', ''), ('Átomos a cada lado', '', '', 'C 1 = 1 · H 4 = 4 · O 4 = 4', ''),
                     ('Se oxida', '', '', 'C: −4 → +4 (CH₄ → CO₂)', ''), ('Se reduce', '', '', 'O: 0 → −2 (O₂ → CO₂)', ''),
                     ('ΔS° a 25 °C', '', '', '−5.3 J/(mol·K)', '')],
            ex_total=('ΔH° a 25 °C', '−802.6 kJ/mol'),
            ex_note='La termodinámica usa los estados físicos del catálogo de reacciones de la app (aquí, el agua como gas). El CH₄ es el reductor y el O₂ el oxidante.',
            app_h='Lo que hace la app por ti',
            app=['Ajusta cualquier ecuación que escribas y enseña los átomos de cada lado para que la compruebes.',
                 'Redox por el método del ion-electrón (semirreacciones), en medio ácido o básico, con números de oxidación, oxidante y reductor.',
                 'ΔH°, ΔS°, ΔG° y K a 25 °C cuando la reacción está en el catálogo de 147 reacciones, que también se abren en el ajustador con un toque.',
                 'Con Pro: estequiometría, con el reactivo limitante y el rendimiento.'],
            faq=[('¿El ajustador de ecuaciones es gratis?', 'Sí. El ajuste, el redox por el método del ion-electrón y la termodinámica de las reacciones del catálogo son gratis. La estequiometría (reactivo limitante y rendimiento) es parte de Pro.'),
                 ('¿Ajusta ecuaciones redox iónicas?', 'Sí. Escribe el esqueleto iónico y elige medio ácido o básico: la app añade H⁺, OH⁻ y H₂O por el método del ion-electrón.'),
                 ('¿De dónde salen ΔH° y ΔS°?', 'De los datos termodinámicos estándar a 25 °C de cada especie, en los estados físicos que indica el catálogo de reacciones de la app.')]),
    },
}


def style():
    s = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
    return re.search(r'<style>(.*?)</style>', s, re.S).group(1) + EXTRA_CSS


def worked_table(c):
    simple = c['ex_cols'][1] == ''          # tabla de dos columnas (magnitud, valor)
    if simple:
        head = f'<thead><tr><th>{e(c["ex_cols"][0])}</th><th class="n">{e(c["ex_cols"][3])}</th></tr></thead>'
        body = ''.join(f'<tr><td>{e(r[0])}</td><td class="n">{e(r[3])}</td></tr>' for r in c['ex_rows'])
        foot = f'<tfoot><tr><td>{e(c["ex_total"][0])}</td><td class="n">{e(c["ex_total"][1])}</td></tr></tfoot>'
    else:
        head = '<thead><tr>' + ''.join(f'<th{" class=\"n\"" if i else ""}>{e(h)}</th>' for i, h in enumerate(c['ex_cols'])) + '</tr></thead>'
        body = ''.join('<tr>' + ''.join(f'<td{" class=\"n\"" if i else ""}>{e(v)}</td>' for i, v in enumerate(r)) + '</tr>' for r in c['ex_rows'])
        n = len(c['ex_cols'])
        foot = f'<tfoot><tr><td colspan="{n - 2}">{e(c["ex_total"][0])}</td><td class="n">{e(c["ex_total"][1])}</td><td></td></tr></tfoot>'
    return f'<div class="table-wrap"><table class="worked">{head}<tbody>{body}</tbody>{foot}</table></div>'


def page(key, lang, css):
    p, c, u = PAGES[key], PAGES[key][lang], UI[lang]
    other = 'es' if lang == 'en' else 'en'
    path, url = p['path'][lang], SITE + p['path'][lang]
    up = '../' * (path.strip('/').count('/') + 1)          # hasta la raíz del sitio
    shots = f'{up}capturas/{lang}/'
    home = SITE + u['home_url']
    related = ''.join(f'<li><a href="{SITE}{PAGES[k]["path"][lang]}">{e(PAGES[k][lang]["name"])}</a></li>'
                      for k in PAGES if k != key)
    ld = [
        {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': u['home'], 'item': home},
            {'@type': 'ListItem', 'position': 2, 'name': c['name'], 'item': url}]},
        {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
            {'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in c['faq']]},
    ]
    ipad = ''
    if p['ipad']:
        ipad = (f'<div class="tablet wide-shot"><img src="{shots}ipad-h-{p["ipad"]}.jpg" width="1400" height="1050" '
                f'alt="{e(c["ipad_alt"])}" loading="lazy" decoding="async"></div>')
    store = f'<a class="store" href="{APP}">{APPLE}<span><small>{e(u["store_small"])}</small><b>App Store</b></span></a>'
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(c["title"])}</title>
<meta name="description" content="{e(c["desc"])}">
<meta name="color-scheme" content="light">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="en" href="{SITE}{p["path"]["en"]}">
<link rel="alternate" hreflang="es" href="{SITE}{p["path"]["es"]}">
<link rel="alternate" hreflang="x-default" href="{SITE}{p["path"]["en"]}">
<meta name="apple-itunes-app" content="app-id=1455103430">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{e(c["title"])}">
<meta property="og:description" content="{e(c["desc"])}">
<meta property="og:image" content="{SITE}/{"og.jpg" if lang == "en" else "og-es.jpg"}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{up}icon.png">
<link rel="apple-touch-icon" href="{up}icon.png">
<script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=1)}
</script>
<style>{css}</style>
</head>
<body>
<a class="skip" href="#main">{e(u["skip"])}</a>
<div class="wrap">
<header class="site">
<a class="brand" href="{home}"><img src="{up}icon.png" width="32" height="32" alt="">{e(u["home"])}</a>
<a class="langlink" href="{SITE}{p["path"][other]}" hreflang="{other}" lang="{other}">{u["other_lang"]}</a>
</header>
<nav class="crumbs" aria-label="{u["crumbs_label"]}"><a href="{home}">{e(u["home"])}</a> › <span aria-current="page">{e(c["name"])}</span></nav>
<main id="main">
<div class="calc-hero">
<div>
<h1>{e(c["h1"])}</h1>
<p class="lead">{e(c["lead"])}</p>
<div class="cta">{store}</div>
</div>
<div class="phone"><img src="{shots}{p["shot"]}.jpg" width="660" height="1434" alt="{e(c["alt"])}" fetchpriority="high"></div>
</div>

<div class="block prose">
<h2>{e(c["how_h"])}</h2>
<ol class="steps">{"".join(f"<li>{e(x)}</li>" for x in c["how"])}</ol>
<h3>{e(c["ex_h"])}</h3>
{worked_table(c)}
<p class="note">{e(c["ex_note"])}</p>
</div>

<div class="block">
<h2>{e(c["app_h"])}</h2>
<ul class="prose">{"".join(f"<li>{e(x)}</li>" for x in c["app"])}</ul>
{ipad}
</div>

<div class="block">
<h2>{e(u["faq"])}.</h2>
<dl class="devlist faq">{"".join(f"<div><dt>{e(q)}</dt><dd>{e(a)}</dd></div>" for q, a in c["faq"])}</dl>
</div>

<div class="block">
<h2>{e(u["more"])}.</h2>
<ul class="related">{related}<li><a href="{home}">{e(u["all_link"])}</a></li></ul>
</div>

<div class="final">
<img src="{up}icon.png" width="180" height="180" alt="">
<h2>{e(u["cta_h"])}</h2>
<p class="sub">{e(u["free_line"])}</p>
<div class="cta">{store}</div>
</div>
</main>

<footer>
<div class="maker">
<p>{u["made_by"]} Josue Echandia · <a href="mailto:josue@echandia.app">josue@echandia.app</a></p>
<p>{u["made"]}</p>
</div>
<nav aria-label="Legal">
<a href="{SITE}{u["privacy"][1]}">{u["privacy"][0]}</a>
<a href="{SITE}{u["support"][1]}">{u["support"][0]}</a>
</nav>
</footer>
</div>
</body>
</html>
'''


def main():
    css = style()
    for key in PAGES:
        for lang in ('en', 'es'):
            path = PAGES[key]['path'][lang]
            out = os.path.join(ROOT, path.strip('/'), 'index.html')
            os.makedirs(os.path.dirname(out), exist_ok=True)
            open(out, 'w', encoding='utf-8').write(page(key, lang, css))
            print('escrito', os.path.relpath(out, ROOT))


if __name__ == '__main__':
    main()
