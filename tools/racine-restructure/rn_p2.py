# -*- coding: utf-8 -*-
from rn_p1 import T, X
EX = []
def ex(id_, d, p_fr, p_en, q, sol, note=None, top=False):
    e = {"id": id_, "d": d, "p": T(p_fr, p_en), "q": q, "sol": sol}
    if note: e["note"] = note; e["top"] = top
    EX.append(e)

# ---------- reusable sentences (identical wording everywhere)
def s1(v, vE=None):
    return T(r"**Étape 1.** On remplace $x$ par $%s$ :" % v, r"**Step 1.** Replace $x$ by $%s$:" % (vE or v))
IND0C = T(r"C’est une **forme indéterminée** $\frac{0}{0}$ : on multiplie par le conjugué cubique.", r"This is an **indeterminate form** $\frac{0}{0}$: multiply by the cubic conjugate.")
IND0 = T(r"C’est une **forme indéterminée** $\frac{0}{0}$.", r"This is an **indeterminate form** $\frac{0}{0}$.")
INDINF = T(r"C’est une **forme indéterminée** $\infty - \infty$ : on multiplie par le conjugué cubique.", r"This is an **indeterminate form** $\infty - \infty$: multiply by the cubic conjugate.")
def s2(a, b, conj):
    return T(r"**Étape 2.** On pose $a = %s$ et $b = %s$. Le conjugué est $%s$ :" % (a, b, conj), r"**Step 2.** Let $a = %s$ and $b = %s$. The conjugate is $%s$:" % (a, b, conj))
def s3(extra_fr="", extra_en=""):
    return T(r"**Étape 3.** On simplifie%s :" % extra_fr, r"**Step 3.** Simplify%s:" % extra_en)
def s4(v):
    return T(r"**Étape 4.** On remplace à nouveau $x$ par $%s$ :" % v, r"**Step 4.** Replace $x$ by $%s$ again:" % v)
LIM = ("Calculer la limite :", "Compute the limit:")
SIM = ("Simplifier :", "Simplify:")
SOL = ("Résoudre dans $\\mathbb{R}$ :", "Solve in $\\mathbb{R}$:")
def aligned(lines, sep=r"\\[12pt]"):
    return r"\begin{aligned}" + sep.join(lines) + r"\end{aligned}"

# =============================================================== CHICK
ex("rn-chick-01", "ve", "Calculer :", "Compute:",
   r"\sqrt[3]{27}\ ;\ \sqrt[4]{16}\ ;\ \sqrt[5]{32}\ ;\ \sqrt[3]{-8}",
   [T(r"Pour chaque racine, on cherche le nombre dont la puissance donne le radicande :", r"For each root, find the number whose power gives the radicand:"),
    T(r"$\sqrt[3]{27} = 3$ car $3^{3} = 27$", r"$\sqrt[3]{27} = 3$ since $3^{3} = 27$"),
    T(r"$\sqrt[4]{16} = 2$ car $2^{4} = 16$", r"$\sqrt[4]{16} = 2$ since $2^{4} = 16$"),
    T(r"$\sqrt[5]{32} = 2$ car $2^{5} = 32$", r"$\sqrt[5]{32} = 2$ since $2^{5} = 32$"),
    T(r"$\sqrt[3]{-8} = -2$ car $(-2)^{3} = -8$ (indice impair : le radicande peut être négatif)", r"$\sqrt[3]{-8} = -2$ since $(-2)^{3} = -8$ (odd index: the radicand can be negative)")])
ex("rn-chick-02", "ve", *SIM, r"\sqrt[3]{2} \times \sqrt[3]{4}",
   [T(r"Même indice : on regroupe sous une seule racine.", r"Same index: combine under a single root."),
    X(r"\sqrt[3]{2} \times \sqrt[3]{4} = \sqrt[3]{8} = 2")])
