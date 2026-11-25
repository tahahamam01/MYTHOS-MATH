# -*- coding: utf-8 -*-
# Part 1: lessons + applications (FR/EN).  AR falls back to the old ARX map where the EN string is unchanged.
def T(fr, en): return {"fr": fr, "en": en}
def X(tex): return {"x": tex}
def tt(fr, en=None, ar=None): return [fr, en or fr, ar or en or fr]

# ---------------------------------------------------------------- LESSONS
L1 = {"id": "rn-l1", "title": tt("Introduction et définition", "Introduction and definition", "تمهيد والتعريف"), "steps": [
 {"id": "s1", "t": tt("Introduction", "Introduction", "تمهيد"), "story": T("", ""), "apps": [], "blocks": [
  T(r"On connaît $x \mapsto x^2$ et sa réciproque $x \mapsto \sqrt{x}$. Pour chaque entier $n \ge 1$, la fonction $x \mapsto x^n$ a aussi une réciproque, la **racine $n$-ième** $\sqrt[n]{x}$ :",
    r"We know $x \mapsto x^2$ and its inverse $x \mapsto \sqrt{x}$. For every integer $n \ge 1$, the function $x \mapsto x^n$ also has an inverse, the **$n$-th root** $\sqrt[n]{x}$:"),
  T(r"• réciproque de $x^3$ : la racine cubique $\sqrt[3]{x}$ ;", r"• inverse of $x^3$: the cube root $\sqrt[3]{x}$;"),
  T(r"• réciproque de $x^4$ : la racine quatrième $\sqrt[4]{x}$ ;", r"• inverse of $x^4$: the fourth root $\sqrt[4]{x}$;"),
  T(r"• réciproque de $x^{1000}$ : la racine $1000$-ième $\sqrt[1000]{x}$.", r"• inverse of $x^{1000}$: the $1000$-th root $\sqrt[1000]{x}$."),
 ]},
 {"id": "s2", "t": tt("Définition", "Definition", "التعريف"), "story": T("", ""), "apps": [], "blocks": [
  T(r"Soit $n \in \mathbb{N}^*$. La fonction $f : x \mapsto x^n$ définie sur $I = [0, +\infty[$ admet une fonction réciproque $f^{-1}$ définie sur $J = f(I) = [0, +\infty[$. Elle s’appelle la **fonction racine d’ordre $n$**, notée $\sqrt[n]{\ }$ :",
    r"Let $n \in \mathbb{N}^*$. The function $f : x \mapsto x^n$ defined on $I = [0, +\infty[$ has an inverse function $f^{-1}$ defined on $J = f(I) = [0, +\infty[$. It is called the **$n$-th root function**, denoted $\sqrt[n]{\ }$:"),
  X(r"\forall x \ge 0,\ \forall y \ge 0 : \quad x^n = y \iff x = \sqrt[n]{y}"),
  T(r"**Remarque : racines d’indice impair.** Si $n$ est **impair**, la racine $\sqrt[n]{x}$ est définie pour **tout** réel $x$ et $\sqrt[n]{-x} = -\sqrt[n]{x}$ (exemple : $\sqrt[3]{-8} = -2$). Si $n$ est **pair**, $\sqrt[n]{x}$ n’existe que pour $x \ge 0$. Cette remarque est utilisée dans tout le cours (équations, limites en $-\infty$).",
    r"**Remark: roots of odd index.** If $n$ is **odd**, the root $\sqrt[n]{x}$ is defined for **every** real number $x$ and $\sqrt[n]{-x} = -\sqrt[n]{x}$ (example: $\sqrt[3]{-8} = -2$). If $n$ is **even**, $\sqrt[n]{x}$ only exists for $x \ge 0$. This remark is used throughout the lesson (equations, limits at $-\infty$)."),
 ]},
]}

# lesson 2 (Propriétés) is kept as in the previous version (loaded from the old data by the build script)

