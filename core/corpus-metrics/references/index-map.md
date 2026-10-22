# Index Map

Which index bears on which diagnostic question, and what each family can and cannot support.

The organising principle: these tools measure **text-internal properties**. The review
framework holds that value is reader-relative. So the map below covers the sentence layer and
part of the movement layer, and stops. There is no index for "does this change what the
committee believes," and any attempt to construct one from these numbers is numerology.

## Contents

0. [Tier 1 — the pip backends](#0-tier-1--the-pip-backends)
1. [Cohesion — TAACO](#1-cohesion--taaco)
2. [Movement and connectives — TAACO](#2-movement-and-connectives--taaco)
3. [Syntactic density — TAASSC](#3-syntactic-density--taassc)
4. [Lexical diversity — TAALED](#4-lexical-diversity--taaled)
5. [ReaderBench](#5-readerbench)
6. [What none of them measure](#6-what-none-of-them-measure)
7. [Validity, stated plainly](#7-validity-stated-plainly)

---

## 0. Tier 1 — the pip backends

These are the default, and for a writing review they are usually enough. Sections 1–5 below
describe the canonical Tier-2 tools; read them for the *conceptual* content, which transfers,
but note that the numbers do not.

| Index | Backend | Bears on | How to read it |
|---|---|---|---|
| `first_order_coherence` | textdescriptives | old before new | Cosine similarity between adjacent sentence embeddings. Low = consecutive sentences give the reader nothing to attach to. The closest Tier-1 analogue to TAACO's adjacent overlap. |
| `second_order_coherence` | textdescriptives | paragraph structure | Same, for sentences one apart. **Low first-order with healthy second-order means interleaved topics, not disconnection** — two threads alternating. That is a different finding and a different fix. |
| `dependency_distance_mean` | textdescriptives | short subject, early verb | Mean distance between dependent and head. High = words held in mind before their relation resolves. The quantitative shadow of the delayed-verb diagnosis. |
| `prop_adjacent_dependency_relation_mean` | textdescriptives | same | Share of dependencies that are adjacent. Falls as the above rises. |
| `pos_prop_NOUN`, `_ADJ`, `_ADP` | textdescriptives | nominalization | Elevated together is the signature of phrasal compression — content packed into noun phrases rather than clauses. |
| `pos_prop_VERB`, `_AUX` | textdescriptives | agency | Low verb share is where characters stop doing things. |
| `pos_prop_PRON` | textdescriptives | given/new | Very low pronoun use usually means full noun phrases repeated where continuity was available. |
| `pos_prop_SCONJ` vs `_CCONJ` | textdescriptives | movement | Subordination carries logical relation; coordination accumulates. The *ratio* is the tell. |
| `flesch_reading_ease`, `gunning_fog`, etc. | textdescriptives | length baselines | Crude — they see only word and sentence length. Useful corpus-relative, meaningless absolute. **Never report a grade level to an academic**; it will read as an insult and it is not measuring what they care about. |
| `sentence_length_*`, `token_length_*` | textdescriptives | rhythm | Variance matters more than the mean. |
| `n_noun`, `a_noun_ps`, syntax-domain keys | lftk | phrasal density | Counts and per-sentence averages. Overlaps textdescriptives' POS proportions; agreement between them is reassuring, disagreement means check the parse. |
| `mattr`, `mtld`, `hdd` | taaled | see §4 | Handle per the warning below. |

**The single most useful Tier-1 pairing** is `first_order_coherence` against
`second_order_coherence`. Four quadrants, four different diagnoses — connected and
developing; connected but restating; two interleaved threads; genuinely disconnected. Report
the quadrant, not the numbers.

**What Tier 1 cannot do that Tier 2 can:** connective incidence *by semantic category*
(TAACO), and the phrasal-vs-clausal complexity split (TAASSC). If the review's finding is
"your text accumulates rather than argues" or "your density is phrasal, not clausal," those
need Tier 2. Everything else, Tier 1 covers.

---

## 1. Cohesion — TAACO

**Bears on:** old-before-new; topic strings; whether consecutive sentences give the reader
something to attach to.

| Index family | What it measures | How to read it |
|---|---|---|
| `adjacent_overlap_*_sent` | Lemma overlap between consecutive sentences, by word class | Low = each sentence starts fresh. This is the quantitative form of the old-before-new diagnosis. |
| `adjacent_overlap_*_para` | Same, across paragraph boundaries | Low = paragraph seams have nothing to hold onto. Often the sharpest single number in a review. |
| `adjacent_overlap_2_*` | Overlap across a two-sentence window | High here with low adjacent overlap suggests interleaved topics rather than disconnection. |
| `adjacent_overlap_binary_*` | Whether *any* overlap exists, not how much | Useful when a few very long sentences distort the continuous measure. |
| `lsa_1_all_sent`, `lda_1_all_sent`, `word2vec_1_all_sent` | Semantic similarity between adjacent segments | Survives synonym variation, which lemma overlap does not. **Low lemma overlap + high LSA = the author is elegantly varying terms for one concept.** That is worth naming: variation reads as distinction to a reader learning a vocabulary. |
| `syn_overlap_*` | WordNet synonym overlap | Same logic, lexical rather than distributional. |
| `pronoun_noun_ratio`, givenness indices | Given/new management | Very low pronoun ratio in expository prose usually means full noun phrases repeated where a pronoun would signal continuity. |
| `repeated_content_lemmas` | Content lemma repetition | High with low semantic development = restating rather than advancing. |

**The most useful pairing:** `adjacent_overlap_content_sent` against `lsa_1_all_sent`. Four
quadrants, four different diagnoses — connected and developing; connected but restating;
varying terms for one idea; genuinely disconnected. Report the quadrant, not the numbers.

Note the *noun* variants specifically. Content-word overlap conflates several things;
noun-only overlap tracks what the paragraph is *about* and maps most directly onto topic
strings.

## 2. Movement and connectives — TAACO

**Bears on:** whether the text advances or accumulates.

Connective incidence by semantic category. The raw count matters less than the ratio: additive
connectives (*also, moreover, furthermore, in addition*) announce that another item is coming;
logical connectives (*but, because, so, which is why*) tell the reader what relation it bears.
A draft heavy on additive and light on causal/adversative is accumulating, and that is a
structural finding rather than a stylistic one.

Section-dependence is severe here. A methods section is legitimately additive. Compare like
with like or the number is meaningless.

## 3. Syntactic density — TAASSC

**Bears on:** short-subject-early-verb; nominalization; whether elaboration is easy or costly
to process.

| Index family | What it measures | How to read it |
|---|---|---|
| `nn_all`, noun counts | Nominal density | The quantitative form of "actions buried in nouns." |
| `np_premod_*`, attributive adjectives, nominal premodifiers | Noun-phrase elaboration | **This is usually the real finding.** Phrasal compression — stacked premodifiers inside a noun phrase — is what makes academic prose feel dense, more than sentence length does. |
| clausal complexity: finite complement, relative, adverbial clauses | Clausal elaboration | Elaboration readers process comparatively easily, because each clause has its own subject and verb. |
| `mean_length_*`, words per clause/T-unit | Length baselines | Weak on their own; useful as a denominator. |
| verb, voice, passive indices | Agency | Bears on whether characters are visible as subjects. |

**The interpretive key — Biber's developmental finding.** Advanced academic writing is *more*
phrasally complex and *less* clausally complex than speech or novice writing. So high phrasal
density is not automatically a defect; it is partly what registers as expert. What you are
looking for is phrasal density that is high **relative to the author's own venue**, which is
the only comparison that separates "writing like a professional" from "writing impenetrably."
This is precisely why raw values are useless here and percentiles are not.

## 4. Lexical diversity — TAALED

**Bears on:** very little, in this framework. Handle with care.

MATTR, MTLD, HD-D, MSTTR and the TTR family measure vocabulary variety corrected for text
length. They were developed and validated as measures of **language proficiency and lexical
development** — largely in L2 acquisition and child language research.

They are not measures of reader value, and in expert academic prose a *low* score often
reflects consistent technical terminology, which is exactly what the code layer wants.
Reporting low lexical diversity as a flaw in a paper that correctly reuses its field's terms
would be actively harmful advice.

Report these only when the author asks for them, and say what they do and do not license.
The one legitimate use in this workflow: an author who suspects they are varying terminology
for stylistic reasons can check whether their diversity is *high* relative to their venue —
which would corroborate a terminological-drift finding that came from reading, not from the
number.

## 5. ReaderBench

Broadest coverage — a cohesion-network graph plus a large set of textual-complexity indices
across several languages. Also the heaviest to run (torch, transformers, gensim, an
NLTK WordNet download) and the most awkward to script, since `usage.py` mixes in
Romanian-specific modules and a Flask server.

Worth the setup cost mainly for its **cohesion graph**, which models inter-sentence and
inter-paragraph links as a network rather than as pairwise adjacency. That captures
long-range cohesion — a paragraph that pays off a promise made four paragraphs earlier —
which TAACO's adjacent-overlap measures structurally cannot see. If a review's finding is
about unpaid promises or long-range structure, this is the tool with something to say.

For plain sentence-to-sentence cohesion, TAACO is faster, easier, and sufficient.

## 6. What none of them measure

Worth stating explicitly, because the temptation to over-read a rich output is strong:

- Whether the draft makes a claim, or only covers a topic.
- Whether anything is at risk for the reader.
- Whether the stakes are stated, or merely asserted with importance words.
- Whether the vocabulary is the target community's.
- Whether the contribution is worth the reader's time.

Levels 1, 2 and 4 of the ladder are unreachable by any text-internal instrument. When the
percentile report comes back clean and the draft is still not working, that is not a null
result — it is evidence pointing at the layers these tools cannot see.

## 7. Validity, stated plainly

Every index here has published validation. What it was validated *for* matters:

- **Cohesion indices** — validated primarily against reading comprehension outcomes and
  human ratings of essay quality, often in student and L2 corpora.
- **Syntactic complexity indices** — validated against register variation, developmental
  level, and writing quality ratings.
- **Lexical diversity indices** — validated against proficiency and vocabulary development.

None was validated against "expert reviewers judged this contribution valuable," which is the
outcome the review skills care about. Using them as a proxy for that is an inferential leap,
and the honest way to handle it is to make the leap visible rather than to hide it behind a
percentile.

Two consequences for how you write:

1. Attach every number to a passage. A number the author cannot see in their own text is a
   number they cannot act on and cannot check.
2. When the author says an index does not mean what you are taking it to mean in their
   subfield, believe them. They read this literature; you are reading its output.