ex("rn-chick-03", "ve", *SIM, r"\dfrac{\sqrt[4]{48}}{\sqrt[4]{3}}",
   [T(r"Même indice : on regroupe sous une seule racine.", r"Same index: combine under a single root."),
    X(r"\frac{\sqrt[4]{48}}{\sqrt[4]{3}} = \sqrt[4]{\frac{48}{3}} = \sqrt[4]{16} = 2")])
ex("rn-chick-04", "ve", *SIM, r"\sqrt[3]{24} - \sqrt[3]{3}",
   [T(r"On fait apparaître un cube : $24 = 8 \times 3$.", r"Make a cube appear: $24 = 8 \times 3$."),
    X(r"\sqrt[3]{24} = \sqrt[3]{8 \times 3} = 2\sqrt[3]{3}"),
    T(r"Donc :", r"So:"),
    X(r"\sqrt[3]{24} - \sqrt[3]{3} = 2\sqrt[3]{3} - \sqrt[3]{3} = \sqrt[3]{3}")])
ex("rn-chick-05", "ve", *SIM, r"\sqrt[6]{8}",
   [T(r"On écrit $8 = 2^{3}$, puis on passe en puissance rationnelle :", r"Write $8 = 2^{3}$, then switch to a rational power:"),
    X(r"\sqrt[6]{8} = \sqrt[6]{2^{3}} = 2^{3/6} = 2^{1/2} = \sqrt{2}")])
ex("rn-chick-06", "ve", r"Comparer $\sqrt{2}$ et $\sqrt[3]{3}$.", r"Compare $\sqrt{2}$ and $\sqrt[3]{3}$.", "",
   [T(r"On met les deux racines au même indice $6$ :", r"Put both roots at the same index $6$:"),
    X(r"\sqrt{2} = \sqrt[6]{8}"), X(r"\sqrt[3]{3} = \sqrt[6]{9}"),
    T(r"Comme $8 < 9$ :", r"Since $8 < 9$:"),
    X(r"\sqrt{2} < \sqrt[3]{3}")])
ex("rn-chick-07", "ve", r"Comparer $\sqrt[3]{2}$ et $\sqrt[6]{5}$.", r"Compare $\sqrt[3]{2}$ and $\sqrt[6]{5}$.", "",
   [T(r"On met les deux racines au même indice $6$ :", r"Put both roots at the same index $6$:"),
    X(r"\sqrt[3]{2} = \sqrt[6]{4}"), X(r"\sqrt[6]{5}"),
    T(r"Comme $4 < 5$ :", r"Since $4 < 5$:"),
    X(r"\sqrt[3]{2} < \sqrt[6]{5}")])
ex("rn-chick-08", "ve", *SOL, r"x^{3} - 1 = 0",
   [T(r"On factorise avec l’identité de $a^{3} - b^{3}$ :", r"Factor with the identity for $a^{3} - b^{3}$:"),
    X(r"x^{3} - 1 = (x - 1)(x^{2} + x + 1) = 0"),
    T(r"Le second facteur a $\Delta = 1 - 4 = -3 < 0$ : pas de solution. Seul $x - 1 = 0$ convient.", r"The second factor has $\Delta = 1 - 4 = -3 < 0$: no solution. Only $x - 1 = 0$ works."),
    X(r"S = \{1\}")])
ex("rn-chick-09", "ve", *SOL, r"\sqrt[3]{x + 1} = 2",
   [T(r"Indice $3$ impair : aucune condition d’existence. On élève au cube :", r"Odd index $3$: no existence condition. Raise to the cube:"),
    X(r"x + 1 = 8 \iff x = 7"),
    T(r"Vérification : $\sqrt[3]{7 + 1} = \sqrt[3]{8} = 2$ ✓.", r"Check: $\sqrt[3]{7 + 1} = \sqrt[3]{8} = 2$ ✓."),
    X(r"S = \{7\}")])
