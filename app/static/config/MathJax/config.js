const HORIZ_SCOLL_DIV_HTML = "<div class=\"scroll-overflow-x\"></div>";
const HORIZ_SCOLL_DIV_HTML_WIDTH_FULL = "<div class=\"scroll-overflow-x\" width=\"full\"></div>";

function onMathJaxTypeset(root_selector) {
    const root_elem = $(root_selector);
    if (!root_elem) {
        return;
    }
    // Make font of \[\] LaTeX blocks shrink on mobile and make them scroll horizontally on overflow
    root_elem.find("mjx-math[style='margin-left: 0px; margin-right: 0px;']").addClass("shrinking-font-15").wrap(HORIZ_SCOLL_DIV_HTML);
    root_elem.find("mjx-math[width='full']").each(function() {
        $(this).parent("mjx-container").css("min-width", ""); // can cause overflow problems
        $(this).addClass("shrinking-font-15").wrap(HORIZ_SCOLL_DIV_HTML_WIDTH_FULL); // for \tag{}ed
    });
}

window.MathJax = {
    tex: {
        tags: "ams",
        macros: {
            // simple math symbols
            divs: "\\mid",
            F: "\\mathbb{F}",
            given: "\\,\\vert\\,",
            givenlong: "\\,\\middle\\vert\\,",
            N: "\\mathbb{N}",
            nequiv: "\\not\\equiv",
            notdivs: "\\nmid",
            powerset: "\\mathcal{P}",
            R: "\\mathbb{R}",
            Q: "\\mathbb{Q}",
            suchthat: "\\,\\vert\\,",
            suchthatlong: "\\,\\middle\\vert\\,",
            Z: "\\mathbb{Z}",
            // redefined functions to always use parentheses around arguments
            Arccos: ["\\arccos{\\left(#1\\right)}", 1],
            Arccot: ["\\arccot{\\left(#1\\right)}", 1],
            Arccsc: ["\\arccsc{\\left(#1\\right)}", 1],
            Arcsec: ["\\arcsec{\\left(#1\\right)}", 1],
            Arcsin: ["\\arcsin{\\left(#1\\right)}", 1],
            Arctan: ["\\arctan{\\left(#1\\right)}", 1],
            Cos: ["\\cos{\\left(#1\\right)}", 1],
            Cot: ["\\cot{\\left(#1\\right)}", 1],
            Csc: ["\\csc{\\left(#1\\right)}", 1],
            Int: ["\\int_{#1}^{#2}{\\left(#3\\right)}", 3],
            Lim: ["\\lim_{#1}{\\left(#2\\right)}", 2],
            Log: ["\\log_{#1}{\\left(#2\\right)}", 2],
            Ln: ["\\ln{\\left(#1\\right)}", 1],
            Sec: ["\\sec{\\left(#1\\right)}", 1],
            Sin: ["\\sin{\\left(#1\\right)}", 1],
            Sum: ["\\sum_{#1}^{#2}{\\left(#3\\right)}", 3],
            Tan: ["\\tan{\\left(#1\\right)}", 1],
            // other math notations and shorthands
            ceil: ["\\left\\lceil #1 \\right\\rceil", 1],
            choose: ["\\begin{pmatrix} #1 \\\\ #2 \\end{pmatrix}", 2],
            comb: ["{}^{#1}C_{#2}", 2],
            ddx: ["\\frac{\\mathrm{d}}{\\mathrm{d} #1}", 1],
            dydx: ["\\frac{\\mathrm{d} #1}{\\mathrm{d} #2}", 2],
            dx: ["\\,\\mathrm{d} #1", 1],
            floor: ["\\left\\lfloor #1 \\right\\rfloor", 1],
            ftc: ["\\left[#3\\right]_{#1}^{#2}", 3],
            multichoose: ["\\left(\\!\\!\\choose{#1}{#2}\\!\\!\\right)", 2],
            perm: ["{}^{#1}P_{#2}", 2],
            ppx: ["\\frac{\\partial}{\\partial #1}", 1],
            pypx: ["\\frac{\\partial #1}{\\partial #2}", 2],
            ppxpy: ["\\frac{\\partial^2}{\\partial #1 \\partial #2}", 2],
            pfpxpy: ["\\frac{\\partial^2 #1}{\\partial #2 \\partial #3}", 3],
            // text
            andd: "\\text{ and }",
            cand: ",\\, \\text{and }",
            c: ",\\,",
            cor: ",\\, \\text{or }",
            DNE: "\\text{DNE}",
            gcd: "\\text{gcd}",
            lcm: "\\text{lcm}",
            mod: "\\text{ mod }",
            orr: "\\text{ or }",
            st: "\\text{ s.t. }",
            t: "\\text",
            // other
            p: ["\\phantom{#1}", 1],
            r: ["\\textcolor{red}{#1}", 1]
        }
    },
    startup: {
        ready: function() {
            MathJax.startup.defaultReady();
            MathJax.startup.promise.then(function() {
                onMathJaxTypeset("body");
            });
        }
    }
};
