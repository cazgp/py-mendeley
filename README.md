py-mendeley
===========

Python wrapper to interact with Mendeley's sqlite database (specifically to extract annotations and highlights for org-mode)

Produces one org file per document requested with all highlights in the document. *Extremely* slow.

Dependent upon:

`pdfquery`
`yaml`

Nice to have:

`emacs`
`vim-orgmode`

To-Do
-----

* [ ] Recursive folder searching.
* [ ] Generate a linked file of all documents in folder (currently only one file per document).
* [ ] Specify on the command line where to put generated org files (currently pwd).
* [x] Add annotations to the output.
* [ ] File watching -> when an annotation is added, automatically recompile.
* [ ] File watching per folder / per tag.
* [ ] Generate annotations for a given tag.
* [ ] Parse references to generate links between documents.