ex("rn-chick-10", "ve", *LIM, r"\lim_{x \to 0} \frac{\sqrt[3]{x + 8} - 2}{x}",
   [s1("0"), X(r"\frac{\sqrt[3]{0 + 8} - 2}{0} = \frac{2 - 2}{0} = \frac{0}{0}"), IND0C,
    s2(r"\sqrt[3]{x+8}", "2", "a^{2} + 2a + 4"),
    X(r"\frac{\sqrt[3]{x+8} - 2}{x} = \frac{(x + 8) - 8}{x\left(\sqrt[3]{(x+8)^{2}} + 2\sqrt[3]{x+8} + 4\right)}"),
    s3(r" par $x$", r" by $x$"),
    X(r"\frac{\sqrt[3]{x+8} - 2}{x} = \frac{1}{\sqrt[3]{(x+8)^{2}} + 2\sqrt[3]{x+8} + 4}"),
    s4("0"),
    X(r"\lim_{x \to 0} \frac{\sqrt[3]{x + 8} - 2}{x} = \frac{1}{4 + 4 + 4} = \frac{1}{12}")])

# =============================================================== CHICKEN
ex("rn-chicken-01", "e", *LIM, r"\lim_{x \to 0} \frac{\sqrt[3]{x + 27} - 3}{x}",
   [s1("0"), X(r"\frac{\sqrt[3]{0 + 27} - 3}{0} = \frac{3 - 3}{0} = \frac{0}{0}"), IND0C,
    s2(r"\sqrt[3]{x+27}", "3", "a^{2} + 3a + 9"),
    X(r"\frac{(x + 27) - 27}{x\left(\sqrt[3]{(x+27)^{2}} + 3\sqrt[3]{x+27} + 9\right)}"),
    s3(r" par $x$", r" by $x$"),
    X(r"\frac{\sqrt[3]{x+27} - 3}{x} = \frac{1}{\sqrt[3]{(x+27)^{2}} + 3\sqrt[3]{x+27} + 9}"),
    s4("0"), X(r"\lim_{x \to 0} \frac{\sqrt[3]{x + 27} - 3}{x} = \frac{1}{9 + 9 + 9} = \frac{1}{27}")])
ex("rn-chicken-02", "e", *LIM, r"\lim_{x \to 1} \frac{\sqrt[3]{x + 7} - 2}{x - 1}",
   [s1("1"), X(r"\frac{\sqrt[3]{1 + 7} - 2}{1 - 1} = \frac{2 - 2}{0} = \frac{0}{0}"), IND0C,
    s2(r"\sqrt[3]{x+7}", "2", "a^{2} + 2a + 4"),
    X(r"\frac{(x + 7) - 8}{(x - 1)\left(\sqrt[3]{(x+7)^{2}} + 2\sqrt[3]{x+7} + 4\right)}"),
    s3(r" ($(x + 7) - 8 = x - 1$, le facteur $x - 1$ disparaît)", r" ($(x + 7) - 8 = x - 1$, the factor $x - 1$ cancels)"),
    X(r"\frac{x - 1}{(x - 1)\left(\sqrt[3]{(x+7)^{2}} + 2\sqrt[3]{x+7} + 4\right)} = \frac{1}{\sqrt[3]{(x+7)^{2}} + 2\sqrt[3]{x+7} + 4}"),
    s4("1"), X(r"\lim_{x \to 1} \frac{\sqrt[3]{x + 7} - 2}{x - 1} = \frac{1}{4 + 4 + 4} = \frac{1}{12}")])
ex("rn-chicken-03", "e", *LIM, r"\lim_{x \to -1} \frac{\sqrt[3]{x} + 1}{x + 1}",
   [s1("-1"), X(r"\frac{\sqrt[3]{-1} + 1}{-1 + 1} = \frac{-1 + 1}{0} = \frac{0}{0}"), IND0,
    T(r"**Étape 2.** On pose $a = \sqrt[3]{x}$. Alors $x + 1 = a^{3} + 1$, et on utilise l’identité de $a^{3} + b^{3}$ :", r"**Step 2.** Let $a = \sqrt[3]{x}$. Then $x + 1 = a^{3} + 1$, and we use the identity for $a^{3} + b^{3}$:"),
    X(r"x + 1 = a^{3} + 1 = (a + 1)(a^{2} - a + 1)"),
    s3(r" par $a + 1$", r" by $a + 1$"),
    X(r"\frac{a + 1}{(a + 1)(a^{2} - a + 1)} = \frac{1}{a^{2} - a + 1} = \frac{1}{\sqrt[3]{x^{2}} - \sqrt[3]{x} + 1}"),
    s4("-1"), X(r"\lim_{x \to -1} \frac{\sqrt[3]{x} + 1}{x + 1} = \frac{1}{1 + 1 + 1} = \frac{1}{3}")])
