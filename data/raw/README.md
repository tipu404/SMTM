unarXive
========

arXiv source data used:
    all LaTeX sources up until Dec 31 2022
arXiv metadata used:
    snapshot from Jan 1 2023
OpenAlex data used:
    snapshot from Nov 28 2022



contents
========

-README                                 // this file
-unarXive_<yymmdd>.tar.xz
    +-<yy>                              // year directory
        +-arXiv_src_<yymm>_<num>.jsonl  // unarXive data



links
=====

GitHub: https://github.com/IllDepence/unarXive
Zenodo: https://doi.org/10.5281/zenodo.7752754 (full)
        https://doi.org/10.5281/zenodo.7752615 (open subset)
Huggingface: https://huggingface.co/datasets/saier/unarXive_citrec
             https://huggingface.co/datasets/saier/unarXive_imrad_clf



usage
=====

(See GitHub repository for more detailed information.)

1. unpack
---------
unarXive is distributed as an XZ compressed TAR archive. You can unpack
it using either of the following methods.
    - On the command line using tar -xJf.
    - Graphically with 7zip (https://www.7-zip.org/).

2. load
-------
Each decompressed file arXiv_src_<yy><mm>_<num>.jsonl is in the JSON Lines
format (https://jsonlines.org/). This means each line is a JSON object and
can, for example, be loaded in Python with json.loads(some_line).

3. use paper data
-----------------
Papers are represented as shown in the example below, which is an excerpt
from the paper 2105.05862 from the file arXiv_src_2105_034.jsonl. A full
documentation of data fields is given further down.

Paper object:
```
{
  "paper_id": "2105.05862",
  "_pdf_hash": None,
  "_source_hash": "b7d5f27b5c8abc3bd8a44d875899fdc0d945a604",
  "_source_name": "2105.05862.gz",
  "metadata": {...},
  "discipline": "Physics",
  "abstract": {...},
  "body_text": [...],
  "bib_entries": {...},
  "ref_entries": {...}
}
```

One example paragraph in "body_text" is:
```
{
  "section": "Memory wave form",
  "sec_number": "2.1",
  "sec_type": "subsection",
  "content_type": "paragraph",
  "text": "The gauge choice leading us to this solution does not fix "
          "completely all the gauge freedom and an additional constraint "
          "should be imposed to leave only the physical degrees of freedom. "
          "This is done by projecting the source tensor {{formula:7fd88bcd-"
          "9013-433d-9756-b874472530d9}}  into its transverse-traceless (TT) "
          "components (see for example {{cite:80dbb6c8b9c12f561a8e585faceac5f"
          "4e104d60d}}). Doing this and without loss of generality, we will "
          "use the following very well known ansatz for the source term "
          "proposed in {{cite:bc9a8ca19785627a087ae0c01abe155c22388e16}}\n",
  "cite_spans": [...],
  "ref_spans": [...]
}
```

where "{{formula:7fd88bcd-9013-433d-9756-b874472530d9}}" refers in
"ref_entries" to
```
{
  "latex": "S_{\\mu \\nu }",
  "type": "formula"
}
```

and "{{cite:bc9a8ca19785627a087ae0c01abe155c22388e16}}", for example, refers in
"bib_entries" to
```
{
  "bib_entry_raw": "R. Epstein, The Generation of Gravitational Radiation by "
                   "Escaping Supernova Neutrinos, Astrophys. J. 223 (1978) "
                   "1037.",
  "contained_arXiv_ids": [],
  "contained_links": [
    {
      "url": "https://doi.org/10.1086/156337",
      "text": "Astrophys. J. 223 (1978) 1037.",
      "start": 87,
      "end": 117
    }
  ],
  "discipline": "Physics",
  "ids" {...}
}
```



data format
===========

root object (paper)
-------------------
paper_id: arXiv ID of the paper
_pdf_hash: always None
_source_hash: SHA1 hash of the arXiv source file
_source_name: name of the arXiv source file
metadata: paper metadata from kaggle.com/datasets/Cornell-University/arxiv
discipline: scientific discipline of the paper
abstract: paper abstract copied from metadata
body_text: list of paper content sections (paragraphs, listings, etc.)
bib_entries: list of bibliographic references
ref_entries: list of non-textual content (figures, formulas, etc.)

  body_text list element
  ----------------------
  section: section name
  sec_number: section number
  sec_type: section type (section, subsection, etc.)
  content_type: content type (paragraph, listing, etc.)
  text: text content
  cite_spans: list of citation markers
  ref_spans: list of referenced non-textual content (figures, formulas, etc.)

    cite_spans list element
    -----------------------
    start: starting character offset in text
    end: ending character offset in text
    text: surface text
    ref_id: dictionary key for linked content in bib_entries

    ref_spans list element
    -----------------------
    start: starting character offset in text
    end: ending character offset in text
    text: surface text
    ref_id: dictionary key for linked content in ref_entries

  bib_entries element
  -------------------
  bib_entry_raw: raw bibliographic reference string
  contained_arXiv_ids: list of linked arXiv papers
  contained_links: list of embedded links
  discipline: scientific discipline of the cited paper
  ids: matched identifiers of referenced paper

    contained_arXiv_ids element
    ---------------------------
    id: ID of linked arXiv paper
    text: text segment in reference that the link was attached to
    start: starting character offset in bib_entry_raw
    end: ending character offset in bib_entry_raw

    contained_links_ids element
    ---------------------------
    url: URL of link
    text: text segment in reference that the link was attached to
    start: starting character offset in bib_entry_raw
    end: ending character offset in bib_entry_raw

    ids element:
    ------------
    open_alex_id: referenced paper’s OpenAlex ID
    sem_open_alex_id: referenced paper’s  SemOpenAlex ID
    pubmed_id: referenced paper’s PubMed ID
    pmc_id: referenced paper’s PMC ID
    doi: referenced paper’s DOI
    arxiv_id: referenced paper’s arXiv ID

  ref_entries dictionary entry (tables and figures)
  -------------------------------------------------
  type: content type
  caption: table/figure caption

  ref_entries dictionary entry (mathematical notation)
  ----------------------------------------------------
  type: always "formula"
  latex: content of LaTeX math mode