L3 = {"id": "rn-l3", "title": tt("Simplification des racines n-ièmes", "Simplifying n-th roots", "تبسيط الجذور من الرتبة n"), "steps": [
 {"id": "s1", "t": tt("Simplification des racines n-ièmes", "Simplifying n-th roots", "تبسيط الجذور من الرتبة n"),
  "story": T("", ""), "apps": ["rn-app1", "rn-app2"], "blocks": [
  T(r"**L’idée clé :** transforme chaque racine en puissance :", r"**The key idea:** turn every root into a power:"),
  X(r"\sqrt[n]{a^{m}} = a^{m/n}"),
  T(r"Puis utilise les règles des puissances que tu connais déjà.", r"Then use the rules for powers that you already know."),
  T(r"**Règles à retenir** (pour $a, b \ge 0$) :", r"**Rules to remember** (for $a, b \ge 0$):"),
  X(r"\sqrt[n]{a} \times \sqrt[n]{b} = \sqrt[n]{ab}"),
  X(r"\dfrac{\sqrt[n]{a}}{\sqrt[n]{b}} = \sqrt[n]{\dfrac{a}{b}}"),
  T(r"(même indice obligatoire pour ces deux règles)", r"(the same index is required for these two rules)"),
  X(r"\left(\sqrt[n]{a}\right)^{n} = a"),
  X(r"\sqrt[n]{\sqrt[m]{a}} = \sqrt[nm]{a}"),
  T(r"**3 étapes :**", r"**3 steps:**"),
  T(r"1. **Décomposer** le nombre sous la racine :", r"1. **Decompose** the number under the root:"),
  X(r"625 = 5^{4}, \qquad 1024 = 2^{10}, \qquad 16 = 2^{4}"),
  T(r"2. **Simplifier** quand l’exposant est égal à l’indice :", r"2. **Simplify** when the exponent equals the index:"),
  X(r"\sqrt[4]{5^{4}} = 5"),
  T(r"3. **Réduire au même indice** pour comparer ou multiplier des racines différentes (on prend un multiple commun).",
    r"3. **Reduce to the same index** to compare or multiply different roots (take a common multiple)."),
 ]},
]}

L4 = {"id": "rn-l4", "title": tt("Identités remarquables et équations", "Remarkable identities and equations", "المتطابقات الهامة والمعادلات"), "steps": [
 {"id": "s1", "t": tt("Identités remarquables", "Remarkable identities", "المتطابقات الهامة"), "story": T("", ""), "apps": [], "blocks": [
  T(r"**Identités pour les équations :**", r"**Identities for equations:**"),
  X(r"a^{3} + b^{3} = (a + b)(a^{2} - ab + b^{2})"),
  X(r"a^{3} - b^{3} = (a - b)(a^{2} + ab + b^{2})"),
  T(r"Le second facteur $a^{2} \pm ab + b^{2}$ ne s’annule que si $a = b = 0$ (pour $b \neq 0$ fixé, son discriminant est $-3b^{2} < 0$). Dans les équations, **seul le premier facteur** donne des solutions réelles.",
    r"The second factor $a^{2} \pm ab + b^{2}$ vanishes only if $a = b = 0$ (for fixed $b \neq 0$, its discriminant is $-3b^{2} < 0$). In equations, **only the first factor** gives real solutions."),
 ]},
 {"id": "s2", "t": tt("Résoudre une équation avec des racines", "Solving an equation with roots", "حل معادلة تحتوي على جذور"),
  "story": T("", ""), "apps": ["rn-app3"], "blocks": [
  T(r"**Méthode en 5 étapes :**", r"**5-step method:**"),
  T(r"1. **Condition d’existence.** Indice pair (racine carrée) : le contenu doit être $\ge 0$. Indice impair (racine cubique) : aucune condition.",
    r"1. **Existence condition.** Even index (square root): the content must be $\ge 0$. Odd index (cube root): no condition."),
  T(r"2. **Isoler** la racine d’un côté du signe $=$.", r"2. **Isolate** the root on one side of the sign $=$."),
  T(r"3. **Élever à la puissance $n$** des deux côtés ($n$ = indice de la racine) :", r"3. **Raise both sides to the power $n$** ($n$ = index of the root):"),
  X(r"\left(\sqrt[n]{A}\right)^{n} = A"),
  T(r"4. **Résoudre** l’équation obtenue (factorisation, identités remarquables ou discriminant $\Delta$).", r"4. **Solve** the resulting equation (factorisation, remarkable identities or discriminant $\Delta$)."),
  T(r"5. **Vérifier chaque solution.** C’est obligatoire pour les indices pairs, car l’élévation au carré peut créer de fausses solutions.",
    r"5. **Check every solution.** This is mandatory for even indices, because squaring can create false solutions."),
  T(r"**Cas $x^{n} = a$ :**", r"**Case $x^{n} = a$:**"),
  T(r"• $n$ impair : une seule solution, $x = \sqrt[n]{a}$ (quel que soit le signe de $a$) ;", r"• $n$ odd: a single solution, $x = \sqrt[n]{a}$ (whatever the sign of $a$);"),
  T(r"• $n$ pair et $a > 0$ : deux solutions, $x = \pm\sqrt[n]{a}$ ;", r"• $n$ even and $a > 0$: two solutions, $x = \pm\sqrt[n]{a}$;"),
  T(r"• $n$ pair et $a < 0$ : aucune solution.", r"• $n$ even and $a < 0$: no solution."),
  T(r"**Cas $x^{3} \pm a^{3} = 0$ :** on utilise les identités, puis on vérifie que le second facteur a $\Delta < 0$, donc ne donne aucune solution réelle.",
    r"**Case $x^{3} \pm a^{3} = 0$:** use the identities, then check that the second factor has $\Delta < 0$, so it gives no real solution."),
 ]},
]}