ex("rn-chicken-04", "e", *LIM, r"\lim_{x \to +\infty} \frac{\sqrt[3]{8x^{3} + 1}}{x}",
   [s1(r"+\infty"), X(r"\frac{+\infty}{+\infty}"),
    T(r"C’est une **forme indéterminée** $\frac{\infty}{\infty}$ : on factorise le terme dominant sous la racine.", r"This is an **indeterminate form** $\frac{\infty}{\infty}$: factor out the dominant term under the root."),
    T(r"**Étape 2.** On factorise $x^{3}$ sous la racine (valable car $\sqrt[3]{x^{3}} = x$) :", r"**Step 2.** Factor out $x^{3}$ under the root (valid since $\sqrt[3]{x^{3}} = x$):"),
    X(r"\frac{\sqrt[3]{x^{3}\left(8 + \frac{1}{x^{3}}\right)}}{x} = \frac{x\sqrt[3]{8 + \frac{1}{x^{3}}}}{x}"),
    T(r"**Étape 3.** On simplifie par $x$ :", r"**Step 3.** Simplify by $x$:"),
    X(r"\frac{\sqrt[3]{8x^{3} + 1}}{x} = \sqrt[3]{8 + \frac{1}{x^{3}}}"),
    T(r"**Étape 4.** Quand $x \to +\infty$, $\frac{1}{x^{3}} \to 0$ :", r"**Step 4.** When $x \to +\infty$, $\frac{1}{x^{3}} \to 0$:"),
    X(r"\lim_{x \to +\infty} \frac{\sqrt[3]{8x^{3} + 1}}{x} = \sqrt[3]{8} = 2")])
ex("rn-chicken-05", "e", *LIM, r"\lim_{x \to +\infty} \left(\sqrt[3]{x^{3} + 1} - x\right)",
   [s1(r"+\infty"), X(r"+\infty - \infty"), INDINF,
    s2(r"\sqrt[3]{x^{3}+1}", "x", "a^{2} + ax + x^{2}"),
    X(r"a - x = \frac{a^{3} - x^{3}}{a^{2} + ax + x^{2}} = \frac{(x^{3} + 1) - x^{3}}{a^{2} + ax + x^{2}}"),
    s3(),
    X(r"a - x = \frac{1}{\sqrt[3]{(x^{3}+1)^{2}} + x\sqrt[3]{x^{3}+1} + x^{2}}"),
    T(r"**Étape 4.** Quand $x \to +\infty$, le dénominateur tend vers $+\infty$ :", r"**Step 4.** When $x \to +\infty$, the denominator tends to $+\infty$:"),
    X(r"\lim_{x \to +\infty} \left(\sqrt[3]{x^{3} + 1} - x\right) = 0")])
ex("rn-chicken-06", "e", *SOL, r"x^{3} + 27 = 0",
   [T(r"On factorise avec l’identité de $a^{3} + b^{3}$, car $27 = 3^{3}$ :", r"Factor with the identity for $a^{3} + b^{3}$, since $27 = 3^{3}$:"),
    X(r"x^{3} + 3^{3} = (x + 3)(x^{2} - 3x + 9) = 0"),
    T(r"Le second facteur a $\Delta = 9 - 36 < 0$ : pas de solution. Seul $x + 3 = 0$ convient.", r"The second factor has $\Delta = 9 - 36 < 0$: no solution. Only $x + 3 = 0$ works."),
    X(r"S = \{-3\}")])
