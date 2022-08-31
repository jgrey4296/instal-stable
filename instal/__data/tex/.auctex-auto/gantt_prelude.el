(TeX-add-style-hook
 "gantt_prelude"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("geometry" "margin=1cm")))
   (TeX-run-style-hooks
    "latex2e"
    "article"
    "art10"
    "graphicx"
    "tikz"
    "pgfgantt"
    "longtable"
    "geometry"))
 :latex)