L5 = {"id": "rn-l5", "title": tt("Limites avec racines", "Limits with roots", "النهايات والجذور"), "steps": [
 {"id": "s1", "t": tt("Ce qu’il faut retenir", "What to remember", "ما يجب تذكره"), "story": T("", ""), "apps": [], "blocks": [
  T(r"Pour une limite avec une **racine carrée**, on remplace $x$ d’abord. Si on tombe sur une **forme indéterminée** ($\frac{0}{0}$ ou $\infty - \infty$), on multiplie par la **quantité conjuguée**.",
    r"For a limit with a **square root**, first replace $x$. If you get an **indeterminate form** ($\frac{0}{0}$ or $\infty - \infty$), multiply by the **conjugate**."),
  T(r"Pour une **racine cubique**, on fait la même chose, mais le conjugué n’est plus $(a + b)$. On utilise l’identité de $a^{3} - b^{3}$ :",
    r"For a **cube root**, do the same, but the conjugate is no longer $(a + b)$. We use the identity for $a^{3} - b^{3}$:"),
  X(r"a^{3} - b^{3} = (a - b)(a^{2} + ab + b^{2})"),
  T(r"Donc pour une expression $\sqrt[3]{A} - b$ :", r"So for an expression $\sqrt[3]{A} - b$:"),
  T(r"• on pose $a = \sqrt[3]{A}$ ;", r"• let $a = \sqrt[3]{A}$;"),
  T(r"• on multiplie en haut et en bas par $a^{2} + ab + b^{2}$ : c’est le **conjugué cubique** ;", r"• multiply top and bottom by $a^{2} + ab + b^{2}$: this is the **cubic conjugate**;"),
  T(r"• le numérateur devient $a^{3} - b^{3} = A - b^{3}$, sans aucune racine.", r"• the numerator becomes $a^{3} - b^{3} = A - b^{3}$, with no root left."),
 ]},
 {"id": "s2", "t": tt("Étapes à suivre", "Steps to follow", "الخطوات"), "story": T("", ""), "apps": [], "blocks": [
  T(r"**Étapes :**", r"**Steps:**"),
  T(r"1. **Remplacer** $x$ par la valeur. Si forme indéterminée, passer à l’étape 2.", r"1. **Replace** $x$ by the value. If it is an indeterminate form, go to step 2."),
  T(r"2. **Multiplier** par le conjugué (carré ou cubique).", r"2. **Multiply** by the conjugate (square or cubic)."),
  T(r"3. **Simplifier** : le facteur qui annule le dénominateur disparaît.", r"3. **Simplify**: the factor that cancels the denominator disappears."),
  T(r"4. **Remplacer à nouveau.**", r"4. **Replace again.**"),
  T(r"**En $\pm\infty$**, on peut aussi factoriser le terme dominant. Attention :", r"**At $\pm\infty$**, you can also factor out the dominant term. Be careful:"),
  X(r"\sqrt[4]{x^{4}} = |x|"),
  T(r"(indice pair : on obtient la valeur absolue)", r"(even index: we get the absolute value)"),
  X(r"\sqrt[3]{x^{3}} = x"),
  T(r"(indice impair : pas de valeur absolue)", r"(odd index: no absolute value)"),
 ]},
 {"id": "s3", "t": tt("Exemple", "Example", "مثال"), "story": T("", ""), "apps": ["rn-app4", "rn-app5", "rn-app6"], "blocks": [
  T(r"**Exemple :** calculer", r"**Example:** compute"),
  X(r"\lim_{x \to 0} \frac{\sqrt[3]{x+1} - 1}{x}"),
  T(r"**Étape 1.** On remplace $x$ par $0$ :", r"**Step 1.** Replace $x$ by $0$:"),
  X(r"\frac{\sqrt[3]{0+1} - 1}{0} = \frac{1 - 1}{0} = \frac{0}{0}"),
  T(r"C’est une **forme indéterminée** $\frac{0}{0}$, donc on passe à l’étape 2.", r"This is an **indeterminate form** $\frac{0}{0}$, so we go to step 2."),
  T(r"**Étape 2.** On pose $a = \sqrt[3]{x+1}$ et $b = 1$. On multiplie en haut et en bas par $a^{2} + a + 1$ :",
    r"**Step 2.** Let $a = \sqrt[3]{x+1}$ and $b = 1$. Multiply top and bottom by $a^{2} + a + 1$:"),
  X(r"\frac{\sqrt[3]{x+1} - 1}{x} = \frac{(x+1) - 1}{x\left(\sqrt[3]{(x+1)^{2}} + \sqrt[3]{x+1} + 1\right)}"),
  T(r"**Étape 3.** On simplifie par $x$ :", r"**Step 3.** Simplify by $x$:"),
  X(r"\frac{\sqrt[3]{x+1} - 1}{x} = \frac{1}{\sqrt[3]{(x+1)^{2}} + \sqrt[3]{x+1} + 1}"),
  T(r"**Étape 4.** On remplace à nouveau $x$ par $0$ :", r"**Step 4.** Replace $x$ by $0$ again:"),
  X(r"\lim_{x \to 0} \frac{\sqrt[3]{x+1} - 1}{x} = \frac{1}{1 + 1 + 1} = \frac{1}{3}"),
 ], "extra": {"badge": tt("Hors programme · bon à savoir", "Outside the syllabus · good to know", "خارج المقرر · للاطلاع"), "blocks": [
  T(r"**Dériver une racine $n$-ième.** On écrit la racine en puissance, $\sqrt[n]{u} = u^{1/n}$, puis on dérive comme une puissance :",
    r"**Differentiating an $n$-th root.** Write the root as a power, $\sqrt[n]{u} = u^{1/n}$, then differentiate like a power:"),
  X(r"(u^{\alpha})' = \alpha \cdot u^{\alpha - 1} \cdot u'"),
  T(r"**Exemple :**", r"**Example:**"),
  X(r"g(x) = \sqrt[3]{x^{2} + 1} = (x^{2} + 1)^{1/3}"),
  X(r"g'(x) = \frac{1}{3}(x^{2} + 1)^{-2/3} \cdot 2x = \frac{2x}{3\sqrt[3]{(x^{2} + 1)^{2}}}"),
 ]}},
]}

