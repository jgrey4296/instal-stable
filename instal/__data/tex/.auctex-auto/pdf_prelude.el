(TeX-add-style-hook
 "pdf_prelude"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("ulem" "normalem")))
   (TeX-run-style-hooks
    "latex2e"
    "article"
    "art10"
    "todonotes"
    "array"
    "longtable"
    "enumitem"
    "tikz"
    "layout"
    "ulem")
   (LaTeX-add-environments
    "events"
    "states")
   (LaTeX-add-lengths
    "tableWidth"))
 :latex)

