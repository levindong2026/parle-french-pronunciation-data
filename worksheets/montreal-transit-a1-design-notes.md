# Keep the answer off the learner sheet: a French transit activity

For A1 French, a public transit guide can supply a real reason to read. A learner needs to decide whether a fictional traveller can use the same ticket, then tell a partner why. The [Montréal exercise and its two printable sheets](https://getparle.app/french-speaking-course/town-directions/#montreal-printable) show how we designed this task at Parle. The [Société de transport de Montréal passenger guide](https://www.stm.info/titres-tarifs/correspondances) is the text learners consult.

## Give learners two different reasons to look up the rule

For fares covered by the guide, STM gives riders 120 minutes from validation to finish the trip. It also lists cases that require another fare, including a return on the same line. Our two fictional cards each isolate one decision:

| Card | Information to give a partner | Question to answer |
| --- | --- | --- |
| A | A rider validated a ticket 35 minutes ago and takes the same bus line back in the opposite direction. | Does the same ticket cover the return? Explain which rule applies. |
| B | A rider validates at 9:00 and arrives at 11:10. | Is the trip within the time limit? Explain how many minutes have elapsed. |

Allow two minutes to predict the meaning of *correspondance* and *aller-retour*, three to locate the rules, four to exchange the cards orally, and three for feedback and a changed arrival time. Give each learner one card. Their partner hears the details, consults the guide and replies using *oui* or *non* and *parce que*. Then swap roles. For the final prompt, move the arrival time to 10:45 and ask for the new total.

Check for a decision plus the relevant reason. Card A requires another fare because of the same-line return; 35 minutes alone would be within the time limit. Card B takes 130 minutes. The changed trip takes 105 minutes and is within the time limit. Both B prompts ask about time alone. Accept any clear French reply that gives the correct decision and reason.

## Separate the materials at the point of use

On paper, put both cut-apart cards and space for reading answers on a single learner page. Put the explanation and reply models in a second file for the teacher. On the web, put the examples behind explicitly labelled reveal controls, with the two roles individually expandable. In both formats ask, “What makes that trip different from a transfer?” An earlier print draft asked, “Why does it need another fare?” and gave away part of the decision.

Our current print generator uses one structured content file to render the two PDFs. The online exercise has its own source and is compared against the sheets during review. Each card needs the same trip details across formats, including the time and the scope of the decision.

## Check the files after export

Download the learner and teacher PDFs from the exercise and keep their filenames. Run this check from the download directory with Python 3 and `pypdf` installed. It checks page sizes, what answer material appears, and whether all three required PDF links survived export.

```python
from pathlib import Path

from pypdf import PdfReader

expected_links = {
    "https://www.stm.info/titres-tarifs/correspondances",
    "https://getparle.app/french-speaking-course/town-directions/#montreal-transit-practice",
    "https://creativecommons.org/licenses/by/4.0/",
}


def check_sheet(filename):
    reader = PdfReader(Path(filename), strict=True)
    assert len(reader.pages) == 1
    page = reader.pages[0]
    assert abs(float(page.mediabox.width) - 595.3) < 1
    assert abs(float(page.mediabox.height) - 841.9) < 1
    links = set()
    for reference in page.get("/Annots", []):
        action = reference.get_object().get("/A")
        if action and action.get("/S") == "/URI":
            links.add(str(action["/URI"]))
    assert links == expected_links, links
    return " ".join(page.extract_text().split())


learner = check_sheet("montreal-transit-a1-learner-sheet.pdf")
teacher = check_sheet("montreal-transit-a1-teacher-key.pdf")
assert "CARTE A" in learner and "CARTE B" in learner
assert "11 h 10" in learner
assert all(text not in learner for text in ("120 minutes", "130 minutes", "105 minutes"))
assert all(text in teacher for text in ("120 minutes", "130 minutes", "105 minutes"))
```

Then open both files in a PDF viewer. Check the cut line, French accents, the placement of times, and the space for writing. The script cannot find a visually clipped card or tell you whether it leaves enough room for handwriting.

Credit Parle (Tingnova Inc.) when adapting its [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) exercise and reply models. The STM guide is a separate publication. Link to the current guide when adapting the activity and confirm its rules before class.