# ---------------------------------------------------------------- APPLICATIONS
APPS = []
def app(id_, p_fr, p_en, q, sol):
    APPS.append({"id": id_, "own": True, "p": T(p_fr, p_en), "q": q, "sol": sol})

app("rn-app1", "**Simplifier :**", "**Simplify:**",
    r"\begin{aligned}A &= \sqrt[3]{54} + \sqrt[3]{16} - \sqrt[3]{128}\\[12pt] B &= \sqrt[4]{81} \times \sqrt[3]{8} - \sqrt[5]{32}\\[12pt] C &= \sqrt[3]{2} \times \sqrt[6]{4}\\[12pt] D &= \dfrac{\sqrt[4]{3^{6}} \times \sqrt{3}}{\sqrt[6]{3^{9}}}\end{aligned}",
    [T(r"**A.** On décompose chaque nombre pour faire apparaître un cube :", r"**A.** Decompose each number to make a cube appear:"),
     X(r"\sqrt[3]{54} = \sqrt[3]{27 \times 2} = 3\sqrt[3]{2}"),
     X(r"\sqrt[3]{16} = \sqrt[3]{8 \times 2} = 2\sqrt[3]{2}"),
     X(r"\sqrt[3]{128} = \sqrt[3]{64 \times 2} = 4\sqrt[3]{2}"),
     T(r"On factorise $\sqrt[3]{2}$ :", r"Factor out $\sqrt[3]{2}$:"),
     X(r"A = (3 + 2 - 4)\sqrt[3]{2} = \sqrt[3]{2}"),
     T(r"**B.** On calcule chaque racine :", r"**B.** Compute each root:"),
     X(r"\sqrt[4]{81} = 3 \quad (3^{4} = 81)"),
     X(r"\sqrt[3]{8} = 2 \quad (2^{3} = 8)"),
     X(r"\sqrt[5]{32} = 2 \quad (2^{5} = 32)"),
     X(r"B = 3 \times 2 - 2 = 4"),
     T(r"**C.** On passe aux puissances rationnelles :", r"**C.** Switch to rational powers:"),
     X(r"\sqrt[6]{4} = 2^{2/6} = 2^{1/3}"),
     X(r"C = 2^{1/3} \times 2^{1/3} = 2^{2/3} = \sqrt[3]{4}"),
     T(r"**D.** On écrit chaque racine comme une puissance de $3$ :", r"**D.** Write each root as a power of $3$:"),
     X(r"\sqrt[4]{3^{6}} = 3^{6/4} = 3^{3/2}, \qquad \sqrt{3} = 3^{1/2}, \qquad \sqrt[6]{3^{9}} = 3^{9/6} = 3^{3/2}"),
     X(r"D = \frac{3^{3/2} \times 3^{1/2}}{3^{3/2}} = 3^{1/2} = \sqrt{3}")])

