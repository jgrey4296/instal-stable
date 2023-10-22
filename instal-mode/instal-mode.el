;;; instal-mode.el -*- lexical-binding: t; no-byte-compile: t; -*-
;;-- header
;;
;; Copyright (C) 2021 John Grey
;;
;; Author: John Grey <https://github.com/johngrey>
;; Maintainer: John Grey <johngrey4296 at gmail.com>
;; Created: July 26, 2021
;; Modified: July 26, 2021
;; Version: 0.0.1
;; Keywords: Symbol’s value as variable is void: finder-known-keywords
;; Homepage: https://github.com/johngrey/instal-mode
;; Package-Requires: ((emacs "24.3"))
;;
;; This file is not part of GNU Emacs.
;;
;;; Commentary:
;;
;;
;;
;;; Code:
;;-- end header

;;-- imports
(require 'instal-faces)

;;-- end imports

;;-- keymap
(defvar-local instal-mode-map
  (make-sparse-keymap))

;;-- end keymap

;;-- fontlock
(defconst instal-font-lock-keywords
  (rx-let ((w (x) (: x (1+ blank)))
           (term (: word-start (1+ word) (| word-end (group "(" (1+ any) ")") ) (0+ blank)))
           (var  (: word-start upper (0+ word) (opt "(" (1+ any) ")") word-end))
           (ln (: punctuation line-end))
           (deontics (: word-start (| "power" "permitted" "genPower" "initPower" "termPower" ) word-end))
           (shortened (: word-start (| "inst" "exo" "viol" "obl") word-end))
           (incomplete (: word-start (| "perm" "pow" "int" "ev" "exogenous" "obl") word-end))
           (obligation (: (opt (| "achievement" "maintenance") blank) "obligation"))
           )
    (list
     ;; -------------------- Declarations
     `(,(rx line-start word-start (w (| "institution" "bridge" "source" "sink")) (group term) ln)
     (0 'font-lock-keyword-face)
     (1 'font-lock-constant-face t))

     `(,(rx line-start (w "type") (group var))
     (0 'font-lock-keyword-face)
     (1 'font-lock-type-face t))

     ;; -------------------- Event Declaration
     `(,(rx line-start (group-n 1 (opt (w (| "external" "institutional" "violation" shortened)))) (w "event" ) (group-n 2 term) ln)
       (0 'font-lock-keyword-face)
       (1 'instal-modifiers-face t)
       (2 'instal-events-face t))

     ;; -------------------- Fluent Declaration
     `(,(rx line-start (group-n 1 (opt (w (| "transient" obligation)))) (w "fluent") (group-n 2 term ) ln)
       (0 'font-lock-keyword-face)
       (1 'instal-modifiers-face t)
       (2 'instal-fluents-face t))

     ;; -------------------- Initial situation
     `(,(rx line-start (w  "initially") (group-n 1 term (0+ (: (w ",") term))) ln)
       (0 'font-lock-keyword-face)
       (1 'instal-fluents-face t))

     ;; -------------------- Rules
     `(,(rx line-start (group-n 1 term) (w "generates") (group-n 2 term))
       (0 'font-lock-keyword-face)
       (1 'instal-events-face t)
       (2 'instal-events-face t))

     `(,(rx line-start (group-n 1 term) (w (| "initiates" "terminates")) (group-n 2 term)
            (| "if" ln))
            (0 'font-lock-keyword-face)
            (1 'instal-events-face t)
            (2 'instal-fluents-face t))

     `(,(rx line-start (group-n 1 term) (w "when") (group-n 2 term))
       (0 'font-lock-keyword-face)
       (1 'instal-fluents-face t)
       (2 'instal-fluents-face t))

     `(,(rx word-start (w "if") (group-n 1 term (0+ (w ",") term) ln))
       (0 'font-lock-keyword-face t)
       (1 'default t))

     ;; -------------------- Modifiers
     `(,(rx deontics)
       (0 'instal-deontics-face))
     `(,(rx (: word-start (or "observed" "occurred") word-end))
       (0 'instal-events-face))
     `(,(rx shortened)
       (0 '(instal-modifiers-face (:weight bold) t)))
     `(,(rx incomplete)
       (0 'font-lock-warning-face t))
     ;; `(,(rx (: "(" (group (*? anychar)) ")"))
     ;;   (1 'instal-highlight-face append))
     `(,(rx (: word-start upper (zero-or-more word) word-end))
       (0 'font-lock-type-face t))
     `(,(rx (: symbol-start (or "<=" ">=" "<>" "!=" "<" ">" "=") symbol-end))
       (0 'instal-operators-face t))
       )
    )
  "Highlighting for instal-mode"
  )

;;-- end fontlock

;;-- syntax
(defvar instal-mode-syntax-table
  (let ((st (make-syntax-table)))
    ;; Punctuation
    (modify-syntax-entry ?. "." st)
    (modify-syntax-entry ?! "." st)
    ;; Symbols
    (modify-syntax-entry ?$ "_" st)
    ;;underscores are valid parts of words:
    (modify-syntax-entry ?_ "w" st)
    ;; Comments start with % and end with newlines
    (modify-syntax-entry ?% "<" st)
    (modify-syntax-entry ?\n ">" st)
    ;; Strings
    (modify-syntax-entry ?\" "\"" st)
    ;; Pair parens, brackets, braces
    (modify-syntax-entry ?\( "()" st)
    (modify-syntax-entry ?\[ "(]" st)
    (modify-syntax-entry ?\{ "(}" st)
    (modify-syntax-entry ?: ".:2" st)
    st)
  "Syntax table for the instal-mode")

;;-- end syntax



;;-- mode definition
(define-derived-mode instal-mode fundamental-mode
  "instal"
  ""
  (interactive)
  (kill-all-local-variables)
  (use-local-map instal-mode-map)

  (set (make-local-variable 'font-lock-defaults) (list instal-font-lock-keywords))
  ;; (set (make-local-variable 'font-lock-syntactic-face-function) 'instal-syntactic-face-function)
  ;; (set (make-local-variable 'indent-line-function) 'instal-indent-line)
  (set (make-local-variable 'comment-style) '(plain))
  (set (make-local-variable 'comment-start) "%%")
  (set (make-local-variable 'comment-use-syntax) t)
  (set (make-local-variable 'font-lock-extra-managed-props) '(:weight))
  (set-syntax-table instal-mode-syntax-table)
  ;;
  (setq major-mode 'instal-mode)
  (setq mode-name "instal")
  (run-mode-hooks)
  (outline-minor-mode)
  (yas-minor-mode)

  )
(add-to-list 'auto-mode-alist '("\\.ia[[:alpha:]]$" . instal-mode))

;;-- end mode definition

(provide 'instal-mode)
;;; instal-mode.el ends here