ex("rn-chicken-07", "e", *SOL, r"\sqrt[3]{2x - 1} = 3",
   [T(r"Indice $3$ impair : aucune condition. On élève au cube :", r"Odd index $3$: no condition. Raise to the cube:"),
    X(r"2x - 1 = 27 \iff 2x = 28 \iff x = 14"),
    T(r"Vérification : $\sqrt[3]{2 \times 14 - 1} = \sqrt[3]{27} = 3$ ✓.", r"Check: $\sqrt[3]{2 \times 14 - 1} = \sqrt[3]{27} = 3$ ✓."),
    X(r"S = \{14\}")])
ex("rn-chicken-08", "e", *SOL, r"\sqrt[3]{x^{2} + x + 6} = 2",
   [T(r"Indice $3$ impair : aucune condition. On élève au cube :", r"Odd index $3$: no condition. Raise to the cube:"),
    X(r"x^{2} + x + 6 = 8 \iff x^{2} + x - 2 = 0 \iff (x + 2)(x - 1) = 0"),
    T(r"Vérification : $x = 1$ donne $1 + 1 + 6 = 8$ ✓ et $x = -2$ donne $4 - 2 + 6 = 8$ ✓.", r"Check: $x = 1$ gives $1 + 1 + 6 = 8$ ✓ and $x = -2$ gives $4 - 2 + 6 = 8$ ✓."),
    X(r"S = \{-2,\ 1\}")])
ex("rn-chicken-09", "e", r"Simplifier $a$ et $b$, puis ranger $a$, $b$ et $c$ par ordre croissant :", r"Simplify $a$ and $b$, then order $a$, $b$ and $c$ from smallest to largest:",
   aligned([r"a &= \sqrt[6]{4}", r"b &= \sqrt[4]{4}", r"c &= \sqrt[3]{3}"]),
   [T(r"**Simplification.** On écrit $4 = 2^{2}$ :", r"**Simplification.** Write $4 = 2^{2}$:"),
    X(r"a = \sqrt[6]{2^{2}} = 2^{1/3} = \sqrt[3]{2}"),
    X(r"b = \sqrt[4]{2^{2}} = 2^{1/2} = \sqrt{2}"),
    T(r"**Comparaison.** On met au même indice $6$ :", r"**Comparison.** Put everything at the same index $6$:"),
    X(r"a = \sqrt[6]{4}, \qquad b = \sqrt[6]{8}, \qquad c = \sqrt[6]{9}"),
    T(r"Comme $4 < 8 < 9$ :", r"Since $4 < 8 < 9$:"),
    X(r"a < b < c \iff \sqrt[3]{2} < \sqrt{2} < \sqrt[3]{3}")])
ex("rn-chicken-10", "e", r"Simplifier $a$ et $b$, puis ranger $a$, $b$ et $c$ par ordre croissant :", r"Simplify $a$ and $b$, then order $a$, $b$ and $c$ from smallest to largest:",
   aligned([r"a &= \sqrt[4]{36}", r"b &= \sqrt[3]{2} \times \sqrt[3]{8}", r"c &= \sqrt[6]{125}"]),
   [T(r"**Simplification :**", r"**Simplification:**"),
    X(r"a = \sqrt[4]{6^{2}} = \sqrt{6}"),
    X(r"b = \sqrt[3]{2 \times 8} = \sqrt[3]{16}"),
    T(r"**Comparaison.** On met au même indice $6$ :", r"**Comparison.** Put everything at the same index $6$:"),
    X(r"a = \sqrt{6} = \sqrt[6]{6^{3}} = \sqrt[6]{216}"),
    X(r"b = \sqrt[3]{16} = \sqrt[6]{16^{2}} = \sqrt[6]{256}"),
    X(r"c = \sqrt[6]{125}"),
    T(r"Comme $125 < 216 < 256$ :", r"Since $125 < 216 < 256$:"),
    X(r"c < a < b")])