app("rn-app2", "**Ordonner par ordre croissant :**", "**Order from smallest to largest:**",
    r"\begin{aligned}\text{a)}\quad & \sqrt[3]{3}\ ;\ \sqrt{2}\ ;\ \sqrt[6]{10}\\[12pt] \text{b)}\quad & \sqrt[3]{2}\ ;\ \sqrt[4]{5}\ ;\ \sqrt{3}\end{aligned}",
    [T(r"**a)** On met toutes les racines au même indice $6$ :", r"**a)** Put all the roots at the same index $6$:"),
     X(r"\sqrt[3]{3} = \sqrt[6]{3^{2}} = \sqrt[6]{9}"),
     X(r"\sqrt{2} = \sqrt[6]{2^{3}} = \sqrt[6]{8}"),
     X(r"\sqrt[6]{10}"),
     T(r"Comme $8 < 9 < 10$ :", r"Since $8 < 9 < 10$:"),
     X(r"\sqrt{2} < \sqrt[3]{3} < \sqrt[6]{10}"),
     T(r"**b)** On met toutes les racines au même indice $12$ :", r"**b)** Put all the roots at the same index $12$:"),
     X(r"\sqrt[3]{2} = \sqrt[12]{2^{4}} = \sqrt[12]{16}"),
     X(r"\sqrt[4]{5} = \sqrt[12]{5^{3}} = \sqrt[12]{125}"),
     X(r"\sqrt{3} = \sqrt[12]{3^{6}} = \sqrt[12]{729}"),
     T(r"Comme $16 < 125 < 729$ :", r"Since $16 < 125 < 729$:"),
     X(r"\sqrt[3]{2} < \sqrt[4]{5} < \sqrt{3}")])

app("rn-app3", "**Résoudre dans $\\mathbb{R}$ :**", "**Solve in $\\mathbb{R}$:**",
    r"\begin{aligned}E_{1} &: x^{3} - 64 = 0\\[12pt] E_{2} &: x^{3} + 125 = 0\\[12pt] E_{3} &: \sqrt[3]{x^{2} - x + 2} = 2\\[12pt] E_{4} &: \sqrt{2x + 3} = x\\[12pt] E_{5} &: x^{4} - 16 = 0\end{aligned}",
    [T(r"**$E_{1}$ :** on utilise l’identité de $a^{3} - b^{3}$ avec $64 = 4^{3}$ :", r"**$E_{1}$:** use the identity for $a^{3} - b^{3}$ with $64 = 4^{3}$:"),
     X(r"x^{3} - 4^{3} = (x - 4)(x^{2} + 4x + 16) = 0"),
     T(r"Pour le second facteur, $\Delta = 16 - 64 < 0$ : pas de solution. Donc seul $x - 4 = 0$ convient.", r"For the second factor, $\Delta = 16 - 64 < 0$: no solution. So only $x - 4 = 0$ works."),
     X(r"S = \{4\}"),
     T(r"**$E_{2}$ :** on utilise l’identité de $a^{3} + b^{3}$ avec $125 = 5^{3}$ :", r"**$E_{2}$:** use the identity for $a^{3} + b^{3}$ with $125 = 5^{3}$:"),
     X(r"x^{3} + 5^{3} = (x + 5)(x^{2} - 5x + 25) = 0"),
     T(r"Pour le second facteur, $\Delta = 25 - 100 < 0$ : pas de solution. Donc seul $x + 5 = 0$ convient.", r"For the second factor, $\Delta = 25 - 100 < 0$: no solution. So only $x + 5 = 0$ works."),
     X(r"S = \{-5\}"),
     T(r"**$E_{3}$ :** condition d’existence : aucune (indice $3$ impair). On élève au cube :", r"**$E_{3}$:** existence condition: none (odd index $3$). Raise to the cube:"),
     X(r"x^{2} - x + 2 = 8 \iff x^{2} - x - 6 = 0"),
     X(r"\Delta = 1 + 24 = 25"),
     X(r"x = \frac{1 + 5}{2} = 3 \qquad ;\qquad x = \frac{1 - 5}{2} = -2"),
     T(r"Vérification : $x = 3$ donne $9 - 3 + 2 = 8$ ✓ et $x = -2$ donne $4 + 2 + 2 = 8$ ✓.", r"Check: $x = 3$ gives $9 - 3 + 2 = 8$ ✓ and $x = -2$ gives $4 + 2 + 2 = 8$ ✓."),
     X(r"S = \{-2,\ 3\}"),
     T(r"**$E_{4}$ :** condition : $2x + 3 \ge 0$, et $x \ge 0$ puisqu’une racine carrée est positive. On élève au carré :", r"**$E_{4}$:** condition: $2x + 3 \ge 0$, and $x \ge 0$ since a square root is positive. Square both sides:"),
     X(r"2x + 3 = x^{2} \iff x^{2} - 2x - 3 = 0 \iff (x - 3)(x + 1) = 0"),
     T(r"$x = 3$ convient : $\sqrt{9} = 3$ ✓.", r"$x = 3$ works: $\sqrt{9} = 3$ ✓."),
     T(r"$x = -1$ est rejeté car $x \ge 0$ n’est pas respecté : $\sqrt{1} = 1 \neq -1$.", r"$x = -1$ is rejected because $x \ge 0$ fails: $\sqrt{1} = 1 \neq -1$."),
     X(r"S = \{3\}"),
     T(r"**$E_{5}$ :** $x^{4} = 16$ avec $n = 4$ pair et $16 > 0$, donc deux solutions :", r"**$E_{5}$:** $x^{4} = 16$ with $n = 4$ even and $16 > 0$, so two solutions:"),
     X(r"x = \pm\sqrt[4]{16} = \pm 2"),
     X(r"S = \{-2,\ 2\}")])

app("rn-app4", "**Calculer la limite :**", "**Compute the limit:**",
    r"\lim_{x \to 1} \frac{\sqrt[3]{9x-1} - 2}{x - 1}",
    [T(r"**Étape 1.** On remplace $x$ par $1$ :", r"**Step 1.** Replace $x$ by $1$:"),
     X(r"\frac{\sqrt[3]{9 \times 1 - 1} - 2}{1 - 1} = \frac{\sqrt[3]{8} - 2}{0} = \frac{2 - 2}{0} = \frac{0}{0}"),
     T(r"C’est une **forme indéterminée** $\frac{0}{0}$ : on multiplie par le conjugué cubique.", r"This is an **indeterminate form** $\frac{0}{0}$: multiply by the cubic conjugate."),
     T(r"**Étape 2.** On pose $a = \sqrt[3]{9x-1}$ et $b = 2$. Le conjugué est $a^{2} + 2a + 4$ :", r"**Step 2.** Let $a = \sqrt[3]{9x-1}$ and $b = 2$. The conjugate is $a^{2} + 2a + 4$:"),
     X(r"\frac{\sqrt[3]{9x-1} - 2}{x - 1} = \frac{(9x - 1) - 8}{(x - 1)\left(\sqrt[3]{(9x-1)^{2}} + 2\sqrt[3]{9x-1} + 4\right)}"),
     T(r"**Étape 3.** On simplifie : $(9x - 1) - 8 = 9x - 9 = 9(x - 1)$, et le facteur $x - 1$ disparaît :", r"**Step 3.** Simplify: $(9x - 1) - 8 = 9x - 9 = 9(x - 1)$, and the factor $x - 1$ cancels:"),
     X(r"\frac{9(x-1)}{(x-1)\left(a^{2} + 2a + 4\right)}"),
     X(r"= \frac{9}{\sqrt[3]{(9x-1)^{2}} + 2\sqrt[3]{9x-1} + 4}"),
     T(r"**Étape 4.** On remplace à nouveau $x$ par $1$ :", r"**Step 4.** Replace $x$ by $1$ again:"),
     X(r"\lim_{x \to 1} \frac{\sqrt[3]{9x-1} - 2}{x - 1} = \frac{9}{4 + 4 + 4} = \frac{9}{12} = \frac{3}{4}")])

app("rn-app5", "**Calculer la limite :**", "**Compute the limit:**",
    r"\lim_{x \to +\infty} \left(\sqrt[3]{x^{3} + 5x^{2} + 1} - x\right)",
    [T(r"**Étape 1.** On remplace $x$ par $+\infty$ : $\sqrt[3]{x^{3} + 5x^{2} + 1} \to +\infty$ et $x \to +\infty$.", r"**Step 1.** Replace $x$ by $+\infty$: $\sqrt[3]{x^{3} + 5x^{2} + 1} \to +\infty$ and $x \to +\infty$."),
     X(r"+\infty - \infty"),
     T(r"C’est une **forme indéterminée** $\infty - \infty$ : on multiplie par le conjugué cubique.", r"This is an **indeterminate form** $\infty - \infty$: multiply by the cubic conjugate."),
     T(r"**Étape 2.** On pose $a = \sqrt[3]{x^{3} + 5x^{2} + 1}$ et $b = x$. On multiplie en haut et en bas par $a^{2} + ax + x^{2}$ :", r"**Step 2.** Let $a = \sqrt[3]{x^{3} + 5x^{2} + 1}$ and $b = x$. Multiply top and bottom by $a^{2} + ax + x^{2}$:"),
     X(r"a - x = \frac{a^{3} - x^{3}}{a^{2} + ax + x^{2}} = \frac{5x^{2} + 1}{a^{2} + ax + x^{2}}"),
     T(r"**Étape 3.** On pose $u = 1 + \frac{5}{x} + \frac{1}{x^{3}}$, donc $a = x\,u^{1/3}$, et on divise en haut et en bas par $x^{2}$ :", r"**Step 3.** Let $u = 1 + \frac{5}{x} + \frac{1}{x^{3}}$, so $a = x\,u^{1/3}$, and divide top and bottom by $x^{2}$:"),
     X(r"a - x = \frac{5 + \frac{1}{x^{2}}}{u^{2/3} + u^{1/3} + 1}"),
     T(r"**Étape 4.** Quand $x \to +\infty$, on a $u \to 1$ et $\frac{1}{x^{2}} \to 0$ :", r"**Step 4.** When $x \to +\infty$, $u \to 1$ and $\frac{1}{x^{2}} \to 0$:"),
     X(r"\lim_{x \to +\infty} \left(\sqrt[3]{x^{3} + 5x^{2} + 1} - x\right) = \frac{5}{1 + 1 + 1} = \frac{5}{3}")])

app("rn-app6", "**Calculer la limite :**", "**Compute the limit:**",
    r"\lim_{x \to -\infty} \frac{\sqrt[4]{x^{4} + 1} - 2}{x + 5}",
    [T(r"**Étape 1.** Ici $x \to -\infty$, donc $x < 0$. Le numérateur tend vers $+\infty$ et le dénominateur vers $-\infty$ :", r"**Step 1.** Here $x \to -\infty$, so $x < 0$. The numerator tends to $+\infty$ and the denominator to $-\infty$:"),
     X(r"\frac{+\infty}{-\infty}"),
     T(r"C’est une **forme indéterminée** $\frac{\infty}{\infty}$ : on factorise le terme dominant.", r"This is an **indeterminate form** $\frac{\infty}{\infty}$: factor out the dominant term."),
     T(r"**Étape 2.** Attention à l’indice pair : $\sqrt[4]{x^{4}} = |x|$, et $|x| = -x$ car $x < 0$ :", r"**Step 2.** Careful with the even index: $\sqrt[4]{x^{4}} = |x|$, and $|x| = -x$ since $x < 0$:"),
     X(r"\sqrt[4]{x^{4} + 1} = |x|\sqrt[4]{1 + \frac{1}{x^{4}}} = -x\sqrt[4]{1 + \frac{1}{x^{4}}}"),
     T(r"**Étape 3.** On divise le numérateur et le dénominateur par $x$ :", r"**Step 3.** Divide the numerator and the denominator by $x$:"),
     X(r"\frac{-x\sqrt[4]{1 + \frac{1}{x^{4}}} - 2}{x + 5} = \frac{-\sqrt[4]{1 + \frac{1}{x^{4}}} - \frac{2}{x}}{1 + \frac{5}{x}}"),
     T(r"**Étape 4.** Quand $x \to -\infty$, $\frac{1}{x^{4}} \to 0$, $\frac{2}{x} \to 0$ et $\frac{5}{x} \to 0$ :", r"**Step 4.** When $x \to -\infty$, $\frac{1}{x^{4}} \to 0$, $\frac{2}{x} \to 0$ and $\frac{5}{x} \to 0$:"),
     X(r"\lim_{x \to -\infty} \frac{\sqrt[4]{x^{4} + 1} - 2}{x + 5} = \frac{-1 - 0}{1 + 0} = -1")])
