# Documento Canónico Certificado: NISTSPECIALPUBLICATION500_235

**Autoridad:** NIST / SEI  
**Rule-ID:** NIST-SP-500-235  
**Categoría:** complexity_and_testing  
**Severidad:** high  
**Identificador:** `nistspecialpublication500_235`  
**Archivo Fuente Original:** `nistspecialpublication500-235.pdf`  
**Motor de Ingesta:** Microsoft MarkItDown (2026-10-12)

---

|     | NIST | Special |     | Publication | 500-235 |     |
| --- | ---- | ------- | --- | ----------- | ------- | --- |
Computer
Systems
|     |            |     |          |     | A Methodology |     |
| --- | ---------- | --- | -------- | --- | ------------- | --- |
|     | Structured |     | Testing: |     | Testing       |     |
Technology
|     |       |     | Cyclomatic |     | Complexity | Metric |
| --- | ----- | --- | ---------- | --- | ---------- | ------ |
|     | Using | the |            |     |            |        |
U.S. DEPARTMENTOF
COMMERCE
TechnologyAdministration
National Instituteof
| Standardsand | Dolores | R. Wallace, |     | Editor |     |     |
| ------------ | ------- | ----------- | --- | ------ | --- | --- |
Technology
| Nisr | Arthur | Watson |     |     |     |     |
| ---- | ------ | ------ | --- | --- | --- | --- |
H.
|     | Thomas | McCabe |     |     |     |     |
| --- | ------ | ------ | --- | --- | --- | --- |
J.
NATL OF STAND & JEC"
INST.
NiST
PUBLICATIONS
AlllDS DH7b5T
'
i .umiliik'i'IJ'Jl
QC
100
.157 NO.500-255
1996

Errata
ofNIST
Pages 9, 37, and 41 ofthe published version Special Publication 500-235 contain
|         | This   | page        |     |           |              | each   |      |         |     |     |
| ------- | ------ | ----------- | --- | --------- | ------------ | ------ | ---- | ------- | --- | --- |
| errors. |        | gives       | the | corrected | textfor      | error. |      |         |     |     |
| •       | Figure | 2-3 on page | 9   | should    | be (changeis | the    | path | shown): |     |     |
test
|     |           | A               |     |     | module |           |     |     |     |     |
| --- | --------- | --------------- | --- | --- | ------ | --------- | --- | --- | --- | --- |
|     | Rgure2-3. | testpaththrough |     |     |        | "euclid." |     |     |     |     |
The paragraph ofsection on page 37 should be (change underlined,
| •   | last |     |     |     | 5.4 |     |     |     |     | bold): |
| --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- | ------ |
"0"
The set oftests in Figure 5-5 detects the error (twice). Input "AB" should produce output
"1"
but instead produces output "1," and input "AC" should produce output but instead pro-
duces output "0." In fact, any set oftests that satisfies the structured testing criterion is guar-
|     |     |     | To  |     |     |     |     |     | nodes and |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --------- | --- |
anteed to detect the error. see this, note that to test the decisions at 3 7
| independently |     |          |          | one | input with |             | number | of   | than  |     |
| ------------- | --- | -------- | -------- | --- | ---------- | ----------- | ------ | ---- | ----- | --- |
|               |     | requires | at least |     |            | a different |        | 'B's | 'C's. |     |
• The paragraph ofsection 6.2 on page 41 should be (change underlined, bold):
first
To facilitate the proofofcorrectness, the method will be described in mathematical terms.
|     |     |     |     | may |     |     |     | 63  | more |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- |
Readers not interested in theory prefer to skip to section where a practical pre-
| sentation | ofthe | technique | is  | given. |     |     |     |     |     |     |
| --------- | ----- | --------- | --- | ------ | --- | --- | --- | --- | --- | --- |

|         |               | Rgure2-2. | Controlflowgraphformodule | "euclid." |
| ------- | ------------- | --------- | ------------------------- | --------- |
| Print]  | iSauej ;ClMe] | iHelp     |                           |           |
|         |               |           | Cyclomatic Test Paths     | Listing   |
| Program | Euclid        |           |                           | 04/07/97  |
| Module: | e:uclid       |           |                           |           |
:
|     |     | User | Specified Cyclomatic Test | Path: Path |
| --- | --- | ---- | ------------------------- | ---------- |
1
| Test       | Pat h 1: 0        | 1 5 6 7     | 1 1 1 2 13       |     |
| ---------- | ----------------- | ----------- | ---------------- | --- |
|            | 8(                | 1 ) n > m   | -- > F A L S E   |     |
|            |                   | :           | - -> F A L SE    |     |
|            | 1 4 (             | 7 ) : r! -0 |                  |     |
| Figure2-3. | A testpaththrough |             | module "euclid." |     |

that satisfies the structured testing criterion, which consists ofthe three tests from Figure 5-4
plus two additional tests to form a complete basis.
Input Output Correctness
X
-1 Correct
ABCX
1 Correct
Rgure5-4. Tests for"count"thatsatisfystatementand branch coverage.
Input Output Correctness
X
-1 Correct
ABCX
1 Correct
A
0 Correct
AB
1 Incorrect
AC 0 Incorrect
Figure5-5. Tests for "count"thatsatisfythestructured testing criterion.
The set oftests in Figure 5-5 detects the error (twice). Input "AB" should produce output "0"
but instead produces output "1," and input "AC" should produce output "1" but instead pro-
duces output "0." In fact, any set oftests that satisfies the structured testing criterion is guar-
anteed to detectthe error. To see this, note thatto test the decisions at nodes 3 and 7
independently requires at least one input with a different number of 'B's than 'C's.
5.5 Weak structured testing
Weak structured testing is, as it appears, a weakvariant ofstructured testing. It can be satis-
fied by exercising at leastv(G) different paths through the control flow graph while simulta-
neously covering aU branches, howevertherequirementthatthe paths form abasis is dropped.
Structured testing subsumes weak structured testing, but not the reverse. Weak structured
testing is much easierto perform manually than structured testing, because thereis no need to
do linear algebra on path vectors. Thus, weak structured testing was a way to get some ofthe
benefits ofstructured testing at a significantly lesser cost before automated support for struc-
tured testing was available, and is still worth considering for programming languages with no
automated structured testing support. In some olderliterature, no distinction is made between
the two criteria.
Ofthe three properties ofstructured testing discussed in section 5.2, two are shared by weak
structured testing. Itsubsumes statement and branch coverage, which provides a base level of
error detection effectiveness. It also requires testing proportional to complexity, which con-
centrates testing on the most error-prone software and supports precise test planning and mon-
itoring. However, it does not require all decision outcomes to be tested independeiitiy, and
37

6 The Baseline Method
The baseline method, described in this section, is a technique for identifying a set ofcontrol
paths to satisfy the structured testing criterion. The technique results in a basis set of test
paths through the module being tested, equal in number to the cyclomatic complexity of the
module. As discussed in section 2, the paths in a basis are independent and generate all paths
via linear combinations. Note that "the baseUne method" is different from "basis path test-
ing." Basis path testing, anothername forstructured testing, is the requirement that a basis set
ofpaths should be tested. The baseline method is one way to derive a basis set of paths. The
word "baseline" comes from the first path, which is typically selected by the tester to repre-
sent the "baseline" functionality ofthe module. The basehne method provides support for
structured testing, since it gives aspecific technique to identify an adequate test set ratherthan
resorting to trial and erroruntil the criterion is satisfied.
6.1 Generating a basis set ofpaths
The idea is to start with a baseline path, then vary exactly one decision outcome to generate
each successive path until all decision outcomes have been varied, at which time a basis will
have been generated. To understand the mathematics behind the technique, a simplified ver-
sion ofthe method will be presented and prove thatit generates a basis [WATS0N5]. Then,
the general technique that gives more freedom to the tester when selecting paths will be
described. Poole describes and analyzes an independently derived variant in [NIST5737].
6.2 The simplified baseline method
,
To facilitate the proofofcorrectness, the method will be described in mathematical terms.
Readers not interested in theory may preferto skip to section 6.3 where a more practical pre-
sentation ofthe technique is given.
In addition to a basis set ofpaths, which is a basis for the rows ofthe path/edge matrix if all
possible paths were represented, it is possible to also consider a basis set ofedges, which is a
basis forthe columns ofthe same matrix. Since row rank equals column rank, the cyclomatic
complexity is also the number of edges in every edge basis. The overall approach ofthis sec-
tion is to first select a basis set ofedges, then use that set in the algorithm to generate each
successive path, and finally use the resulting path/edge matrix restricted to basis columns to
show thatthe set of generated paths is a basis.
41

1

500-235
| NIST | Special | Publication |     |
| ---- | ------- | ----------- | --- |
A
| Structured | Testing:       | Testing    | Methodology |
| ---------- | -------------- | ---------- | ----------- |
| Using      | the Cyciomatic | Complexity | Metric      |
Dolores
|          | R. Wallace, Editor |     |     |
| -------- | ------------------ | --- | --- |
| Computer | Systems            |     |     |
Laboratory
| National | Institute of Standards | and Technology |     |
| -------- | ---------------------- | -------------- | --- |
MD
| Gaithersburg, | 20899-0001 |     |     |
| ------------- | ---------- | --- | --- |
| Arthur H.     | Watson     |     |     |
| Thomas        | McCabe     |     |     |
J.
| McCabe | &   |     |     |
| ------ | --- | --- | --- |
Associates
MD
| Columbia,     | 21045        |     |     |
| ------------- | ------------ | --- | --- |
| NIST Contract | 43NANB517266 |     |     |
August 1996
| Department         | Commerce        |                |     |
| ------------------ | --------------- | -------------- | --- |
| U.S.               | of              |                |     |
| Michael Kantor,    | Secretary       |                |     |
| Technology         | Administration  |                |     |
| Mary L. Good,      | Under Secretary | for Technology |     |
|                    | ofStandards     | and Technology |     |
| National Institute |                 |                |     |
| Arati Prabhakar.   | Director        |                |     |

|     |     | Reports |     | on Computer |     | Systems | Technology |     |     |     |     |
| --- | --- | ------- | --- | ----------- | --- | ------- | ---------- | --- | --- | --- | --- |
| The |     |         |     | and         |     |         |            |     |     |     |     |
National Institute of Standards Technology (NIST) has a unique responsibility for computer
systems technology within the Federal government. NIST's Computer Systems Laboratory (CSL) devel-
ops standards and provides and conducts research computers and
|     | guidelines, |     |     | technical |     | assistance, |     |     | for |     |     |
| --- | ----------- | --- | --- | --------- | --- | ----------- | --- | --- | --- | --- | --- |
related telecommunications systems to achieve more effective utilization of Federal information technol-
ogy resources. CSL's responsibilities include development of technical, management, physical, and ad-
and
ministrative standards guidelines for the cost-effective security and privacy of sensitive unclassified
information processed in Federal computers. CSL assists agencies in developing security plans and in
| improving computer |     |          | awareness |           |     | This Special |             | 500    |         | CSL |     |
| ------------------ | --- | -------- | --------- | --------- | --- | ------------ | ----------- | ------ | ------- | --- | --- |
|                    |     | security |           | training. |     |              | Publication | series | reports |     | re- |
search and guidelines to Federal agencies as well as to organizations in industry, government, and
academia.
National Institute of Standards and Technology Special Publication 500-235
|       | Stand. |     | Technol.   | Spec.  | Publ. | 500-235, | 119    | pages (August |     | 1996) |     |
| ----- | ------ | --- | ---------- | ------ | ----- | -------- | ------ | ------------- | --- | ----- | --- |
| Natl. | Inst.  |     |            |        |       |          |        |               |     |       |     |
|       |        |     |            | CODEN: |       | NSPUE2   |        |               |     |       |     |
|       |        |     | GOVERNMENT |        |       |          | OFFICE |               |     |       |     |
|       |        |     | U.S.       |        |       | PRINTING |        |               |     |       |     |
WASHINGTON:
1996
| For     |                    |     | Documents, |     |      | Government |          | Washington, |     | DC  | 20402 |
| ------- | ------------------ | --- | ---------- | --- | ---- | ---------- | -------- | ----------- | --- | --- | ----- |
| sale by | the Superintendent |     | of         |     | U.S. |            | Printing | Office,     |     |     |       |

Abstract
The purpose ofthis document is to describe the structured testing methodology for software
testing, also known as basis path testing. Based on the cyclomatic complexity measure of
McCabe, structured testing uses the control flow structure ofsoftware to establish path cover-
age criteria. The resultant test sets provide more thorough testing than statement and branch
coverage. Extensions ofthe fundamental structured testing techniques for integration testing
and object-oriented systems are also presented. Several related software complexity metrics
are described. Summaries oftechnical papers, case studies, andempirical results are presented
in the appendices.
Keywords
Basis path testing, cyclomatic complexity, McCabe, object oriented, software development,
software diagnostic, software metrics, software testing, structured testing
Acknowledgments
The authors acknowledge the contributions by Patricia McQuaid to Appendix A ofthis report.
Disclaimer
Certaintrade names andcompanynames are mentionedin thetextoridentified. In no case
does such identification imply recommendation orendorsementby the National Institute
ofStandards and Technology, nor does it imply that theproducts are necessarily the best
available for the purpose.
iii

| Executive |     | Summary |     |     |     |     |
| --------- | --- | ------- | --- | --- | --- | --- |
This document describes the structured methodology software and
|     |     |     | testing | for | testing | related |
| --- | --- | --- | ------- | --- | ------- | ------- |
software complexity analysis techniques. The key requirement ofstructured testing that
is all
decision outcomes must be exercised independently during testing. The number oftests
required for a software module is equal to the cyclomatic complexity ofthat module. The
|     |     | document | [NBS99] |     |     |     |
| --- | --- | -------- | ------- | --- | --- | --- |
original structured testing discusses cyclomatic complexity and the basic
technique. This document gives an expanded and updated presentation ofthose
| testing |     |     |     |     |     | topics, |
| ------- | --- | --- | --- | --- | --- | ------- |
describes several new complexity measures and testing strategies, and presents the experience
| gained through | the practical | application | ofthese | techniques. |     |     |
| -------------- | ------------- | ----------- | ------- | ----------- | --- | --- |
| The            |               | measures    |         | document    |     |     |
software complexity described in this are: cyclomatic complexity,
module design complexity, integration complexity, object complexity, com-
|     |     |     |     | integration |     | actual |
| --- | --- | --- | --- | ----------- | --- | ------ |
plexity, realizable complexity, essential complexity, and data complexity. The testing tech-
niques are described for module testing, integration testing, and object-oriented testing.
| A   | amount |     |     | concerning |     |     |
| --- | ------ | --- | --- | ---------- | --- | --- |
significant ofpractical advice is given the application ofthese tech-
niques. The use ofcomplexity measurement manage software and maintainabil-
|     |     |     | to  | reliability |     |     |
| --- | --- | --- | --- | ----------- | --- | --- |
ity discussed, along with strategies to control complexity during maintenance. Methods to
is
apply the testing techniques are also covered. Both manual techniques and the use ofauto-
| mated support | are described. |     |     |     |     |     |
| ------------- | -------------- | --- | --- | --- | --- | --- |
Many detailed examples ofthe techniques are given, as well as summaries oftechnical papers
and case studies. Experimental results are given showing that structured testing superior to
is
statement and branch coverage testing for detecting errors. The bibliography lists over 50 ref-
| erences to | related information. |     |     |     |     |     |
| ---------- | -------------------- | --- | --- | --- | --- | --- |
V

f
I
!
i

CONTENTS
Abstract
iii
Keywords
iii
Acknowledgments
iii
| Executive Summary |     |     |     |     |     |     |     |
| ----------------- | --- | --- | --- | --- | --- | --- | --- |
v
Introduction
| 1   |                  |            |          |                          |             |     | 1   |
| --- | ---------------- | ---------- | -------- | ------------------------ | ----------- | --- | --- |
|     | 1.1 Software     | testing    |          |                          |             |     | 1   |
|     | 1.2 Software     | complexity |          | measurement              |             |     | 2   |
|     | 1.3 Relationship |            | between  | complexity               | and testing |     | 3   |
|     | Document         |            | overview | and audiencedescriptions |             |     | 4   |
1.4
| 2   | Cyclomatic             |              | Complexity |             |                |       | 7   |
| --- | ---------------------- | ------------ | ---------- | ----------- | -------------- | ----- | --- |
|     | 2.1 Control            | flow         | graphs     |             |                |       | 7   |
|     | 2.2 Definition         | ofcyclomatic |            | complexity, | v(G)           |       | 10  |
|     |                        |              | ofv(G)     | using       | ofcontrol flow |       |     |
|     | 2.3 Characterization   |              |            |             | abasis set     | paths | 11  |
|     | 2.4 Example            | ofv(G)       | and        | basis paths |                |       | 13  |
|     | 2.5 Limitingcyclomatic |              |            | complexity  | to 10          |       | 15  |
Examples
| 3   |              |             | of Cyclomatic |                     | Complexity  |     | 17    |
| --- | ------------ | ----------- | ------------- | ------------------- | ----------- | --- | ----- |
|     | Independence |             | ofcomplexity  |                     | and         |     |       |
|     | 3.1          |             |               |                     | size        |     | ...17 |
|     | 3.2 Several  | flow        | graphs        | and theircomplexity |             |     | 17    |
| 4   | Simplified   |             | Complexity    |                     | Calculation |     | 23    |
|     | 4.1 Counting | predicates  |               |                     |             |     | 23    |
|     | Counting     | flow        | graph         |                     |             |     | 28    |
|     | 4.2          |             |               | regions             |             |     |       |
|     | 4.3 Use      | ofautomated | tools         |                     |             |     | 29    |
| 5   | Structured   |             | Testing       |                     |             |     | 31    |
The
|     | 5.1       | structured | testing    | criterion |     |     | 31  |
| --- | --------- | ---------- | ---------- | --------- | --- | --- | --- |
|     | 5.2       | behind     | structured |           |     |     | 32  |
|     | Intuition |            |            | testing   |     |     |     |
vii

|     |     | Complexity     |            | and         |         |     |     | 34  |
| --- | --- | -------------- | ---------- | ----------- | ------- | --- | --- | --- |
|     |     | 5.3            |            | reliability |         |     |     |     |
|     |     | 5.4 Structured | testing    |             | example |     |     | 34  |
|     | '   | 5.5 Weak       | structured | testing     |         |     |     | 37  |
l i' J
|     |     | 5.6 Advantages     |          | ofautomation |             |     |     | 38  |
| --- | --- | ------------------ | -------- | ------------ | ----------- | --- | --- | --- |
|     |     | 5.7 Critical       | software |              |             |     |     | 39  |
| 6   |     | The Baseline       |          |              | Method      |     |     | 41  |
|     |     | 6.1 Generating     |          | abasis       | set ofpaths |     |     | 41  |
|     |     | 6.2 The simplified |          | baseline     | method      |     |     | 41  |
The
|     |     | 6.3 baseline |     | method | in practice |     |     | 42  |
| --- | --- | ------------ | --- | ------ | ----------- | --- | --- | --- |
,
|     |     | Example         |                 |             | method            |             |         | 44  |
| --- | --- | --------------- | --------------- | ----------- | ----------------- | ----------- | ------- | --- |
|     |     | 6.4             | ofthe           | baseline    |                   |             |         |     |
|     |     | 6.5 Completing  |                 | testing     | with the baseline | method      |         | 46  |
| 7   |     | Integration     |                 | Testing     |                   |             |         | 47  |
|     |     | 7.1 Integration |                 | strategies  |                   |             |         | 47  |
|     |     | Combining       |                 | module      |                   |             |         | 48  |
|     |     | 7.2             |                 |             | testing and       | integration | testing |     |
|     |     | Generalization  |                 | ofmodule    |                   |             |         | 49  |
|     |     | 7.3             |                 |             | testing           | criteria    |         |     |
|     |     | 7.4 Module      | design          | complexity  |                   |             |         | 50  |
| *   |     | 7.5 Integration |                 | complexity  |                   |             |         | 54  |
|     |     | 7.6 Incremental |                 | integration |                   |             |         | 57  |
|     |     |                 |                 |             |                   | Programs    |         | 59  |
| 8   |     | Testing         | Object-Oriented |             |                   |             |         |     |
|     |     | Benefits        | and             | dangers     | ofabstraction     |             |         | 59  |
8.1
|     |     | 8.2 Object-oriented |     | module  | testing           |          |     | 60  |
| --- | --- | ------------------- | --- | ------- | ----------------- | -------- | --- | --- |
| '   |     | 8.3 Integration     |     | testing | ofobject-oriented | programs |     | 61  |
.
|     |     | 8.4 Avoiding    | unnecessary |             | testing        |                 |     | 65  |
| --- | --- | --------------- | ----------- | ----------- | -------------- | --------------- | --- | --- |
| 9   |     | Complexity      |             | Reduction   |                |                 |     | 67  |
|     |     | 9.1 Actual      | complexity  |             | and realizable | complexity      |     | 67  |
|     |     | 9.2 Removing    | control     |             | dependencies   |                 |     | 71  |
|     |     | 9.3 Trade-offs  | when        | reducing    | complexity     |                 |     | 74  |
| 10  |     | Essential       |             | Complexity  |                |                 |     | 79  |
|     |     | 10.1 Structured |             | programming | and            | maintainability |     | 79  |
'
|     |     | 10.2 Definition |     | ofessential | complexity, | ev(G). |     | 80  |
| --- | --- | --------------- | --- | ----------- | ----------- | ------ | --- | --- |
|     |     | 10.3 Examples   |     | ofessential | complexity  |        |     | 81  |

Maintenance
| 11  |            |                                  |                                       |         |            | 83  |
| --- | ---------- | -------------------------------- | ------------------------------------- | ------- | ---------- | --- |
|     | 11.1       | Effects ofchanges                | on complexity                         |         |            | 83  |
|     |            | 11.1.1                           | Effectofchangesoncyclomaticcomplexity |         |            | 83  |
|     |            | 11.1.2Effectofchangesonessential |                                       |         | complexity | 83  |
|     |            | 11.1.3                           | Incremental reengineering             |         |            | 84  |
|     | 11.2       | Retesting                        | at thepath level                      |         |            | 85  |
|     | 11.3       | Datacomplexity                   |                                       |         |            | 85  |
|     | 11.4 Reuse | oftesting                        | information                           |         |            | 86  |
| 12  | Summary    |                                  | by                                    | Process |            | 87  |
Lifecycle
|     | 12.1 Designprocess |                |                 |     |     | 87  |
| --- | ------------------ | -------------- | --------------- | --- | --- | --- |
|     | 12.2 Coding        | process        |                 |     |     | 87  |
|     | 12.3 Unit          | testingprocess |                 |     |     | 87  |
|     | 12.4 Integration   |                | testing process |     |     | 87  |
|     | 12.5 Maintenance   |                | process         |     |     | 88  |
| 13  | References         |                |                 |     |     | 89  |
A
| Appendix | Related          | Case | Studies     |     |     | 95  |
| -------- | ---------------- | ---- | ----------- | --- | --- | --- |
|          | A.l Myers        |      |             |     |     | 95  |
|          | A.2 Schneidewind |      | and Hoffman |     |     | 95  |
A.3 Walsh
96
|     | A.4 Henry,      | Kafura, | and Harris |     |     | 96  |
| --- | --------------- | ------- | ---------- | --- | --- | --- |
|     | A.5 Sheppard    | and     | Kruesi     |     |     | 96  |
|     | A.6Carver       |         |            |     |     | 97  |
|     | A.7 Kafura      | and     | Reddy      |     |     | 97  |
|     | A.8 Gibson      | and     | Senn       |     |     | 98  |
|     | A.9Ward         |         |            |     |     | 99  |
|     | A.lOCaldieraand |         |            |     |     | 99  |
Basili
|     | A.11 | Gill andKemerer |     |     |     | 99  |
| --- | ---- | --------------- | --- | --- | --- | --- |
|     | A.12 | Schneidewind    |     |     |     | 100 |
Computer
|     | A.13 | Case study | at Stratus                      |                |     | 101 |
| --- | ---- | ---------- | ------------------------------- | -------------- | --- | --- |
|     | A.14 | Case study | at Digital EquipmentCorporation |                |     | 101 |
|     | A.15 | Case study | U.S. Army                       | MissileCommand |     | 102 |
at
|     | A.16 | Coleman | etal |     |     | 102 |
| --- | ---- | ------- | ---- | --- | --- | --- |
A.17 Case study at the AT&TAdvanced SoftwareConstruction Center 103
|     |      | Case  |             |          |     | 103 |
| --- | ---- | ----- | ----------- | -------- | --- | --- |
|     | A.18 | study | at Sterling | Software |     |     |
GTEGovernment
|     | A.19     | Case Study | at             |         | Systems    | 103 |
| --- | -------- | ---------- | -------------- | ------- | ---------- | --- |
|     | A.20Case | study      | atElsag Bailey | Process | Automation | 103 |
04
|     | A.21 | Koshgoftaaret | al  |     |     | 1   |
| --- | ---- | ------------- | --- | --- | --- | --- |
ix

| Appendix | B Extended     | Example          | 105 |
| -------- | -------------- | ---------------- | --- |
|          | B.l Testingthe | blackjackprogram | 105 |
B.2Experimental comparison ofstructured testing and branch coverage 112

1 Introduction
Software
| 1.1 |     | testing |     |     |     |     |     |     |     |     |     |
| --- | --- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
This document describes the structured testing methodology for software Software
testing.
testing is the process ofexecuting software and comparing the observed behavior to the
desired behavior. The major goal ofsoftware testing is to discover errors in the software
[MYERS2],
with a secondary goal ofbuilding confidence in the proper operation ofthe soft-
| ware | when | does    | not discover |         | The |          | between |       | two   |             |     |
| ---- | ---- | ------- | ------------ | ------- | --- | -------- | ------- | ----- | ----- | ----------- | --- |
|      |      | testing |              | errors. |     | conflict |         | these | goals | is apparent |     |
when considering atesting process that did not detect any In the absence ofother
errors.
information, this could mean either that the software high quality or that the testing process
is
is low quality. There are many approaches to software testing that attempt to control the qual-
ity ofthe testing process to yield useful information about the quality ofthe software being
tested.
Although most testing research concentrated on finding effective testing techniques,
|     |     |     |     | is  |     |     |     |     |     |     | it is |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- |
also important to make software that can be effectively tested. It is suggested in [VOAS] that
software is testable iffaults are likely to cause failure, since then those faults are most likely to
| be  |     | by  |     |     | programming |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | ----------- | --- | --- | --- | --- | --- | --- |
detected failure during testing. Several techniques are suggested to raise
such as minimizing variable reuse and maximizing output parameters. [BER-
| testability, |     |     |     |     |     |     |     |     |     | In  |     |
| ------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
TOLINO] noted that although having faults cause failure good during testing, bad
|     |     | it is |     |     |     |     | is  |     |     | it  | is  |
| --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
after delivery. For a more intuitive testability property, it is best to maximize the probability
offaults being detected during testing while minimizing the probability offaults causing fail-
programming
ure after delivery. Several techniques are suggested to raise testability, includ-
ing assertions observe the internal ofthe software during but do not the
|     |     | that |     | state |     |     |     | testing |     | affect |     |
| --- | --- | ---- | --- | ----- | --- | --- | --- | ------- | --- | ------ | --- |
specifiedoutput, andmultiple version development [BRILLIANT] in which any disagreement
between versions can be reported during testing but a majority voting mechanism helps
reduce the likelihood ofincorrect output after delivery. Since both ofthose techniques are fre-
|     | used |     |     | systems |     |     |     |     |     | may |     |
| --- | ---- | --- | --- | ------- | --- | --- | --- | --- | --- | --- | --- |
quently to help construct reliable in practice, this version oftestability cap-
| ture | a significant | factor | software | development. |     |     |     |     |     |     |     |
| ---- | ------------- | ------ | -------- | ------------ | --- | --- | --- | --- | --- | --- | --- |
in
Forlarge systems, many errors are often found atthebeginningofthe testingprocess, with the
When
observed error rate decreasing as errors are fixed in the software. the observed error
used determine
rate during testing approaches zero, statistical techniques are often to areason-
|      |       |                 | [MUSA]. | This | approach | has | two significant |     | weaknesses. |        | the |
| ---- | ----- | --------------- | ------- | ---- | -------- | --- | --------------- | --- | ----------- | ------ | --- |
| able | point | to stop testing |         |      |          |     |                 |     |             | First, |     |
testing effort cannot be predicted in advance, since a function ofthe intermediate results
|     |     |     |     |     |     | it  | is  |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
A
ofthe testing effort itself. related problem is that the testing schedule can expire long
more
before the error rate drops to an acceptable level. Second, and perhaps importantly, the
|     |     | model |     |     |     |     | underlying |     | case |     |     |
| --- | --- | ----- | --- | --- | --- | --- | ---------- | --- | ---- | --- | --- |
statistical only predicts the estimated error rate for the test distribution
1

being used during the testing process. It may have little or no connection to the likelihood of
errors manifesting once the system is delivered or to the total number oferrors present in the
software.
Another common approach to testing is based on requirements analysis. A requirements specifi-
cation is converted into test cases, which are then executed so that testing verifies system behav-
ior for at least one test case within the scope ofeach requirement. Although this approach is an
important part ofa comprehensive testing effort, it is certainly not a complete solution. Even
setting aside the fact that requirements documents are notoriously error-prone, requirements are
written at a much higher level ofabstraction than code. This means that there is much more
detail in the code than the requirement, so a test case developed from a requirement tends to
exercise only a small fraction ofthe software that implements that requirement. Testing only at
the requirements level may miss many sources oferror in the software itself.
The structured testing methodology falls into anothercategory, the white box (orcode-based, or
glass box) testing approach. In white box testing, the software implementation itselfis used to
guide testing. A common white box testing criterion is to execute every executable statement
during testing, and verify that the output is correct for all tests. In the more rigorous branch cov-
erage approach, every decision outcome must be executed during testing. Structured testing is
still more rigorous, requiring that each decision outcome be tested independently. A fundamen-
tal strength that all white box testing strategies share is that the entire software implementation
is taken into account during testing, which facilitates error detection even when the software
A
specification is vague or incomplete. corresponding weakness is that ifthe software does not
implement one or more requirements, white box testing may not detect the resultant errors of
omission. Therefore, both white box and requirements-based testing are important to an effec-
tive testing process. The rest ofthis document deals exclusively with white box testing, concen-
trating on the structured testing methodology.
1.2 Software complexity measurement
Software complexity is one branch ofsoftware metrics that is focused on direct measurement of
software attributes, as opposed to indirect software measures such as project milestone status
and reported system failures. There are hundreds ofsoftware complexity measures [ZUSE],
ranging from the simple, such as source lines ofcode, to the esoteric, such as the number of
variable definition/usage associations.
An important criterion for metrics selection is uniformity ofapplication, also known as "open
reengineering." The reason "open systems" are so popular for commercial software applica-
—
tions is that the user is guaranteed a certain level ofinteroperability the applications work
together in a common framework, and applications can be ported across hardware platforms
with minimal impact. The open reengineering concept is similar in that the abstract models
2

used to represent software systems should be as independent as possible ofimplementation
characteristics such as source code formatting and programming language. The objective is to
be able to set complexity standards and interpret the resultant numbers uniformly across
projects and languages. A particularcomplexity value should mean the same thing whether it
was calculated from source code written in Ada, C, FORTRAN, or some other language. The
most basic complexity measure, the number of lines ofcode, does not meet the open reengi-
neering criterion, since it is extremely sensitive to programming language, coding style, and
textual formatting ofthe source code. The cyclomatic complexity measure, which measures
the amount ofdecision logic in a source code function, does meet the open reengineering cri-
terion. It is completely independent oftext formatting and is nearly independent ofprogram-
ming language since the same fundamental decision structures are available and uniformly
used in all procedural programming languages [MCCABE5].
Ideally, complexity measures should have both descriptive and prescriptive components.
Descriptive measures identify software that is error-prone, hard to understand, hard to modify,
hard to test, and so on. Prescriptive measures identify operational steps to help control soft-
ware, for example splitting complex modules into several simpler ones, or indicating the
amount oftesting that should be performed on given modules.
1.3 Relationship between complexity and testing
There is a strong connection between complexity and testing, and the structured testing meth-
odology makes this connection explicit.
First, complexity is a common source oferror in software. This is true in both an abstract and
aconcrete sense. In the abstract sense, complexity beyond a certain point defeats the human
mind's ability to perform accurate symbolic manipulations, and errors result. The same psy-
chological factors that limit people's ability to do mental manipulations ofmore than the infa-
mous "7 +/- 2" objects simultaneously [MILLER] apply to software. Structuredprogramming
techniques can push this barrier further away, but not eliminate it entirely. In the concrete
sense, numerous studies and general industry experience have shown that the cyclomatic com-
plexity measure correlates with errors in software modules. Other factors being equal, the
more complex a module is, the more likely it is to contain errors. Also, beyond a certain
thresholdofcomplexity, the likelihoodthat amodule contains errors increases sharply. Given
this information, many organizations limit the cyclomatic complexity oftheir software mod-
ules in an attempt to increase overall reliability. A detailed recommendation for complexity
limitation is given in section 2.5.
Second, complexity can beused directly to allocate testingeffortby leveragingthe connection
between complexity and error to concentrate testing effort on t — he most error-prone software.
In the structured testing methodology, this allocation is precise the number oftest paths
3

required for each software module exactly the cyclomatic complexity. Other common
is
white box testing criteria have the inherent anomaly that they can be satisfied with a small
number oftests for arbitrarily complex (by any reasonable sense of"complexity") software as
shown
|     |          | in section | 5.2. |          |     |              |     |              |     |     |     |     |
| --- | -------- | ---------- | ---- | -------- | --- | ------------ | --- | ------------ | --- | --- | --- | --- |
|     | Document |            |      | overview |     | and audience |     |              |     |     |     |     |
| 1.4 |          |            |      |          |     |              |     | descriptions |     |     |     |     |
Section gives an overview ofthis document. also gives some general information about
| •   |     | 1   |     |     |     |     |     | It  |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
software testing, software complexity measurement, and the relationship between the two.
• Section 2 describes the cyclomatic complexity measure for software, which provides the
|     | foundation |     | for structured |     | testing. |     |     |     |     |     |     |     |
| --- | ---------- | --- | -------------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- |
• Section 3 gives some examples ofboth the applications and the calculation ofcyclomatic
complexity.
4
• Section describes several practical shortcuts for calculating cyclomatic complexity.
• Section 5 defines structured testing and gives a detailed example ofits application.
• Section 6 describes the Baseline Method, a systematic technique forgenerating a set oftest
|     | paths   | that        | satisfy | structured |     | testing. |     |             |        |     |     |     |
| --- | ------- | ----------- | ------- | ---------- | --- | -------- | --- | ----------- | ------ | --- | --- | --- |
|     | Section | 7 describes |         | structured |     | testing  | the | integration | level. |     |     |     |
| •   |         |             |         |            |     |          | at  |             |        |     |     |     |
• Section 8 describes structured testing for object-oriented programs.
|     | Section    | 9         |             | techniques |     |                 |     | and | removing | unnecessary | complexity | and |
| --- | ---------- | --------- | ----------- | ---------- | --- | --------------- | --- | --- | -------- | ----------- | ---------- | --- |
| •   |            | discusses |             |            |     | for identifying |     |     |          |             |            |     |
|     | the impact |           | on testing. |            |     |                 |     |     |          |             |            |     |
• Section 10 describes the essential complexity measure for software, which quantifies the
|     | extent | to which |     | software | is  | poorly structured. |     |     |     |     |     |     |
| --- | ------ | -------- | --- | -------- | --- | ------------------ | --- | --- | --- | --- | --- | --- |
Section discusses software modification, and how apply structured pro-
| •   |       | 1 1    |              |     |     |     |     |     | to  |     | testing to |     |
| --- | ----- | ------ | ------------ | --- | --- | --- | --- | --- | --- | --- | ---------- | --- |
|     | grams | during | maintenance. |     |     |     |     |     |     |     |            |     |
• Section 12 summarizes this document by software lifecycle phase, showing where each
|     | technique |     | fits into | the | overall | development |     | process. |     |     |     |     |
| --- | --------- | --- | --------- | --- | ------- | ----------- | --- | -------- | --- | --- | --- | --- |
A
|     | Appendix |     | describes |     | several | related | case | studies. |     |     |     |     |
| --- | -------- | --- | --------- | --- | ------- | ------- | ---- | -------- | --- | --- | --- | --- |
•
B
• Appendix presents an extended example ofstructured testing. It also describes an exper-
|     |     |     |     | comparing |     |     |     |     |     | and |     |     |
| --- | --- | --- | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
imental design for structural testing strategies, applies that design to illus-
|     |       |                 |     | of  | structured |         | over | branch | coverage. |     |     |     |
| --- | ----- | --------------- | --- | --- | ---------- | ------- | ---- | ------ | --------- | --- | --- | --- |
|     | trate | the superiority |     |     |            | testing |      |        |           |     |     |     |

| Figure | 1-1 shows | the dependencies |     | among | the | sections. |     |     |     |     |
| ------ | --------- | ---------------- | --- | ----- | --- | --------- | --- | --- | --- | --- |
|        |           |                  |     |       |     | first 1 1 |     |     |     |     |
8. Object-Oriented
amongsections
|     | Figure1-1. | Dependencies |     |     |     | 1-11. |     |     |     |     |
| --- | ---------- | ------------ | --- | --- | --- | ----- | --- | --- | --- | --- |
Readers with different interests may concentrate on specific areas ofthis document and skip
or skim the others. Sections 2, 5, and 7 form the primary material, presenting the core struc-
|     | method. | The |     |     |     | can be | on  |     | by  |     |
| --- | ------- | --- | --- | --- | --- | ------ | --- | --- | --- | --- |
tured testing mathematical content skipped afirst reading or read-
primarily interested appUcations. Sections 4 and 6 concentrate on manual
| ers |     | in  | practical |     |     |     |     |     |     |     |
| --- | --- | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
techniques, and are therefore ofmost interest to readers without access to automated tools.
Readers working with object-oriented systems should read section 8. Readers familiar with
NBS
the original structured testing document [NBS991 should concentrate on the updated
|          |            | and | new |          |     | and           |     |     |     |     |
| -------- | ---------- | --- | --- | -------- | --- | ------------- | --- | --- | --- | --- |
| material | in section | 5   | the | material | in  | sections 7 8. |     |     |     |     |
Programmerswho arenotdirectly involvedintestingmayconcentrate on sections 1-4 and 10.
These sections describe how to limit and control complexity, to help produce more testable,
reliable, and maintainable software, without going into details about the testing technique.
Testers may concentrate on and 5-8. These sections give the information
|     |     |     | sections | 1,  | 2,  |     |     | all |     |     |
| --- | --- | --- | -------- | --- | --- | --- | --- | --- | --- | --- |
necessary to apply the structured testing methodology with or without automated tools.
|     | who |     |     |     |     |     | may |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Maintainers are not directly involved in the testing process concentrate on sections
| and   | These |          |          |     | how | keep maintenance | changes | from | degrading |     |
| ----- | ----- | -------- | -------- | --- | --- | ---------------- | ------- | ---- | --------- | --- |
| 1, 2, | 9-11. | sections | describe |     | to  |                  |         |      |           | the |
5

testability, reliability, and maintainability ofsoftware, without going into details about the
testing technique.
ProjectLeaders andManagers should read through the entire document, but may skim over
the details in sections 2 and 5-8.
QualityAssurance, Methodology, and Standards professionals may skim the material in sec-
tions 1, 2, and 5 to get an overview ofthe method, then read section 12 to see where it fits into
the software lifecycle. The Appendices also provide important information about experience
with the method and implementation details for specific languages.

| 2   | Cyclomatic |     |     | Complexity |     |     |     |     |     |     |     |     |
| --- | ---------- | --- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
[MCCABEl]
Cyclomatic complexity measures the amount ofdecision logic in a single soft-
| ware module. |     | used | two |     |     |     |     |     |     |     |     |     |
| ------------ | --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
It is for related purposes in the structured testing methodology. First,
| gives | the numberofrecommended |     |     |       |     |           | Second, |       | used |        |            |     |
| ----- | ----------------------- | --- | --- | ----- | --- | --------- | ------- | ----- | ---- | ------ | ---------- | --- |
| it    |                         |     |     | tests | for | softwaie. |         | it is |      | during | all phases | of  |
the software lifecycle, beginning with design, to keep software and manage-
|     |     |     |     |     |     |     |     | reliable, |     | testable, |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --------- | --- | --------- | --- | --- |
able. Cyclomatic complexity is based entirely on the structure ofsoftware's control flow
graph.
| Controlflow |     | graphs |     |     |     |     |     |     |     |     |     |     |
| ----------- | --- | ------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
2.1
| Control | flow graphs | describe |     |           |           | of software | modules. |     | A   | module |             |     |
| ------- | ----------- | -------- | --- | --------- | --------- | ----------- | -------- | --- | --- | ------ | ----------- | --- |
|         |             |          |     | the logic | structure |             |          |     |     |        | corresponds |     |
to a single function or subroutine typical languages, has a single entry and and
|     |     |     |     | in  |     |     |     |     |     | exit | point, | is  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | ------ | --- |
able to be used as a design component via acall/return mechanism. This document uses C as
C
the language for examples, and in a module is a function. Each flow graph consists of
The
nodes andedges. nodes representcomputational statements orexpressions, andthe edges
|           |          | ofcontrol | between |        |     |     |     |     |     |     |     |     |
| --------- | -------- | --------- | ------- | ------ | --- | --- | --- | --- | --- | --- | --- | --- |
| represent | transfer |           |         | nodes. |     |     |     |     |     |     |     |     |
Each possible execution path ofa software module has acorresponding path from the entry to
the exit node ofthe module's control flow graph. This correspondence is the foundation for
| the structured | testing | methodology. |     |     |     |     |     |     |     |     |     |     |
| -------------- | ------- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
As an example, consider the C function in Figure 2-1, which implements Euclid's algorithm
|     |     |     |     |     |     |     |     | AO  |     | A   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
forfinding greatest common divisors. The nodes are numbered through 13. The control
flow graph is shown in Figure 2-2, in which each node is numbered 0 through 13 and edges
| shown |     |     |     |     | Node |     |     |     |     |     |     |     |
| ----- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- |
are by lines connecting the nodes. 1 thus represents the decision ofthe "if state-
| ment with |          | outcome |     | node 2 | and | outcome |     |                |     | node | The |       |
| --------- | -------- | ------- | --- | ------ | --- | ------- | --- | -------------- | --- | ---- | --- | ----- |
|           | the true |         | at  |        | the | false   | at  | the collection |     |      | 5.  | deci- |
sion ofthe "while" loop represented by node and the upward flow ofcontrol to the next
|     |     |     | is  |     |     | 7,  |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
iteration shown by the dashed line from node 10 to node 7. Figure 2-3 shows the path
is
resulting when the module is executed with parameters4 and2, as in "euclid(4,2)." Execution
|     |     |     |     |     |     |     |     | node |     |     | node |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | ---- | --- |
begins at node 0, the beginning ofthe module, and proceeds to 1, the decision for
| "if |     | Since |     | node |     | execution |     |     |     |     | node | the |
| --- | --- | ----- | --- | ---- | --- | --------- | --- | --- | --- | --- | ---- | --- |
the statement. the test at 1 is false, transfers directly to 5,
node ofthe "if statement, and proceeds to node At node the value of"r"
| collection |     |     |     |     |     |     | 6.  |     | 6,  |     |     | is  |
| ---------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
calculated to be 0, and execution proceeds to node 7, the decision node for the "while" state-
ment. Since the test at node 7 is false, execution transfers out ofthe loop directly to node 11,
7

then proceeds to node 12, returning the result of2. The actual return modeled by execution
is
| proceeding | to node | 13, the module | exit | node. |     |     |     |     |     |
| ---------- | ------- | -------------- | ---- | ----- | --- | --- | --- | --- | --- |
[Convert] jciose] pHelp]
Prifitl fSavej
|     |               |          |            | Annotated    | Source Listing |             |          |            |        |
| --- | ------------- | -------- | ---------- | ------------ | -------------- | ----------- | -------- | ---------- | ------ |
|     | Program       | Euclid   |            |              |                |             |          | 01/15/96   |        |
|     | File          | euclid.c |            |              |                |             |          |            |        |
|     | Language      | instc    |            |              |                |             |          |            |        |
|     | Module Module |          |            |              |                |             |          | Start      | Num of |
|     | Letter Name   |          |            |              |                | v(G)        | ev(G)    | iv(G) Line | Lines  |
|     | A euclid      |          |            |              |                | 3           | 1        | 1          | 19     |
|     |               | AO       | euclid(int |              |                |             |          |            |        |
|     | 2             |          |            | m,           | int n)         |             |          |            |        |
|     | 3             |          | (/*        | Assuming     | m and n both   | greater     | than     | 0,         |        |
|     | 4             |          | *          | return their | greatest       | common      | divisor. |            |        |
|     |               |          |            | Enforce      | m >= n for     | efficiency. |          |            |        |
|     | 5             |          | *          |              |                |             |          |            |        |
|     | 6             |          | */         |              |                |             |          |            |        |
|     | 7             |          |            | int r;       |                |             |          |            |        |
|     | 8             | A l      |            | if (n >      | m ) {          |             |          |            |        |
|     | 9             | A 2      |            | r -          | m;             |             |          |            |        |
|     | 10            | A3       |            | m -          | n;             |             |          |            |        |
|     | 11            | A4       |            | n =          | r;             |             |          |            |        |
12
|     | 13  | A5 A6 |     | r) = m % | n; /*     | m modulo | n   | */  |     |
| --- | --- | ----- | --- | -------- | --------- | -------- | --- | --- | --- |
|     | 1 4 | A 7   |     | while (r | != 0)     |          |     |     |     |
|     | 1 5 | A 8   |     | m =      | n; {      |          |     |     |     |
|     |     | A9    |     | n =      |           |          |     |     |     |
|     | 16  |       |     |          | r;        |          |     |     |     |
|     | 17  | AlO   |     | r =      | m % n; /* | m modulo | n   | */  |     |
|     | 18  | All   |     |          |           |          |     |     |     |
|     |     | A12   |     | r}eturn  |           |          |     |     |     |
|     | 19  |       |     | n;       |           |          |     |     |     |
|     | 20  | A13   |     |          |           |          |     |     |     |
)
Figure2-1. Annotatedsourcelistingformodule"euclid."
8

|     | Plotj[Savel | [convert] jiorwd] jiackuardl | [Enlarge] [Reduce |
| --- | ----------- | ---------------------------- | ----------------- |
| fciosel [ttelp]
|     | Page 1 of 1 | 2X  |     |
| --- | ----------- | --- | --- |
.12 |     | Figure2-2. | Controlflow graphformodule"euclid." |     |
| --- | ---------- | ----------------------------------- | --- |
<punEuclM
i
| {Print| [Save | (pjnuert jciose] jhlelpj |     |     |
| ------------- | ------------------------ | --- | --- |
[ |
|         |        | Cyclomatic Test | Paths Listing |
| ------- | ------ | --------------- | ------------- |
| Program | Euclid |                 | 01/15/96      |
e:uclid
Module:
|     | User | Specified Cyclomatic | Test Path: Path |
| --- | ---- | -------------------- | --------------- |
1
| Test Path | 1:01 2 3 4 | 5 6 7 8 9 10 7 | 8 9 10 7 11 12 13 |
| --------- | ---------- | -------------- | ----------------- |
|           | n>m =—=>   | TRUE           |                   |
8( 1)
|     | 14( 7) r!=0 | —> TRUE   |     |
| --- | ----------- | --------- | --- |
|     | 14( 7) r!=0 | > TRUE    |     |
|     | r!=0        | ==> FALSE |     |
14( 7)
=
W-F^^
A
| Figure2-3. | testpath through | module"eucUd." |     |
| ---------- | ---------------- | -------------- | --- |

2.2 Definition ofcyclomatic complexity, v(G)
Cyclomatic complexity is defined for each module to be e - n + 2, where e and n are the num-
ber ofedges and nodes in the control flow graph, respectively. Thus, for the Euclid's algo-
rithm example in section 2.1, the complexity is 3 (15 edges minus 14 nodes plus 2).
Cyclomatic complexity is also known as v(G), where v refers to the cyclomatic number in
G
graph theory and indicates that the complexity is a function ofthe graph.
The word "cyclomatic" comes from the number offundamental (or basic) cycles in con-
nected, undirected graphs [BERGE]. More importantly, it also gives the number ofindepen-
A
dent paths through strongly connected directed graphs. strongly connected graph is one in
which each node can be reached from any other node by following directed edges in the
graph. The cyclomatic number in graph theory is defined as e - n + 1. Program control flow
graphs are not strongly connected, but they become strongly connected when a "virtual edge"
is added connecting the exit node to the entry node. The cyclomatic complexity definition for
program control flow graphs is derived from the cyclomatic number formula by simply add-
ing one to represent the contribution ofthe virtual edge. This definition makes the cyclomatic
complexity equal the number ofindependent paths through the standard control flow graph
model, and avoids explicit mention ofthe virtual edge.
Figure 2-4 shows the control flow graph ofFigure 2-2 with the virtual edge added as a dashed
line. This virtual edge is notjust a mathematical convenience. Intuitively, it represents the
control flow through the rest ofthe program in which the module is used. It is possible to cal-
culate the amount of (virtual) control flow through the virtual edge by using the conservation
offlow equations at the entry and exit nodes, showing it to be the number oftimes that the
module has been executed. For any individual path through the module, this amount offlow is
exactly one. Although the virtual edge will notbe mentioned again in this document, note that
since its flow can be calculated as a linear combination ofthe flow through the real edges, its
presence or absence makes no difference in determining the number of linearly independent
paths through the module.
10

|                  |     | Figure2-4. | Control flowgraph with | virtual edge.      |
| ---------------- | --- | ---------- | ---------------------- | ------------------ |
| Characterization |     | ofv(G)     | using a                | ofcontrolflowpaths |
| 2.3              |     |            | basis                  | set                |
Cyclomatic complexity can be characterized number ofelements ofa ofcon-
as the basis set
trol flow paths through the module. Some familiarity with linear algebra required to follow
is
the details, but the point is that cyclomatic complexity is precisely the minimum number of
To
paths thatcan, in (linear) combination, generate all possible paths through the module. see
which
this, considerthe following mathematical model, gives a vector space corresponding to
| each flow | graph. |     |     |     |
| --------- | ------ | --- | --- | --- |
Each path has an associated row vector, with the elements corresponding to edges in the flow
graph. The value ofeach element is the number oftimes the edge is traversed by the path.
Consider the path described in Figure 2-3 through the graph in Figure 2-2. Since there are 15
edges graph, vector has 15 elements. Seven ofthe edges are traversed exactly once
| in  | the | the |     |     |
| --- | --- | --- | --- | --- |
as partofthe path, so those elements have value The othereightedges were nottraversed as
1.
| part ofthe | path, so | they have value | 0.  |     |
| ---------- | -------- | --------------- | --- | --- |
11

|     |     |     |     |     |     |     |     | which | columns |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ----- | ------- | --- | --- | --- | --- |
Considering a set ofseveral paths gives a matrix in the correspond to edges
and rows correspond paths. From linear algebra, known each matrix has
|     | the |     |     | to  |     |     |     | it is |     | that |     |     | a   |
| --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | ---- | --- | --- | --- |
unique rank (number oflinearly independent rows) that less than or equal to the number of
is
matterhow
columns. This means thatno many ofthe (potentially infinite) number ofpossible
number
paths are added to the matrix, the rank can neverexceed the ofedges in the graph. In
|     | maximum |     |     | ofthis | rank |     |     |     |     |     |     |     | A   |
| --- | ------- | --- | --- | ------ | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
fact, the value is exactly the cyclomatic complexity ofthe graph.
minimal ofvectors (paths) with maximumrank known as abasis, and abasis can alsobe
|     | set |     |     |     |     |     | is  |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
described as a linearly independent set ofvectors that generate vectors in the space by
|     |     |     |     |     |     |     |     |     |     | all |     |     | lin- |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- |
ear combination. This means that the cyclomatic complexity is the number ofpaths in any
independent set ofpaths that generate all possible paths by linear combination.
Given any ofpaths, determine rank by doing Gaussian Elimination on
|     |     | set |     | it is | possible | to  | the |     |     |     |     |     |     |
| --- | --- | --- | --- | ----- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
the associated matrix. The rank the numberofnon-zero rows once elimination complete.
|     |     |     |     |     | is  |     |     |     |     |     |     | is  |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Ifno rows are driven to zero during elimination, the original paths are linearly independent. If
the rankequals the cyclomatic complexity, the original set ofpaths generate all paths by linear
combination. Ifboth conditions hold, the original set ofpaths are a basis for the flow graph.
There a few important points note about algebra ofcontrol flow
|     | are |     |     |     |     | to  | the linear |     |     |     |     | paths. | First, |
| --- | --- | --- | --- | --- | --- | --- | ---------- | --- | --- | --- | --- | ------ | ------ |
although every path has a corresponding vector, not every vector has a corresponding path.
This is obvious, for example, for a vector that has a zero value for all elements corresponding
to edges out ofthe module entry node but has a nonzero value for any other element cannot
correspond to any path. Slightly less obvious, but also true, is that linear combinations ofvec-
|      | correspond |     |     |        | paths | may be | vectors | do   | not correspond |     |     |               |     |
| ---- | ---------- | --- | --- | ------ | ----- | ------ | ------- | ---- | -------------- | --- | --- | ------------- | --- |
| tors | that       |     | to  | actual |       |        |         | that |                |     | to  | actual paths. |     |
This follows from the non-obvious fact (shown in section that always possible to con-
|     |     |     |     |     |     |     |     |     | 6)  | it is |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- |
struct a basis consisting ofvectors that correspond to actual paths, so any vector can be gener-
ated from vectors corresponding to actual paths. This means that one can notjust find a basis
—
them
set ofvectors by algebraic methods and expect to correspond to paths one must use a
|               |     | technique |     | such |         | ofsection | 6      |        |     | ofpaths. |          |       |       |
| ------------- | --- | --------- | --- | ---- | ------- | --------- | ------ | ------ | --- | -------- | -------- | ----- | ----- |
| path-oriented |     |           |     |      | as that |           | to get | abasis | set |          | Finally, | there | are a |
potentially infinite number ofbasis sets ofpaths for a given module. Each basis has the
set
same number ofpaths in (the cyclomatic complexity), but there is no limit to the number of
it
different sets ofbasis paths. For example, it is possible to start with any path and construct a
shown
| basis | that | contains | it, as |     | in  | section 6.3. |     |     |     |     |     |     |     |
| ----- | ---- | -------- | ------ | --- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- |
The ofthe theory behindcyclomatic complexity are too mathematically complicatedto
details
be used directly during software development. However, the good news that this mathe-
is
matical insight yields an effective operational testing method in which a concrete basis set of
| paths | is tested: | structured |     | testing. |     |     |     |     |     |     |     |     |     |
| ----- | ---------- | ---------- | --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
12

1
| Example | ofv(G) and | basispaths |     |     |     |
| ------- | ---------- | ---------- | --- | --- | --- |
2.4
Figure 2-5 shows the control flow graph for module "euclid" with the fifteen edges numbered
0 to 14 along with the fourteen nodes numbered 0 to 13. Since the cyclomatic complexity is 3
| +   |     |     | One |     | B   |
| --- | --- | --- | --- | --- | --- |
(15 - 14 2), there is a basis set ofthree paths. such basis set consists ofpaths
| through B3, shown | Figure |      |     |     |     |
| ----------------- | ------ | ---- | --- | --- | --- |
|                   | in     | 2-6. |     |     |     |
CydlomaticRowGraph
|     | |Plot[ [Save~| | Convert] [Foruard] jiackuard) | jEnlarse] |Recluce| | [ciose] |Hc1p| |     |
| --- | -------------- | ----------------------------- | ------------------- | -------------- | --- |
I
|     | Pago 1 of 1 | 3X     |     |              |     |
| --- | ----------- | ------ | --- | ------------ | --- |
|     | Program:    | Euclid |     | 01/15/9S     |     |
|     | eucLid (A)  |        |     | Superinposed |     |
|     | Cyclomatic  | Graph  |     | Upward Flows |     |
|     | Cyclomatic  |        |     | Loop Exits   |     |
3
|     | Essential | 1   |     | Plain Edges |     |
| --- | --------- | --- | --- | ----------- | --- |
|     | Design 1  |     |     |             |     |
13
12)
14
13
|     | Figure2-5. | Controlflowgraphwith | edges | numbered. |     |
| --- | ---------- | -------------------- | ----- | --------- | --- |
13

::
Module: euclid
Basis Test Paths: 3 Paths
Test Path Bl: 0 1 5 6 7 11 12 13
8{ 1) n>m ==> FALSE
14 7) r!=0 ==> FALSE
(
Test Path B2 0 1 2 3 4 5 6 7 11 12 13
8( 1) n>m ==> TRUE
14 7) r!=0 ==> FALSE
(
Test Path B3 0 1 5 6 7 8 9 10 7 11 12
8( 1) n>m ==> FALSE
14( 7) r!=0 ==> TRUE
14{ 7) r!=0 ==> FALSE
Figure2-6. A basis setofpaths,Bl through B3.
Any arbitrary path can be expressed as alinearcombination ofthebasis paths B 1 throughB3.
For example, the path P shown in Figure 2-7 is equal to B2 - 2 * B 1 + 2 * B3.
Module: euclid
User Specified Path: 1 Path
Test Path P: 0 1 2 3 4 5 6 7 8 9 10 7 8 9 10 7 11 12 13
8( 1) : n>m ==> TRUE
14 7) r!=0 ==> TRUE
( :
14 7) r!=0 ==> TRUE
( :
14 7) r!=0 ==> FALSE
( :
Figure2-7. Path P.
To see this, examine Figure 2-8, which shows the number oftimes each edge is executed
along each path.
Path/Edge 0 1 2 3 4 5 6 7 8 9 10 11 12
Bl 1 0 1 0 0 0 1 1 0 1 0 0 0
B2 1 1 0 1 1 1 1 1 0 1 0 0 0
B3 1 0 1 0 0 0 1 1 1 1 1 1 1
P 1 1 0 1 1 1 1 1 2 1 2 2 2
Figure2-8. Matrixofedgeincidenceforbasis paths B1-B3andotherpath P.
One interesting property ofbasis sets is that every edge ofaflow graph is traversed by at least
one path in every basis set. Put another way, executing a basis set ofpaths will always cover
every control branch in the module. This means that to cover all edges never requires more
14

than the cyclomatic complexity number ofpaths. However, executing abasis setjust to cover
all edges is overkill. Covering all edges can usually be accomplished with fewer paths. In
this example, paths B2 and B3 cover all edges without path B 1. The relationship between
basis paths and edge coverage is discussed further in section 5.
Note that apart from forming a basis together, there is nothing special about paths B 1 through
B3. Path P in combination with any two ofthe paths B 1 through B3 would also form abasis.
The fact that there are many sets ofbasis paths through mostprograms is importantfortesting,
since it means it is possible to have considerable freedom in selecting a basis set ofpaths to
test.
2.5 Limiting cyclomatic complexity to 10
There are many good reasons to limit cyclomatic complexity. Overly complex modules are
more prone to error, are harder to understand, are harder to test, and are harder to modify.
Deliberately limiting complexity at all stages ofsoftware development, for example as a
departmental standard, helps avoid the pitfalls associated with high complexity software.
Many organizations have successfully implementedcomplexity limits as part oftheir software
programs. The precise number to use as a limit, however, remains somewhat controversial.
The original limit of 10 as proposed by McCabe has significant supporting evidence, but lim-
its as high as 15 have been used successfully as well. Limits over 10 should be reserved for
projects that have several operational advantages over typical projects, for example experi-
enced staff, formal design, a modem programming language, structured programming, code
walkthroughs, and acomprehensive testplan. In other words, an organization can pick acom-
plexity limit greater than 10, but only ifit is sure it knows what it is doing and is willing to
devote the additional testing effort required by more complex modules.
Somewhat more interesting than the exact complexity limit are the exceptions to that limit.
For example, McCabe originally recommended exempting modules consisting ofsingle mul-
tiway decision ("switch" or "case") statements from the complexity limit. The multiway deci-
sion issue has been interpreted in many ways over the years, sometimes with disastrous
results. Some naive developers wondered whether, since multiway decisions qualify for
exemption from the complexity limit, the complexity measure shouldjust be altered to ignore
them. The result would be that modules containing several multiway decisions would not be
identified as overly complex. One developer started reporting a "modified" complexity in
which cyclomatic complexity was dividedby the numberofmultiway decision branches. The
stated intent ofthis metric was that multiway decisions would be treated uniformly by having
them contribute the average value ofeach case branch. The actual result was that the devel-
oper could take a module with complexity 90 and reduce it to "modified" complexity 10 sim-
ply by adding a ten-branch multiway decision statement to it that did nothing.
15

Consideration ofthe intent behind complexity limitation can keep standards policy on track.
There are two main facets ofcomplexity to consider: the number oftests and everything else
number
(reliability, maintainability, understandability, etc.). Cyclomatic complexity gives the
oftests, which for a multiway decision statement the number ofdecision branches. Any
is
attempt to modify the complexity measure to have a smaller value for multiway decisions will
result in anumberoftests thatcannotevenexercise eachbranch, and will hence be inadequate
for testing purposes. However, the pure number oftests, while important to measure andcon-
when
trol, is not a major factor to consider limiting complexity. Note that testing effort is
| much | more |          | numberoftests, |     |     |            | multipliedby |     |     |                       |     |     |
| ---- | ---- | -------- | -------------- | --- | --- | ---------- | ------------ | --- | --- | --------------------- | --- | --- |
|      |      | thanjust | the            |     |     | since that | is           |     | the | efforttoconstructeach |     |     |
individual bringing the other facet ofcomplexity. correlation ofcomplexity
|     |     | test, | in  |     |     |     |     | It is | this |     |     |     |
| --- | --- | ----- | --- | --- | --- | --- | --- | ----- | ---- | --- | --- | --- |
with reliability, maintainability, and understandability that primarily drives the process to
limit complexity.
among
Complexity limitation affects the allocation ofcode individual software modules, lim-
|       | amount | ofcode | any | one | module, | and |      | tending |           | more | modules |         |
| ----- | ------ | ------ | --- | --- | ------- | --- | ---- | ------- | --------- | ---- | ------- | ------- |
| iting | the    |        | in  |     |         |     | thus |         | to create |      |         | for the |
same application. Other than complexity limitation, the usual factors to consider when
allo-
cating code among modules are the cohesion and coupling principles ofstructured design: the
ideal module performs a single conceptual function, and does so in a self-contained manner
them
without interacting with other modules except to use as subroutines. Complexity limita-
|      |          |             |            |     | where | doing | would | render |     | module | complex |     |
| ---- | -------- | ----------- | ---------- | --- | ----- | ----- | ----- | ------ | --- | ------ | ------- | --- |
| tion | attempts | to quantify | an "except |     |       |       | so    |        | a   |        | too     | to  |
understand, or maintain" clause the structured design principles. This rationale pro-
|     |     | test, |     |     | to  |     |     |     |     |     |     |     |
| --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
vides an effective framework for considering exceptions to a given complexity limit.
module
Rewriting a single multiway decision to cross a boundary is a clear violation ofstruc-
|     |     |     |     |     | module |     |     |     |     | multiway |     | may |
| --- | --- | --- | --- | --- | ------ | --- | --- | --- | --- | -------- | --- | --- |
tured design. Additionally, although a consisting ofa single decision
require many each should be easy construct and execute. Each decision branch
|     |     | tests, | test |     |     | to  |     |     |     |     |     |     |
| --- | --- | ------ | ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
can be understood and maintained in isolation, so the module likely to be reliable andmain-
is
tainable. Therefore, it is reasonable to exempt modules consisting ofa single multiway deci-
sion statement from a complexity limit. Note that ifthe branches ofthe decision statement
|     |     |     |     |     |     | and |     | exemption |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --------- | --- | --- | --- | --- |
contain complexity themselves, the rationale thus the does not automatically
However, branches have very low complexity code them, may well apply.
| apply. |     | ifall |     |     |     |     |     |     | in  | it  |     |     |
| ------ | --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Although constructing "modified" complexity measures not recommended, considering the
is
maximum complexity ofeach multiway decision branch is likely to be much moreuseful than
the average. At this point it shouldbe clearthatthe multiway decision statementexemption is
|     |     | anomaly |     |     | measure |     |     |     |     |     |     |     |
| --- | --- | ------- | --- | --- | ------- | --- | --- | --- | --- | --- | --- | --- |
not a bizarre in the complexity but rather the consequence ofareasoning
process seeks abalance between complexity ofstructured design,
|     | that |     |     |     | the |     | limit, | the | principles |     |     |     |
| --- | ---- | --- | --- | --- | --- | --- | ------ | --- | ---------- | --- | --- | --- |
and the fundamental properties of software that the complexity limit intended to control.
is
This process should serve as a model for assessing proposed violations ofthe standard com-
plexity limit. For developers with a solid understanding ofboth the mechanics and the intent
|     |     |     |     | most |     |     |     | "For each |     |     |     |     |
| --- | --- | --- | --- | ---- | --- | --- | --- | --------- | --- | --- | --- | --- |
ofcomplexity limitation, the effective policy is: module, either limit cyclo-
matic complexity 10 discussedearlier, an organization can a similarnumber),
|            |     | to        | (as         |       |     |       |     |            | substitute |     |     |     |
| ---------- | --- | --------- | ----------- | ----- | --- | ----- | --- | ---------- | ---------- | --- | --- | --- |
| or provide |     | a written | explanation | ofwhy | the | limit | was | exceeded." |            |     |     |     |
16

| 3   | Examples     |     |              | of  | Cyclomatic |     |     | Complexity |     |     |     |     |
| --- | ------------ | --- | ------------ | --- | ---------- | --- | --- | ---------- | --- | --- | --- | --- |
| 3.1 | Independence |     | ofcomplexity |     | and        |     |     |            |     |     |     |     |
size
There a big difference between complexity and Consider the difference between the
|     | is  |     |     |     |     |     | size. |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- |
cyclomatic complexity measure and the number oflines ofcode, a common size measure.
|     |     | common |     |     |     |     |     | acommon |     |     |     |     |
| --- | --- | ------ | --- | --- | --- | --- | --- | ------- | --- | --- | --- | --- |
Just as 10 is a limit forcyclomatic complexity, 60 is limit for the number
|     |     |     | somewhat |     |     |     |     |     |     | module |     |     |
| --- | --- | --- | -------- | --- | --- | --- | --- | --- | --- | ------ | --- | --- |
oflines ofcode, the archaic rationale being thateach software should fit on
| one     | page |     | be manageable. |     | Although |     | number |         | ofcode |     | used  |      |
| ------- | ---- | --- | -------------- | --- | -------- | --- | ------ | ------- | ------ | --- | ----- | ---- |
| printed |      | to  |                |     |          | the |        | oflines |        | is  | often | as a |
crude complexity measure, there no consistent relationship between the two. Many mod-
is
ules with no branching ofcontrol flow (and hence the minimum cyclomatic complexity of
one) consist offar greater than 60 lines ofcode, and many modules with complexity greater
than ten have far fewer than 60 lines ofcode. For example, Figure 3-1 has complexity 1 and
| 282 |               | while |     | Figure | 3-9 has complexity |     | 28  | and 30 |         | Thus, | although |     |
| --- | ------------- | ----- | --- | ------ | ------------------ | --- | --- | ------ | ------- | ----- | -------- | --- |
|     | lines ofcode, |       |     |        |                    |     |     | lines  | ofcode. |       |          |     |
the number oflines ofcode an important size measure, independent ofcomplexity and
|        |        |      |         | is   |           |     |     | it is |     |     |     |     |
| ------ | ------ | ---- | ------- | ---- | --------- | --- | --- | ----- | --- | --- | --- | --- |
| should | not be | used | for the | same | purposes. |     |     |       |     |     |     |     |
and
| 3.2 | Severalflow |     | graphs |     | their complexity |     |     |     |     |     |     |     |
| --- | ----------- | --- | ------ | --- | ---------------- | --- | --- | --- | --- | --- | --- | --- |
Several actual control flow graphs and theircomplexity measures are presented in Figures 3-1
through understanding ofthe measure. The graphs presented order of
|     | 3-9, to | solidify |     |     |     |     |     |     | are |     | in  |     |
| --- | ------- | -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
increasing complexity, in order to emphasize the relationship between the complexity num-
| bers | and an intuitive |     | notion | ofthe | complexity | ofthe | graphs. |     |     |     |     |     |
| ---- | ---------------- | --- | ------ | ----- | ---------- | ----- | ------- | --- | --- | --- | --- | --- |
17

f^"}} t^o'^tj'porwaTjjiBaduwrdjiEfilary];RedCT|\c\<no\[Mp]
| a         |     | \   |
| --------- | --- | --- |
| ] 39of134 |     | r.  |
EBt^imtriJierai^m(m)
i«9«cia!«i«d
| Cittntl&l1 | B rlftlnEiftf | ^   |
| ---------- | ------------- | --- |
1
| i   |     | 1   |
| --- | --- | --- |
Controlflowgraph withcomplexity
| Figure3-1. |     | 1.  |
| ---------- | --- | --- |
graph
| Figure3-2. Controlflow | with complexity3. |     |
| ---------------------- | ----------------- | --- |

| Figure3-3. Controlflowgraph | with complexity4.     |     |
| --------------------------- | --------------------- | --- |
| Figure3-4. Controlflow      | graph with complexity | 5.  |
19

Figure3-5. Controlflowgraph with complexity6.
Figure3-6. Controlflowgraphwith complexify8.

| Figure3-8. Controlflow | graph withcomplexity | 17. |
| ---------------------- | -------------------- | --- |

j
CycftiinattcFlowGraph
|     |     |         | l^o^^s'^t    | Forujard Backuardj Enlarge] | Reduce| | Close Help |     |
| --- | --- | ------- | ------------ | --------------------------- | ------- | ---------- | --- |
|     |     | I ^l^il | \            | }                           |         | j          |     |
|     |     | Page    | 61 of 194 3X |                             |         |            |     |
I
|           |            |            | Controlflow | graph       | with complexity |             |              |
| --------- | ---------- | ---------- | ----------- | ----------- | --------------- | ----------- | ------------ |
|           |            | Figure3-9. |             |             |                 | 28.         |              |
| One       | ingredient |            | any         | methodology |                 | the program | logic during |
| essential |            |            | in testing  |             | is              | to limit    |              |
development so that the programcan be understood, and the amount oftesting required to ver-
A
ify the logic is not overwhelming. developer who, ignorant ofthe implications ofcomplex-
ity, expects to verify a module such as that ofFigure 3-9 with a handful oftests is heading for
|     | The |     | module |     |     |     | The |
| --- | --- | --- | ------ | --- | --- | --- | --- |
disaster. size ofthe in Figure 3-9 is only 30 lines ofsource code. size ofsev-
ofthe previous graphs exceeded 60 forexample 282-line module Figure 3-1.
| eral |     |     |     | lines, |     | the | in  |
| ---- | --- | --- | --- | ------ | --- | --- | --- |
In practice, large programs often have low complexity and small programs often have high
complexity. Therefore, the common practice ofattempting to limit complexity by controlling
| how | many |     |     |     |     |     |     |
| --- | ---- | --- | --- | --- | --- | --- | --- |
only lines a module will occupy is entirely inadequate. Limiting complexity
| directly | is abetter | alternative. |     |     |     |     |     |
| -------- | ---------- | ------------ | --- | --- | --- | --- | --- |
22

4
|     | Simplified |     |     | Complexity |     | Calculation |     |     |     |
| --- | ---------- | --- | --- | ---------- | --- | ----------- | --- | --- | --- |
+
Applying the e - n 2 formula by hand is tedious and error-prone. Fortunately, there are sev-
|          | easierways   |             | complexity |              |         | fromcounting |          |            |     |
| -------- | ------------ | ----------- | ---------- | ------------ | ------- | ------------ | -------- | ---------- | --- |
| eral     |              | tocalculate |            | in practice, | ranging |              | decision | predicates |     |
| to using | an automated |             |            |              |         |              |          |            |     |
tool.
4.1 Countingpredicates
|     |     |     |     |     |     |     | =   | + A |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Ifall decisions are binary and there are p binary decision predicates, v(G) p 1. binary
|     |     |     | on  |     |     | anode | two |     |     |
| --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- |
decision predicate appears the control flow graph as with exactly edges flowing
out of Starting with one and adding the number ofsuch nodes yields the complexity. This
it.
A
formula a simple consequence ofthe complexity definition. straight-line control flow
is
graph, which has exactly one edge flowing out ofeach node except the module exit node, has
complexity one. Each node with two edges out ofit adds one to complexity, since the "e" in
+
the e - n 2 formula is increased by one while the "n" is unchanged. In Figure 4-1, there are
|       | binary | decision nodes |       | and so complexity |     | 4 by      |             | ofthe | +   |
| ----- | ------ | -------------- | ----- | ----------------- | --- | --------- | ----------- | ----- | --- |
| three |        |                | (1,2, | 6),               |     | is direct | application |       | p 1 |
formula. The original e n + 2 gives the same answer, albeit with a bit more counting,
-
12 edges - 10 nodes + 2 = 4. Figure 4-2 has two binary decision predicate nodes (1 and 3), so
come
complexity is 3. Since the decisions in Figure 4-2 from loops, they are represented dif-
same
ferently on the control flow graph, but the counting technique applies.
|     |     |     |     | Figure4-1. Module | with complexityfour. |     |     |     |     |
| --- | --- | --- | --- | ----------------- | -------------------- | --- | --- | --- | --- |
23

|     |     |     | Figure4-2. | Module withcomplexity |     | three. |     |     |
| --- | --- | --- | ---------- | --------------------- | --- | ------ | --- | --- |
Multiway decisions can be handled by the same reasoning as binary decisions, although there
|     |     | As  | +   |     |     |     |     | acomplex- |
| --- | --- | --- | --- | --- | --- | --- | --- | --------- |
is not such aneat formula. in the p 1 formulafor binary predicates, start with
value ofone and add something each decision node flow graph. The
| ity |     |     | to it | for |     | in the | control |     |
| --- | --- | --- | ----- | --- | --- | ------ | ------- | --- |
number added one less than the number ofedges out ofthe decision node. Note that for
is
binary decisions, this number one, which consistent with the p + formula. For athree-
|     |     | is  |     | is  |     |     | 1   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
way decision, add two, and so on. In Figure 4-3, there is a four-way decision, which adds
mod-
three to complexity, as well as three binary decisions, each ofwhich adds one. Since the
|     | one |     |     |     | complexity |     | becomes | +   |
| --- | --- | --- | --- | --- | ---------- | --- | ------- | --- |
ule started with unit ofcomplexity, the calculated 1 -i- 3 3, for a
of7.
total
|     |     |     | Figure4-3. | Modulewithcomplexity7. |     |     |     |     |
| --- | --- | --- | ---------- | ---------------------- | --- | --- | --- | --- |
24

|     |     |     |     | 0 6 |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
,
In addition to counting predicates from the flow graph, it is possible to count them directly
| from |     | source | code. This |       |          |     |         | way | measure |     | and     |            |     |
| ---- | --- | ------ | ---------- | ----- | -------- | --- | ------- | --- | ------- | --- | ------- | ---------- | --- |
|      | the |        |            | often | provides | the | easiest |     | to      |     | control | complexity |     |
during development, since complexity can be measured even before the module complete.
is
For most programming language constructs, the construct has a direct mapping to the control
flow graph, and hence contributes a fixed amount to complexity. However, constructs that
may
appear similar in different languages not have identical control flow semantics, so cau-
|     |     |     | For most |     |     | impact |     |     |     | An  | "if |     |     |
| --- | --- | --- | -------- | --- | --- | ------ | --- | --- | --- | --- | --- | --- | --- |
tion is advised. constructs, the is easy to assess. statement, "while"
statement, and so on are binary decisions, and therefore add one complexity. Boolean
|     |     |     |     |     |     |     |     |     |     | to  |     |     | oper- |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- |
ators add either one or nothing to complexity, depending on whether they have short-circuit
evaluation semantics that can lead to conditional execution of side-effects. For example, the
| C   | "&&" |     |     |     |     |     |     | Ada |     |     |     |     |     |
| --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
operator adds one to complexity, as does the "and then" operator, because both
|     |     |     |     |     |     | The | Ada | "and" |     |     | on  |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- |
are defined to use short-circuit evaluation. operator, the other hand, does
not add complexity, because defined use the full-evaluation and therefore
|      |     | to       |            |        | it is | to          |      |        |     |     | strategy, |     |     |
| ---- | --- | -------- | ---------- | ------ | ----- | ----------- | ---- | ------ | --- | --- | --------- | --- | --- |
| does | not | generate | a decision | node   | in    | the control | flow | graph. |     |     |           |     |     |
|      |     | shows    | C          | module |       |             |      |        |     |     |           |     |     |
Figure 4-4 a code with complexity 6. Starting with 1, each ofthe two "if
|            |     | add | "while" |           |     | adds | and | each |       | two | "&&"      | adds |     |
| ---------- | --- | --- | ------- | --------- | --- | ---- | --- | ---- | ----- | --- | --------- | ---- | --- |
| statements |     |     | 1, the  | statement |     |      | 1,  |      | ofthe |     | operators |      | 1   |
for a of For reference. Figure 4-5 shows the control flow graph corresponding Fig-
|     | total |     | 6.  |     |     |     |     |     |     |     |     |     | to  |
| --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
ure 4-4.
AiwiotatediSouttMUsUngforProgramSamplBs
|     |     |     | tPrintIfSave][Eonvert][Hosel |     | iHelp] |           |     |         |     |     |     |     |     |
| --- | --- | --- | ---------------------------- | --- | ------ | --------- | --- | ------- | --- | --- | --- | --- | --- |
|     |     |     |                              |     |        | Annotated |     | Listing |     |     |     |     |     |
Source
1
|     |     |     | Program | Samples    |     |     |     |     |     |     | 01/16/96 |     |     |
| --- | --- | --- | ------- | ---------- | --- | --- | --- | --- | --- | --- | -------- | --- | --- |
|     |     |     | File :  | samples4.c |     |     |     |     |     |     |          | 1   |     |
:
|     |     |     | Language:     | c_npp |     |     |     |     |            |       |            |     |     |
| --- | --- | --- | ------------- | ----- | --- | --- | --- | --- | ---------- | ----- | ---------- | --- | --- |
|     |     |     | Module Module |       |     |     |     |     |            |       | Start Num  | of  |     |
|     |     |     | Letter Name   |       |     |     |     |     | v(G) ev(G) | iv(G) | Line Lines | |   |     |
1
|     |     |     | D complexity |     |                  |          |                |                 | 6    | 6 3  | 40  | 12  |     |
| --- | --- | --- | ------------ | --- | ---------------- | -------- | -------------- | --------------- | ---- | ---- | --- | --- | --- |
|     |     |     | 40 DO        |     | coraplexity6(int |          | i,             | int j)          |      |      |     |     |     |
|     |     |     | 41           |     | {/*              | Sample   | module         | with complexity |      | 6 */ |     |     |     |
|     |     |     | 4 2 D l      | 02  |                  | if ( i > | 0 s s          | > 0)            |      |      |     |     |     |
|     |     |     | 0 3          |     |                  |          | j >            | {               |      |      |     |     |     |
|     |     |     | 4 3          |     |                  | v jh il  | e ( i          | j ) (           |      |      |     |     |     |
|     |     |     | 44 D4        | D5  |                  |          | if (i          | % 2 SS j        | % 2) |      |     |     |     |
|     |     |     | 45 06        |     |                  |          | printf("%d\n", |                 | i);  |      |     |     |     |
|     |     |     | 46           |     |                  |          | else           |                 |      |      |     |     |     |
|     |     |     | 47 07        | 08  |                  |          | printf("%d\n", |                 | j);  |      |     |     |     |
|     |     |     | 48 09        |     |                  |          | i~;            |                 |      |      |     |     |     |
|     |     |     | 49 01        |     |                  |          |                |                 |      |      |     |     |     |
)
|     |     |     | 50     |     |     | )   |     |     |     |     |     |     |     |
| --- | --- | --- | ------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     | 51 Oil | D12 |     |     |     |     |     |     |     |     |     |
)
|     |     |     |     |     |     |     |     |     |     |     | - — | ,^  |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
. .
I
|     |     |     | Figure4-4. Codeformodulewith |     |     | complexity6. |     |     |     |     |     |     |     |
| --- | --- | --- | ---------------------------- | --- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- |
25

|     |     |     | Figure4-5. Graphformodulewith |     | complexity6. |     |     |
| --- | --- | --- | ----------------------------- | --- | ------------ | --- | --- |
possible, under special circumstances, to generate control flow graphs that do not model
It is
the execution semantics ofboolean operators in a language. This is known as "suppressing"
When
short-circuit operators or "expanding" full-evaluating operators. this is done, it is
meaning
important to understand the implications on the ofthe metric. For example, flow
graphs based on suppressed boolean C can give good view ofcontrol
|     |     |     | operators | in  | a high-level |     |     |
| --- | --- | --- | --------- | --- | ------------ | --- | --- |
flow for reverse engineering purposes by hiding the details ofthe encapsulated and often
unstructured expression-level control flow. However, this representation should not be used
for testing (unless perhaps it is first verified that the short-circuit boolean expressions do not
|     |     |     |     |     | when |     | from |
| --- | --- | --- | --- | --- | ---- | --- | ---- |
contain any side effects). In any case, the important thing calculating complexity
| source code | be               | with |                    | oflanguage |            |        | flow   |
| ----------- | ---------------- | ---- | ------------------ | ---------- | ---------- | ------ | ------ |
|             | is to consistent |      | the interpretation |            | constructs | in the | graph. |
Multiway decision constructs present a couple ofissues when calculating complexity from
source code. As with boolean operators, consideration ofthe control flow graph representa-
tion ofthe relevant language constructs is the key to successful complexity measurement of
|     | An  |     |     |     | by  |     | must be |
| --- | --- | --- | --- | --- | --- | --- | ------- |
source code. implicit default or fall-through branch, ifspecified the language,
taken account when calculating complexity. For example, C an default
| into |     |     |     |     | in there | is implicit |     |
| ---- | --- | --- | --- | --- | -------- | ----------- | --- |
ifno default outcome specified. In that case, the complexity contribution ofthe "switch"
is
statement is exactly the number ofcase-labeled statements, which is one less than the total
A
number ofedges out ofthe multiway decision node in the control flow graph. less fre-
|     |     |     |     | on  |     | between |     |
| --- | --- | --- | --- | --- | --- | ------- | --- |
quently occurring issue that has greater impact complexity is the distinction
"case-labeled statements" and "case When case apply same pro-
|     |     |     | labels." | several | labels | to the |     |
| --- | --- | --- | -------- | ------- | ------ | ------ | --- |
gram statement, this modeled as a single decision outcome edge in the control flow graph,
is
adding one to complexity. is certainly possible to make a consistent flow graph model in
It
which each individual case label contributes adifferent decision outcome edge and hence also
one
| adds | to complexity, | but that | is not the typical | usage. |     |     |     |
| ---- | -------------- | -------- | ------------------ | ------ | --- | --- | --- |

|     |     |     |     |     |     | ;   | ;   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
C
Figure 4-6 shows a code module with complexity 5. Starting with one unit ofcomplexity,
the switch statement has threecase-labeled statements (although having five total case labels),
| which, considering |     | the      | default |               |     | a four-way |     |               | contributes |
| ------------------ | --- | -------- | ------- | ------------- | --- | ---------- | --- | ------------- | ----------- |
|                    |     | implicit |         | fall-through, |     | is         |     | decision that |             |
three units ofcomplexity. The "if statement contributes one unit, for a total complexity of
five. For reference. Figure 4-7 shows the control flow graph corresponding to Figure 4-6.
Wnotatea3<ium>UsMmiforProgramSamplw
Print [Save|[conwt]jciose|jlteip|
I I
|     |     |                        |     | Annotated   | Source          | Listing         |             |            |     |
| --- | --- | ---------------------- | --- | ----------- | --------------- | --------------- | ----------- | ---------- | --- |
|     |     | Program Samples        |     |             |                 |                 |             | 01/16/96   |     |
|     |     | F i l e s a m p l 6s4  | .c  |             |                 |                 |             |            |     |
|     |     | L a n g uage c _ n p p |     |             |                 |                 |             |            |     |
|     |     | Module Module          |     |             |                 |                 |             | Start Num  | of  |
|     |     | Letter Name            |     |             |                 | v(G)            | ev(G) iv(G) | Line Lines |     |
|     |     | E complexityS          |     |             |                 |                 |             | 53         | 14  |
|     |     | 5 3 EO                 |     | c o mpl e x | i t y S i nt n) |                 |             |            |     |
|     |     | 54                     |     | ( /* S a m  | p l e m(o d ule | with complexity | */          |            |     |
5
|     |     | 5 5 E l |     | if  | (n > 0 ) (n() |                        |     |             |     |
| --- | --- | ------- | --- | --- | ------------- | ---------------------- | --- | ----------- | --- |
|     |     | 5 6 E 2 |     |     | sui tc h      |                        |     |             |     |
|     |     | 57 E3   |     |     | case 0:       | ( case 1: printfC'zero |     | or one\n"); |     |
|     |     | 58      |     |     |               | brealc;                |     |             |     |
printf("two\n")
|     |            | 59 E4         |            |                | case 2:              |                       |              |            |     |
| --- | ---------- | ------------- | ---------- | -------------- | -------------------- | --------------------- | ------------ | ---------- | --- |
|     |            | 60            |            |                |                      | break;                |              |            |     |
|     |            | 61 E5         |            |                | case 3:              | case 4: printf("three |              | or four\n" |     |
|     |            | 62            |            |                |                      | break;                |              |            |     |
|     |            | 63 E6         |            |                | s)e                  |                       |              |            |     |
|     |            | 6 4           |            | ) el           |                      |                       |              |            |     |
|     |            | 6 5 E7 E8     |            |                | p rintf("negative\n" |                       |              |            |     |
|     |            | 66 E9         |            |                |                      | )                     |              |            |     |
|     | Figure4-6. | Codeformodule |            | withcomplexity |                      | 5.                    |              |            |     |
|     |            |               | Figure4-7. |                | Graphformodule       | with                  | complexity5. |            |     |
27

| 4.2 Countingflow |     | graph regions |     |     |     |     |     |
| ---------------- | --- | ------------- | --- | --- | --- | --- | --- |
| When             |     |               |     |     |     | R   |     |
the flow graph isplanar (no edges cross) and divides theplane into regions (including
the infinite region "outside" the graph), the simplified formula for cyclomatic complexity is
|     |     | from |     | which |     |     | n + R = |
| --- | --- | ---- | --- | ----- | --- | --- | ------- |
just R. This follows Euler's formula, states that for planar graphs - e 2.
Re-arranging the terms, R = e n + which the definition ofcyclomatic complexity. Thus,
|     |     | -   | 2,  | is  |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
for a planar flow graph, counting the regions gives a quick visual method for determining
complexity. Figure 4-8 shows a planar flow graph with complexity 7, with the regions num-
number
bered from 1 to 7 to illustrate this counting technique. Region 1 is the infinite region,
| and       |             |             | no  |            |        |     |     |
| --------- | ----------- | ----------- | --- | ---------- | ------ | --- | --- |
| otherwise | the regions | are labeled | in  | particular | order. |     |     |
cyclomaticflowGraph
|     |     | jSave               | ,Foruard| ;Backuard|    | Enlarge] | -Reduce      |           |     |
| --- | --- | ------------------- | ----------------------- | -------- | ------------ | --------- | --- |
|     |     | iPlotI I |Corivert| |                         | !        | | iClose]    | iHelp[    |     |
|     |     | Page 3 of 6 3X      |                         |          |              |           |     |
|     |     | Program: Samples    |                         |          | 01/16/96     |           |     |
|     |     | complexity7 (C)     |                         |          | Superimposed |           |     |
|     |     | Cyclomatic Graph    |                         |          | Upward       | Flows     |     |
|     |     | Cyclomatic 7        |                         |          | Loop         | Exits     |     |
|     |     | Essential 1         |                         |          | Plain        | Edges     |     |
|     |     | Design 7            |                         |          |              |           |     |
|     |     | Planargraph         | withcomplexity7,regions |          |              | numbered. |     |
Figure4-8.
28

| 4.3 Use | ofautomated |     | tools |     |     |     |     |     |     |
| ------- | ----------- | --- | ----- | --- | --- | --- | --- | --- | --- |
The most efficient and reliable way to determine complexity is through use ofan automated
tool. Even calculating by hand the complexity ofa single module such as that ofFigure 4-9 is
|     |     | and | such | modules | come |     |     | With |     |
| --- | --- | --- | ---- | ------- | ---- | --- | --- | ---- | --- |
a daunting prospect, often in large groups. an automated tool,
complexity can be determined forhundreds ofmodules spanning thousands oflines ofcode
in
amatter ofminutes. When dealing with existing code, automated complexity calculation and
control flow graph generation is an enabling technology. However, automation is not a pana-
cea.
|     |     |     |        |                    |                |       |     | ' ., i  |     |
| --- | --- | --- | ------ | ------------------ | -------------- | ----- | --- | ------- | --- |
|     |     |     |        |                    | CyclomaticRow: | Graph |     | :,, : : |     |
|     |     |     | Module | with complexity77. |                |       |     |         |     |
Figure4-9.
| The      |      |              |     | may  | come |          |               | development | ofnew |
| -------- | ---- | ------------ | --- | ---- | ---- | -------- | ------------- | ----------- | ----- |
| feedback | from | an automated |     | tool |      | too late | for effective |             |       |
Once code a software module (or or subsystem) finished and pro-
| software. |     | the | for |     |     | file, |     | is  |     |
| --------- | --- | --- | --- | --- | --- | ----- | --- | --- | --- |
cessedby automated tools, reworking to reduce complexity is more costly and error-prone
it
29

developing module with complexity mind from Awareness ofmanual
| than | the | in  | the outset. |
| ---- | --- | --- | ----------- |
techniques forcomplexity analysis helps design andbuildgood software, ratherthan deferring
complexity-related issues to a later phase ofthe life cycle. Automated tools are an effective
way to confirm and control complexity, but they work best where at least rough estimates of
some Ada
complexity are used during development. In cases, such as development, designs
| be              | and      | programming   |           |
| --------------- | -------- | ------------- | --------- |
| can represented | analyzed | in the target | language. |
30

| 5   | Structured |     |     | Testing |     |     |     |     |     |     |
| --- | ---------- | --- | --- | ------- | --- | --- | --- | --- | --- | --- |
Structured testing uses cyclomatic complexity and the mathematical analysis ofcontrol flow
graphs to guide the testing process. Structured testing is more theoretically rigorous and more
common
effective at detecting errors in practice than other test coverage criteria such as state-
| ment and | branch | coverage | [WATS0N5]. |     |            |         |              |          | when |       |
| -------- | ------ | -------- | ---------- | --- | ---------- | ------- | ------------ | -------- | ---- | ----- |
|          |        |          |            |     | Structured | testing | is therefore | suitable |      | reli- |
ability an important consideration for software. not intended as a substitute for
|     | is  |     |     |     |     | It is |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- |
requirements-based "black box" testing techniques, but as a supplement to them. Structured
testing forms the "white box," or code-based, part ofacomprehensive testing program, which
when
quality is critical will also include requirements-based testing, testing in a simulated
| production | environment, |     | and |          | techniques | such |                | random |          |     |
| ---------- | ------------ | --- | --- | -------- | ---------- | ---- | -------------- | ------ | -------- | --- |
|            |              |     |     | possibly | other      |      | as statistical |        | testing. |     |
Other "white box" techniques may also be used, depending on specific requirements for the
software being tested. Structured testing as presented in this section applies to individual soft-
ware modules, where the most rigorous code-based "unit testing" is typically performed. The
integration level Structured testing technique is described in section 7.
| The | structured |     | testing | criterion |     |     |     |     |     |     |
| --- | ---------- | --- | ------- | --------- | --- | --- | --- | --- | --- | --- |
5.1
After the mathematical preliminaries ofsection 2 (especially Sec. the structured testing
2.3),
criterion is simply stated: Test abasis set ofpaths through the control flow graph ofeach mod-
ule. This means that any additional path through the module's control flow graph can be
| expressed | as  | a linear combination |     | ofpaths | that have | been | tested. |     |     |     |
| --------- | --- | -------------------- | --- | ------- | --------- | ---- | ------- | --- | --- | --- |
Note that the structured testing criterion measures the quality oftesting, providing a way to
determine whether testing is complete. It is not a procedure to identify test cases or generate
test datainputs. Section 6 gives atechniqueforgenerating testcases that satisfy the structured
testing criterion.
Sometimes, not possible to a complete basis set ofpaths through the control flow
|     | it  | is  |     | test |     |     |     |     |     |     |
| --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- |
graph ofa module. This happens when some paths through the module can not be exercised
by any input data. For example, ifthe module makes the same exact decision twice in
|     | no  |     |     |     |     |     | outcome | while |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------- | ----- | --- | --- |
sequence, input data will cause it to vary the first decision leaving the sec-
ond constant vice This explored section 9 (especially including
|     |     | or versa. |     | situation | is  | in  |     |     | 9.1), |     |
| --- | --- | --------- | --- | --------- | --- | --- | --- | --- | ----- | --- |
the possibilities ofmodifying the software to remove control dependencies orjust relaxing the
maximum
testing criterion to require the attainable matrix rank (known as the actual complex-
assumed
ity) whenever this differs from the cyclomatic complexity. All paths are to be exer-
method.
| cisable | for the | initial | presentation | ofthe |     |     |     |     |     |     |
| ------- | ------- | ------- | ------------ | ----- | --- | --- | --- | --- | --- | --- |
31

| A program |     |      | cyclomatic | complexity |     | has |              | no of4   |       |      |             |
| --------- | --- | ---- | ---------- | ---------- | --- | --- | ------------ | -------- | ----- | ---- | ----------- |
|           |     | with |            |            |     | 5   | the property | that set | paths | will | suffice for |
even for example, there are 39 distinct that concentrate on the 4 As
| testing, |     | if, |     |     |     |     | tests |     |     | paths. | dis- |
| -------- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | ------ | ---- |
cussed in section the cyclomatic complexity gives the number ofpaths in any basis This
|     |     |     | 2,  |     |     |     |     |     |     |     | set. |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- |
means that ifonly 4 paths have been tested for the complexity 5 module, there must be, indepen-
dent ofthe programming language or the computational statements ofthe program, at least one
|     |     |     |     | be  |     |     | once |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- |
additional test path that can executed. Also, a fifth independent path is tested, any fur-
therpaths a fundamental sense redundant, acombination of5 paths gen-
|       |       | are in  |        |     |     |     | in that |     | basis |     | will |
| ----- | ----- | ------- | ------ | --- | --- | --- | ------- | --- | ----- | --- | ---- |
| erate | those | further | paths. |     |     |     |         |     |       |     |      |
Notice thatmost programs with aloop have apotentially infinite numberofpaths, which are not
|     |     |     |     | even |     |     | The |     |     |     | acom- |
| --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- | ----- |
subject to exhaustive testing in theory. structured testing criterion establishes
|         | number, |     | v(G), oftest | paths |      | have | two      |             |     |     |     |
| ------- | ------- | --- | ------------ | ----- | ---- | ---- | -------- | ----------- | --- | --- | --- |
| plexity |         |     |              |       | that |      | critical | properties: |     |     |     |
A
1. test set ofv(G) paths can be realized. (Again, see section 9.1 for discussion ofthe
more general case in which actual complexity substituted for v(G).)
is
2. Testing beyond v(G) independent paths is redundantly exercising linear combinations
|     | ofbasis | paths. |       |     |     |     |     |         |     |     |         |
| --- | ------- | ------ | ----- | --- | --- | --- | --- | ------- | --- | --- | ------- |
|     |         | have   | shown |     |     |     |     | overthe |     |     | program |
Several studies that the distribution ofrun time statements in the
has peculiar shape. Typically, 50% ofthe run time within a program concentrated within
|     | a   |     |     |     |     |     |     |     | is  |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
only 4% ofthe code [KNUTH]. When the test data derived from only arequirements pointof
is
view and is not sensitive to the internal structure ofthe program, likewise will spend most of
it
the run time testing afew statements over and over again. The testing criterion in this document
establishes a level oftesting that is inherently related to the internal complexity ofa program's
|        | One |       |         |        |                  |     |               | over a largernumberofindependent |     |     |     |
| ------ | --- | ----- | ------- | ------ | ---------------- | --- | ------------- | -------------------------------- | --- | --- | --- |
| logic. |     | ofthe | effects | ofthis | is to distribute |     | the test data |                                  |     |     |     |
paths, which can provide more effective testing with fewer For very simple programs
tests.
(complexity less than other testing techniques seem likely to exercise a basis set ofpaths.
5),
However, for more realistic complexity levels, othertechniques are notlikely to exercise abasis
amore
set ofpaths. Exphcitly satisfying the structured testing criterion will then yield rigorous
| set | oftest    | data. |        |            |     |         |     |     |     |     |     |
| --- | --------- | ----- | ------ | ---------- | --- | ------- | --- | --- | --- | --- | --- |
| 5.2 | Intuition |       | behind | structured |     | testing |     |     |     |     |     |
The solid mathematical foundation ofstructured testing has many advantages [WATSON2].
First ofall, since any basis set ofpathscovers all edges and nodes ofthe control flow graph, sat-
|     |     |     |     |     |     |     |     | weaker |     | and |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------ | --- | --- | --- |
isfying the structured testing criterion automatically satisfies the branch statement
|         |           |              |     |                   |     |     | subsumesbranch | and statementcoveragetesting. |     |     |     |
| ------- | --------- | ------------ | --- | ----------------- | --- | --- | -------------- | ----------------------------- | --- | --- | --- |
| testing | criteria. | Technically, |     | structuredtesting |     |     |                |                               |     |     |     |
This means any benefit software gained by statement andbranch coveragetest-
|     |               | that |        | in            |     | reliability |     |     |     |     |     |
| --- | ------------- | ---- | ------ | ------------- | --- | ----------- | --- | --- | --- | --- | --- |
| ing | automatically |      | shared | by structured |     | testing.    |     |     |     |     |     |
is
32

minimum
Next, with structured testing, testing is proportional to complexity. Specifically, the
| number | oftests |     |     |     |     |     |     |     |     |     |     |
| ------ | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
required to satisfy the structured testing criterion is exactly the cyclomatic
complexity. Given the correlation between complexity and makes sense concen-
|     |     |     |     |     |     |     | errors, | it  |     |     | to  |
| --- | --- | --- | --- | --- | --- | --- | ------- | --- | --- | --- | --- |
trate testing effort on the most complex and therefore error-prone software. Structured testing
makes this notion mathematically precise. Statement and branch coverage testing do not even
come
close to sharing this property. All statements and branches ofan arbitrarily complex
module can be covered withjust one even though module same com-
|     |     |     |     |     | test, |     | another |     | with | the |     |
| --- | --- | --- | --- | --- | ----- | --- | ------- | --- | ---- | --- | --- |
plexity may requirethousands oftests using the samecriterion. Forexample, aloop enclosing
arbitrarily complex code canjustbe iterated as many times as necessary forcoverage, whereas
may
complex code with no loops require separate tests for each decision outcome. With
how much
structured testing, any path, no matter ofthe module it covers, can contribute at
| most | one | element |     |          |            |               |       | minimum |     |          | number |
| ---- | --- | ------- | --- | -------- | ---------- | ------------- | ----- | ------- | --- | -------- | ------ |
|      |     | to      | the | required | basis set. | Additionally, | since | the     |     | required |        |
oftests known advance, structured testing supports objective planning and monitoring of
|     | is  | in  |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
the testing process to a greater extent than other testing strategies.
Another strength of structured testing is that, for the precise mathematical interpretation of
"independent"
as "linearly independent," structured testing guarantees that all decision out-
comes are tested independently. This means unlike other common testing
|     |     |     |     |     |     | that |     |     |     | strategies, |     |
| --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | ----------- | --- |
structured testing does not allow interactions between decision outcomes during testing to
C
hide errors. As a very simple example, consider the function ofFigure 5-1. Assume that
this function is intended to leave the value ofvariable "a" unchanged under all circumstances,
| and |     |     |     | The | branch |     | can | be  |     | with two |     |
| --- | --- | --- | --- | --- | ------ | --- | --- | --- | --- | -------- | --- |
is thus clearly incorrect. testing criterion satisfied tests that
detect the both decision outcomes be FALSE, which case the value of
| fail | to  | error: | first | let |     |     |     |     | in  |     |     |
| ---- | --- | ------ | ----- | --- | --- | --- | --- | --- | --- | --- | --- |
"a" not affected, and then let both decision outcomes be TRUE, in which case the value of
is
"a" is first incremented and then decremented, ending up with its original value. The state-
ment testing criterion can be satisfied withjust the second ofthose two tests. Structured test-
on
ing, the otherhand, is guaranteed to detectthis error. Sincecyclomatic complexity is three,
|       | independent |     | paths | required, |     | so       | one  | one | decision | outcome |     |
| ----- | ----------- | --- | ----- | --------- | --- | -------- | ---- | --- | -------- | ------- | --- |
| three |             |     | test  | are       |     | at least | will | set |          |         | to  |
TRUE and the other to FALSE, leaving "a" either incremented or decremented and therefore
| detecting |     | the error | during | testing. |     |     |     |     |     |     |     |
| --------- | --- | --------- | ------ | -------- | --- | --- | --- | --- | --- | --- | --- |
voidfuncO
{
if(condition1)
|     |     |     |     |     |     | a=a+ | 1;  |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- |
if(condition2)
|     |     |     |     |     |     | a=a- 1; |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ------- | --- | --- | --- | --- | --- |
}
|     |     |     |     |     |     |            | Example | C         |     |     |     |
| --- | --- | --- | --- | --- | --- | ---------- | ------- | --------- | --- | --- | --- |
|     |     |     |     |     |     | Figure5-1. |         | function. |     |     |     |
33

| 5.3 Complexity |     | and | reliability |     |     |     |     |     |     |
| -------------- | --- | --- | ----------- | --- | --- | --- | --- | --- | --- |
A
Several ofthe studies discussed in Appendix show a correlation between complexity and
errors, as well as a connection between complexity and difficulty to understand software.
|     |     | combination |     |     | and |     | [MCCABE4]. |     |     |
| --- | --- | ----------- | --- | --- | --- | --- | ---------- | --- | --- |
Reliability is a oftesting understanding In theory, either per-
|              |         | program | behavior |     | every | possible | sequence | ofinput) | or under- |
| ------------ | ------- | ------- | -------- | --- | ----- | -------- | -------- | -------- | --------- |
| fect testing | (verify |         |          |     | for   |          |          |          | perfect   |
standing (build a completely accurate mental model ofthe program so that any errors would
be obvious) are sufficient by themselves to ensure reliability. Given that a piece ofsoftware
| known |     |     |     |     |     |     | how |     |     |
| ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
has no errors, its perceived reliability depends both on well it has been tested and
how
well it is understood. In effect, the subjective reliability ofsoftware is expressed in state-
| ments such |       | understand |      | program | well | enough | know    |     | have executed |
| ---------- | ----- | ---------- | ---- | ------- | ---- | ------ | ------- | --- | ------------- |
|            | as "I |            | this |         |      |        | to that | the | tests I       |
are adequate to provide my desired level ofconfidence in the software." Since complexity
makes software both harder to test and harder to understand, complexity is intimately tied to
reliability. From one perspective, complexity measures the effort necessary to attain a given
level ofreliability. Given afixed level ofeffort, atypical case in the real world ofbudgets and
|                | complexity | measures |         |             |     |         |     |     |     |
| -------------- | ---------- | -------- | ------- | ----------- | --- | ------- | --- | --- | --- |
| schedules,     |            |          |         | reliability |     | itself. |     |     |     |
| 5.4 Structured |            | testing  | example |             |     |         |     |     |     |
As an example ofstructured testing, consider the C module "count" in Figure 5-2. Given a
string, is intended to return the total number ofoccurrences ofthe letter 'C ifthe string
it
| begins with | the | letter 'A.' | Otherwise, |     | it is | supposed | to return -1. |     |     |
| ----------- | --- | ----------- | ---------- | --- | ----- | -------- | ------------- | --- | --- |
34

|     |     |     | |   |     |     |     | •   | ;;  | . 1; |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- |
^notatedSourcelistingforPrograniCotmt
Print]
|     |          | [Save] [Convert | [ciose | ] jHeip] |           |     |        |         |     |     |          |     |
| --- | -------- | --------------- | ------ | -------- | --------- | --- | ------ | ------- | --- | --- | -------- | --- |
|     |          |                 |        |          | Annotated |     | Source | Listing |     |     |          |     |
|     | Program  |                 | Count  |          |           |     |        |         |     |     |          |     |
|     |          | :               |        |          |           |     |        |         |     |     | 01/18/96 |     |
|     | File     |                 | stex.c |          |           |     |        |         |     |     |          |     |
|     | Language | :               | c_npp  |          |           |     |        |         |     |     |          |     |
:
|     | Module | Module |     |     |     |     |     |     |            |     | Start Num of |     |
| --- | ------ | ------ | --- | --- | --- | --- | --- | --- | ---------- | --- | ------------ | --- |
|     | Letter | Name   |     |     |     |     |     |     | v(G) ev(G) |     | Line Lines   |     |
iv(G)
|     |     | A count |     |     |     |     |     |     |     |     |     |     |
| --- | --- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
30
|     | qJ  |     |     |     | int count(string) |        |            |            |             |               |      |     |
| --- | --- | --- | --- | --- | ----------------- | ------ | ---------- | ---------- | ----------- | ------------- | ---- | --- |
|     | /4I |     |     |     | char *string,     |        |            |            |             |               |      |     |
|     |     |     |     |     | /* This           | module |            | incorrect. | Its         | specification |      |     |
|     | 5   |     |     |     | (                 |        | is         |            |             |               | is:  |     |
|     | 6   |     |     |     | * If              | string | begins     | with       | 'A' (eg     | "ABXCCZBZ")   | then |     |
|     | 7   |     |     |     | return            |        | the number | of         | occurrences | of 'C         | (eg  |     |
|     |     |     |     |     | *                 |        |            |            |             |               | 2),  |     |
|     | 8   |     |     |     | * otherwise       |        | return     | -1         |             |               |      |     |
*/
9
|     | 10  |     |     |     | int | index          | = 0, | i = 0, | j = 0, k | = 0; |     |     |
| --- | --- | --- | --- | --- | --- | -------------- | ---- | ------ | -------- | ---- | --- | --- |
|     | 11  | Al  |     |     | if  | (string[index] |      | ==     | 'A')     |      |     |     |
{
|     | 12  | A2  |     |     | LI  |     | index             | = index | + 1  |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ----------------- | ------- | ---- | --- | --- | --- |
|     | 13  | A3  |     |     |     |     | if (string[index] |         | 'B') |     |     |     |
f
|     | 14  | A4  |     |     |     |     | j    | = j + | 1;  |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ---- | ----- | --- | --- | --- | --- |
|     | 15  |     |     |     |     |     | X    | = 0;  |     |     |     |     |
|     | 16  | AS  |     |     |     |     | goto | LI    |     |     |     |     |
17
==
|     | 18  | A6  | A7  |     |     |     | if ( string | [ index | 'C') | {   |     |     |
| --- | --- | --- | --- | --- | --- | --- | ----------- | ------- | ---- | --- | --- | --- |
|     | 19  | A8  |     |     |     |     |             | = i +   |      |     |     |     |
|     |     |     |     |     |     |     | i           |         | j;   |     |     |     |
|     | 20  |     |     |     |     |     | k           | = k +   | 1;   |     |     |     |
|     | 21  |     |     |     |     |     |             | = 0;    |      |     |     |     |
goto j
|     | 22  | A9  |     |     |     |     |     | LI; |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
23
|     |            | MO                   |        |     |         |       | )                 |              |       |              |            |      |
| --- | ---------- | -------------------- | ------ | --- | ------- | ----- | ----------------- | ------------ | ----- | ------------ | ---------- | ---- |
|     | 24         |                      |        |     |         |       | i = i             | + j;         |       |              |            |      |
|     | 25         | All                  |        |     |         |       | if (string[index] |              | '\0') |              |            |      |
|     |            | A12                  |        |     |         |       |                   | =            |       | {            |            |      |
|     | 26         |                      |        |     |         |       | j                 | 0;           |       |              |            |      |
|     | 27         | A13                  |        |     |         |       | goto              | LI           |       |              |            |      |
|     | 28         |                      |        |     |         | els)e |                   |              |       |              |            |      |
|     | 29         | A14                  |        |     |         |       |                   |              |       |              |            |      |
|     |            | A15                  | A16    |     |         | )     | = -1;             |              |       |              |            |      |
|     | 30         |                      |        |     |         |       | i                 |              |       |              |            |      |
|     | 31         |                      |        |     | return  | i;    |                   |              |       |              |            |      |
|     | 32         | A17                  |        |     |         |       |                   |              |       |              |            |      |
|     | Figure5-2. | Codeformodule"count" |        |     |         |       |                   |              |       |              |            |      |
| The |            | "count"              | module |     |         | count |                   |              |       |              | begin with | the  |
|     | error in   | the                  |        |     | is that | the   |                   | is incorrect | for   | strings that |            | let- |
'A' and in which the number ofoccurrences of 'B' not equal to the number ofoccur-
| ter |     |     |     |     |     |     |     |     | is  |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
'C
rences of This is because the module is really counting 'B's rather than 'C's. It could be
'C
fixed by exchanging the bodies ofthe "if statements that recognize 'B' and Figure 5-3
| shows |             |      |       |     | module |          |     |     |     |     |     |     |
| ----- | ----------- | ---- | ----- | --- | ------ | -------- | --- | --- | --- | --- | --- | --- |
|       | the control | flow | graph | for |        | "count." |     |     |     |     |     |     |
35

'
|     | :„ /. ;                     |     | '            |
| --- | --------------------------- | --- | ------------ |
| , ; | Cy c l omatic: F:l,owGr:aph |     | : ;,.„),:„„: |
' 1 [plot] [Save] [Conuert] [Foruard] |Backiijard| [Enlarge] iReduce] [cTose] [Help] '
t Page 1 of 1 3X
| Prograjn: Count |     | 01/18/96     |     |
| --------------- | --- | ------------ | --- |
| count (A)       |     | Superimposed |     |
1
| 1 Cyclomatic Graiph |     | Upward Flows | i s  |
| ------------------- | --- | ------------ | ---- |
| Cyclomatic 5        |     | Loop Exits   | -- - |
| Essential           |     | Plain Edges  |      |
S
Design 1
:
0 , :
/f2
/ 1
1
.13 \|l6
_17
| •-T |     |     | '   |
| --- | --- | --- | --- |
Figure5-3. Controlflowgraphformodule"count."
The "count" module illustrates the effectiveness of structured testing. The commonly used
statement and branch coverage testing criteria can both be satisfied with the two tests in Fig-
ure 5-4, none ofwhich detect the error. Since the complexity of"count" is five, it is i mmedi-
—
5-4 do
ately apparent that the tests ofFigure not satisfy the structured testing criterion three
additional are needed testeach decision independently. Figure 5-5 shows a set oftests
tests to
36

which
that satisfies the structured testing criterion, consists ofthe three tests from Figure 5-4
| plus | two   | additional |       | form | a complete |        |     |     |             |     |     |     |     |
| ---- | ----- | ---------- | ----- | ---- | ---------- | ------ | --- | --- | ----------- | --- | --- | --- | --- |
|      |       |            | tests | to   |            | basis. |     |     |             |     |     |     |     |
|      | Input |            |       |      | Output     |        |     |     | Correctness |     |     |     |     |
|      | X     |            |       |      | -1         |        |     |     | Correct     |     |     |     |     |
|      | ABCX  |            |       |      |            |        |     |     | Correct     |     |     |     |     |
1
|     | Figure5-4. |     | Testsfor"count" |     | thatsatisfystatementand |     |     |     | branch coverage. |     |     |     |     |
| --- | ---------- | --- | --------------- | --- | ----------------------- | --- | --- | --- | ---------------- | --- | --- | --- | --- |
|     | Input      |     |                 |     | Output                  |     |     |     | Correctness      |     |     |     |     |
X
|     |     |     |     |     | -1  |     |     |     | Correct |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ------- | --- | --- | --- | --- |
ABCX
|     |     |     |     |     | 1   |     |     |     | Correct |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ------- | --- | --- | --- | --- |
A
|     |     |     |     |     | 0   |     |     |     | Correct |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ------- | --- | --- | --- | --- |
AB
|     |     |     |     |     | 1   |     |     |     | Incorrect |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --------- | --- | --- | --- | --- |
AC
|     |            |     |                 |     | 0                               |     |     |     | Incorrect  |     |     |     |     |
| --- | ---------- | --- | --------------- | --- | ------------------------------- | --- | --- | --- | ---------- | --- | --- | --- | --- |
|     |            |     | Testsfor"count" |     | thatsatisfythestructuredtesting |     |     |     |            |     |     |     |     |
|     | Figure5-5. |     |                 |     |                                 |     |     |     | criterion. |     |     |     |     |
| The |            |     |                 |     |                                 |     |     |     | "AB"       |     |     |     | "0" |
set oftests in Figure 5-5 detects the error (twice). Input should produce output
|       |         | produces |        | "1,"  | and     | "AC" |           |     | produce    |         | "1"       |         |       |
| ----- | ------- | -------- | ------ | ----- | ------- | ---- | --------- | --- | ---------- | ------- | --------- | ------- | ----- |
| but   | instead |          | output |       | input   |      | should    |     |            | output  | but       | instead | pro-  |
| duces | output  | "1."     | In     | any   | oftests |      |           | the | structured |         |           |         | guar- |
|       |         |          |        | fact, | set     | that | satisfies |     |            | testing | criterion |         | is    |
anteed to detect the error. To see this, note that to test the decisions nodes 3 and 7
at
independently requires at least one input with a different number of 'B's than 'C's.
Weak
| 5.5  |     | structured |     | testing |     |      |     |     |     |     |     |     |     |
| ---- | --- | ---------- | --- | ------- | --- | ---- | --- | --- | --- | --- | --- | --- | --- |
| Weak |     |            |     |         |     | weak |     | of  |     |     |     | can | be  |
structured testing is, as it appears, a variant structured testing. It satis-
fied by exercising least v(G) different paths through the control flow graph while simulta-
at
neously covering allbranches, howeverthe requirementthatthepaths formabasis dropped.
is
Weak
Structured testing subsumes weak structured testing, but not the reverse. structured
much
testing is easierto perform manually than structured testing, because there is no needto
| do  |        | algebra | on path |          | Thus, | weak |            |     | was     | way |     | some | ofthe |
| --- | ------ | ------- | ------- | -------- | ----- | ---- | ---------- | --- | ------- | --- | --- | ---- | ----- |
|     | linear |         |         | vectors. |       |      | structured |     | testing | a   | to  | get  |       |
benefits ofstructured testing a significantly lesser cost before automated support for struc-
at
tured testing was available, and is worth considering for programming languages with no
still
automated structured testing support. In some older literature, no distinction is made between
two
the criteria.
Ofthe three properties ofstructured testing discussed in section 5.2, two are shared by weak
structured testing. It subsumes statement andbranch coverage, which provides abase level of
error detection effectiveness. It also requires testing proportional to complexity, which con-
|     |     |     | on  | most |     |     | and |     |     |     |     |     | and mon- |
| --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- | -------- |
centrates testing the error-prone software supports precise test planning
However, does not decision outcomes be tested independently, and
| itoring. |     |     | it  |     | require | all |     |     | to  |     |     |     |     |
| -------- | --- | --- | --- | --- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
37

thus may not detect errors based on interactions between decisions. Therefore, should only
it
when
| be used  |            | structured |              | testing | itselfis | impractical. |      |         |     |       |             |     |
| -------- | ---------- | ---------- | ------------ | ------- | -------- | ------------ | ---- | ------- | --- | ----- | ----------- | --- |
| 5.6      | Advantages |            | ofautomation |         |          |              |      |         |     |       |             |     |
| Although |            |            |              | can     | be       | manually     |      |         | 6   | way   |             |     |
|          | structured |            | testing      |         |          | applied      | (see | section |     | for a | to generate | a   |
basis ofpaths without doing linear algebra), use ofan automated tool provides several
set
compelling advantages. The relevant features ofan automated tool are the ability to instru-
ment software to track the paths being executed during testing, the ability to report the number
ofindependent paths that have been tested, and the ability to calculate a minimal set oftest
|           | would   |         | complete |              |       | any     |             | have     | been |          | Forcomplex  |       |
| --------- | ------- | ------- | -------- | ------------ | ----- | ------- | ----------- | -------- | ---- | -------- | ----------- | ----- |
| paths     | that    |         |          | testing      | after | given   | set oftests |          |      | run.     |             | soft- |
| ware,     | the     |         | report   | dependencies |       | between | decision    | outcomes |      |          | also        |       |
|           | ability |         | to       |              |       |         |             |          |      | directly | is helpful, | as    |
| discussed | in      | section | 9.       |              |       |         |             |          |      |          |             |       |
A
typical manual process is to examine each software module being tested, derive the control
flow graph, select a basis set oftests to execute (with the technique ofsection 6), determine
|       |           |      |          | each |       | and execute |     |        | Although |      | process | can  |
| ----- | --------- | ---- | -------- | ---- | ----- | ----------- | --- | ------ | -------- | ---- | ------- | ---- |
| input | data that | will | exercise |      | path, |             | the | tests. |          | this |         | cer- |
tainly be used effectively, has several drawbacks when compared with an automated pro-
it
cess.
A
typical automated process is to leverage the "black box" functional testing in the structured
|     |     |     |     |     |     | anduse |     |     |     |     | ofpoorcoverage. |     |
| --- | --- | --- | --- | --- | --- | ------ | --- | --- | --- | --- | --------------- | --- |
testing effort. Firstrun the functional tests, the tool to identify areas
Often, process can be as the poor coverage can be associated with areas offunc-
|     | this |     |     | iterated, |     |     |     |     |     |     |     |     |
| --- | ---- | --- | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
tionality, and more functional tests developed for those areas. An important practical note
is
that is easier to test statements and branches than paths, and testing a new statement or
it
branch is always guaranteed to improve structured testing coverage. Thus, concentrate first
| on  |     |     |     |     |     |     | move |     |     |     | Near | end |
| --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | ---- | --- |
the untested branch outputs ofthe tool, and then on to untested paths. the
| ofthe |     | use |     |     |     |     |     | dependencies" |     |     |     |     |
| ----- | --- | --- | --- | --- | --- | --- | --- | ------------- | --- | --- | --- | --- |
process, the tool's "untested paths" or "control outputs to derive
| inputs | that | complete | the | structured |     | testing process. |     |     |     |     |     |     |
| ------ | ---- | -------- | --- | ---------- | --- | ---------------- | --- | --- | --- | --- | --- | --- |
By building on a black-box, functional test suite, the automated process bypasses the labor-
num-
intensive process ofderiving input data for specific paths except for the relatively small
|     |     |     |     | augmentthe |     |     |     | complete |     |     |     | This |
| --- | --- | --- | --- | ---------- | --- | --- | --- | -------- | --- | --- | --- | ---- |
ber ofpaths necessary to functional test suite to structured testing.
advantage even larger than may appear since functional done on a com-
|     | is  |     |     |     | it  | at first, |     |     |     | testing | is  |     |
| --- | --- | --- | --- | --- | --- | --------- | --- | --- | --- | ------- | --- | --- |
pleteexecutable program, whereas deriving datatoexecute specific paths (oreven statements)
is often only practical for individual modules or small subprograms, which leads to the
expense ofdeveloping stub and driver code. Finally, and perhaps most significantly, an auto-
| mated |     |     |     |     |     |     |     | was |     |     | Manual |     |
| ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ | --- |
tool provides accurate verification that the criterion successfully met. der-
ivation oftest data an error-prone process, in which the intended paths are often not
is
exercised by a given data set. Hence, ifan automated tool available, using to verify and
|          |          |     |         |            |     |     |     | is  |     |     | it  |     |
| -------- | -------- | --- | ------- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
| complete | coverage |     | is very | important. |     |     |     |     |     |     |     |     |
38

5.7 Critical software
Differenttypes ofsoftware require different levels oftesting rigor. All code worth developing
is worth having basic functional and structural testing, forexample exercising all ofthe major
requirements and all ofthe code. In general, most commercial and government software
should be tested more stringently. Each requirement in a detailed functional specification
should be tested, the software should be tested in a simulated production environment (and is
typically beta tested in a real one), at least all statements and branches should be tested for
each module, and structured testing should be used for key or high-risk modules. Where qual-
ity is a major objective, structured testing should be applied to all modules. These testing
methods form a continuum offunctional and structural coverage, from the basic to the inten-
sive. For truly critical software, however, a qualitatively different approach is needed.
Critical software, in which (forexample) failure can result in the loss ofhuman life, requires a
unique approach to both development and testing. For this kind of software, typically found
in medical and military applications, the consequences offailure are appalling [LEVESON].
Even in the telecommunications industry, where failure often means significant economic
loss, cost-benefit analysis tends to limit testing to the most rigorous ofthe functional and
structural approaches described above.
Although the specialized techniques forcritical software span the entire software lifecycle,
this section is focused on adapting structured testing to this area. Although automated tools
may be used to verify basis path coverage during testing, the techniques ofleveraging func-
tional testing to structured testing are not appropriate. The key modification is to not merely
exercise a basis set ofpaths, but to attempt as much as possible to establish correctness ofthe
software along each path ofthat basis set. First ofall, a basis set ofpaths facilitates structural
code walkthroughs and reviews. It is much easier to find errors in straight-line computation
than in a web ofcomplex logic, and each ofthe basis paths represents a potential single
sequence ofcomputational logic, which taken together represent the full structure ofthe orig-
inal logic. The next step is to develop and execute several input datasets foreach ofthe paths
in the basis. As with the walkthroughs, these tests attempt to establish correctness ofthe soft-
ware along each basis path. It is important to give special attention to testing the boundary
values of all data, particularly decision predicates, along that path, as well as testing the con-
tribution ofthat path to implementing each functional requirement.
Although no software testing method can ensure correctness, these modifications ofthe struc-
tured testing methodology for critical software provide significantly more power to detect
errors in return for the significant extra effort required to apply them. It is important to note
that, especially for critical software, structured testing does not preclude the use ofother tech-
niques. A notable example is exhaustive path testing: for simple modules without loops, it
may be appropriate to test all paths ratherthanjust abasis. Many critical systems may benefit
from using several different techniques simultaneously [NIST234].
39

6 The Baseline Method
The baseline method, described in this section, is a technique for identifying a set ofcontrol
paths to satisfy the structured testing criterion. The technique results in a basis set oftest
paths through the module being tested, equal in number to the cyclomatic complexity ofthe
module. As discussed in section 2, the paths in a basis are independent and generate all paths
via linear combinations. Note that "the baseline method" is different from "basis path test-
ing." Basis path testing, anothername for structured testing, is the requirement that abasis set
ofpaths should be tested. The baseline method is one way to derive a basis set ofpaths. The
word "baseline" comes from the first path, which is typically selected by the tester to repre-
sent the "baseline" functionality ofthe module. The baseline method provides support for
structured testing, since it gives a specific technique to identify an adequate test setratherthan
resorting to trial and error until the criterion is satisfied.
6.1 Generating a basis set ofpaths
The idea is to start with abaseline path, then vary exactly one decision outcome to generate
each successive path until all decision outcomes have been varied, at which time a basis will
have been generated. To understand the mathematics behind the technique, a simplified ver-
sion ofthe method will be presented and prove that it generates a basis [WATSONS] . Then,
the general technique that gives more freedom to the tester when selecting paths will be
described. Poole describes and analyzes an independently derived variant in [NIST5737].
6.2 The simplified baseline method
To facilitate the proofofcorrectness, the method will be described in mathematical terms.
Readers not interested in theory may preferto skip to section 6.2.2 where a more practical pre-
sentation ofthe technique is given.
In addition to a basis set ofpaths, which is a basis for the rows ofthe path/edge matrix ifall
possible paths were represented, it is possible to also consider a basis set ofedges, which is a
basis forthe columns ofthe same matrix. Since row rank equals column rank, the cyclomatic
complexity is also the number ofedges in every edge basis. The overall approach ofthis sec-
tion is to first select a basis set ofedges, then use that set in the algorithm to generate each
successive path, and finally use the resulting path/edge matrix restricted to basis columns to
show that the set ofgenerated paths is abasis.
41

First, for every decision in the module, select an outcome with the shortest (in terms ofnumber
ofother decisions encountered) path to the module exit. Ties can be broken arbitrarily. Mark
|     |     |     | outcomes |     |     | outcomes |     |     |     |     |
| --- | --- | --- | -------- | --- | --- | -------- | --- | --- | --- | --- |
these selected decision non-basic. Call these non-basic because all other
decision outcome edges, along with the module entry edge, form column The key
|     |     |     |     |     |     |     | the |     | basis. | to  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ | --- |
the simplified baseline method to execute exactly one new basis edge with each successive
is
path. This is possible because from any node in the control flow graph, there is apath to the exit
node that avoids all basis columns (taking the non-basic outcome ofevery decision encoun-
which
tered, also gives a shortest path in terms ofdecisions encountered to the exit).
The simplified baseline algorithm can now be described. For the baseline take
|     |     |     |     |     |     |     | initial |     | path, | the |
| --- | --- | --- | --- | --- | --- | --- | ------- | --- | ----- | --- |
non-basic outcome ofevery decision encountered. Note that this gives a shortest path through
the module. For each successive path, first pick any decision that has had the non-basic out-
come
traversed by an earlier path, but that has a basis outcome that has not been executed by
|     |     |     |     | by  |     |     |     | up  |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
any earlier path. Then, constructthe path following the earlierpath to that decision point,
new outcome edge, and then follow only non-basic decision outcomes
| traverse | that | basis |     |     |     |     |     |     |     | to the |
| -------- | ---- | ----- | --- | --- | --- | --- | --- | --- | --- | ------ |
module At each step, exactly one new basis edge added, so the number ofpaths
|     | exit. |     |     |     |     | is  |     | total |     |     |
| --- | ----- | --- | --- | --- | --- | --- | --- | ----- | --- | --- |
generated is the cyclomatic complexity. sufficient to show that they are linearly indepen-
|     |     |     |     | It is |     |     |     |     |     |     |
| --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- |
dent to complete the proofthat they are abasis set ofpaths. To see that, consider the path/edge
matrix with the generated set ofpaths in order as the rows and the basis edges as the columns,
|     | columns |     | by  | index | which |     |     | each |     |     |
| --- | ------- | --- | --- | ----- | ----- | --- | --- | ---- | --- | --- |
with the ordered the ofthe path first traversed corresponding
edge. The matrix then lower-triangular with major diagonal equal "1," so
|     |     | is  |     |     | all |     | entries |     | to  | all |
| --- | --- | --- | --- | --- | --- | --- | ------- | --- | --- | --- |
rows are linearly independent. Thus, the simplified baseline algorithm generates a basis.
| 6.3      | The baseline | method |     | in practice |     |     |     |     |     |     |
| -------- | ------------ | ------ | --- | ----------- | --- | --- | --- | --- | --- | --- |
| Although |              |        |     | method      |     |     |     |     |     |     |
the simplified baseline ofthe previous section has the advantages oftheoreti-
elegance and aconcise proofofcorrectness, lack offlexibility and on
| cal |     |     |     |     | its |     |     | its | reliance | shortest |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | -------- | -------- |
paths are drawbacks in practice. The general technique allows the tester to choose between var-
ious alternatives when generating paths, so that a more robust set oftests can be developed.
This is important for two reasons. First, although executing any basis set ofpaths assures acer-
|     |     |     |     | may |     |     | some |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- |
tain level oftesting rigor, a test designer recognize that major functional paths are
| more | important |            |        | than     | some | ofthe paths | given | by  |            |       |
| ---- | --------- | ---------- | ------ | -------- | ---- | ----------- | ----- | --- | ---------- | ----- |
|      |           | to include | in the | test set |      |             |       | the | simplified | tech- |
nique. Second, may be impossible to execute some paths due to the specifics ofthe module's
it
computation, and any addedflexibility helps avoidthose impossiblepaths while developing
still
| a robust | set | oftests. |     |     |     |     |         |     |     |     |
| -------- | --- | -------- | --- | --- | --- | --- | ------- | --- | --- | --- |
| The      |     |          |     |     |     |     | program |     |     |     |
first step is to pick a functional "baseline" path through the that represents a legit-
imate function and notjust an error The selection ofthis baseline path somewhat arbi-
|     |     |     |     | exit. |     |     |     |     | is  |     |
| --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- |
trary. The key, however, to pick a representative function rather than an exceptional
is
condition. The exceptional conditions will ofcourse be tested on some path generated by the
many
method, but since ofthe decision outcomes along the baseline path tend to be shared with
42

several other paths it is helpful to make them as "typical" as possible. To summarize, the
baseline should be, in the tester'sjudgement, the most important path to test. It is usually
helpful to devote extra effort to the baseline path, exercising all its functional requirements
and developing several data sets that might expose errors.
To generate the next path, change the outcome ofthe first decision along the baseline path
while keeping the maximumnumberofotherdecision outcomes the same as thebaselinepath.
That is, once the baseline path is "rejoined," it should be followed to the module exit. Any
decisions encountered that are not part ofthe baseline path may be taken arbitrarily, and, as
with the baseline path, it is a good idea to follow a robust functional path subject to the con-
straint of varyingjust the first baseline decision. To generate the third path, begin again with
the baseline but vary the second decision outcome rather than the first. When all of the deci-
sions along the baseline have been flipped, proceed to the second path, flipping its new deci-
sions as if it were the baseline. When every decision in the module has been flipped, the test
path set is complete. Multiway decisions must ofcourse be flipped to each oftheir possible
outcomes in turn.
Sometimes a tester wants even more flexibility, relaxing the requirement that once rejoined,
the path from which a decision was flipped is followed to the end. Unfortunately, this may
result in a linearly dependent set ofpaths, not satisfying the structured testing criterion
(although weak structured testing is still satisfied). For complete freedom in selecting test
paths for structured testing, the answer lies with an automated tool. The tester can specify
arbitrary paths by their decision outcome sequence, and the tool then determines whethereach
new path is linearly independent ofthe previous ones in the same way that it would analyze
the execution trace ifthe paths were actually executed during testing. Similarly, the tool can
at any stage produce a minimal set ofpaths to complete the basis set, which the tester can
either accept or change. Even with the standard baseline method, it may be worth having a
tool verify that a basis has indeed been generated, since it takes much less effort to correct the
test set in the test planning stage than after the tests have already been executed.
43

| 6.4 Example |     | ofthe | baseline | method |     |     |     |     |     |
| ----------- | --- | ----- | -------- | ------ | --- | --- | --- | --- | --- |
The baseline method is now demonstrated using the "count" program from section Refer
5.4.
to Figure 5-2 forthe source code. Figure 6-1 shows the control flow graph for "count" with
| the decision | outcomes |     | marked. |     |     |     |     |     |     |
| ------------ | -------- | --- | ------- | --- | --- | --- | --- | --- | --- |
fForwd]
|     |     | |piot]      | jSave| (convert | I   | fiackMai-d] {Enlarge] | |Reduce | jciose] | jHelp| |     |     |
| --- | --- | ----------- | --------------- | --- | --------------------- | ----------------- | ------ | --- | --- |
|     |     | Page        | of 3X           |     |                       |                   |        |     |     |
|     |     |             | 1 1             |     |                       |                   |        |     |     |
|     |     | Program:    | Count           |     |                       | 01/18/96          |        |     |     |
|     |     | count       | (A)             |     |                       | Superimposed      |        |     |     |
|     |     | Cyclomatic  | Graph           |     |                       | Upward            | Flows  |     |     |
|     |     | Cycloraatic | 5               |     |                       | Loop              | Exits  |     |     |
|     |     | Eseential   | 5               |     |                       | Plain             | Edges  |     |     |
Design
1
Graphof"count"
|     |     | Figure6-1. |     |     | withdecisionoutcomesmarked. |     |     |     |     |
| --- | --- | ---------- | --- | --- | --------------------------- | --- | --- | --- | --- |
Figure 6-2 shows the set oftest paths constructed by the method. The baseline path corre-
sponds to input "AB", a representative functional input (which happens to expose the mod-
|            |     |              |          |        |          | "=A" TRUE, | "=B" TRUE, | "=B" | FALSE |
| ---------- | --- | ------------ | -------- | ------ | -------- | ---------- | ---------- | ---- | ----- |
| ule's bug, | the | goal ofevery | baseline | test). | It takes |            |            |      |       |
does notcount flipping the "=B" "=C" FALSE, and "!='\0'" FALSE.
| (note, this |     |     | as  |     | decision!), |     |     |     |     |
| ----------- | --- | --- | --- | --- | ----------- | --- | --- | --- | --- |
The second path generated by flipping the decision along the baseline, so takes "=A"
|     |     | is  |     |     | first |     |     | it  |     |
| --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- |
FALSE, and there are no other decisions before the module exit. It corresponds to input "X."
|     |     |     |     |     |     |     | "=A" | TRUE |     |
| --- | --- | --- | --- | --- | --- | --- | ---- | ---- | --- |
The third path flips the second decision along the baseline, so it takes (following
|           |            | "=B" | FALSE |           | second |            | "=C" FALSE |          | up  |
| --------- | ---------- | ---- | ----- | --------- | ------ | ---------- | ---------- | -------- | --- |
| the first | decision), |      |       | (flipping | the    | decision), |            | (picking | the |
44

|          |         |     | and "!='\0"' |     | FALSE | (following |     |          |     |           |     | corresponds |     |
| -------- | ------- | --- | ------------ | --- | ----- | ---------- | --- | -------- | --- | --------- | --- | ----------- | --- |
| baseline | again), |     |              |     |       |            | the | baseline | to  | the end). | It  |             | to  |
input "A." The fourth path the third decision along the baseline, so takes "=A" TRUE
|     |     |     |     | flips |     |      |     |     |     |     | it  |       |     |
| --- | --- | --- | --- | ----- | --- | ---- | --- | --- | --- | --- | --- | ----- | --- |
|     |     |     |     |       |     | TRUE |     |     |     |     |     | FALSE |     |
(following the first decision), "=B" (following the second decision), "=B"
—
(still following the second decision when a decision is revisited due to looping it is not con-
|     |     |     |     |     |     |     |     | "=C" TRUE |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --------- | --- | --- | --- | --- | --- |
sidered a separate decision for flipping purposes), (flipping the third decision),
| "=B" | FALSE |          |     | up  |          |     |          | occurrence | ofthe | "=B" |          |        |      |
| ---- | ----- | -------- | --- | --- | -------- | --- | -------- | ---------- | ----- | ---- | -------- | ------ | ---- |
|      |       | (picking |     | the | baseline | at  | the last |            |       |      | decision | rather | than |
going through the loop again), "=C" FALSE (continuing to follow the rest ofthe baseline),
FALSE
"!='\0"' (following thebaseline to the end). It corresponds to input "ABC." The fifth
TRUE
and final path flips the fourth and final decision, so it takes "=A" (following), "=B"
| TRUE   |              |       | "=B"     | FALSE |              |          | "=C"    | FALSE        |              |              | "!='0"' | TRUE     |        |
| ------ | ------------ | ----- | -------- | ----- | ------------ | -------- | ------- | ------------ | ------------ | ------------ | ------- | -------- | ------ |
|        | (following), |       |          |       | (following), |          |         |              | (following), |              |         |          | (flip- |
|        | "=B"         | FALSE | (picking |       | up           |          |         | "=C"         | FALSE        |              |         | "!='\0"' |        |
| ping), |              |       |          |       | the          | baseline | again), |              |              | (following), |         |          |        |
| FALSE  | (following   |       | to the   | end). | corresponds  |          | to      | input "ABX." |              |              |         |          |        |
It
|     |     |     | TestPath |     | (baseline): | 01234523671011 |        |     | 14 16 17 |     |     |     |     |
| --- | --- | --- | -------- | --- | ----------- | -------------- | ------ | --- | -------- | --- | --- | --- | --- |
|     |     |     |          | 1   |             |                | =>TRUE |     |          |     |     |     |     |
string[index]='A'
|     |     |     |     | 11( 1): |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
=>TRUE
|     |     |     |     | 13( 3):  | string[index]='B'   |     |          |       |     |     |     |     |     |
| --- | --- | --- | --- | -------- | ------------------- | --- | -------- | ----- | --- | --- | --- | --- | --- |
|     |     |     |     |          |                     |     | =>       | FALSE |     |     |     |     |     |
|     |     |     |     | 13( 3):  | string[index]=='B'  |     |          |       |     |     |     |     |     |
|     |     |     |     | 18( 7):  | string[index]=='C'  |     | ==>FALSE |       |     |     |     |     |     |
|     |     |     |     | 25( 11): | string[index]!='\0' |     | ==>FALSE |       |     |     |     |     |     |
0
|     |     |     | TestPath | 2:  | 1 15                  | 16 17 |           |       |     |     |     |     |     |
| --- | --- | --- | -------- | --- | --------------------- | ----- | --------- | ----- | --- | --- | --- | --- | --- |
|     |     |     |          |     |                       |       | =>        | FALSE |     |     |     |     |     |
|     |     |     |          | 11( | 1): string[index]='A' |       |           |       |     |     |     |     |     |
|     |     |     | TestPath |     | 0 23                  | 67 10 | 14 16 17  |       |     |     |     |     |     |
|     |     |     |          | 3:  | 1                     |       | 11 =>TRUE |       |     |     |     |     |     |
string[index]='A'
|     |     |     |     | 11( | 1): |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
==>FALSE
|     |     |     |            | 13( 3):  | string[index]=='B'  |     |          |       |          |     |     |     |     |
| --- | --- | --- | ---------- | -------- | ------------------- | --- | -------- | ----- | -------- | --- | --- | --- | --- |
|     |     |     |            |          |                     |     | =>       | FALSE |          |     |     |     |     |
|     |     |     |            | 18( 7):  | string[index]='C'   |     |          |       |          |     |     |     |     |
|     |     |     |            | 25( 11): | string[index]!='\0' |     | ==>FALSE |       |          |     |     |     |     |
|     |     |     | TestPath4: |          | 0123452367892367    |     |          | 10    | 14 16 17 |     |     |     |     |
11
|     |     |     |     |     | string[index]=='A' |     | ==>TRUE |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | ------------------ | --- | ------- | --- | --- | --- | --- | --- | --- |
|     |     |     |     | 11( | 1):                |     |         |     |     |     |     |     |     |
=>TRUE
|     |     |     |     | 13( 3): | string[index]='B' |     |          |     |     |     |     |     |     |
| --- | --- | --- | --- | ------- | ----------------- | --- | -------- | --- | --- | --- | --- | --- | --- |
|     |     |     |     | 13( 3): | string[index]='B' |     | ==>FALSE |     |     |     |     |     |     |
=>TRUE
|     |     |     |     | 18( | string[index]=='C' |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | ------------------ | --- | --- | --- | --- | --- | --- | --- | --- |
7):
|     |     |     |     |         | string[index]='B' |     | ==>FALSE |     |     |     |     |     |     |
| --- | --- | --- | --- | ------- | ----------------- | --- | -------- | --- | --- | --- | --- | --- | --- |
|     |     |     |     | 13( 3): |                   |     |          |     |     |     |     |     |     |
==>FALSE
|     |     |     |     | 18( 7): | string[index]='C' |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | ------- | ----------------- | --- | --- | --- | --- | --- | --- | --- | --- |
==>FALSE
|     |     |     |          | 25( 11): | string[index]!='\0' |     |          |          |          |       |     |     |     |
| --- | --- | --- | -------- | -------- | ------------------- | --- | -------- | -------- | -------- | ----- | --- | --- | --- |
|     |     |     | TestPath |          | 0 2345              | 23  | 67 10 11 | 12 13 23 | 67 10 11 | 14 16 | 17  |     |     |
|     |     |     |          | 5:       | 1                   |     | =>TRUE   |          |          |       |     |     |     |
string[index]='A'
|     |     |     |     | 11( | 1): |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
=>TRUE
|     |     |     |     | 13( | 3): string[index]='B' |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
=>FALSE
|     |     |     |     | 13( | 3): string[index]=='B' |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | ---------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
=>FALSE
|     |     |     |     | 18(  | 7): string[index]='C' |     |         |     |     |     |     |     |     |
| --- | --- | --- | --- | ---- | --------------------- | --- | ------- | --- | --- | --- | --- | --- | --- |
|     |     |     |     | 25(  | string[index]!='\0'   |     | ==>TRUE |     |     |     |     |     |     |
|     |     |     |     | 11): |                       |     | =>FALSE |     |     |     |     |     |     |
string[index]='B'
|     |     |     |     | 13( | 3): |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
=>FALSE
|     |     |     |     | 18( | 7): string[index]='C' |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
==>FALSE
|     |     |     |     | 25( 11):   | string[index]!='\0'    |     |     |                    |     |     |     |     |     |
| --- | --- | --- | --- | ---------- | ---------------------- | --- | --- | ------------------ | --- | --- | --- | --- | --- |
|     |     |     |     | Figure6-2. | Testpathsgeneratedwith |     |     | thebaselinemethod. |     |     |     |     |     |
45

Ofthe tests in Figure 6-2, thebaseUne and test 5 both detect the errorin the module. Although
this is a different set oftestpaths than the ones shown (by input data only) in Figure 5-5, both
sets satisfy the structured testing criterion and both sets detect the module's error. One ofthe
strengths ofboth the structured testing criterion and the baseline method is that testers have a
great deal offreedom when developing tests, yet the resultant tests have a guaranteed level of
rigor.
6.5 Completing testing with the baseline method
While the baseline method can be used to construct a stand-alone set oftests that satisfy the
structured testing criterion, it is usually most cost-effective to first run functional tests and
then only construct as many additional test paths as are necessary to have the entire testing
process satisfy the structured testing criterion [WATS0N5]. Assuming that it is possible to
trace paths during testing, specify paths manually, and determine the rank ofany set ofthose
paths (for example, using an automated tool), the baseline method can be used to execute the
minimum additional tests required.
The technique is to first run the functional test suite and (again, automation is key) fill matri-
ces with the paths that were executed. Next, for those modules that did not have a complete
basis set tested, use the baseline method to generate abasis set ofpaths. Then, for each ofthe
paths resulting from the basis set, determine whether it increases the matrix rank. Ifit does,
execute it; ifit does not, discard it. The new independentpaths that were not discarded form a
minimal set of additional paths to complete testing.
This technique works because, in essence, it extends an independent subset ofthe function-
ally-tested paths to form a basis. Regardless ofthe initial set ofpaths, adding each indepen-
dent member of a basis results in a set oftests that generates that basis and therefore also
generates all possible paths by linear combination. Additionally, no matter which basis is
selected first, each non-discarded member ofthe basis increases the rank ofthe matrix by
exactly one. The new tests are therefore guaranteed to be a minimal set. In fact, the number
ofnew tests will be the cyclomatic complexity minus the rank ofthe original set offunctional
tests.
It may seem that since an automated tool is required to perform the path tracing ofthe func-
tional test suite and the detennination whether each member ofthe basis generated by the
baseline method is independent, it is also possible to usejust the minimal set ofadditional test
paths provided by the tool rather than using the baseline method at all. Much ofthe time this
is true. However,just as testers benefit from using the baseline method rather than the simpli-
fied baseline method when planning structured testing from scratch, so also the freedom to
select candidate completion tests after functional testing is often valuable.
46

7 Integration Testing
In sections 2 and 5, cyclomatic complexity and the structured testing methodology are dis-
cussed at the level ofindividual modules and unit testing. This section generalizes the
approach to the integration level, addressing the complexity and integration testing of design
structures that consist ofmultiple modules.
7.1 Integration strategies
One ofthe most significant aspects of a software development project is the integration strat-
egy. Integration may be performed all at once, top-down, bottom-up, critical piece first, orby
first integrating functional subsystems and then integrating the subsystems in separate phases
using any ofthe basic strategies. In general, the larger the project, the more important the
integration strategy.
Very small systems are often assembled and tested in one phase. Formost real systems, this is
impractical for two major reasons. First, the system would fail in so many places at once that
the debugging and retesting effort would be impractical [PRESSMAN]. Second, satisfying
any white box testing criterion would be very difficult, because ofthe vast amount of detail
separating the input data from the individual code modules. In fact, most integration testing
has been traditionally limited to "black box" techniques [HETZEL]. Large systems may
require many integration phases, beginning with assembling modules into low-level sub-
systems, then assembling subsystems into larger subsystems, and finally assembling the high-
est level subsystems into the complete system.
To be most effective, an integration testing technique should fit well with the overall integra-
tion strategy. In a multi-phase integration, testing at each phase helps detect errors early and
keep the system under control. Performing only cursory testing at early integration phases
and then applying a more rigorous criterion for the final stage is reallyjust a variant ofthe
high-risk "big bang" approach. However, performing rigorous testing ofthe entire software
involved in each integration phase involves a lot ofwasteful duplication ofeffort across
phases. The key is to leverage the overall integration structure to allow rigorous testing at
each phase while minimizing duplication ofeffort.
It is important to understand the relationship between module testing and integration testing.
In one view, modules are rigorously tested in isolation using stubs and drivers before any inte-
gration is attempted. Then, integration testing concentrates entirely on module interactions,
assuming that the details within each module are accurate. At the other extreme, module and
47

,
|             |         | can | be combined, |           |     |     |         | ofeach | module's |     |                |     |
| ----------- | ------- | --- | ------------ | --------- | --- | --- | ------- | ------ | -------- | --- | -------------- | --- |
| integration | testing |     |              | verifying |     | the | details |        |          |     | implementation | in  |
an integration context. Many projects compromise, combining module with lowest
|     |     |     |     |     |     |     |     |     |     | testing |     | the |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------- | --- | --- |
level of subsystem integration testing, and then performing pure integration testing higher
at
levels. Each ofthese views ofintegration testing may be appropriate for any given project, so
method
an integration testing shouldbe flexible enough to accommodate them all. The restof
some
this section describes the integration-level structured testing techniques, first for special
| cases and | then |     | generality. |     |     |     |     |     |     |     |     |     |
| --------- | ---- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
in full
| 7.2 Combining |     | module | testing | and | integration |     |     | testing |     |     |     |     |
| ------------- | --- | ------ | ------- | --- | ----------- | --- | --- | ------- | --- | --- | --- | --- |
The simplest application ofstructured testing to integration is to combine module testing with
module
integration testing so that a basis set ofpaths through each is executed in an integra-
|               |     | This means |      | techniques |     |            |     | can | be used |         |              |     |
| ------------- | --- | ---------- | ---- | ---------- | --- | ---------- | --- | --- | ------- | ------- | ------------ | --- |
| tion context. |     |            | that | the        |     | of section |     | 5   |         | without | modification | to  |
measure the level oftesting. However, method only suitable for a subset ofintegration
|     |     |     |     |     | this |     | is  |     |     |     |     |     |
| --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- |
strategies.
The
most obvious combined strategy is pure "big bang" integration, in which the entire sys-
| tem assembled |     | and |           | one  |         | even     |       | module   |     |          | As        |       |
| ------------- | --- | --- | --------- | ---- | ------- | -------- | ----- | -------- | --- | -------- | --------- | ----- |
| is            |     |     | tested in | step | without |          | prior |          |     | testing. | discussed | ear-  |
|               |     | not |           | most |         | systems. |       | However, |     |          |           | makes |
lier, this strategy is practical for real at least in theory, it
efficient use oftesting resources. First, there no overhead associated with constructing
is
stubs and drivers to perform module testing or partial integration. Second, no additional inte-
gration-specifictests are requiredbeyondthemodule tests as determinedby structuredtesting.
|     |     |     |     |     |     |     |     |     | ofcombining |     | module |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ----------- | --- | ------ | --- |
Thus, despite its impracticality, this strategy clarifies the benefits test-
with
| ing | integration | testing | to  | the greatest | feasible |     | extent. |     |     |     |     |     |
| --- | ----------- | ------- | --- | ------------ | -------- | --- | ------- | --- | --- | --- | --- | --- |
is also possible to combine module and integration testing with the bottom-up integration
It
strategy. In this strategy, using test drivers but not stubs, begin by performing module-level
structured testing on the lowest-level modules using test drivers. Then, perform module-level
each
structured testing in a similar fashion at successive level ofthe design hierarchy, using
drivers foreach new module being tested integration with lower-level modules. Fig-
| test |     |     |     |     |     | in  |     |     | all |     |     |     |
| ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
ure 7-1 illustrates the technique. First, the lowest-level modules "B" and "C" are tested with
drivers. Next, the higher-level module "A" is tested with a driver in integration with modules
| "B" |     |     |     |     |     |     |     |     |     | module |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ | --- | --- |
and "C." Finally, integration could continue until the top-level ofthe program is
|              |      |       |          |             | with |     |        | program. |     | As shown | Figure | 7-  |
| ------------ | ---- | ----- | -------- | ----------- | ---- | --- | ------ | -------- | --- | -------- | ------ | --- |
| tested (with | real | input | data) in | integration |      | the | entire |          |     |          | in     | 1   |
the number oftests required by technique the sum ofthe cyclomatic complexities
| total |     |     |     | this |     |     | is  |     |     |     |     |     |
| ----- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
ofall modules being integrated. As expected, this the same number oftests that would be
is
required to perform structured testing on each module in isolation using stubs and drivers.
48

Driver
|     |     |     |     | Driver |     |     |     | Driver |     |     |     |
| --- | --- | --- | --- | ------ | --- | --- | --- | ------ | --- | --- | --- |
A
|     |     | forB |     | forC |     |     |     | for |     |     |     |
| --- | --- | ---- | --- | ---- | --- | --- | --- | --- | --- | --- | --- |
A
|     |     | B             |        |         | C     |     |     |     |     |     |     |
| --- | --- | ------------- | ------ | ------- | ----- | --- | --- | --- | --- | --- | --- |
|     |     | Phase         | Test a |         | of    |     |     |     |     |     |     |
|     |     | 1:            | basis  | set     |       |     |     |     |     |     |     |
|     |     |               | B      | C       |       |     |     |     |     |     |     |
|     |     | paths through |        | and     | using |     |     |     |     |     |     |
|     |     | drivers.      | Number | oftests |       |     |     |     |     |     |     |
is
+
|     |     | v(B) v(C). |     |     |     |       |         |              |                |     |     |
| --- | --- | ---------- | --- | --- | --- | ----- | ------- | ------------ | -------------- | --- | --- |
|     |     |            |     |     |     | Phase | 2:      | Test a basis | set of         |     |     |
|     |     |            |     |     |     |       | through | A            |                |     |     |
|     |     |            |     |     |     | paths |         |              | in integration |     |     |
B C
|     |     |     |     |     |     | with   | and | using   | a driver. |     |     |
| --- | --- | --- | --- | --- | --- | ------ | --- | ------- | --------- | --- | --- |
|     |     |     |     |     |     | Number |     | oftests | v(A).     |     |     |
is
|                |            | number                 |          |            |         | +              | +     | sum          |                  |     |     |
| -------------- | ---------- | ---------------------- | -------- | ---------- | ------- | -------------- | ----- | ------------ | ---------------- | --- | --- |
|                |            | Total                  | oftests  | is         | v(A)    | v(B)           | v(C), | the          | ofthe cyclomatic |     |     |
|                |            | complexities           | ofall    | integrated |         | modules.       |       |              |                  |     |     |
|                | Figure7-1. | Combiningmoduletesting |          |            |         | with bottom-up |       | integration. |                  |     |     |
| 73             |            |                        | ofmodule |            |         |                |       |              |                  |     |     |
| Generalization |            |                        |          |            | testing | criteria       |       |              |                  |     |     |
Module testing can often be generalized several possible ways support integra-
|     |     | criteria |     |     |     | in  |     |     | to  |     |     |
| --- | --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
tion testing. As discussed in the previous subsection, the most obvious generalization to
is
satisfy the module testingcriterion in an integration context, in effect using the entire program
However,
as atestdriverenvironmentforeach module. this trivial kindofgeneralization does
| not  | advantage | ofthe |             |     | between | module | and |             |          | Applying |       |
| ---- | --------- | ----- | ----------- | --- | ------- | ------ | --- | ----------- | -------- | -------- | ----- |
| take |           |       | differences |     |         |        |     | integration | testing. |          | it to |
each phase ofamulti-phase integration strategy, forexample, leads to an excessive amount of
| redundant | testing. |     |     |     |        |     |     |     |     |     |     |
| --------- | -------- | --- | --- | --- | ------ | --- | --- | --- | --- | --- | --- |
| More      |          |     |     |     | module |     |     |     |     |     |     |
useful generalizations adapt the testing criterion to focus on interactions
between modules than attempting ofthe ofeach module's implementa-
|     |     | rather |     |     | to  | test all | details |     |     |     |     |
| --- | --- | ------ | --- | --- | --- | -------- | ------- | --- | --- | --- | --- |
tion in an integration context. The statementcoverage module testing criterion, in which each
statement is requiredto be exercised during module testing, can be generalizedto require each
module call statement tobe exercised during integration testing. Although the specifics ofthe
more
generalization ofstructured testing are detailed, the approach is the same. Since stnic-
49

tured testing at the module level requires that all the decision logic in a module's control flow
graph be tested independently, the appropriate generalization to the integration level requires
|     |     |     |     | involved | with |     | modules |     |     |     |     |     | The |
| --- | --- | --- | --- | -------- | ---- | --- | ------- | --- | --- | --- | --- | --- | --- |
thatjust the decision logic calls to other be tested independently.
| following  | subsections |        | explore    |      | approach |            |     |     |     |     |     |     |     |
| ---------- | ----------- | ------ | ---------- | ---- | -------- | ---------- | --- | --- | --- | --- | --- | --- | --- |
|            |             |        |            | this |          | in detail. |     |     |     |     |     |     |     |
| 7.4 Module |             | design | complexity |      |          |            |     |     |     |     |     |     |     |
Ratherthan testing all decision outcomes within a module independently, structured testing at
|     |     |     |     | on  |     | outcomes |     |     |     |     | module |     |     |
| --- | --- | --- | --- | --- | --- | -------- | --- | --- | --- | --- | ------ | --- | --- |
the integration level focuses the decision that are involved with calls
[MCCABE2]. The design reduction technique helps those outcomes,
|     |     |     |     |     |     |     | identify |     | decision |     |     |     | so that |
| --- | --- | --- | --- | --- | --- | --- | -------- | --- | -------- | --- | --- | --- | ------- |
possible to exercise them independently during integration testing. The idea behind
it is
design reduction is to start with a module control flow graph, remove all control structures
that are not involved with module calls, and then use the resultant "reduced" flow graph to
shows
drive integration testing. Figure 7-2 a systematic set ofrules for performing design
|     | Although |     | not |     | reduction |     |     |     |     |     |     |     |     |
| --- | -------- | --- | --- | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
reduction. strictly a rule, the call rule states that function call ("black
dot") nodes cannot be reduced. The remaining rules work together to eliminate the parts of
the flow graph that are not involved with module calls. The sequential rule eliminates
sequences ofnon-call ("white dot") nodes. Since application ofthis rule removes one node
and one edge from the flow graph, it leaves the cyclomatic complexity unchanged. However,
|     |     |     | graph |     |     | can | be  |     | The |     |     |     |     |
| --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
it does simplify the so that the other rules applied. repetitive rule eliminates
loops not involved with module The conditional eliminates condi-
| top-test |     | that | are |     |     | calls. |     |     |     | rule |     |     |     |
| -------- | --- | ---- | --- | --- | --- | ------ | --- | --- | --- | ---- | --- | --- | --- |
tional statements that do not contain calls in their bodies. The looping rule eliminates bottom-
test loops that are not involved with module calls. It is important to preserve the module's
may
connectivity when using the looping rule, since for poorly-structured code it be hard to
distinguish the "top" of the loop from the "bottom." For the rule to apply, there must be a
| from |     | module |       |        |           | loop | and    | from |     | bottom |       | loop |        |
| ---- | --- | ------ | ----- | ------ | --------- | ---- | ------ | ---- | --- | ------ | ----- | ---- | ------ |
| path | the |        | entry | to the | top ofthe |      | a path |      | the |        | ofthe |      | to the |
module Since the conditional, and looping rules each remove one edge from
|          | exit.  |      | repetitive, |        |            |            |     |         |     |     |     |     |     |
| -------- | ------ | ---- | ----------- | ------ | ---------- | ---------- | --- | ------- | --- | --- | --- | --- | --- |
| the flow | graph, | they | each        | reduce | cyclomatic | complexity |     | by one. |     |     |     |     |     |
50

Rules 1 through 4 are intended to be appHed iteratively until none of them can be applied, at
| which |     |     |     | By  |     |     |     |     |
| ----- | --- | --- | --- | --- | --- | --- | --- | --- |
point the design reduction is complete. this process, even very complex logic can
| be eliminated | long | does         |             | any module |        |     |     |     |
| ------------- | ---- | ------------ | ----------- | ---------- | ------ | --- | --- | --- |
|               | as   | as it        | not involve |            | calls. |     |     |     |
|               |      |              |             | •          | •      |     |     |     |
|               |      | Rule 0: Call |             |            |        |     |     |     |
Rule
1: Sequential
|     |     | Rule 2: Repetitive  |     |     |     |     |     |     |
| --- | --- | ------------------- | --- | --- | --- | --- | --- | --- |
|     |     | Rule 3: Conditional |     |     |     |     |     |     |
|     |     | Rule Looping        |     |     |     |     |     |     |
4:
|     |     | • =  |      | O =      |      |     |     |     |
| --- | --- | ---- | ---- | -------- | ---- | --- | --- | --- |
|     |     | Call | node | Non-call | node |     |     |     |
®
|     |     | =     |        | more        | nodes    |     |     |     |
| --- | --- | ----- | ------ | ----------- | -------- | --- | --- | --- |
|     |     | Path  | ofzero | or          | non-call |     |     |     |
|     |     | = Any | node,  | or non-call |          |     |     |     |
call
|     |     | Figure7-2. Design | reduction |     |     |     |     |     |
| --- | --- | ----------------- | --------- | --- | --- | --- | --- | --- |
rules.
|     | shows |     |     |     |     |     | and4 |     |
| --- | ----- | --- | --- | --- | --- | --- | ---- | --- |
Figure 7-3 acontrol flow graph before and afterdesign reduction. Rules 3 can be
| applied immediately |     |                 | graph, |          |                  |        | Then | can be |
| ------------------- | --- | --------------- | ------ | -------- | ---------------- | ------ | ---- | ------ |
|                     |     | to the original |        | yielding | the intermediate | graph. | rule | 1      |
applied three times to the conditional branch, which point rule 3 can be applied again,
|     |     | left |     | at  |     |     |     |     |
| --- | --- | ---- | --- | --- | --- | --- | --- | --- |
afterwhichfive more applications ofrule complete the reduction. The second application of
1
51

rule 3 that aconditional structure may be eliminated even body
| illustrates |     |     |     |     | ifits | contains acall |
| ----------- | --- | --- | --- | --- | ----- | -------------- |
node, as long as there is at least one path through body that does notcontain any call nodes.
its
|     | Original graph, |     | Intermediate | graph,        | Reduced | graph, |
| --- | --------------- | --- | ------------ | ------------- | ------- | ------ |
|     | v(G) = 5        |     | after        | rules 3 and 4 | v(G) =  | 2      |
|     |                 |     | have         | been          |         |        |
applied
|     |     | O          | #    |        |     |     |
| --- | --- | ---------- | ---- | ------ | --- | --- |
|     |     | = Non-call | node | = node |     |     |
Call
|     | Figure7-3. Design | reduction | example. |     |     |     |
| --- | ----------------- | --------- | -------- | --- | --- | --- |
The module design complexity, defined the cyclomatic complexity ofthe reduced
|     |     | iv(G), | is  | as  |     |     |
| --- | --- | ------ | --- | --- | --- | --- |
graph after design reduction has been performed. In Figure 7-3, the module design complex-
ity is 2. The design flow graph in Figure 7-4 displays the logic that contributes to module
design complexity superimposed on the entire control flow graph for a module with cyclo-
module
| matic complexity | 6 and |     | design complexity | 3.  |     |     |
| ---------------- | ----- | --- | ----------------- | --- | --- | --- |
52

!"
, ;
|     |     |     | i7;:ii      | Flowgraphs |          | for fjal  | analyze line' | in '   | prsftn' |      |     |     |
| --- | --- | --- | ----------- | ---------- | -------- | --------- | ------------- | ------ | ------- | ---- | --- | --- |
|     |     |     | Plot fSave] | ConverT]   | [Forward | [Backward | Enlarge       | Reduce | Close   | Help |     |     |
|     |     |     |             |            |          | |         | |             |        |         |      |     |     |
|     |     |     | Page 1 of   | 1 2X       |          |           |               |        |         |      |     |     |
IF
H
|     |     |     | Program:     | prsftn           |     |     | 04/02/96 |                |     |     | B   |     |
| --- | --- | --- | ------------ | ---------------- | --- | --- | -------- | -------------- | --- | --- | --- | --- |
|     |     |     | F i l e: h a | l s t ea d . c   |     |     | S u p e  | r im p o s e d |     |     |     |     |
|     |     |     | h a l an a l | p z e l i ne (J) |     |     | u p w a  | r d F l o w s  |     |     | H   |     |
|     |     |     | Language:    |                  |     |     | Loop     | Exits          |     |     |     |     |
|     |     |     |              | c                |     |     |          |                |     |     | H   |     |
|     |     | ;   | Design Graph |                  |     |     | Plain    | Edges          |     |     | H   |     |
|     |     |     | Cpclomatic   | 6                |     | ^0  |          |                |     |     |     |     |
|     |     |     | Essential    |                  |     |     |          |                |     |     | BH| |     |
Design
|     |     |     | 3   |          |     | J i    |     |     |     |     |     |     |
| --- | --- | --- | --- | -------- | --- | ------ | --- | --- | --- | --- | --- | --- |
|     |     |     |     | \ /^^""^ |     | ^"^11* |     |     |     |     |     |     |
1
1
\
\
\
i
\
1^20*
i
|     |     | i   |     | —   | *inclicatescallnocl—es |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | ---------------------- | --- | --- | --- | --- | --- | --- | --- |
|
|     |     |            |        | """   |      |                |     |     |     | ..»-.."..»...,m,.I |     |     |
| --- | --- | ---------- | ------ | ----- | ---- | -------------- | --- | --- | --- | ------------------ | --- | --- |
|     |     | '          | r      |       |      |                |     |     | .   |                    |     |     |
|     |     | Figure7-4. | Design | graph | with | v(G) = 6,iv(G) | =   |     |     |                    |     |     |
3.
| When |            |     |         |             | been | performed |     | module |        | module |        | com- |
| ---- | ---------- | --- | ------- | ----------- | ---- | --------- | --- | ------ | ------ | ------ | ------ | ---- |
|      | structured |     | testing | has already |      |           | at  | the    | level, |        | design |      |
plexity can be used drive integration requiring a basis ofpaths through each
|     |     |     | to  |     |     | testing, |     |     | set |     |     |     |
| --- | --- | --- | --- | --- | --- | -------- | --- | --- | --- | --- | --- | --- |
module's reduced graph to be tested in integration. Forthe bottom-up integration strategy dis-
cussed in section 7-2, the total number of integration tests becomes the sum ofthe module
design complexities ofall modules being integrated. Since module design complexity can be
number
significantly less than cyclomatic complexity, this technique reduces the ofintegra-
|      |        |         |            | process |     | ofderiving | data | for each |      | path, since | there | are |
| ---- | ------ | ------- | ---------- | ------- | --- | ---------- | ---- | -------- | ---- | ----------- | ----- | --- |
| tion | tests. | It also | simplifies | the     |     |            |      |          | test |             |       |     |
fewer constraints on paths through the reduced graph than on paths through the full graph.
53

| 7.5 Integration |     | complexity |     |         |     |     |     |
| --------------- | --- | ---------- | --- | ------- | --- | --- | --- |
| The             |     |            |     | program |     |     |     |
integration complexity, Sj, is defined for a with n modules (Gi through 0^) by
the formula: S| = (Z iv(Gj)) - n + [MCCABE2]. Integration complexity measures the num-
1
ber ofindependent integration tests through an entire program's design. To understand the
formula, recall the baseline method ofsection 6 for generating a set ofindependent tests
through an individual module. The analogous integration-level method generates a set of
|     |     |     |     | Begin |     | which |     |
| --- | --- | --- | --- | ----- | --- | ----- | --- |
independent tests through the program's design. with abaseline test, contributes
formula and one path through program's main module. Then, make
| 1 to the Sj |     | exercises |     | the     |     |     |     |
| ----------- | --- | --------- | --- | ------- | --- | --- | --- |
|             |     |           | new | outcome |     |     |     |
each successive test exercise exactly one decision in exactly one module's
| design-reduced |        | Since |                       | path through | each | module comes |      |
| -------------- | ------ | ----- | --------------------- | ------------ | ---- | ------------ | ---- |
|                | graph. | the   | first "mini-baseline" |              |      |              | as a |
result ofexercising a path in a higher-level module (except for the main module, which gets
firstpath from the baseline test), each module contributes anumberofnew integration tests
its
ofZ
equal to one less than its module design complexity, for a total contribution (iv(Gi) -
1),
which (smce there are n modules) equals (E iv(Gi)) - n. Adding the for the baseline test
1
|           | formula. | A       | argument shows |                   | v(G) | iv(G) |           |
| --------- | -------- | ------- | -------------- | ----------------- | ---- | ----- | --------- |
| gives the | full Sj  | similar |                | that substituting |      | for   | in the Sj |
number
formula gives the oftests necessary to test every decision outcome in the entire pro-
| gram independently |     | [FEGHALI]. |     |     |     |     |     |
| ------------------ | --- | ---------- | --- | --- | --- | --- | --- |
Figure 7-5 shows an example program with integration complexity giving the control struc-
4,
ture, cyclomatic complexity, and module design complexity foreach module and a set offour
| independent | integration | tests. |     |     |     |     |     |
| ----------- | ----------- | ------ | --- | --- | --- | --- | --- |
54

=
|     |     |     | v(A) 2 |     |
| --- | --- | --- | ------ | --- |
=
|     |     |     | iv(A) 2 |     |
| --- | --- | --- | ------- | --- |
/
/
/
=
|     |     | v(B) 2    |     | v(C)  |
| --- | --- | --------- | --- | ----- |
|     |     | iv(B) = 2 |     | iv(C) |
/
|     |     | '   | /   |     |
| --- | --- | --- | --- | --- |
|     |     | \   | /   |     |
|     |     | \   | /   |     |
\ i
'
\
/
\
=
v(D) 2
iv(D) =
1
2+
| Si = (2 | + 2 + | 1) -4+ = | 4.  |     |
| ------- | ----- | -------- | --- | --- |
1
| Independent | integration | tests: |     |     |
| ----------- | ----------- | ------ | --- | --- |
LA
A>B<A>C<A
2. A>B>D<B<A>C<A
3.
A>B<A>C>D<C<A
4.
| Y          |                       |          | Y             |         |
| ---------- | --------------------- | -------- | ------------- | ------- |
| C'X >      | < X" means            | "X calls | which returns | to X.") |
| O =        |                       | •        | =             |         |
| non-call   | node                  |          | call node     |         |
| Figure7-5. | Integrationcomplexity |          | example.      |         |

| Although |     |     |     |     | module's |     |     |     |     |     |     |     |     |
| -------- | --- | --- | --- | --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
a basis set ofpaths through each design-reduced control flow graph can
|           | be exercised | with | fewer | than | Sj          |     |        | more |       | never |           |     | For |
| --------- | ------------ | ---- | ----- | ---- | ----------- | --- | ------ | ---- | ----- | ----- | --------- | --- | --- |
| typically |              |      |       |      | integration |     | tests, |      | tests | are   | required. |     |     |
mostrigorous
the level ofstructured testing, acomplete basis setofS] integration tests should
be performed.
|             | complexity  | can | be approximatedfrom |        |     |        |             |     |        | [YOURDON], |     |            |     |
| ----------- | ----------- | --- | ------------------- | ------ | --- | ------ | ----------- | --- | ------ | ---------- | --- | ---------- | --- |
| Integration |             |     |                     |        |     |        | astructured |     | design |            |     | allowing   |     |
|             |             | be  | predicted           | before |     | coding | begins.     | The | number | ofdesign   |     |            |     |
| integration | test effort | to  |                     |        |     |        |             |     |        |            |     | predicates |     |
in a structure chart (conditional and iterative calls) can be used to approximate the eventual
integration complexity. Recall the simplified formulaforcyclomatic complexity from section
4. that for modules with only binary decisions and p decision predicates, v(G) = p + The
| 1,  |     |     |     |     |     |     |     |     |     |     |     | 1.  |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
corresponding formula for integration complexity is that for programs with d design predi-
|        | be approximately |     |     | d + | The reason |     |         | each |        |           |              |     |     |
| ------ | ---------------- | --- | --- | --- | ---------- | --- | ------- | ---- | ------ | --------- | ------------ | --- | --- |
| cates, | Sj will          |     |     | 1.  |            |     | is that |      | design | predicate | (conditional |     | or  |
iterative call) tends to be implemented by a decision predicate in the design-reduced graph of
| module |                 | implemented |     |     | program. |     | Hence, |           |      |       |        |            |     |
| ------ | --------------- | ----------- | --- | --- | -------- | --- | ------ | --------- | ---- | ----- | ------ | ---------- | --- |
| a      | in the eventual |             |     |     |          |     |        | recalling | that | iv(G) | is the | cyclomatic |     |
complexity ofthe design-reduced graph, combine the v(G) and S formulas calculate the
|     |     |     |     |     |     |     |     |     | j   |     | to  |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     | = I |     | +   | = E |     |     | + = | Z   |     |     | + = | +   |
approximation that Sj iv(G) - n 1 (iv(G) - 1) 1 (v(GReduced) - 1) 1 d 1,
where d is the total numberofdecision predicates in the design-reducedgraphs ofthe modules
|     | implemented |     |     |     |     |     |     |     | number |     |     |     |     |
| --- | ----------- | --- | --- | --- | --- | --- | --- | --- | ------ | --- | --- | --- | --- |
ofthe program, and approximately equal to the ofdesign predicates in
|              | program |         | Figure | 7-6 | shows |     |            | design |     |                |     |            |     |
| ------------ | ------- | ------- | ------ | --- | ----- | --- | ---------- | ------ | --- | -------------- | --- | ---------- | --- |
| the original |         | design. |        |     |       | a   | structured |        |     | representation |     | with three |     |
design predicates and therefore an expected integration complexity offour.
A
|     |     |            | * =design              |                                  |           |                   |                   |       |     |     |     |     |     |
| --- | --- | ---------- | ---------------------- | -------------------------------- | --------- | ----------------- | ----------------- | ----- | --- | --- | --- | --- | --- |
|     |     |            |                        |                                  | predicate | (conditional      |                   | call) |     |     |     |     |     |
|     |     |            | Sincetherearethree     |                                  |           | designpredicates, |                   |       |     |     |     |     |     |
|     |     |            | Theexpectedintegration |                                  |           |                   | complexityisfour. |       |     |     |     |     |     |
|     |     | Figure7-6. |                        | Predictingintegrationcomplexity. |           |                   |                   |       |     |     |     |     |     |
56

| 7.6 Incremental |     |        | integration |     |      |     |     |     |     |     |     |     |
| --------------- | --- | ------ | ----------- | --- | ---- | --- | --- | --- | --- | --- | --- | --- |
|                 |     | system |             |     | each |     |     |     |     |     |     |     |
Hierarchical design limits stage ofdevelopment to a manageable effort, and it is
important to limit the corresponding stages oftesting well [WATSON5].
|     |     |     |     |     |     |     |     | as  |     |     | Hierarchical |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------------ | --- |
design is most effective when the coupling among sibling components decreases the com-
as
ponent size increases, which simplifies the derivation ofdata sets that test interactions among
The
components. remainder ofthis section extends the integration testing techniques ofstruc-
handle
tured testing to the general case ofincremental integration, including support for hier-
| archical | design. | The | key | principle |       |          |     |             |     | among | components | each |
| -------- | ------- | --- | --- | --------- | ----- | -------- | --- | ----------- | --- | ----- | ---------- | ---- |
|          |         |     |     |           | is to | testjust | the | interaction |     |       |            | at   |
integration stage, avoiding redundant testing ofpreviously integrated sub-components.
As
a simple example ofthe approach, recall the statement coverage module testing criterion
| and |     |     |     |     | from |     |     |     | module |     |     |     |
| --- | --- | --- | --- | --- | ---- | --- | --- | --- | ------ | --- | --- | --- |
its integration-level variant section 7.2 that all call statements should be
| exercised | during |     |     |     | Although |     |     |     |     |     |     |     |
| --------- | ------ | --- | --- | --- | -------- | --- | --- | --- | --- | --- | --- | --- |
integration. this criterion is certainly not as rigorous as structured
testing, simplicity makes easy toextendto support incremental integration. Although the
|     | its |     |     | it  |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
generalization ofstructured testing is niore detailed, thebasic approach is the same. To extend
statement coverage to support incremental integration, it is required that all module call state-
| ments   | from         | component |          |      |             | component |            |     |           |             |                  |           |
| ------- | ------------ | --------- | -------- | ---- | ----------- | --------- | ---------- | --- | --------- | ----------- | ---------------- | --------- |
|         | one          |           |          | into | a different |           |            | be  | exercised | at          | each integration | stage.    |
| To form | a completely |           |          |      | "statement  |           |            |     |           |             | each             |           |
|         |              |           | flexible |      |             | testing"  | criterion, |     | it        | is required | that             | statement |
be executed during the phase (which may be anything from single modules to the entire
first
program), and that at each integration phase all call statements that cross the boundaries of
previously integrated components are tested. Given hierarchical integration stages with good
cohesive partitioning properties, this limits the testing effort to a small fraction ofthe effort to
| cover each | statement |     | ofthe | system |     | each        |     | phase. |     |     |     |     |
| ---------- | --------- | --- | ----- | ------ | --- | ----------- | --- | ------ | --- | --- | --- | --- |
|            |           |     |       |        | at  | integration |     |        |     |     |     |     |
Structured testing can be extended to coverthe fully general case ofincremental integration in
a similar manner. The key is to perform design reduction at each integration phase usingjust
| module |      |       |      |       | component |     |             |     |          | component-reduced |     |         |
| ------ | ---- | ----- | ---- | ----- | --------- | --- | ----------- | --- | -------- | ----------------- | --- | ------- |
| the    | call | nodes | that | cross |           |     | boundaries, |     | yielding |                   |     | graphs, |
and exclude from consideration modules do not contain any cross-component
|     |     |     |     |     | all |     | that |     |     |     |     | calls. |
| --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | ------ |
Integration are derived from the reduced graphs using the techniques ofsections 7.4 and
tests
7.5. The complete testing method is to test abasis set ofpaths through each module at the first
phase (which can be either single modules, subsystems, or the entire program, depending on
compo-
the underlying integration strategy), and then test abasis set ofpaths through each
|              |     | graph | ateach | successive |     |             |        |     | As discussedin |     |         | most     |
| ------------ | --- | ----- | ------ | ---------- | --- | ----------- | ------ | --- | -------------- | --- | ------- | -------- |
| nent-reduced |     |       |        |            |     | integration | phase. |     |                |     | section | 7.5, the |
rigorous approach execute a complete basis set ofcomponent integration tests each
|     |     |     | is to |     |     |     |     |     |     |     |     | at  |
| --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
stage. However, for incremental integration, the integration complexity formulamay not give
the precise number ofindependent tests. The reason is that the modules with cross-compo-
may
nent calls not be connected in the design structure, so it is not necessarily the case that
| one  | through | each | module |     | a         | ofexercising |     | a   | path |                | However, | most |
| ---- | ------- | ---- | ------ | --- | --------- | ------------ | --- | --- | ---- | -------------- | -------- | ---- |
| path |         |      |        |     | is result |              |     |     |      | in its caller. |          | at   |
one additional per module required, so using the S formula gives a reasonable
|               |     | test   |         |        | is      |        |     |     | \   | still |     |     |
| ------------- | --- | ------ | ------- | ------ | ------- | ------ | --- | --- | --- | ----- | --- | --- |
| approximation |     | to the | testing | effort | at each | phase. |     |     |     |       |     |     |
57

A
Figure 7-7 illustrates the structured testing approach to incremental integration. Modules
C B
and have been previously integrated, as have modules and D. It would take three tests to
| system |     | However, | design |     |
| ------ | --- | -------- | ------ | --- |
integrate this in a single phase. since the predicate decision to call
D
module from module B has been tested a previous phase, only two additional
in tests are
D
required to complete the integration testing. Modules B and are removed from consider-
ation because they do not contain cross-component calls, the component module design com-
A C
plexity of module is 1, and the component module design complexity ofmodule is 2.
| Independent | component |             |        |     |
| ----------- | --------- | ----------- | ------ | --- |
|             |           | integration | tests: |     |
1:A>B<A>C<A
Test
2:A>B<A>C>D<C<A
Test
| Y     |            |          | Y             |         |
| ----- | ---------- | -------- | ------------- | ------- |
| ("X > | < X" means | "X calls | which returns | to X.") |
O
= non-call node
#
| =               |     | node |     |     |
| --------------- | --- | ---- | --- | --- |
| cross-component |     | call |     |     |
#
| = call     | node within | acomponent  |          |     |
| ---------- | ----------- | ----------- | -------- | --- |
| Figure7-7. | Incremental | integration | example. |     |
58

| 8       |     |                 |     | Programs |     |     |
| ------- | --- | --------------- | --- | -------- | --- | --- |
| Testing |     | Object-Oriented |     |          |     |     |
Object-oriented software differs significantly from traditional procedural software in terms of
and development
analysis, design, structure, techniques, so specific testing support is also
required [FIRESMITH]. The object-oriented language features ofencapsulation, polymor-
phism, and inheritance require special testing support, but also provide opportunities for
To
exploitation by a testing strategy. adapt structured testing for object-oriented programs,
module
consider both testing and integration testing. Structured testing at the module level is
object-orientedprograms,
directly applicableto although thatfact is not immediately obvious.
At the integration level, structured testing does require modification address the dynamic
to
binding ofobject-oriented methods. The rest ofthis section discusses the specific implica-
tions ofobject-oriented programming for structured testing. The majority ofthis information
| was        |             | [MCCABE3]     | [MCCABE4]. |     |     |     |
| ---------- | ----------- | ------------- | ---------- | --- | --- | --- |
| previously | published   | in            | and        |     |     |     |
|            | and dangers | ofabstraction |            |     |     |     |
8.1 Benefits
Object-oriented languages and techniques use new and higher levels ofabstraction than most
traditional languages, particularly via the inheritance mechanism. There are both benefits and
The
dangers to this abstraction. benefit is that the closer the implementation is to the logical
The danger
design, the easier it is to understand the intended function ofthe code. is that the
further the implementation from the machine computation, the harder understand the
|     |     | is  |     |     | it is to |     |
| --- | --- | --- | --- | --- | -------- | --- |
actual function of the code. Figure 8-1 illustrates this trade-off. The abstraction power of
object-oriented languages typically make it easier forprogrammers to write misleading code.
Informally, it is easy to tell what the code was supposed to do, but hard to tell what it actually
| Hence, | automated |     | and |     |     | an  |
| ------ | --------- | --- | --- | --- | --- | --- |
does. support for analysis testing is particularly important in object-
| oriented environment. |        |     |     |     |          |     |
| --------------------- | ------ | --- | --- | --- | -------- | --- |
|                       | Actual |     |     |     | Intended |     |
Function
Function
|     | = Low                       | ofabstraction,        |                 | procedural | languages |     |
| --- | --------------------------- | --------------------- | --------------- | ---------- | --------- | --- |
|     |                             | level                 | traditional     |            |           |     |
|     | = High                      | level of abstraction, | object-oriented | languages  |           |     |
|     | Figure8-1. Abstractionlevel | trade-off.            |                 |            |           |     |
59

When abstraction works well, it hides details that do not need to be tested, so testing becomes
easier. When abstraction works poorly, it hides details that need to be tested, so testing
becomes harder (or at worst, infeasible). Typically, testing must occur at some compromise
level of abstraction, gaining leverage from the abstractions that clarify the software's func-
tionality while penetrating the abstractions that obscure it. Often, asoftware developer's level
offamiliarity with object-oriented development techniques is a key factor in determining
whether abstraction is used in a positive or negative way, which in turn determines whether
testing is helped or hindered by the unique features ofobject-oriented languages. As dis-
cussed in section 8-3, the basic object-oriented structured testing approach can be adapted to
unusually positive or negative situations.
Metrics designed specifically for object-oriented software, such as those of [CHIDAMBER],
can help assess the effectiveness with which the object-oriented paradigm is used. Ifclass
methods are notcohesive andthere is substantial coupling between objects, the abstractions of
the programming language may have been misused in the software. This in turn suggests that
extra caution should be taken during testing.
8.2 Object-oriented module testing
Object-oriented methods are similar in most respects to ordinary functions, so structured test-
ing (as well as other structural testing criteria) applies at the module level without modifica-
tion. Since methods in object-oriented languages tend to be less complex than thefunctions of
traditional procedural programs, module testing is typically easier for object-oriented pro-
grams.
The inheritance and polymorphism features ofobject-oriented languages may seem to compli-
cate module testing, because ofthe implicit control flow involved in resolving dynamic
method invocations. For example, ifan object reference could result in any one ofseveral
alternative methods being executed at run time, it is possible to represent the reference as a
multi-way decision construct ("case" statement) on the flow graph in which a different possi-
ble resolution method for the object reference is called from each branch. Since this represen-
tation of implicit control flow would increase the cyclomatic complexity, it would also
increase the number oftests required to perform structured testing for the module containing
the reference. Figure 8-2 illustrates implicit control flow.
60

M, showing
implicit
|     |     |     |     |     |     |     |     |     |     | control | flow |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------- | ---- | --- |
/
|     |     |     | Object | reference |     |     |     |     |     |     |     |     |
| --- | --- | --- | ------ | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
/
I
'A
/
|     |     |            |     |                      |     | ^\ /       |     |            |     |     |     |     |
| --- | --- | ---------- | --- | -------------------- | --- | ---------- | --- | ---------- | --- | --- | --- | --- |
|     |     | Resolution |     | 1                    |     | Reso/ution | 2   | Resolution |     | 3   |     |     |
|     |     | Figure8-2. |     | Implicitcontrolflow. |     |            |     |            |     |     |     |     |
Although implicit control flow has significant implications for testing, there are strong rea-
number
sons to ignore it at the level ofmodule testing. First, the ofpossible resolutions of a
|     |     |     |     | depends | on  |     |     |     | which |     |     |     |
| --- | --- | --- | --- | ------- | --- | --- | --- | --- | ----- | --- | --- | --- |
particular object reference the class hierarchy in the reference occurs.
Hence, ifmodule depended on control flow, would only be possible
|     |     | testing |     |     |     | implicit |     |     | it  |     |     | to per- |
| --- | --- | ------- | --- | --- | --- | -------- | --- | --- | --- | --- | --- | ------- |
form module testing in the context of a complete class hierarchy, a clearly unrealistic require-
ment. Also, viewing implicit complexity as a module property rather than a system property
defeats one ofthe major motivations for using an object-oriented language: to develop easily
|     | and |     | components. |     |     | Forthese |     |     |     |     |     |     |
| --- | --- | --- | ----------- | --- | --- | -------- | --- | --- | --- | --- | --- | --- |
reusable extensible reasons, consideration ofimplicit control flow
deferred the integration phase when applying object-oriented pro-
| is  | until |     |     |     |     |     |     | structured | testing | to  |     |     |
| --- | ----- | --- | --- | --- | --- | --- | --- | ---------- | ------- | --- | --- | --- |
grams.
| 8.3 | Integration |     | testing | ofobject-orientedprograms |     |     |     |     |     |     |     |          |
| --- | ----------- | --- | ------- | ------------------------- | --- | --- | --- | --- | --- | --- | --- | -------- |
| The |             |     |         |                           |     |     |     |     |     |     |     | programs |
most basic application ofstructured testing to the integration ofobject-oriented
|                |     |            | application |     | ofthe | techniques |     | ofsection |     |               | important, | how- |
| -------------- | --- | ---------- | ----------- | --- | ----- | ---------- | --- | --------- | --- | ------------- | ---------- | ---- |
| is essentially |     | the direct |             |     |       |            |     |           | 7.  | It is vitally |            |      |
ever, to consider the implicit method invocations through object references (not to be con-
fused with the implicit control flow ofdynamic binding) when identifying function call nodes
|     |     |     |     |     | method |     |     | may |     |     |     |     |
| --- | --- | --- | --- | --- | ------ | --- | --- | --- | --- | --- | --- | --- |
to perform design reduction. These invocations not be apparent from examina-
|            |        |       |     | an automated |     |      |             | For | example, |             |     | and "b" |
| ---------- | ------ | ----- | --- | ------------ | --- | ---- | ----------- | --- | -------- | ----------- | --- | ------- |
| tion ofthe | source | code, | so  |              |     | tool | is helpful. |     |          | ifvariables |     | "a"     |
are the expression "a+b" a simple computation. However, ifthose variables
| integers, |     | C+-i- |     |     |     | is  |     |     |     |     |     |     |
| --------- | --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
61

|     |     | ofaclass |     |     | same |     |     |     |     | amethod |     |
| --- | --- | -------- | --- | --- | ---- | --- | --- | --- | --- | ------- | --- |
are objects type, the exact expression can be acall to ofthatclass via
the operator overloading mechanism of C++, which requires and hence
|      |              |     |           |            |     |     |     |     |     | integration testing |     |
| ---- | ------------ | --- | --------- | ---------- | --- | --- | --- | --- | --- | ------------------- | --- |
| must | be preserved |     | by design | reduction. |     |     |     |     |     |                     |     |
While the treatment ofimplicit method calls due to object references is straightforward, the
more
situation with implicit control flow is complicated. In this case, several possible
| approaches |     | worth |              |     | depending |     | on  |            |     | which               |     |
| ---------- | --- | ----- | ------------ | --- | --------- | --- | --- | ---------- | --- | ------------------- | --- |
|            |     | are   | considering, |     |           |     |     | the extent | to  | the object-oriented |     |
abstraction has a positive or negative impact. This section describes three approaches:
opti-
mistic, pessimistic, and balanced. Each approach builds upon the techniques ofsection
7,
requiring that at least a basis set oftests through the design-reduced graph ofeach module be
exercised in an integration context, treating the implicit method invocations due to object ref-
|     |     | when | performing |     |     |     |     | The |     | and |     |
| --- | --- | ---- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
erences as calls design reduction. pessimistic balanced approaches
also require additional based on control flow. Figure 8-3 shows of
|     |     |     | tests |     |     | implicit |     |     |     |     | the structure |
| --- | --- | --- | ----- | --- | --- | -------- | --- | --- | --- | --- | ------------- |
a small subset of a program that illustrates each approach. Each ofmodules "A," "B," and
"C" invokes the dynamically bound "Draw" method, which can be resolved at run time to any
of"Line::Draw," "Polygon::Draw," and "Ellipse::Draw." For the rest ofthis section, the
| methods |      | may be | invoked |     |          |     |               |     | bound |                  |         |
| ------- | ---- | ------ | ------- | --- | -------- | --- | ------------- | --- | ----- | ---------------- | ------- |
|         | that |        |         | as  | a result | of  | a dynamically |     |       | object reference | will be |
"resolutions."
| referred | to  | as  |     |     |     |     |     |     |     |     |     |
| -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|          |     |     |     |     | A   |     |     |     | C   |     |     |
B
Draw
|     |     | Line::Draw |     |                 |     | Polygon::Draw |          |     |     | Ellipse:: Draw |      |
| --- | --- | ---------- | --- | --------------- | --- | ------------- | -------- | --- | --- | -------------- | ---- |
|     |     | Figure8-3. |     | Implicitcontrol |     | flow          | example. |     |     |                |      |
| The |     |            |     |                 |     |               |          |     |     |                | With |
optimistic approach is the most straightforward integration testing approach. this
| approach, |     | expected |     |     |     |     | have |     |     | and |     |
| --------- | --- | -------- | --- | --- | --- | --- | ---- | --- | --- | --- | --- |
it is that abstraction will a positive impact, therefore testing will
be confined to the level ofabstraction ofthe source code. The integration testing techniques
ofsection 7 apply directly. The consequences for implicit control flow are that each call site
exercises at least one resolution, and each resolution is exercised by at least one call site.
| Assuming |     | no  |     | uncovered |     | by  |     |     |     |     |     |
| -------- | --- | --- | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
that errors are testing those interfaces, the object-oriented abstrac-
|         |         | gain | confidence |     |      | the otherpossible |     |     |            |                   | Figure 8-4 |
| ------- | ------- | ---- | ---------- | --- | ---- | ----------------- | --- | --- | ---------- | ----------------- | ---------- |
| tion is | trusted | to   |            |     | that |                   |     |     | interfaces | are also correct. |            |
shows a set ofinterface tests that are adequate to satisfy the optimistic approach for the exam-
| ple ofFigure |     | 8-3. |     |     |     |     |     |     |     |     |     |
| ------------ | --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
62

|     |     | Figure8-4. | Theoptimistic | approach | to implicitcontrolflow. |     |     |     |
| --- | --- | ---------- | ------------- | -------- | ----------------------- | --- | --- | --- |
The pessimistic approach another fairly straightforward approach. With this approach,
is
abstraction is expected to have a negative impact, and therefore testing is required at the level
ofabstraction ofthe machine computation underlying the source code. In addition to the inte-
gration testing techniques of section 7, implicit control flow is tested by requiring that every
| resolution | be     | from | every | Thus, | each      |                     | and | no       |
| ---------- | ------ | ---- | ----- | ----- | --------- | ------------------- | --- | -------- |
|            | tested |      | call  | site. | interface | is tested directly, |     | trust is |
placed in the object-oriented abstraction. The drawback that the testing effort can quickly
is
become infeasible as complexity increases. Figure 8-5 shows a set ofinterface tests that are
adequate to satisfy the pessimistic approach for the example ofFigure 8-3.
A
|     |     |            |                |               | B C               |               |     |     |
| --- | --- | ---------- | -------------- | ------------- | ----------------- | ------------- | --- | --- |
|     |     | Line::Draw |                | Polygon::Draw |                   | Ellipse::Draw |     |     |
|     |     |            | Thepessimistic | approach      |                   |               |     |     |
|     |     | Figure8-5. |                |               | toimplicitcontrol | flow.         |     |     |
The balanced approach is a compromise between the optimistic and pessimistic approaches,
| and | more |     |     |     | The |     |     |     |
| --- | ---- | --- | --- | --- | --- | --- | --- | --- |
is complicated than either ofthem. idea is to test at a level of abstraction
between ofthe code and ofthe underlying mechanics. Abstraction expected
|     | that |     | that |     |     |     | is  | to  |
| --- | ---- | --- | ---- | --- | --- | --- | --- | --- |
hide some details that require testing, but also to provide a framework that can be exploited to
facilitate testing. In addition to the integration testing techniques of section 7, it is required
The
that some call site exercise the entire set ofpossible resolutions. effect ofthis require-
63

ment is to provide evidence that the set ofpossible resolutions from a given call site form an
"equivalence class" in the sense that ifexercising one ofthose resolutions from anew call site
| works |     |     |     |     |     |     |     | workproperly. |     |
| ----- | --- | --- | --- | --- | --- | --- | --- | ------------- | --- |
properly than exercising the otherpossible resolutions are also likely to
This property assumed by the optimistic approach and exhaustively by
|     |     | is  |     |     |     |     |     | tested | the pessimis- |
| --- | --- | --- | --- | --- | --- | --- | --- | ------ | ------------- |
tic approach. The balanced approach provides more thorough testing than the optimistic
approach without requiring as many tests as the pessimistic approach, and is therefore a good
candidate for use in typical situations. Also, the call site used to establish the "equivalence
classes" could be a test driver rather than part ofthe specific application being tested, which
| provides | added |              |     | For example, |     | driverprogram | could | be            |             |
| -------- | ----- | ------------ | --- | ------------ | --- | ------------- | ----- | ------------- | ----------- |
|          |       | flexibility. |     |              |     | a test        |       | first written | to test all |
resolutions ofthe "Draw" method in the "Shape" class hierarchy, which the optimistic
after
approach could be used without modification when testing "Draw" method invocations in
programs using the "Shape" hierarchy. Figure 8-6 shows a set ofinterface tests that are ade-
quate to satisfy the balanced approach for the example ofFigure 8-3.
|     |     |            | Thebalanced |     | approach |                    |       |     |     |
| --- | --- | ---------- | ----------- | --- | -------- | ------------------ | ----- | --- | --- |
|     |     | Figure8-6. |             |     |          | to implicitcontrol | flow. |     |     |
Specific resolutions to dynamic control flow are often ofinterest. For example, the bulk ofa
|     |     |     |     |     | may |     |     |     | may |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
drawing application's typical usage involve polygons, or the polygon functionality
| have | been |     |     |     |     |     |     | asystem | view |
| ---- | ---- | --- | --- | --- | --- | --- | --- | ------- | ---- |
recently re-implemented. In thatcase, it is appropriate to consider in
which shapes are assumed be polygons, example connecting the polymorphic
|     | all |     |     | to  |     | for |     | all |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
"Draw" calls directly to "Polygon::Draw" and removing alternatives such as "Ellipse::Draw"
from consideration. For such a set ofresolutions, the object integration complexity, OSi, is
defined as the integration complexity (Sj) ofthe corresponding resolved system. Object inte-
|         | complexity |     | very |           |       | measurement | based | on any desired | ofreso- |
| ------- | ---------- | --- | ---- | --------- | ----- | ----------- | ----- | -------------- | ------- |
| gration |            |     | is   | flexible, | since | its         | is    |                | set     |
lutions. Those resolutions could be specified either for specific polymorphic methods, or
| more | generally | for | entire classes. |     |     |     |     |     |     |
| ---- | --------- | --- | --------------- | --- | --- | --- | --- | --- | --- |
64

|     | Avoiding | unnecessary |     |         |     |     |     |     |     |     |     |     |
| --- | -------- | ----------- | --- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
| 8.4 |          |             |     | testing |     |     |     |     |     |     |     |     |
Object-oriented systems are often from components, such commercial
|     |     |     |     |     | built | stable |     |     |     | as  | class |     |
| --- | --- | --- | --- | --- | ----- | ------ | --- | --- | --- | --- | ----- | --- |
libraries or re-usedclasses fromprevious successful projects. Indeed, component-based reuse
is one ofthe fundamental goals ofobject-oriented development, so testing techniques must
The
allow for it. Stable, high integrity software can be referred to as "trusted." concept of
|     | can | apply |     |     | modules, |     |     |     |     |     |     |     |
| --- | --- | ----- | --- | --- | -------- | --- | --- | --- | --- | --- | --- | --- |
trustedness to individual classes, class hierarchies, or a set ofpotential res-
olutions for dynamically bound methods, but each case the meaning that trusted software
|     |     |     |     |     |     | in  |     |     |     | is  |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
is assumed to function correctly and to conform to the relevant object-oriented abstraction. In
addition to trusted commercial and reused software, new software becomes trusted after it has
been properly tested. In structured testing, the implementation oftrusted software is not
|         | although |     |             | with | other | software | requiredtobe |     |         | Trusted | software |     |
| ------- | -------- | --- | ----------- | ---- | ----- | -------- | ------------ | --- | ------- | ------- | -------- | --- |
| tested, |          | its | integration |      |       |          | is           |     | tested. |         |          | is  |
treated as an already-integrated component using the incremental integration techniques of
section 7-6.
Trusted software does not have to be tested at the module level at all, and calls internal to a
|         | component |     | do have |     | be     |        |             |        | The | handling | oftrusted |     |
| ------- | --------- | --- | ------- | --- | ------ | ------ | ----------- | ------ | --- | -------- | --------- | --- |
| trusted |           |     | not     | to  | tested | at the | integration | level. |     |          |           |     |
modules, and class hierarchies straightforward, that only integration testing need
|     | classes, |     |     |     | is  |     |     | in  |     |     |     |     |
| --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
be performed, and even then applying the design reduction technique based on only those
calls that cross aboundary oftrustedness. Forthe case ofa trusted set ofpotential resolutions
for a dynamically bound method, only one resolution need be tested from each call site even
| when |     |     |     | approach |     |     |     |     | When | automated |     |     |
| ---- | --- | --- | --- | -------- | --- | --- | --- | --- | ---- | --------- | --- | --- |
using the pessimistic for testing non-trusted code. an tool is
used trustedness information, integration can be stopped the trustedness
|     | to display |     |     |     |     |     | tests |     |     | at  |     |     |
| --- | ---------- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- |
boundary.
65

I
1
I.

9 Complexity Reduction
Although the amount ofdecision logic in a program is to some extent determined by the
intended functionality, software is often unnecessarily complex, especially at the level ofindi-
vidual modules. Unnecessary complexity is an impediment toeffective testing for three major
reasons. First, the extra logic must be tested, which requires extra tests. Second, tests that
exercise the unnecessary logic may not appear distinct from other tests in terms ofthe soft-
ware's functionality, which requires extra effort to perform each test. Finally, it may be
impossible to test the extra logic due to control flow dependencies in the software, which
means that unless the risk ofnot satisfying the testing criterion is accepted, significant effort
must be expended to identify the dependencies and show that the criterion is satisfied to the
greatest possible extent.
Unnecessary complexity also complicates maintenance, since the extra logic is misleading
unless its unnecessary nature is clearly identified. Even worse, unnecessary complexity may
indicate that the original developer did not understand the software, which is symptomatic of
both maintenance difficulty and outright errors. This section quantifies unnecessary complex-
ity, and discusses techniques for removing and testing it.
9.1 Actual complexity and realizable complexity
The most innocuous kind ofunnecessary complexity merely requires extra testing. It may
increase testing effort and obscure the software's functionality, so it is often appropriate to
remove it by reengineering the software. However, when the structured testing methodology
can be used to verify proper behavior for a basis set oftests, adequate testing is simply a mat-
ter ofresources.
A more problematic kind ofunnecessary complexity prevents structured testing as described
in section 5 from being fully satisfied by any amount oftesting. The problem is that data-
driven dependencies between the control structures ofa software module can prevent a basis
set ofpaths through the module's control flow graph from being exercised. The "classify"
module in Figure 9-1 and its control flow graph in Figure 9-2 illustrate this phenomenon.
Although the cyclomatic complexity is 4, only 3 paths can possibly be executed, because the
"TRUE" outcome ofexactly one ofthe three decisions must be exercised on any path.
Another way to view this is that the outcome ofthe first decision may determine the outcome
ofthe second, and the outcomes ofthe first two decisions always determine the outcome of
67

—
|     |     |         |      |     |     | —   | ; ;; |     |
| --- | --- | ------- | ---- | --- | --- | --- | ---- | --- |
|     | 9-3 | and 9-4 | show |     |     |     |      | no  |
the third. Figures "classify2," a reengineered version with unnecessary
complexity.
| Print | jSave| [corwrt] | [cTose] | [Help] |     |     |     |     |     |
| ----- | --------------- | ------- | ------ | --- | --- | --- | --- | --- |
j I
|         |     |          |     | Annotated | Source Listing |     |     |          |
| ------- | --- | -------- | --- | --------- | -------------- | --- | --- | -------- |
| Program |     | Classify |     |           |                |     |     | 04/09/96 |
:
| File      | :      | classify. |     |     |     |      |             |              |
| --------- | ------ | --------- | --- | --- | --- | ---- | ----------- | ------------ |
| Language: |        | c_npp     |     |     |     |      |             |              |
| Module    | Module |           |     |     |     |      |             | Start Num of |
| Letter    | Name   |           |     |     |     | v(G) | ev(G) iv(G) | Line Lines   |
& classify
|     |     |     |      |              |             | 4          | 1   | 4   |
| --- | --- | --- | ---- | ------------ | ----------- | ---------- | --- | --- |
|     | AO  |     | void | classify(int | n)          |            |     |     |
|     |     |     |      | Example of   | unnecessary | complexity | */  |     |
{/*
|     | Al  |     |     | if (n | > 0)                |     |     |     |
| --- | --- | --- | --- | ----- | ------------------- | --- | --- | --- |
|     | A2  |     |     |       | printf("Positive\n" |     |     |     |
|     | A3  | A4  |     |       |                     |     | )   |     |
|     |     |     |     | if (n | < 0)                |     |     |     |
|     | AS  |     |     |       | printf("Negative\n" |     |     |     |
|     | A6  | A7  |     | if (n | 0)                  |     | )   |     |
printf("Zero\n"
|     | A8  |     |     |     |     |     | )   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | A9  | AlO |     |     |     |     |     |     |
)
Codeformodulewith
| Figure9-1. |     |     |     | unnecessarycomplexity. |     |     |     |     |
| ---------- | --- | --- | --- | ---------------------- | --- | --- | --- | --- |
JassHy'tn'Otasliy
|     |     | [Eave]   |            | fForwd| [Backuard| |           | jReduce] |         |     |
| --- | --- | -------- | ---------- | ------------------ | --------- | -------- | ------- | --- |
|     |     | [pTot]   | [Corr<ert| |                    | jinfa-gel | [cicise] | [fielp] |     |
|     |     | Page 1of | 1 2X       |                    |           |          |         |     |
04AI9/96
|     |     | c l a s s i r    | y laasify.c |     | p Superiiaopsed.. i p v a r g | F l o v s |     |     |
| --- | --- | ---------------- | ----------- | --- | ----------------------------- | --------- | --- | --- |
|     |     | L a x i au a g f | e ( c A) '  |     | L o o p E                     | x i t s   |     |     |
|     |     | C y c l o m a    | t x;c       |     | P l a i n                     | E d g e s |     |     |
CycLomatic^
|     |     | E De s s s i e g n n ti | 4 al 1                                   |     |     |     |     |     |
| --- | --- | ----------------------- | ---------------------------------------- | --- | --- | --- | --- | --- |
|     |     | Figure9-2.              | Graphformodulewithunnecessarycomplexity. |     |     |     |     |     |
68

c
|                         |         |        |     |     |     | ; ;; |     |
| ----------------------- | ------- | ------ | --- | --- | --- | ---- | --- |
| IPrinT] fsave| |Convert | [cTose] | jHelp] |     |     |     |      |     |
|
|         |          |     | Annotated | Source Listing |     |     |     |
| ------- | -------- | --- | --------- | -------------- | --- | --- | --- |
| Program | Classify |     |           |                |     |     |     |
04/09/96
| File     | classify |     |     |     |     |     |     |
| -------- | -------- | --- | --- | --- | --- | --- | --- |
| Language | c__npp . |     |     |     |     |     |     |
Module
| [todule     |       |      |                   |                      |             |             | Start Num of |
| ----------- | ----- | ---- | ----------------- | -------------------- | ----------- | ----------- | ------------ |
| Letter Name |       |      |                   |                      | v(G)        | ev(G) iv(G) | Line Lines   |
| B classify2 |       |      |                   |                      |             | 1           | 11           |
| 11 BO       |       | void | classify2         | (int n)              |             |             |              |
| 12          |       | {/*  | After eliminating |                      | unnecessary | complexity  | */           |
| 13 Bl       |       |      | if                | (n > 0)              |             |             |              |
| 14 B2       |       |      |                   | printf("PositiveXn") |             |             |              |
| 15 B3       |       |      | else              | if (n < G)           |             |             |              |
| 16 B4       |       |      |                   | printf("Negative\n"  |             |             |              |
| 17          |       |      | else              |                      |             | )           |              |
| 18 B5       | B6 B7 |      |                   | printf("ZeroXn"      |             |             |              |
| 19 B8       |       |      |                   |                      |             | )           |              |
mm
Codeafterremovingunnecessarycomplexity.
Figure9-3.
|     |     | Graphafter |     | removingunnecessary |     | complexity. |     |
| --- | --- | ---------- | --- | ------------------- | --- | ----------- | --- |
Figure9-4.
The actualcomplexity, ofamodule defined as the number ofHnearly independent paths
|     | ac, |     | is  |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
that have been executed during testing, or more formally as the rank ofthe set ofpaths that
69

have been executed during testing. The structured testing criterion requires that the actual
complexity equal the cyclomatic complexity aftertesting. Note thatthe actual complexity is a
property ofboth the module and the testing. For example, each new independent test
increases the actual complexity.
The realizable complexity, rc, is the maximum possible actual complexity, i.e., the rank ofthe
set ofthe paths induced by all possible tests. This is similar to the characterization ofcyclo-
matic complexity as therank ofthe set ofall possiblepaths, exceptthat some paths may notbe
induced by any test. In the "classify" example, rc is 3 whereas v(G) is 4. Although rc is an
objective and well-defined metric, it may be hard to calculate. In fact, calculating rc is theo-
retically undecidable [HOPCROFT], since, ifit were possible to calculate rc, it would also be
possible to determine whether rc is at least 1, which would indicate whether at least one com-
plete path could be executed, which is equivalent to the module halting on some input.
One obvious property ofrc is that after any amount oftesting has been performed on a mod-
ule, ac <= rc <= v(G). Satisfying the structured testing criterion therefore suffices to prove
that rc = v(G). However, when ac < v(G), one oftwo situations can hold:
1. At least one additional independent test can be executed.
2. ac = rc, and hence rc < v(G).
In the first case, the solution is simply to continue testing until either ac = v(G) orcase 2 is
reached. In the second case, the software can typically be reengineered to remove unneces-
sary complexity, yielding a module in which rc = v(G). This was performed in the "classify"
example. As an alternative to reengineering the software, the structured testing criterion can
be modified to require testing until ac = rc. However, due to the undecidability ofrc, some
manual work is required to set the target value when using an automated tool to measure ac.
A tool can help by reporting the current set ofcontrol dependencies, at which point the user
can review the observed dependencies and decide whether or not additional tests could
increase ac. Ifadditional tests can increase ac, dependency information can also help con-
struct those tests. One special case is "infinite loop" modules, which have rc = 0 because no
complete path can be executed. This does notmean that these modules should not be tested at
all! Infinite loops in real software are typically not really infinite, they arejust waiting for
some external event to interrupt them in a way that is not explicitly specified in their source
code. Such modules should be as small as possible, so that they can be adequately testedjust
by executing them once. Any complex processing should be performed by subordinate mod-
ules that do not contain infinite loops, and hence have basis paths to test.
70

|     |     |     |     |     | )   | ;   | )   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
There are many situations in which easy to see that re < v(G). One example a loop with
|     |     |     |     | it is |     |     |     |     |     | is  |     |
| --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- |
a constant number of iterations, such as the "min" module in Figure 9-5. The "TRUE" out-
|     | =   |     |     | AnnotatodSourcalistingforwin |     |     |     | ^   | •   |     |     |
| --- | --- | --- | --- | ---------------------------- | --- | --- | --- | --- | --- | --- | --- |
.
|     | Print jSave] | (Convert jciosej | |Help| |     |     |     |     |     |     |     |     |
| --- | ------------ | ---------------- | ------ | --- | --- | --- | --- | --- | --- | --- | --- |
|     | 1 1          | |                |        |     |     |     |     |     |     |     |     |
A
|     |         |     |     | Annotated | Source | Listing |     |     |          |     |     |
| --- | ------- | --- | --- | --------- | ------ | ------- | --- | --- | -------- | --- | --- |
|     | Program | Dep |     |           |        |         |     |     | 04/09/96 |     |     |
:
|     | Language:: File | dep.c |     |     |     |     |     |     |     |     |     |
| --- | --------------- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
c_npp
|     | Module Module |     |     |     |     |      |        |        | Start | Num of |     |
| --- | ------------- | --- | --- | --- | --- | ---- | ------ | ------ | ----- | ------ | --- |
|     | Letter Name   |     |     |     |     | v(G) | ev(G1) | i1v(G) | Line  | Lines  |     |
B min
|     |       |       |       |                |            |          | 3       |         | 3            | 9   |     |
| --- | ----- | ----- | ----- | -------------- | ---------- | -------- | ------- | ------- | ------------ | --- | --- |
|     | 3     | BO    | i n t | m i n int      | a [1 0]    |          |         |         |              |     |     |
|     |       |       |       | r e ad ( s arr | a y of ten | elements | and     | returns | the smallest |     | */  |
|     | 4     |       | ( /*  |                |            |          |         |         |              |     |     |
|     | 5     |       |       | int            | i, result; |          |         |         |              |     |     |
|     | 6     |       |       | result         | = a[0]     |          |         |         |              |     |     |
|     |       |       |       | for            | -          |          |         |         |              |     |     |
|     | I     | Bl B2 |       |                | (i 0;      | i < 10;  | i++)    |         |              |     |     |
|     | 8     | B3    |       |                | if (result | >        | a[i]    |         |              |     |     |
|     | 9     | B4    |       |                |            | result   | - a[i]; |         |              |     |     |
|     |       |       |       | return         | result;    |          |         |         |              |     |     |
|     | 10    | B5 B6 |       |                |            |          |         |         |              |     |     |
|     | II B7 |       |       |                |            |          |         |         |              |     |     |
|     |       |       | )     |                |            |          |         |         |              |     | .   |
/
|     | ^   |      |     |     |     |       |     |      |     |     | 1.^ |
| --- | --- | ---- | --- | --- | --- | ----- | --- | ---- | --- | --- | --- |
|     |     | II 1 |     |     |     | 11.11 |     | 1. . |     |     |     |
Loop with constantnumberofiterations.
Figure9-5.
come ofthe loop always executed ten times as frequently as the "ENTRY" branch along
is
any executable path, which a linear control dependency and thus reduces rc by one. Loops
is
|     |     |     |     |     | common |     |     |     | When |     |     |
| --- | --- | --- | --- | --- | ------ | --- | --- | --- | ---- | --- | --- |
with aconstant number ofiterations are fairly in software. the constant might
change during maintenance (for example, a hash table size), it is worth running a test with a
|     |     | When |     |     |     | change |     | example, |     | number |     |
| --- | --- | ---- | --- | --- | --- | ------ | --- | -------- | --- | ------ | --- |
different constant value. the constant will not (for the ofaxes
graphics rendering code), the dependency can simply be taken into account during
| in  |          |         |              |     |     |     |     |     |     |     | testing. |
| --- | -------- | ------- | ------------ | --- | --- | --- | --- | --- | --- | --- | -------- |
| 9.2 | Removing | control | dependencies |     |     |     |     |     |     |     |          |
Removing control dependencies often improves code, since the resulting modules tend to be
|     |     |     |     |     |     | When |     |     |     |     | removed, |
| --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | -------- |
less complex and have straightforward decision logic. all dependencies are
|         |                | by       |     | cyclomatic |     | complexity |     | be used |      |        | actual |
| ------- | -------------- | -------- | --- | ---------- | --- | ---------- | --- | ------- | ---- | ------ | ------ |
| testing | is facilitated | allowing |     | the        |     |            | to  |         | as a | target | for    |
complexity. Two important reduction techniques are direct logic simplification and modular-
ization. The following complex example [WATS0N5] illustrates both techniques. Figure 9-
[HANSON]
6 shows the code for module "printwords," which contains three control depen-
71

c ; ;) ;;
dencies (for this example, HASHSIZE is not constant). One dependency is the "&& k~ > 0"
^otetetfSourcettetln^forprtntwomsi
jPrintl fSave) jConvert| fciose] fHelT]
Annotated Source Listing
Program Printwords 04/09/96
File : printwords.
Language: c_npp
Module Mo:dule Start Num of
Letter Name v(G) ev(G) iv(G) Line Lines
D printwords 11 3 2 32 22
32 DO printwords (k)
33 int k;
34 (/* Print the k most common words in the table, original */
35 int i, max;
36 struct word *wp, **list, *q;
37 max - 0;
38 Dl 02 for (i = 0; i <= HASHSIZE; i++)
3 4 9 0 D D 3 6 04 D5 for i ( f wp ( - wp h - a > s c h o t u a n b t le > [ m i a ] x ; ) wp; wp = wp->next)
41 D7 max = wp->count
42 D8 D9 DIO Oil list " (struct word **) alloc(max + 1, sizeof wp)
43 D12 013 for (i = 0; i <= HASHSIZE; i++)
4 4 4 5 D 0 1 1 4 7 015 016 for q (wp = w = p- h > a n s e h x t t a ; ble[i]; wp; wp = q) {
4 4 6 7 018 w 1 p i - s > t n [ e w x p t ->c = ou 1 n i t st ] [ - wp w - p > ; count ]
4 4 8 9 0 0 1 21 9 D 0 2 2 0 2 023 for (i =)max; i >= 0 «£ k >—0; i —
50 024 D25 if ((wp = list[i]) <;s k > 0)
5 51 2 D 0 2 2 6 9 0 O 2 3 7 0 0 03 2 1 8 for p(ri;nt wp f ; ("% w d p = %s\ w n p " - , >ne w x p t - ) >count, wp->word)
53 032 033 034
)
ijmuuinm.ii.ji»jiiiimumiM)juuii»iJ»JLimurouiu.uuiujJ^u^^^
Figure9-6. Modulewith threedependencies.
condition at line 50. This condition is always true, since it can only be reached when "k > 0"
is true at line 49, and the value ofk is not changed in the interim. The condition can therefore
be eliminated, moving the "k~" to the initialization part ofthe loop on line 51 to preserve
functionality. The other two dependencies are due to the hash table being traversed twice,
once to get the value of"max" for the list allocation, then again to fill the list. These depen-
dencies can be eliminated by modularization ofthe "max" calculation. Figures 9-7 and 9-8
72

|     |     |     |     | c c |     |     |     |     |     | ;)  |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     |     |     | ;   | )   |     |     | ;   |     |
show the reengineered functions "printwords2" and "getmax," which = v(G) and
|         |     |          |      |         |      |       |     |     |     | for | rc  | the |
| ------- | --- | -------- | ---- | ------- | ---- | ----- | --- | --- | --- | --- | --- | --- |
| maximum |     | v(G) has | been | reduced | from | 11 to |     |     |     |     |     |     |
7.
/VinetatetlSourcelistingfortirtntwontsz
|     | iPrVnt] | fSaue] jConvert] | jcTosel | [Help] |           |        |         |     |     |     |          |     |
| --- | ------- | ---------------- | ------- | ------ | --------- | ------ | ------- | --- | --- | --- | -------- | --- |
|     |         |                  |         |        | Annotated | Source | Listing |     |     |     |          |     |
|     | Program | Printwords       |         |        |           |        |         |     |     |     | 04/09/96 |     |
:
|     | Language:: File | printwords. |     |     |     |     |     |     |     |     |     |     |
| --- | --------------- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
c_npp
|     | Module | Module |     |     |     |     |     |      |       | Start      | Num of |     |
| --- | ------ | ------ | --- | --- | --- | --- | --- | ---- | ----- | ---------- | ------ | --- |
|     | Letter | Name   |     |     |     |     |     | v(G) | ev(G) | iv(G) Line | Lines  |     |
printwords2
|     |     |     |     |                 |        |            |         |       |     |            | 13 18        |     |
| --- | --- | --- | --- | --------------- | ------ | ---------- | ------- | ----- | --- | ---------- | ------------ | --- |
|     |     | CO  |     | printwords2()c) |        |            |         |       |     |            |              |     |
|     |     |     |     | int             | k;     |            |         |       |     |            |              |     |
|     |     |     |     | (/*             | Print  | the k most | common  | words | in  | the table, | restructured | */  |
|     |     |     |     |                 | int i, | max;       |         |       |     |            |              |     |
|     |     |     |     |                 | struct | word *wp,  | **list, |       |     |            |              |     |
*q;
|     |     | CI     |     |     | max =  | getmax    |                  |           |        |             |     |     |
| --- | --- | ------ | --- | --- | ------ | --------- | ---------------- | --------- | ------ | ----------- | --- | --- |
|     |     | C2     |     |     | list = | (struc(t) | word **)         | alloc(max |        | + 1, sizeof | wp) |     |
|     |     | C3     |     |     | for    | = <=      | HASHSIZE;        |           |        |             |     |     |
|     |     | C4     |     |     | (i     | 0; i      |                  |           | i++)   |             |     |     |
|     |     | C 5 C6 | C7  |     | for    | (wp = h   | a s h t a ble[   | i];       | wp; wp | = q)        |     |     |
|     |     | C 8    |     |     |        | q = w p-  | > n e x t ;      |           |        | {           |     |     |
|     |     |        |     |     |        | wp->next  | = list[wp->count |           |        |             |     |     |
]
|     |            | C9                |           |     |         | 1ist[wp->count |      | ] = wp; |           |                      |     |     |
| --- | ---------- | ----------------- | --------- | --- | ------- | -------------- | ---- | ------- | --------- | -------------------- | --- | --- |
|     |            | C IO C            | ll        |     |         |                |      |         | —         |                      |     |     |
|     |            |                   |           |     | for     | =)max;         | >-   |         |           |                      |     |     |
|     |            | CI 2 CI           | 3 CI4     |     | (i      |                | i 0  | Sfi k > | 0; i      |                      |     |     |
|     |            | CIS               |           |     | if      | (wp = l—ist[i] |      |         |           |                      |     |     |
|     |            | C I6 C            | I 7 C I 8 |     |         | for ( k        | wp ; | wp =    | w p-> n e | x t )                |     |     |
|     |            |                   |           |     |         | p r int;f(     | " %d |         | w p -     | > c ount, wp->word); |     |     |
|     |            | C I 9 C           | 20 C 21   |     |         |                |      | %s\ n"  | ,         |                      |     |     |
|     |            | C22 C23           | C24       |     |         |                |      |         |           |                      |     |     |
|     | Figure9-7. | Firstreengineered |           |     | module. |                |      |         |           |                      |     |     |
/Annotated!Sourcelistingforgetoiax
|     |     | |Print| jSavej [Convert| | iClose] | ^Help |           |        |         |     |     |     |          |     |
| --- | --- | ------------------------ | ------- | ----- | --------- | ------ | ------- | --- | --- | --- | -------- | --- |
|     |     |                          |         |       | Annotated | Source | Listing |     |     |     |          |     |
|     |     | Program                  |         |       |           |        |         |     |     |     | 04/09/96 |     |
Printwords
|     |     | File        | printwords |     |              |     |     |      |        |        |            |     |
| --- | --- | ----------- | ---------- | --- | ------------ | --- | --- | ---- | ------ | ------ | ---------- | --- |
|     |     | Language    | c_npp      | .   |              |     |     |      |        |        |            |     |
|     |     | Mo:dule     |            |     |              |     |     |      |        |        | Num        |     |
|     |     | Module      |            |     |              |     |     |      |        |        | Start of   |     |
|     |     | Letter Name |            |     |              |     |     | v(G) | ev(G1) | i1v(G) | Line Lines |     |
|     |     | B getmax    |            |     |              |     |     |      | 4      |        | 1 11       |     |
|     |     | BO          |            |     | int getmax() |     |     |      |        |        |            |     |
1
2 {/* Return the maximum frequency of any word in the table */
|     |     | 3   |     |     | int    | i, max; |      |     |     |     |     |     |
| --- | --- | --- | --- | --- | ------ | ------- | ---- | --- | --- | --- | --- | --- |
|     |     |     |     |     | struct | word    | *wp; |     |     |     |     |     |
4
|     |     | 5      |        |     | max    | = 0;     |                |            |         |                |     |     |
| --- | --- | ------ | ------ | --- | ------ | -------- | -------------- | ---------- | ------- | -------------- | --- | --- |
|     |     | 6 Bl   | B2     |     | for    | (i = 0;  | i <- HASHSIZE; |            | i++)    |                |     |     |
|     |     | B 3    | B4 BS  |     |        | for ( wp | = h a s h      | t a b le [ | wp;     | wp = wp->next) |     |     |
|     |     | 7      |        |     |        |          |                |            | i] ax;) |                |     |     |
|     |     | 8 B 6  |        |     |        | i f      | ( wp - > c o   | u n t >    | m       |                |     |     |
|     |     | 9 B7   |        |     |        |          | max =          | wp->count; |         |                |     |     |
|     |     | 10 B8  | 39 BIO |     | return | max;     |                |            |         |                |     |     |
|     |     | 11 Bll |        |     | >      |          |                |            |         |                |     |     |
Second
|     | Figure9-8. |     | reengineered |     | module. |     |     |     |     |     |     |     |
| --- | ---------- | --- | ------------ | --- | ------- | --- | --- | --- | --- | --- | --- | --- |

c
;;
when
| 9.3      | Trade-offs |               | reducing |          | complexity |     |             |     |               |     |      |           |
| -------- | ---------- | ------------- | -------- | -------- | ---------- | --- | ----------- | --- | ------------- | --- | ---- | --------- |
| Removing |            | dependencies, |          | although |            |     |             |     | can sometimes |     | have |           |
|          | control    |               |          |          | typically  |     | beneficial, |     |               |     |      | anegative |
impact on software. The most common when reducing complexity introduce
|     |     |     |     |     | pitfall |     |     |     |     |     | is to |     |
| --- | --- | --- | --- | --- | ------- | --- | --- | --- | --- | --- | ----- | --- |
unstructured logic. The essential complexity metric, described in section 10, can help resolve
this problem by quantifying unstructured logic. However, structural degradation is often
obvious directly from thecode and flow graph. Figures 9-9 and 9-10 show the code and graph
|     |     |     |     | module |     |     | = 4 and |     | =   |     |     |     |
| --- | --- | --- | --- | ------ | --- | --- | ------- | --- | --- | --- | --- | --- |
for "search," a well-structured with v(G) rc 3. This type ofcode is often
seen Pascal programs, using a Boolean a loop and assigning value
| in    |             |             |     | single      |     | to  | control |     |     |     |     | it a |
| ----- | ----------- | ----------- | --- | ----------- | --- | --- | ------- | --- | --- | --- | --- | ---- |
| based | on multiple | termination |     | conditions. |     |     |         |     |     |     |     |      |
AnnotatedSourceUstingforsearch
]
|     | jPrlnt| | [Save] fcotiwert) | [ciosej | [fielp] |     |     |     |     |     |     |     |     |
| --- | ------- | ----------------- | ------- | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
|
|     |     |     |     |     | Annotated | Source | Listing |     |     |     |     |     |
| --- | --- | --- | --- | --- | --------- | ------ | ------- | --- | --- | --- | --- | --- |
IF
|
|     | Program | Tradeoff    |     |     |     |     |     |     |     |     | 04/10/96 |     |
| --- | ------- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- | -------- | --- |
|     | File    | : tradeoff. |     |     |     |     |     |     |     |     |          | \   |
Language:
c_npp
|     | Module | Mo:dule  |       |     |             |           |          |         |             | Start | Num   | of | |
| --- | ------ | -------- | ----- | --- | ----------- | --------- | -------- | ------- | ----------- | ----- | ----- | ---- |
|     | Letter | Name     |       |     |             |           |          |         |             | Line  | Lines |      |
|     |        |          |       |     |             |           |          | vCG)    | ev(G) iv(G) |       |       |      |
|     |        | B search |       |     |             |           |          | 4       |             |       |       | 14   |
|     |        |          |       |     |             |           |          |         | 1           | 1     | 1     | 1    |
|     | 1      | BO       |       | int | search(char | s[],      | int      | ch)     |             |       |       |      |
|     | 2      |          |       | (   |             |           |          |         |             |       |       |      |
|     | 3      |          |       |     | int         | i, fDone, | fFound;  |         |             |       |       |      |
|     | 4      |          |       |     | i =         | fDone     | = fFound | = 0;    |             |       |       |      |
|     |        | B l      |       |     | while       | (!f D     | on e )   |         |             |       |       |      |
|     | 5      |          |       |     |             |           | [i]{     | ==      |             |       |       |      |
|     | 6      | B 2      |       |     |             | i f       | ( s      | ch)     | {           |       |       |      |
|     | 7      | B 3      |       |     |             |           |          | fD one  | =           |       |       |      |
|     |        |          |       |     |             |           |          | fFound  | = 1         |       |       |      |
|     | 8      |          |       |     |             |           |          |         | 1           |       |       |      |
|     | 9      | B 4      |       |     |             | )         | else if  | ( s [i] | = = '\0')   |       |       |      |
|     | 10     | B 5      |       |     |             |           |          | fDo n e | = 1 ;       |       |       |      |
|     |        | B6       | B7 B8 |     |             | i++;      |          |         |             |       |       |      |
11
|     | 12  | B9  |     |     |         |         |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | ------- | ------- | --- | --- | --- | --- | --- | --- |
|     | 13  |     |     |     | r)eturn | fFound; |     |     |     |     |     |     |
BIO
|     | 14  |     |     | )   |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
1
|     | Figure9-9. | Codeforstructured |     |     | module, | rc < v(G). |     |     |     |     |     |     |
| --- | ---------- | ----------------- | --- | --- | ------- | ---------- | --- | --- | --- | --- | --- | --- |
74

nowgraphsfor'saarch'InTraiteoff
[cl^
|     |     |     |     | [Plot] [save | [convert! | [poruard! |iackuard! | [Enlygel [Reduce] | |Help| |     |     |     |
| --- | --- | --- | --- | ------------ | --------- | -------------------- | ----------------- | ------ | --- | --- | --- |
I
|     |     |     | Page             | 1 of 1 | 2X  |               |         |            |     |     |     |
| --- | --- | --- | ---------------- | ------ | --- | ------------- | ------- | ---------- | --- | --- | --- |
|     |     |     | Figure9-10.Graph |        |     | forstructured | module, | rc < v(G). |     |     |     |
Figures 9-1 1 and 9-12 show the code and graph for a reengineered version ofthe same mod-
|         |         | and v(G)         |      |       |       | Although |              |         | improvement, |      | new        |
| ------- | ------- | ---------------- | ---- | ----- | ----- | -------- | ------------ | ------- | ------------ | ---- | ---------- |
| ule,    | with rc |                  | both | equal | to 3. |          | in principle | this is | an           |      | the        |
| version | not     |                  |      | The   | loop  | has      | two          | bottom  |              | and  | the condi- |
|         | is      | well-structured. |      |       |       |          | exit points, | the     |              | test |            |
tional return in the middle. Even so, most programmers would agree that the reengineered
version is better in this simple example. However, for more complex programs the structural
much
degradation from complexity reduction can be more severe, in which case the original
|         | would |     |            | There |     | "middle | ground" | ofprograms |     | which |         |
| ------- | ----- | --- | ---------- | ----- | --- | ------- | ------- | ---------- | --- | ----- | ------- |
| version |       | be  | preferred. |       | is  | also a  |         |            |     | for   | reason- |
programmers can disagree about the ofreengineering, depending on
| able |     |     |     |     |     | desirability |     |     |     |     | their |
| ---- | --- | --- | --- | --- | --- | ------------ | --- | --- | --- | --- | ----- |
75

|     |     | .   |     |     | ;   |     |
| --- | --- | --- | --- | --- | --- | --- |
experience and stylistic preferences. In such cases, it is less importantto worry about making
|     | and more |     | document |     |     |     |
| --- | -------- | --- | -------- | --- | --- | --- |
the "right" choice, important to the reasons for the trade-off.
| [Prlntl  | ISave] fconvert| iClose| | ;Help| |           |                |     |              |
| -------- | ------------------------ | ------ | --------- | -------------- | --- | ------------ |
|          |                          |        | Annotated | Source Listing |     |              |
| Program  | Tradeoff                 |        |           |                |     | 04/10/96     |
| File     | tradeoff                 |        |           |                |     |              |
| Language | c_npp                    |        |           |                |     |              |
| Module   | Module                   |        |           |                |     | Start Num of |
Letter
|     | Name    |     |              |      | v(G) ev(G) iv(G) | Line Lines |
| --- | ------- | --- | ------------ | ---- | ---------------- | ---------- |
|     | search2 |     |              |      |                  | 16 10      |
| 16  | CO      | int | search2(char | s[], | int ch)          |            |
17
{
| 18  |          |     | int     | i;        |        |     |
| --- | -------- | --- | ------- | --------- | ------ | --- |
| 19  |          |     | i =     | 0;        |        |     |
| 20  |          |     | do      |           |        |     |
|     | Cl       |     | {       |           |        |     |
| 21  | C2       |     |         | if (s[i]  | == ch) |     |
| 22  | C3       |     |         |           | return |     |
|     |          |     | while   |           | 1      |     |
| 23  | C4 C5 C6 |     | r)eturn | (s[i++]); |        |     |
| 24  |          |     |         | 0;        |        |     |
| 25  | C7       |     |         |           |        |     |
)
| Figure9-11 | .Reengineered                     | code, | rc =v(G) | butnotwell-structured. |                             |     |
| ---------- | --------------------------------- | ----- | -------- | ---------------------- | --------------------------- | --- |
|            | Figure9-12.Reengineeredgraph,v(G) |       |          |                        | = rc butnotwell-structured. |     |
76

In addition to the trade-offbetween directcomplexity reduction and structural quality, there is
| atrade-offbetween |        |                    |            |         | [PARNAS].          | When    |                 |
| ----------------- | ------ | ------------------ | ---------- | ------- | ------------------ | ------- | --------------- |
| also              |        | modularization     | and design | quality |                    |         | splitting acon- |
| dependency        |        | a module boundary, |            |         |                    |         | coupling        |
| trol              | across |                    | there      | is the  | risk ofintroducing | control |                 |
between the modules and limiting the cohesion ofeach module. As when considering
split-
ting up a module to satisfy a complexity threshold, the most important consideration is
new
whether each module performs a single cohesive function. Ifit does, then the modular-
must
ization is consistent with design quality. Otherwise, the design quality degradation be
weighed against ofthe reduced complexity. "printwords" example,
|     | the | benefits |     |     | In the |     | the |
| --- | --- | -------- | --- | --- | ------ | --- | --- |
new "getmax" function performed a single cohesive function, so the complexity reduction
wasjustified. If, on the other hand, the module was split in such a way as to require passing
|     |     |     | name |     |     |     | new |
| --- | --- | --- | ---- | --- | --- | --- | --- |
local variables by reference and the only that could be thought offor the module
| was                |     |                    | would |     | have beenjustified. | As  |                 |
| ------------------ | --- | ------------------ | ----- | --- | ------------------- | --- | --------------- |
| "more_printwords," |     | the modularization |       | not |                     |     | with structural |
having a documented reasoning process when the trade-offseems
| quality, | clearly |     |     |     | is vital |     |     |
| -------- | ------- | --- | --- | --- | -------- | --- | --- |
balanced.
fairly
77

|     | 0   |     |     | Complexity |     |     |     |     |     |     |     |
| --- | --- | --- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- |
1 Essential
| In addition |     | the quantity | ofdecision |     |       | measured |     | by         |             |     |             |
| ----------- | --- | ------------ | ---------- | --- | ----- | -------- | --- | ---------- | ----------- | --- | ----------- |
|             |     | to           |            |     | logic | as       |     | cyclomatic | complexity, |     | the quality |
ofthat logic also a significant factor in software development [PRESSMAN]. Structured
is
programming [DAHL] avoids unmaintainable "spaghetti code" by restricting the usage of
control structures to those that are easily analyzed and decomposed. Most programming lan-
| guages | allow |     |     | and | few |     |     |     |     |     |     |
| ------ | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
unstructured logic, real programs consist entirely ofperfectly structured
| code. | The | essential | complexity | metric | described |     |         |                    |     |            | which |
| ----- | --- | --------- | ---------- | ------ | --------- | --- | ------- | ------------------ | --- | ---------- | ----- |
|       |     |           |            |        |           |     | in this | section quantifies |     | the extent | to    |
software unstructured, providing a continuous range ofstructural quality assessments
|     | is  |     |     |     |     |     |     |     |     |     | appli- |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ |
cable to all software ratherthan the "all ornothing" approach ofpure structured programming.
|            | Structuredprogramming |            |              |     | and          |                 |       |           |       |     |           |
| ---------- | --------------------- | ---------- | ------------ | --- | ------------ | --------------- | ----- | --------- | ----- | --- | --------- |
| 10.1       |                       |            |              |     |              | maintainability |       |           |       |     |           |
| The        |                       | operations | ofstructured |     | programming, |                 | shown |           |       |     |           |
|            | primitive             |            |              |     |              |                 |       | in Figure | 10-1, | are | sequence, |
| selection, |                       | and        |              |     |              |                 |       |           |       |     |           |
iteration.
|     |     |                        |     | "if         |             | "case"      |     | "while"   | "repeat" |     |     |
| --- | --- | ---------------------- | --- | ----------- | ----------- | ----------- | --- | --------- | -------- | --- | --- |
|     |     | Sequence               |     | Selection   |             |             |     | Iteration |          |     |     |
|     |     | Figure 10-1.Structured |     | programming |             | primitives. |     |           |          |     |     |
| The |     |                        |     |             | programming |             |     |           |          |     |     |
fundamental strength ofstructured is that the primitive operations give a
|         | decomposition |     | ofarbitrarily |     | complex |             |     | This decomposition |     |             | modu- |
| ------- | ------------- | --- | ------------- | --- | ------- | ----------- | --- | ------------------ | --- | ----------- | ----- |
| natural |               |     |               |     |         | structures. |     |                    |     | facilitates |       |
larization ofsoftware because each primitive construct appears as acomponent with one entry
point and one exitpoint. The decomposition also allows a "divide andconquer" strategy to be
when
used to understand and maintain complex software even the software is not physically
musttypically
decomposed. Unstructuredcode be understood and maintained as asingleunit,
| which | can | be          | even |     | programs | ofmoderate |     | cyclomatic | complexity. |     |     |
| ----- | --- | ----------- | ---- | --- | -------- | ---------- | --- | ---------- | ----------- | --- | --- |
|       |     | impractical |      | for |          |            |     |            |             |     |     |
Since poor module structure makes software harder to understand, also impedes testing.
it
First, as discussed in section 5.3, poorly understood software requires extra testing to gain
more
confidence. Second, it requires effort to construct each specific test case for poorly
79

.
|     |     |     |     |     | between |     |     | and |     |     |     |     |
| --- | --- | --- | --- | --- | ------- | --- | --- | --- | --- | --- | --- | --- |
understood code, since the connection input data the details ofthe implementa-
tends be unclear. Finally, poorly understood code both error-prone and hard
| tion | to  |     |     |     |     |     |     | is  |     |     |     | to  |
| ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
debug, so an iterative process oftesting anderror correction may be required.
| 10.2 Definition |     | ofessential |     | complexity, |     | ev(G) |        |     |     |     |     |     |
| --------------- | --- | ----------- | --- | ----------- | --- | ----- | ------ | --- | --- | --- | --- | --- |
| The             |     |             |     | [MCCABEl],  |     |       | module |     |     |     |     |     |
essential complexity, ev(G) ofa is calculated by first removing
|            | programming |     |            | from |     | module's |         |     | flow graph |       | graph |      |
| ---------- | ----------- | --- | ---------- | ---- | --- | -------- | ------- | --- | ---------- | ----- | ----- | ---- |
| structured |             |     | primitives |      | the |          | control |     |            | until | the   | can- |
not be reduced any further, and then calculating the cyclomatic complexity ofthe reduced
A
graph. An immediate consequence that <= ev(G) <= v(G). somewhat less obvious con-
|     |     |     |     | is  | 1   |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
sequence, which can help when evaluating complexity analysis tools, is that ev(G) can never
be equal to 2. This is because after all sequential nodes have been eliminated, the only graphs
| v(G) |       | 2      | structuredprogramming |     |     |             |     | which | can | be   | removed |        |
| ---- | ----- | ------ | --------------------- | --- | --- | ----------- | --- | ----- | --- | ---- | ------- | ------ |
| with | equal | to are |                       |     |     | primitives, |     |       |     | then |         | to get |
an ev(G) of The reduction proceeds from the deepest ofnesting outward, which
|     |     | 1.  |     |     |     |     |     | level |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- |
means that a primitive construct can be removed only when no other constructs are nested
within
it.
programming
It is important to note that the structured primitives used in the calculation of
complexity based on flow graph ratherthan source codetext. This
| essential |     |     | are | the | control |     |     |     | the |     |     |     |
| --------- | --- | --- | --- | --- | ------- | --- | --- | --- | --- | --- | --- | --- |
allows the essential complexity metric to measure structural quality independently ofthe syn-
tax ofany particular programming language. For example, a bottom-test loop is a structured
primitive whether it is written using a high-level looping construct or an assembly language
Programming
conditional branch. language constructs such as the "goto" statement only
|          |           | complexity |     | when |     |          | used | implement |     |        |            |     |
| -------- | --------- | ---------- | --- | ---- | --- | -------- | ---- | --------- | --- | ------ | ---------- | --- |
| increase | essential |            |     | they | are | actually |      | to        |     | poorly | structured |     |
notjust because they could be used way. Ofcourse, any program written
| logic, |     |     |     |     | that |     |     |     |     | that | is  |     |
| ------ | --- | --- | --- | --- | ---- | --- | --- | --- | --- | ---- | --- | --- |
entirely with high-level "structured programming" language constructs will have a perfectly
structured control flow graph and therefore have an essential complexity of
1
| The |     |     |     |     |     |     |     |     |     | ofmodule |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | -------- | --- | --- |
essential complexity calculation process is similar to the calculation design
| complexity |     | described |            | 7.4 | (and |         | was developed |     |         | but   |     | two key |
| ---------- | --- | --------- | ---------- | --- | ---- | ------- | ------------- | --- | ------- | ----- | --- | ------- |
|            | as  |           | in section |     |      | in fact |               |     | first), | there | are |         |
differences. primitive constructs can be removed whether or not they involve module
First,
calls when calculating essential complexity. Second, only entire primitive constructs can be
when
removed calculating essential complexity. The module design complexity reduction
|     | removing |     |     |     |     | when |     |     | no module |     |     |     |
| --- | -------- | --- | --- | --- | --- | ---- | --- | --- | --------- | --- | --- | --- |
rules allow partial decision constructs there are calls involved,
which can eliminate unstructured code. Thus, despite the between the two calcula-
similarity
tion methods, there no mathematical relationship between the two metrics.
is
80

| 10.3 | Examples | ofessential | complexity |     |     |     |     |     |
| ---- | -------- | ----------- | ---------- | --- | --- | --- | --- | --- |
Figure 10-2 illustrates the calculation ofessential complexity from a control flow graph. The
original graph has a cyclomatic complexity of8. First the innermost primitive constructs are
| removed | (abottom-test | loop | and two |             | Then, new | innermost |           |           |
| ------- | ------------- | ---- | ------- | ----------- | --------- | --------- | --------- | --------- |
|         |               |      |         | decisions). | the       |           | primitive | construct |
removed (a top-test loop), after which no further reductions are possible. The cyclomatic
is
complexity ofthe final reduced graph is 4, so the essential complexity ofthe original graph is
also 4.
|     |     | v(G)=8 |     |     |     | v(G)=4 |     |     |
| --- | --- | ------ | --- | --- | --- | ------ | --- | --- |
ev(G)=4
Figure10-2.Essentialcomplexitycalculationexample.
|        | 10-3 shows |            | code | module | with cyclomatic | complexity | 9   | and       |
| ------ | ---------- | ---------- | ---- | ------ | --------------- | ---------- | --- | --------- |
| Figure |            | the source |      | for a  |                 |            |     | essential |
complexity The essential complexity caused by the conditional break out ofthe loop.
|     | 4.  |     |     | is  |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
Figure 10-4 shows the essential control flow graph forthe same module, in which the unstruc-
81

—
tured logic is superimposed on the entire flow graph structure. This representation
identifies
| the control | structures | that contribute | to essential |                            | complexity. |     |     |     |
| ----------- | ---------- | --------------- | ------------ | -------------------------- | ----------- | --- | --- | --- |
|             |            |                 |              | If ( o n ly arn1t_fl«9•(n; |             |     |     |     |
r » p
r a p a l n t f l a g - 0 ;
|     |     |     |     | h w i h t lT« B o f( ~ - n 6 ; > | - 0 )                                      |     |     |     |
| --- | --- | --- | --- | -------------------------------- | ------------------------------------------ | --- | --- | --- |
|     |     |     |     | r a t - b a                      | d e l l n ( * ( p o a } ;                  |     |     |     |
|     |     |     |     | f ( I p f O B                    | ( " i f " o k r U c L a L ) _ P 0 8 I T I( |     |     |     |
Una-NULL:
a)dd_baci[_pos(pQ9):
If(^apalnc_f1*0)
I
|     |     |     |     | IfTn•lolftibaaHllO;0) | —   |     |     |     |
| --- | --- | --- | --- | --------------------- | --- | --- | --- | --- |
^
&26&27AZa
|     |     |                        |              | codeformodule |                        |           | =9andev(G) | =4. |
| --- | --- | ---------------------- | ------------ | ------------- | ---------------------- | --------- | ---------- | --- |
|     |     | Figure10-3.Source      |              |               |                        | with v(G) |            |     |
|     |     | ffl'^l^'J'W^'          | nowgraia»fOT |               | 'Essential'            |           |            |     |
|     |     | [piot] [iave| [Convert | [Foruard]    | |Backuiard|   | jEnlarge] fReduce      | |Close]   | jHelp      |     |
|     |     |                        | [            |               |                        | |         |            |     |
|     |     | Page 2 of 3            | 2X           |               |                        |           |            |     |
|     |     | Easential              |              |               | 04/18/96               |           |            |     |
|     |     | I I I                  |              |               | S up e r i mD ps e     | d .—s . . |            |     |
|     |     | ba c k                 |              |               | U p w a r d F l o      | w —       |            |     |
|     |     | Language, c Graph      | npp          |               | Plain Loop Exits Edges |           |            |     |
|     |     | ~3sintla]. •yclomatic  | 9            |               |                        |           |            |     |
|     |     | Essential 4            |              |               |                        |           |            |     |
Design
-24
26
|     |     |                       |       | formodule |      |      | =9 andev(G) | =4. |
| --- | --- | --------------------- | ----- | --------- | ---- | ---- | ----------- | --- |
|     |     | Figure 10-4.Essential | graph |           | with | v(G) |             |     |
82

11 Maintenance
Maintenance is the most expensive phase ofthe software lifecycle, with typical estimates
ranging from 60% to 80% oftotal cost [PRESSMAN]. Consequently, maintenance methodol-
ogy has a major impact on software cost. "Bad fixes," in which errors are introduced while
fixing reported problems, are a significant source oferror [JONES]. Complexity analysis can
guide maintenance activity to preserve (or improve) system quality, and specialized testing
techniques help guard against the introduction oferrors while avoiding redundant testing.
11.1 Effects ofchanges on complexity
Complexity tends to increase during maintenance, for the simple reason thatboth errorcorrec-
tion and functional enhancement are much more frequently accomplishedby addingcode than
by deleting it. Not only does overall system complexity increase, but the complexity ofindi-
vidual modules increases as well, because it is usually easierto "patch" the logic in an existing
module rather than introducing a new module into the system design.
11.1.1 Effect ofchanges on cyclomatic complexity
Cyclomatic complexity usually increases gradually during maintenance, since the increase in
complexity is proportional to the complexity ofthe new code. Forexample, adding four deci-
sions to a module increases its complexity by exactly four. Thus, although complexity can
become excessive ifnot controlled, the effects of any particular modification on complexity
are predictable.
11.1.2 Effect ofchanges on essential complexity
Essential complexity can increase suddenly during maintenance, since adding a single state-
ment can raise essential complexity from 1 to the cyclomatic complexity, making a perfectly
structured module completely unstructured. Figure 11-1 illustrates this phenomenon. The
first flow graph is perfectly structured, with an essential complexity of 1. The second flow
graph, derived from the first by replacing a functional statement with a single "goto" state-
ment, is completely unstructured, with an essential complexity of 12. The impact on essential
83

complexity may not be obvious from inspection ofthe source code, or even to the developer
making the change. It is therefore very important to measure essential complexity before
accepting each modification, to guard against such catastrophic structural degradation.
v(G)=12 v(G)=12
ev(G)=
l
ev(G)=12
Figure 11-1.Catastrophicstructural degradation.
11.1.3 Incremental reengineering
An incremental reengineering strategy [WATSON 1] provides greater benefits than merely
A
monitoring the effects ofindividual modifications on complexity. majorproblem with soft-
ware is that it gets out ofcontrol. Generally, the level ofreengineering effort increases from
simple maintenance patches through targeted reverse engineering to complete redevelopment
as software size increases and quality decreases, but only up to a point. There is a boundary
beyond which quality is too poor for effective reverse engineering, size is too large for effec-
tive redevelopment, and so the only approach left is to make the system worse by performing
localized maintenance patches. Once that boundary is crossed, the system is out ofcontrol
and becomes an ever-increasing liability. The incremental reengineering technique helps
keep systems away from theboundary by improving software quality in the vicinity ofroutine
maintenance modifications. The strategy is to improve the quality ofpoor software that inter-
acts with software that mustbe modified during maintenance. The result is that software qual-
ity improves during maintenance rather than deteriorating.
84

Retesting
| 77.2     |     |      | at thepath     | level   |               |     |              |     |            |     |           |          |
| -------- | --- | ---- | -------------- | ------- | ------------- | --- | ------------ | --- | ---------- | --- | --------- | -------- |
| Although |     | most | well-organized |         |               |     |              |     |            |     |           |          |
|          |     |      |                | testing | is repeatable |     | as discussed |     | in section |     | 1 1.4, it | is some- |
times expensive to perform complete regression When a change module
|     |     |     |     |     |     | testing. |     |     |     | to  | a   | is local- |
| --- | --- | --- | --- | --- | --- | -------- | --- | --- | --- | --- | --- | --------- |
ized, may be possible to avoid testing the changed module from scratch. Any path that had
it
been tested in the previous version and does not execute any ofthe changed software may be
new
considered tested in the version. After testing information for those preserved paths has
| been |         | forward |     | had been | executed | through |     | new |         |     |          |        |
| ---- | ------- | ------- | --- | -------- | -------- | ------- | --- | --- | ------- | --- | -------- | ------ |
|      | carried |         | as  | ifit     |          |         |     | the | system, | the | standard | struc- |
tured testing techniques can be used to complete the basis. This technique most effective
is
when the change is to a rarely executed area ofthe module, so that most ofthe tested paths
through the previous version can be preserved. The technique is not applicable when the
| changed |     |     |     |     | example |     |     |     |     |     |     |     |
| ------- | --- | --- | --- | --- | ------- | --- | --- | --- | --- | --- | --- | --- |
software is always executed, for the module's initialization code, since in
|      | case | paths      | must | be        |     |     |     |     |     |     |     |     |
| ---- | ---- | ---------- | ---- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
| that |      | all        |      | retested. |     |     |     |     |     |     |     |     |
| 11.3 | Data | complexity |      |           |     |     |     |     |     |     |     |     |
The specifieddata complexity, sdv, ofa module and a set ofdata elements is defined as the
cyclomatic complexity ofthe reduced graph after applying the module design complexity
|     |     |     | from |     |     |     |     | nodes | correspond |     |     |     |
| --- | --- | --- | ---- | --- | --- | --- | --- | ----- | ---------- | --- | --- | --- |
reduction rules section 7.4, except that the "black dot" to references to
| data | elements |     | the specified |            | than | module |        | As  | a       |       | the | sdv ofa |
| ---- | -------- | --- | ------------- | ---------- | ---- | ------ | ------ | --- | ------- | ----- | --- | ------- |
|      |          |     | in            | set rather |      |        | calls. |     | special | case, |     |         |
module with no references to data in the specified set defined to be 0. Specified data com-
is
plexity is really an infinite class ofmetrics rather than a single metric, since any set ofdata
may
elements be specified. Examples include a single element, all elements of aparticular
[WATS0N3].
| type, | or  | all global | elements |     |     |     |     |     |     |     |     |     |
| ----- | --- | ---------- | -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
The data-reduced graph contains control structures that interact with references to speci-
all
fied data, and changes to that data may be tested by executing a basis set ofpaths through the
reduced graph. Specified data complexity can therefore be used to predict the impact of
changes
|     |     | to the | specified | data. |     |     |     |     |     |     |     |     |
| --- | --- | ------ | --------- | ----- | --- | --- | --- | --- | --- | --- | --- | --- |
One particularly interesting data set consists of references to dates [MCCABE6]. The
all
"Year 2000 Problem" refers to the fact that a vast amount ofsoftware only stores the last two
When
digits ofthe year field ofdate data. this field changes from 99 to 00 in the year 2000,
| computations |     |     |           | comparison |      |       |            |     | problem |     |            |     |
| ------------ | --- | --- | --------- | ---------- | ---- | ----- | ---------- | --- | ------- | --- | ---------- | --- |
|              |     |     | involving | date       | will | fail. | Correcting |     | this    |     | is already | (in |
1996) becoming a major focus ofsoftware maintenance Calculating the "date com-
activity.
plexity" (specified datacomplexity with respect to date references) helps determine the scope
oftheproblem, andthecorresponding "date-reduced" flow graphs can be used to generate test
when
| cases |     | the | corrections | are implemented. |     |     |     |     |     |     |     |     |
| ----- | --- | --- | ----------- | ---------------- | --- | --- | --- | --- | --- | --- | --- | --- |
85

11.4 Reuse oftesting information
Although the technique described in section 1 1.2 can occasionally be used to reduce the
regression testing effort, it is best to rerun all ofthe old tests after making modifications to
software. The outputs should be examined to make sure that correct functionality was pre-
served and that modified functionality conforms to the intended behavior. Then, the basis
path coverage ofthe new system induced by those old tests should be examined and aug-
mented as necessary. Although this may seem like atremendous effort, it is mostly a matter
ofgood organization and proper tool selection.
Graphical regression testing tools and embedded system simulators facilitate test execution
and functional comparison in the most difficult environments. Most non-interactive applica-
tions software can be tested effectively at the integration level with simple regression suites
and a text comparison utility for outputs, tied together with system command scripts. At the
module level, stub and driver code should certainly not be discarded after one use ~ minimal
extra effort is required to store it for automated regression purposes, although it must be kept
current as the software itselfis modified.
An automated coverage tool can determine the level ofbasis path coverage at each regression
run, and indicate what further tests need to be added to reflect the changes to the software.
The resulting new tests should ofcourse be added to the automated regression suite rather
than executed once and discarded. Some discipline is required to maintain regression suites in
the face oflimited schedules and budgets, but the payoff is well worth the effort.
When full regression testing is really impractical, there are various shortcuts that still give a
reasonable level of testing. First is to keep "minimized" regression suites, in which only key
functional tests and tests that increased basis path coverage on the original system are exe-
cuted. This technique preserves most but not all ofthe error detection ability ofthe complete
set oforiginal tests, as discussed in Appendix B, and may result in a regression suite ofman-
ageable size. A possible drawback is that some ofthe original tests that were eliminated due
to not increasing coverage ofthe original system might have increased coverage ofthe new
system, so extra test cases may be needed. Another technique is to save the old coverage
information for modules that have not changed, and fully test only those modules that have
changed. At the integration level, calls to changed modules from unchanged modules can be
tested using the incremental integration method described in section 7-6.
One final point about regression testing is that it is only as effective as the underlying behav-
ior verification oracle. Too many otherwise comprehensive regression suites use unexamined
(and therefore probably incorrect) output from the time when the suite was constructed as the
standard for comparison. Although it may not be feasible to verify correctness for every test
case in a large regression suite, it is often appropriate to have an ongoing project that gradu-
ally increases the percentage ofverified regression outputs.
86

1 2 Summary by Lifecycle Process
This section gives abriefsummary ofthe structured testing techniques during each process in
a simplified software lifecycle.
12.1 Designprocess
Consider the expected cyclomatic complexity when partitioning functionality into modules,
with a view towards limiting the complexity ofeach module to 10. Limiting the explicit com-
plexity ofmodules in the design to 7 is usually sufficient. Estimate unit testing effort. Esti-
mate the eventual integration complexity from the design. Plan high-level integration tests.
12.2 Codingprocess
Limit the cyclomatic complexity ofmodules to 10 wherever possible without violating other
good design principles, and document any exceptions. Examine the control flow graphs of
modules with essential complexity greater than 1 and improve the quality oftheir logic struc-
ture where feasible. Plan unit tests.
12.3 Unit testingprocess
Test a basis set ofpaths through each module. This can be done either by first running func-
tional tests and then executing only the additional paths to completebasis path coverage, orby
planning andexecuting acomplete basis set ofpaths using the baseline method independently
offunctional testing. For modules for which acomplete basis cannot be executed due to con-
trol flow dependencies, analyze those dependencies and either eliminate or document them.
Build a unit level regression suite so that all tests are repeatable.
12.4 Integration testing process
Test abasis set ofpaths through the design-reduced control flow graph ofeach module, either
by first running functional tests and then executing only the additional paths to complete cov-
erage, orby using integration complexity to plan and execute a complete basis set ofintegra-
tion subtrees. Apply the incremental integration testing techniques ateach stage ofthe overall
integration strategy. For object-oriented systems, select a strategy for testing polymorphic
87

call resolutions based on complexity emalysis and subjective risk assessment, and apply the
safety analysis technique to avoid unnecessary testing. Build an integration level regression
suite so that all tests are repeatable. Take care to verify initial system behavior to the greatest
feasible extent so that the error detection power ofthe regression suite is not wasted.
12.5 Maintenanceprocess
Prevent sudden degradation ofcontrol structure quality by rejecting modifications that signif-
icantly increase essential complexity. Avoid increasing the cyclomatic complexity ofmod-
ules beyond 10 whenever feasible. Use the incremental reengineering technique to improve
overall system quality during routine modifications. Use data complexity analysis to assess
the impact ofpotential data structure changes and guide testing ofdatachanges. Perform full
regression testing where feasible, otherwise select a shortcut technique to test the specific
changed software.
88

13 References
[BERGE]
|        | C, Graphs | and | Hvpergraphs |     |                |       |     |     |     |     |
| ------ | --------- | --- | ----------- | --- | -------------- | ----- | --- | --- | --- | --- |
| Berge, |           |     |             |     | North-Holland, | 1973. |     |     |     |     |
.
[BERTOUNO]
Bertolino, A. and "On Use ofTestability Measures Dependability
|     |     | L.  | Strigini, | the |     |     |     | for |     |     |
| --- | --- | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
Assessment," IEEE Transactions on Software Engineering, February 1996.
[BORGER]
Borger, D., "Supporting Process Improvement With McCabe Tools," Proceedings of
| 1995McCabe |     |       |       |             |     | May   |     |     |     |     |
| ---------- | --- | ----- | ----- | ----------- | --- | ----- | --- | --- | --- | --- |
| the        |     | Users | Group | Conference, |     | 1995. |     |     |     |     |
[BOYD]
McCabe
Boyd, D., "Application ofthe Metric in Evolutionar>' Prototyping," Proceed-
|            | 1995McCabe |     | Users | Group |             | May |       |     |     |     |
| ---------- | ---------- | --- | ----- | ----- | ----------- | --- | ----- | --- | --- | --- |
| ings ofthe |            |     |       |       | Conference, |     | 1995. |     |     |     |
[BRE.LIANT]
and Knight and N. Leveson, "The Consistent Comparison Problem
| Brilliant, | S.  | J.  |     |     |     |     |     |     |     | in  |
| ---------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
ACM
N-Version Software," Software Engineering Notes, January 1987.
[CALDffiRA]
SW
Caldiera, G. and V. Basili, "Identifying and Qualifying Reusable Components,"
IEEE
| Computer, |     | February | 1991. |     |     |     |     |     |     |     |
| --------- | --- | -------- | ----- | --- | --- | --- | --- | --- | --- | --- |
[CARVER]
|         | "Producing |     | Maintainable |     |            | Computers |     | andIndustrialEngineer- |     |     |
| ------- | ---------- | --- | ------------ | --- | ---------- | --------- | --- | ---------------------- | --- | --- |
| Carver, | D.,        |     |              |     | Software," |           |     |                        |     |     |
| April   | 1987.      |     |              |     |            |           |     |                        |     |     |
ing,
[CHIDAMBER]
Chidamber, S. and C. Kemerer, "Towards a Metrics Suite for Object Oriented
| Design," | Proceedings |     | ofOOPSLA, |     | July 1991. |     |     |     |     |     |
| -------- | ----------- | --- | --------- | --- | ---------- | --- | --- | --- | --- | --- |
[COLEMAN]
|          |        |        | Ash | Lowther |                | Oman,  | "Using |         |             |     |
| -------- | ------ | ------ | --- | ------- | -------------- | ------ | ------ | ------- | ----------- | --- |
| Coleman, | D.     | and D. | and | B.      | and            | P.     |        | Metrics | to Evaluate |     |
| Software | System |        |     |         | IEEE Computer, | August |        | 1994.   |             |     |
Maintainability,"
89

[DAHL]
Dahl, O. and E. Dijkstra and C. Hoare, Structured Programming. Academic Press,
1973.
[FEGHALI]
Feghali, I. and A. Watson, "Clarification Concerning Modularization and McCabe's
|            |              | Communications |     |       | ACM,        |     |
| ---------- | ------------ | -------------- | --- | ----- | ----------- | --- |
| Cyclomatic | Complexity," |                |     | ofthe | April 1994. |     |
[FIRESMITH]
|                   | "Testing | Object-Oriented |     | Software," | Software Engineering |             |
| ----------------- | -------- | --------------- | --- | ---------- | -------------------- | ----------- |
| Firesmith,        | D.,      |                 |     |            |                      | Strategies, |
| November/December |          | 1993.           |     |            |                      |             |
[GEORGE]
George, "Proving Design Integrity," Proceedings ofthe 1993 McCabe Users
P.,
| Group | Conference, | April 1993. |     |     |     |     |
| ----- | ----------- | ----------- | --- | --- | --- | --- |
[GIBSON]
Gibson, V. and J. Senn, "System Structure and Software Maintenance Performance,"
|                |     | ACM, March |       |     |     |     |
| -------------- | --- | ---------- | ----- | --- | --- | --- |
| Communications |     | ofthe      | 1989. |     |     |     |
[GILL]
and Kemerer, "Cyclomatic Complexity Density and Software Maintenance
| Gill, G. | C.  |     |     |     |     |     |
| -------- | --- | --- | --- | --- | --- | --- |
Productivity," IEEE Transactions on Software Engineering, December 1991.
[HANSON]
Hanson, D., "Printing Common Words," Communications ofthe ACM, July 1987.
[HEIMANN]
—
A CASE
Heimann, D., "Complexity and Defects in Software Study," Proceedings
|       | 1994McCabe |             |             | May |       |     |
| ----- | ---------- | ----------- | ----------- | --- | ----- | --- |
| ofthe |            | Users Group | Conference, |     | 1994. |     |
[HENRY]
"On Among
Henry, S. and D. Kafura and K. Harris, the Relationships Three Software
ACM
|               | 1981  | Workshop/Symposium |     | on MeasurementandEvaluation |     |         |
| ------------- | ----- | ------------------ | --- | --------------------------- | --- | ------- |
| Metrics,"     |       |                    |     |                             |     | ofSoft- |
| ware Quality, | March | 1981.              |     |                             |     |         |
[HETZEL]
QED
Hetzel, W., The Complete Guide to Software Testing Information Sciences,
,
1984.
90

[HOPCROFT]
|                 | and | Ullman, |              |     | Automata |         |            |     | Compu- |
| --------------- | --- | ------- | ------------ | --- | -------- | ------- | ---------- | --- | ------ |
| Hopcroft,       | J.  | J.      | Introduction |     | to       | Theory, | Languages, |     | and    |
| Addison-Wesley. |     |         | 1979.        |     |          |         |            |     |        |
tation.
[JONES]
| Jones, C, | Applied | Software | Measurement |     | McGraw-Hill, |     | 1991. |     |     |
| --------- | ------- | -------- | ----------- | --- | ------------ | --- | ----- | --- | --- |
.
[KAFURA]
Kafura, D. and G. Reddy, "The Use ofSoftware Complexity Metrics in Software
IEEE
Maintenance," Transactions on Software Engineering, March 1987.
[KERNIGHAN]
| Kernighan, | and |             | The |          | ofProgramming |     |       | McGraw-Hill, |     |
| ---------- | --- | ----------- | --- | -------- | ------------- | --- | ----- | ------------ | --- |
|            | B.  | P. Plauger, |     | Elements |               |     | Style |              |     |
,
1974.
[KNUTH]
FORTRAN
Knuth, D., "An Empirical Study of Programs," Software Practice and
| Experience, | April-June |     | 1971. |     |     |     |     |     |     |
| ----------- | ---------- | --- | ----- | --- | --- | --- | --- | --- | --- |
[KOSHGOFTAAR]
Koshgoftaar, T. and E. Allen and K. Kalaichelvan and N. Goel, "Early Quality Predic-
| A     | Case  |                         |     |     | IEEESoftware, |     |         |     |       |
| ----- | ----- | ----------------------- | --- | --- | ------------- | --- | ------- | --- | ----- |
| tion: | Study | in Telecommunications," |     |     |               |     | January |     | 1996. |
[LEVESON]
Leveson, SAFEWARE: System and Computers Addison-Wesley, 1995.
|     | N., |     |     |     | Safety |     |     |     |     |
| --- | --- | --- | --- | --- | ------ | --- | --- | --- | --- |
.
[MCCABEl]
McCabe, "A Complexity Measure," IEEE Transactions on Software Engineering,
T.,
| December | 1976. |     |     |     |     |     |     |     |     |
| -------- | ----- | --- | --- | --- | --- | --- | --- | --- | --- |
[MCCABE2]
Communi-
McCabe T. and C. Butler, "Design Complexity Measurement and Testing,"
|         | ACM,  | December |     |       |     |     |     |     |     |
| ------- | ----- | -------- | --- | ----- | --- | --- | --- | --- | --- |
| cations | ofthe |          |     | 1989. |     |     |     |     |     |
[MCCABE3]
McCabe, and Dreyer and A. Dunn and A. Watson, "Testing an Object-Oriented
T. L.
Application," Journal ofthe QualityAssurance Institute, October 1994.
[MCCABE4]
McCabe, T. and A. Watson, "Combining Comprehension and Testing in Object-Ori-
| ented Development," |     | ObjectMagazine, |     |     | March-April | 1994. |     |     |     |
| ------------------- | --- | --------------- | --- | --- | ----------- | ----- | --- | --- | --- |
91

.
[MCCABE5]
| McCabe, |     | and      | Watson,     |     |           |              |       |            | The |            |
| ------- | --- | -------- | ----------- | --- | --------- | ------------ | ----- | ---------- | --- | ---------- |
|         |     | T,       | A.          |     | "Software | Complexity," |       | CrossTalk: |     | Journal of |
| Defense |     | Software | Engineering |     | December  |              | 1994. |            |     |            |
[MCCABE6]
McCabe, T., "Cyclomatic Complexity and the Year 2000," IEEESoftware, May 1996.
[MILLER]
Miller, G., "The Magical Number Seven, Plus or Minus Two: Some Limits on Our
Capacity for Processing Information," The PsychologicalReview, March 1956.
[MOSEMANN]
Mosemann,
L., "Metrics Are Meaningful," CrossTalk: The Journal ofDefense Soft-
| ware |              |     | August |     |       |     |     |     |     |     |
| ---- | ------------ | --- | ------ | --- | ----- | --- | --- | --- | --- | --- |
|      | Engineering, |     |        |     | 1992. |     |     |     |     |     |
[MUSA]
Musa, and A. Ackerman, "Quantifying Software Validation: When Stop Test-
|        | J.            |     |     |     |       |     |     |     |     | to  |
| ------ | ------------- | --- | --- | --- | ----- | --- | --- | --- | --- | --- |
| ing?," | IEEESoftware, |     |     | May | 1989. |     |     |     |     |     |
[MYERSl]
Myers, G., "An Extension to the Cyclomatic Measure ofProgram Complexity," SIG-
PLAN
|     | Notices, |     | October | 1 977 |     |     |     |     |     |     |
| --- | -------- | --- | ------- | ----- | --- | --- | --- | --- | --- | --- |
[MYERS2]
| Myers, |     | G., The | Art ofSoftware |     | Testing | Wiley, | 1989. |     |     |     |
| ------ | --- | ------- | -------------- | --- | ------- | ------ | ----- | --- | --- | --- |
.
[NBS99]
| NBS |         |             |     |         |     | McCabe, |                     |     |     | A SoftwareTesting |
| --- | ------- | ----------- | --- | ------- | --- | ------- | ------------------- | --- | --- | ----------------- |
|     | Special | Publication |     | 500-99, |     | T.      | "StructuredTesting: |     |     |                   |
Methodology Using Cyclomatic Complexity Metric," U.S. Department ofCom-
the
| merce/National |     |     | Bureau | of Standards |     | (U.S.), | December | 1982. |     |     |
| -------------- | --- | --- | ------ | ------------ | --- | ------- | -------- | ----- | --- | --- |
[NIST234]
NIST Special Publication 500-234, D. Wallace and L. Ippolito andB. Cuthill, "Refer-
ence Information for the Software Verification and Validation Process," U.S. Depart-
ment ofCommerce/National Institute ofStandards and Technology, April 1996.
[NIST5737]
| NISTIR |     |       |           | "A  | Method | Determine |     | a Basis | Set ofPaths | Perform Pro- |
| ------ | --- | ----- | --------- | --- | ------ | --------- | --- | ------- | ----------- | ------------ |
|        |     | 5737, | J. Poole, |     |        | to        |     |         |             | to           |
gram Testing," U.S. Department ofCommerce/National Institute ofStandards and
| Technology, |     | November |     | 1995. |     |     |     |     |     |     |
| ----------- | --- | -------- | --- | ----- | --- | --- | --- | --- | --- | --- |
92

[PARNAS]
Pamas, D., "On Criteria to be used in Decomposing Systems into Modules," Commu-
ACM,
| nications | ofthe |     | April 1972. |     |     |     |     |     |
| --------- | ----- | --- | ----------- | --- | --- | --- | --- | --- |
[PRESSMAN]
A
Pressman, R., Software Engineering: Practitioner's Approach McGraw-Hill, 1992.
.
[ROBERTS]
|             |               |      | McCabe | onReal-TimeEmbeddedComputerSoftware," |             |     |       |     |
| ----------- | ------------- | ---- | ------ | ------------------------------------- | ----------- | --- | ----- | --- |
| Roberts,    | B., "Usingthe |      |        | Tools                                 |             |     |       |     |
| Proceedings |               | 1994 | McCabe | Users Group                           |             | May |       |     |
|             | ofthe         |      |        |                                       | Conference, |     | 1994. |     |
[SCHNEIDEWINDl]
Schneidewind, N. and H. Hoffmann, "An Experiment Software Error Data Collec-
in
tion and Analysis," IEEE Transactions on Software Engineering, May 1979.
[SCHNEIDEWIND2]
IEEE
Schneidewind, N., "Methodology For Validating Software Metrics," Transac-
May
| tions on | Software | Engineering, |     | 1992. |     |     |     |     |
| -------- | -------- | ------------ | --- | ----- | --- | --- | --- | --- |
[SCHULTZ-JONES]
"Reverse Engineering With Forward Engineering Tools," Proceed-
| Schultz-Jones, |            | T., |       |                   |     |       |     |     |
| -------------- | ---------- | --- | ----- | ----------------- | --- | ----- | --- | --- |
| ings ofthe     | 1995McCabe |     | Users | Group Conference, | May | 1995. |     |     |
[SHEPPARD]
Sheppard, S. and E. Kruesi, "The Effects ofthe Symbology and Spatial Arrangement
of Software Specifications in a Coding Task," TechnicalReport TR-81-388200-3,
Company,
| General | Electric |     | 1981. |     |     |     |     |     |
| ------- | -------- | --- | ----- | --- | --- | --- | --- | --- |
[VENTRESS]
|           |               |       |               |                  |     | Proceedings | 1995  |     |
| --------- | ------------- | ----- | ------------- | ---------------- | --- | ----------- | ----- | --- |
| Ventress, | A., "Bailey's |       | Multiplatform | Implementation," |     |             | ofthe |     |
| McCabe    | User          | Group |               | May 1995.        |     |             |       |     |
Conference,
[VOAS]
Voas, and K. Miller, "SoftwareTestability: The New Verification," IEEESoftware,
J.
May 1995.
[WALSH]
|        | "A  |          |             |             |              | Measure,"AFIPS |     | Con- |
| ------ | --- | -------- | ----------- | ----------- | ------------ | -------------- | --- | ---- |
| Walsh, | T., | Software | Reliability | Study Using | a Complexity |                |     |      |
AFIPS
| ference | Proceedings, |     | Press, | 1979. |     |     |     |     |
| ------- | ------------ | --- | ------ | ----- | --- | --- | --- | --- |
93

[WARD]
Ward, W., "Software Defect Prevention Using McCabe's Complexity Metric,"
Hewlett-PackardJournal,
April 1989.
[WATSON
1]
Watson, "Incremental Reengineering: Keeping Control ofSoftware," CrossTalk:
A.,
| The Journal | ofDefense | Software Engineering, | January 1994. |     |
| ----------- | --------- | --------------------- | ------------- | --- |
[WATSON2]
&
Watson, A., "Why Basis Path Testing?," McCabe Associates Outlook, Winter 1994-
1995.
[WATSON3]
"McCabe
Watson, A., Complexity in Software Development," Systems Development
| Management34-40-35, |     | Auerbach, |     |     |
| ------------------- | --- | --------- | --- | --- |
1995.
[WATS0N4]
Watson, "Error Detection with Basis Path McCabe & Associates Out-
|              | A.,        |     | Testing," |     |
| ------------ | ---------- | --- | --------- | --- |
| look, Winter | 1995-1996. |     |           |     |
[WATSON5]
Watson, A., StructuredTesting: Analysis andExtensions. Ph.D. dissertation, Princeton
| University, | in preparation. |     |     |     |
| ----------- | --------------- | --- | --- | --- |
[YOURDON]
Yourdon
Yourdon, E. and L. Constantine, Structured Design Press, 1978.
.
[ZUSE]
|           | Software Complexity: | Measures | and Methods de |       |
| --------- | -------------------- | -------- | -------------- | ----- |
| Zuse, H., |                      |          | , Gruyter,     | 1990. |
94

Appendix
|     |     |     |     | A.  | Related |     | Case | Studies |     |     |
| --- | --- | --- | --- | --- | ------- | --- | ---- | ------- | --- | --- |
The structured testing methodology, including the testing techniques and related complexity
metrics described in this document, is above all apractical tool to support effective software
The
engineering. vast majority ofthis document describes structured testing by using mathe-
|     | examples, |     |     | and |     |     |     |     |     |     |
| --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
matics, intuition, theoretical analysis. This appendix provides empirical evi-
dence by presenting several case studies from the software engineering
literature.
Lloyd K. Mosemann III, while serving as Deputy Assistant Secretary ofthe Air Force (Com-
| munications, |     | Computers, |     | and Logistics), |     | wrote: |     |     |     |     |
| ------------ | --- | ---------- | --- | --------------- | --- | ------ | --- | --- | --- | --- |
Formany years, mostofus have been guilty ofthrowing verbal rocks atthosedeveloping soft-
ware metrics. Wehavedenigrated theirworkon thebasis thattheirproductsdid not"fully"or
"completely" measure such quantities as software size, structure, performance, and productiv-
ity. While wehave been waiting forthe perfect metrics we demand, however, wehavebeen
|     | measuring | almostnothing... |     |     |         |          | come      | toceaseouradmiration | ofthe |     |
| --- | --------- | ---------------- | --- | --- | ------- | -------- | --------- | -------------------- | ----- | --- |
|     |           |                  |     | I   | believe | the time | has forus |                      |       |     |
[MOSEMANN]
|     | metrics | problem | and | to start | implementing | some | metrics. |     |     |     |
| --- | ------- | ------- | --- | -------- | ------------ | ---- | -------- | --- | --- | --- |
Fortunately, complexity measurement has become a standard part of software engineering
practice, and the metrics described in this document have gained wide acceptance. Cyclo-
some
matic complexity in particular is calculated in form by nearly every commercial soft-
| ware |     |     |     |     | The |     |     |     |     | from |
| ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- |
complexity analysis product. papers in this section are listed chronologically,
work 1977 most recent 1996. Mostexamine various uses ofcyclomatic
| the        | earliest | in          |     | to the       |     | in  |     |     |     |     |
| ---------- | -------- | ----------- | --- | ------------ | --- | --- | --- | --- | --- | --- |
| complexity |          | in software |     | development. |     |     |     |     |     |     |
A.1 Myers
| Myers | [MYERS |     |     |     |     |     |     | programs |     |     |
| ----- | ------ | --- | --- | --- | --- | --- | --- | -------- | --- | --- |
1] calculatedcyclomatic complexity for the contained in the classic
by Kemighan and Plauger [KERNIGHAN]. For every case which an improved pro-
| text |     |     |     |     |     |     |     | in  |     |     |
| ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
gram was suggested, this improvementresulted in alowervalue ofv(G). Myers describes one
interesting case in which Kemighan and Plauger suggested two simplified versions ofa pro-
gram that has v(G) equal to 16. Myers found thatboth improvements resulted in acomplexity
| value | of 10.       |     |     |         |     |     |     |     |     |     |
| ----- | ------------ | --- | --- | ------- | --- | --- | --- | --- | --- | --- |
| A.2   | Schneidewind |     | and | Hojfman |     |     |     |     |     |     |
[SCHNEIDEWIND
Schneidewind and Hoffman performed an experimentthatrelatedcom-
1]
| plexity | to  | various | error | characteristics |     | ofsoftware. | They wrote: |     |     |     |
| ------- | --- | ------- | ----- | --------------- | --- | ----------- | ----------- | --- | --- | --- |
95

Thepropensitytomakeprogrammingerrors
|     |     |     |     |     |     |     | andtherates | oferrordetection |     | andcorrection | are |
| --- | --- | --- | --- | --- | --- | --- | ----------- | ---------------- | --- | ------------- | --- |
dependentonprogramcomplexity. Knowledge oftheserelationships can be used to avoid
|     |     |     |     | software | design |     | and |     |     | which |     |
| --- | --- | --- | --- | -------- | ------ | --- | --- | --- | --- | ----- | --- |
error-prone structures in to deviseatesting strategy is based on
anticipateddifficulty oferrordetection and correction. An experiment in softwareerrordata
collection and analysis was conducted in orderto study theserelationships underconditions
wheretheerrordatacould becarefully defined andcollected. Several complexity measures
whichcanbedefinedin terms ofthedirectedgraphrepresentation ofaprogram, suchascyclo-
|     | matic | number, | wereanalyzed |     | withrespectto |     | thefollowing |                       |     |        |        |
| --- | ----- | ------- | ------------ | --- | ------------- | --- | ------------ | --------------------- | --- | ------ | ------ |
|     |       |         |              |     |               |     |              | errorcharacteristics: |     | errors | found, |
timebetween errordetections, and errorcorrection time. Significantrelationships were found
between complexity measures and errorcharacteristics. Themeaning ofdirected graph
struc-
turalproperties in terms ofthecomplexity oftheprogrammingand testingtasks was exam-
ined.
Basedonthisexperimentweconcludethat,
|     |     |     |     |     |     |     | forsimilarprogrammingenvironments |     |     | andassum- |     |
| --- | --- | --- | --- | --- | --- | --- | --------------------------------- | --- | --- | --------- | --- |
ing astable programmingpersonnel situation, structure would have asignificanteffecton the
|     | numberoferrors |     | made |     |                   |     |        |             |           |                |     |
| --- | -------------- | --- | ---- | --- | ----------------- | --- | ------ | ----------- | --------- | -------------- | --- |
|     |                |     |      | and | labortimerequired |     | tofind | and coiTect | theerrors | ... complexity |     |
measures serveto partition structures into high orlowerroroccurrenceaccording to whether
|     | complexity |     | measure |        |         |        |               |     |     |     |     |
| --- | ---------- | --- | ------- | ------ | ------- | ------ | ------------- | --- | --- | --- | --- |
|     | the        |     |         | values | arehigh | orlow, | respectively. |     |     |     |     |
A.3 Walsh
| Walsh | [WALSH] |     |     |     |     | number |     |     |     |     |     |
| ----- | ------- | --- | --- | --- | --- | ------ | --- | --- | --- | --- | --- |
collected data on the of software errors detected during the devel-
opment phase ofthe AEGIS Naval Weapon System. The system contained of276
a total
modules, approximately halfofwhich had a v(G) than 10 and halfwith v(G) of 10 or
less
greater. The average error rate for modules with complexity less than 10 was 4.6 per 100
source statements, while the corresponding error rate for the more complex modules was 5.6.
| As Walsh |     |     |     | would |     |     |     |     |     |     |     |
| -------- | --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- |
pointed out, one expect a similarpattern forundetected errors as well, so that
|      | complex | modules |      | have | lower  |       |            |          |     |       |     |
| ---- | ------- | ------- | ---- | ---- | ------ | ----- | ---------- | -------- | --- | ----- | --- |
| less |         |         | will |      | a      | error | rate after | delivery | as  | well. |     |
| A.4  | Henry,  | Kafura, |      | and  | Harris |       |            |          |     |       |     |
UNIX
Henry, Kafura, and Harris [HENRY] reported empirical error data collected on the
UNIX
operating system. The authors obtained a list oferrors from the Users Group and per-
| formed |     |     |     |     |     | The |     |     |     | was most |     |
| ------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | -------- | --- |
correlations with three metrics. cyclomatic complexity the closely
—
|         |           |     | ofthe |        |                 |     | between | v(G) | and number | oferrors | was  |
| ------- | --------- | --- | ----- | ------ | --------------- | --- | ------- | ---- | ---------- | -------- | ---- |
| related | to errors |     | three |        | the correlation |     |         |      |            |          | .96. |
| A.5     | Sheppard  |     | and   | Kruesi |                 |     |         |      |            |          |      |
[SHEPPARD]
Sheppard and Kruesi examined the performance ofprogrammers in construct-
|     |     | from |     |     |     |     | An  |     |     |     |     |
| --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
ing programs various specification formats. automated data collection system
recorded complete sequence ofevents involved constructing and debugging the pro-
|     | the |     |     |     |     |     |     | in  |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
gram. An analysis ofthe error data revealed that the major source ofdifficulty was related to
96

|     | flow | and |     |     |     | number |     |     |     |     |     |     |
| --- | ---- | --- | --- | --- | --- | ------ | --- | --- | --- | --- | --- | --- |
the control not to such factors as the ofstatements or variables. The most
|           | program |     | had the most | complex | decision |     |            | while |     |              |        |      |
| --------- | ------- | --- | ------------ | ------- | -------- | --- | ---------- | ----- | --- | ------------ | ------ | ---- |
| difficult |         |     |              |         |          |     | structure, |       | a   | considerably | easier | pro- |
gram performed extremely complex arithmetic calculations but had a simpler decision
struc-
ture. Thus, v(G) can be used to measure a difficult aspect ofprogramming.
A.6 Carver
Carver [CARVER] collected data on approximately 14,000 ofcode order
|     |     |     |     |     |     |     |     | lines |     | in  | to  | study the |
| --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --------- |
change in complexity metrics from code initiation to code completion. Structured program-
ming practices were followed and code reviews used in the generation ofthe code. The cyclo-
matic complexity values ranged from 8 to 78 for this code, with changes to v(G) averaging
| 35% | with | median | of25%, |     |     |     |     |     |     |     |     |     |
| --- | ---- | ------ | ------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
a value indicating that "approximately 1/3 ofthe control flow logic
| was added |       | code |             |     | percentage | of  | 35% | increase | suggests |      |        |            |
| --------- | ----- | ---- | ----------- | --- | ---------- | --- | --- | -------- | -------- | ---- | ------ | ---------- |
|           | after |      | initiation. |     | ...A       |     |     |          |          | that | either | the origi- |
nal designs wereincomplete ortheprogrammers implementedthe designs in an unsatisfactory
manner." The complexity metric variance investigation benefits include: "First, is valuable
it
for anticipating complexity increases during design so that proper module sizing can be
addressed. Secondly, it provides input for measuring the completeness ofthe original design
|                 |     | The | study concludes |     |      | complexity |           |     |        | ranges | noted    |     |
| --------------- | --- | --- | --------------- | --- | ---- | ---------- | --------- | --- | ------ | ------ | -------- | --- |
| specification." |     |     |                 |     | that |            | increases |     | in the |        | indicate |     |
that designers must not only plan for growth, but also modularize the code to allow for con-
trolled growth, otherwise modules will be implemented with unacceptable complexity levels.
|     |     | and | Reddy |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
A.7 Kafura
A was performed by Kafura and Reddy [KAFURA] cyclomatic complexity
| study |     |     |     |     |     |     |     | that | related |     |     |     |
| ----- | --- | --- | --- | --- | --- | --- | --- | ---- | ------- | --- | --- | --- |
as well as other software complexity metrics the experience ofvarious maintenance
|     | six |     |     |     |     | to  |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
activities performed on a database management system consisting of 16,000 lines ofFOR-
TRAN
code. The authors used a subjective evaluation technique, relating the quantitative
who
measures obtained from the metrics to assessments by informed experts are very familiar
with systems being This was done determine information obtained from
|     | the |     | studied. |     |     | to  |     | ifthe |     |     |     |     |
| --- | --- | --- | -------- | --- | --- | --- | --- | ----- | --- | --- | --- | --- |
the metrics would be consistent with expert experience and could be used as a guide to avoid
| poor    | maintenance |     | work. |     |     |     |     |     |      |     |     |     |
| ------- | ----------- | --- | ----- | --- | --- | --- | --- | --- | ---- | --- | --- | --- |
| Changes |             |     |       |     |     |     |     |     | were |     |     |     |
in system level complexity for each ofthree versions analyzed. After an analy-
| ofthe |         | ofthe |          |     | authors | concluded |      |     | "change | complexities |     | over |
| ----- | ------- | ----- | -------- | --- | ------- | --------- | ---- | --- | ------- | ------------ | --- | ---- |
| sis   | results |       | metrics, | the |         |           | that | the |         | in           |     |      |
time agrees with what one would expect." Also noted was that the complexity growth curves
"seemed to support the view that maintenance activities - either enhancements or repairs -
many
| impact |     | different | aspects | ofthe | system | simultaneously." |     |     |     |     |     |     |
| ------ | --- | --------- | ------- | ----- | ------ | ---------------- | --- | --- | --- | --- | --- | --- |
An made changes procedure complexity can be monitored question
| observation |     |     | is that |     | in  |     |     |     |     |     | to  |     |
| ----------- | --- | --- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
large changes in complexity that are not planned. The authors also note that developers tend
97

to avoid changing very complex procedures during maintenance, even ifthe
alternative
changes lead to a degradation in overall design quality, and suggest that managers monitorthe
| implementation |        | ofthose  | changes. |     |     |     |     |     |     |     |     |     |
| -------------- | ------ | -------- | -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A.8            | Gibson | and Senn |          |     |     |     |     |     |     |     |     |     |
Gibson and Senn [GIBSON] conducted an experiment using COBOL code
|     |     |     |     |     |     |     |     |     |     | to investigate |     | the |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | -------------- | --- | --- |
relationship between system structure and maintainability, with the purpose ofdetermining
whether a set ofsix objective complexity metrics might offerpotential as project management
|     |     |     |     | when |     |     |     |     |     |     |     | how |
| --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
tools. They studied the effects an old, badly structured system is "improved" and
| improvements |     | impact     |                  |     |        | The        |     | were         |              | whether    |     |      |
| ------------ | --- | ---------- | ---------------- | --- | ------ | ---------- | --- | ------------ | ------------ | ---------- | --- | ---- |
| the          |     |            | maintainability. |     |        | objectives |     |              | to determine |            |     |      |
| improvements |     | the system |                  |     |        | measurable |     | improvements |              | programmer |     |      |
|              |     | in         | structure        |     | result | in         |     |              |              | in         |     | per- |
formance, whether programmers can discern system differences, and whether these system
| differences |     | can be measured | by  | existing, | automated |     | metrics. |     |     |     |     |     |
| ----------- | --- | --------------- | --- | --------- | --------- | --- | -------- | --- | --- | --- | --- | --- |
While all six metrics appeared to be related to performance, the metrics were grouped into two
|              |     |               | The | cyclomatic |     | complexity |     |        | was    | which | provided |     |
| ------------ | --- | ------------- | --- | ---------- | --- | ---------- | --- | ------ | ------ | ----- | -------- | --- |
| sets ofthree |     | metrics each. |     |            |     |            |     | metric | in the | set   |          |     |
rankings consistent with time and the frequency ofserious ripple
| "relative |     |     |     | relative |     |     |     |     |     |     | effect |     |
| --------- | --- | --- | --- | -------- | --- | --- | --- | --- | --- | --- | ------ | --- |
errors", while the other set was related more to the frequency ofprimary errors introduced
with modifications. To address the first issue ofthe study, the average maintenance time did
when
decrease the system structure was improved, measured in terms ofthe effect ofstructure
| on time, | accuracy, | and | confidence. |     |     |     |     |     |     |     |     |     |
| -------- | --------- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
With respect to their second objective, the study revealed that structural differences were not
discernible to programmers since programmers in the study could not separate out the com-
plexity ofthe system from the complexity ofthe task being undertaken. The authors stated
that this result "offers important evidence on the efficacy of subjectively based complexity
|            | The |             |             |     | may | conform |     |          | ofthe | maintenance | program- |     |
| ---------- | --- | ----------- | ----------- | --- | --- | ------- | --- | -------- | ----- | ----------- | -------- | --- |
| metrics... |     | inspector's | perceptions |     | not |         |     | to those |       |             |          |     |
mers, which may affect the predictive ofsubjective metrics overthe ofthe system."
|        |     |            |            |            | ability |     |                 |     |     | life |     |     |
| ------ | --- | ---------- | ---------- | ---------- | ------- | --- | --------------- | --- | --- | ---- | --- | --- |
| should | be  | noted that | cyclomatic | complexity |         |     | not subjective. |     |     |      |     |     |
| It     |     |            |            |            |         | is  |                 |     |     |      |     |     |
| The    |     |            |            |            |         |     |                 |     |     | when |     |     |
third objective dealt with the effect ofsystem structure and metrics, and the system
was improved, cyclomatic complexity indeed The authors conclude
| structure |     |     |     |     |     | did |     | decrease. |     |     |     |     |
| --------- | --- | --- | --- | --- | --- | --- | --- | --------- | --- | --- | --- | --- |
"objectively based metrics might provide more information for managers than
| that         |     |                  |     |     |     |     | reliable |     |     |     |     |     |
| ------------ | --- | ---------------- | --- | --- | --- | --- | -------- | --- | --- | --- | --- | --- |
| subjectively |     | based measures." |     |     |     |     |          |     |     |     |     |     |
98

A.9 Ward
Ward [WARD] studied two large-scale firmware projects HP's Waltham Division had
|     |     |     |     |     |     | at  |     |     | that |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- |
a very low postrelease defect density. He found that approximately 60% ofpost-release
defects had been introduced during the implementation phase, indicating that implementation
improvements
such as limiting complexity had the largest potential for quality improvement.
| Upon |                        |     | he found |      |            | complexity | had  |             |      |
| ---- | ---------------------- | --- | -------- | ---- | ---------- | ---------- | ---- | ----------- | ---- |
|      | further investigation, |     |          | that | cyclomatic |            | a .8 | correlation | with |
error density for the projects, and concluded limiting complexity was a
|     |     |     |     |     | that |     |     | significant | factor |
| --- | --- | --- | --- | --- | ---- | --- | --- | ----------- | ------ |
in software quality. He also reported successful usage ofthe baseline method to generate
| module | test cases. |        |     |     |     |     |     |     |     |
| ------ | ----------- | ------ | --- | --- | --- | --- | --- | --- | --- |
| A.10   | and         |        |     |     |     |     |     |     |     |
|        | Caldiera    | Basili |     |     |     |     |     |     |     |
Caldiera and Basili [CALDIERA] conducted experiments by using software metrics iden-
to
tify and "qualify" reusable software components from existing systems in order to reduce the
|     |     |     |     |     |     |     |     |     | ANSI C |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ |
amount ofcode that experts must analyze. The data consisted of 187,000 lines of
They
code, spanning 9 existing systems which represented a variety ofapplications. used four
|         |                 | one | ofwhich | was cyclomatic |     | complexity. | The reason |           |        |
| ------- | --------------- | --- | ------- | -------------- | --- | ----------- | ---------- | --------- | ------ |
| metrics | in their study, |     |         |                |     |             |            | for using | cyclo- |
matic complexity in their study was "The component complexity affects reuse cost and
that,
quality, taking into account the characteristics ofthe component's control flow. As with vol-
may
ume, reuse ofa component with very low complexity not repay the cost, whereas high
may
component complexity indicate poor quality - low readability, poor testability, and a
|     |     |     | On  |     |     | complexity |     |     |     |
| --- | --- | --- | --- | --- | --- | ---------- | --- | --- | --- |
higherpossibility oferrors. the other hand, high with high regularity ofimple-
mentation suggests high functional usefulness. Therefore, measure we need both an
|       |             |       |              |         |     | for | this |     |     |
| ----- | ----------- | ----- | ------------ | ------- | --- | --- | ---- | --- | --- |
| upper | and a lower | bound | in the basic | model." |     |     |      |     |     |
By
using the metrics, the authors were able to identify candidates for code reuse. They deter-
mined
that they could obtain satisfactory results using values that they calculated as extremes
|     | ranges ofacceptable |     |         |         |        | upper bound | v(G) | was 15.00 | with a |
| --- | ------------------- | --- | ------- | ------- | ------ | ----------- | ---- | --------- | ------ |
| for | the                 |     | values. | In this | study, | the         | for  |           |        |
lower bound of 5.00. The authors concluded that "these case studies show that reusable com-
ponents have measurable properties that can be synthesized in a simple quantitative model."
|     | and Kemerer |     |     |     |     |     |     |     |     |
| --- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- |
A.11 Gill
and Kemerer [GILL] presented research studied "the relationship between McCabe's
| Gill |     |     |     |     | that |     |     |     |     |
| ---- | --- | --- | --- | --- | ---- | --- | --- | --- | --- |
cyclomatic complexity and software maintenance productivity, given that a metric which
measures complexity should prove to be a useful predictor ofmaintenance costs." They con-
ducted this study to specifically validate the cyclomatic complexity metric foruse in software
99

testing and maintenance. The project analyzed approximately 150,000 lines ofcode from 19
software systems, comprising 834 modules ofwhich 771 were written in Pascal and 63 in
FORTRAN.
|     |     | The | authors | wrote: |     |     |     |     |     |     |     |     |
| --- | --- | --- | ------- | ------ | --- | --- | --- | --- | --- | --- | --- | --- |
Knowledgeofthe impactofcyclomatic complexity on maintenanceproductivity ispotentially
more valuable than thatof NCSLOC [noncomment source because managers
|     |     |     |     |     |     |     |     |     | lines | ofcode], |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | -------- | --- | --- |
typically do nothavea greatdeal ofcontrol overthe size ofaprogram since it is intimately
connected to the size ofthe application. However, by measuring and adoptingcomplexity
|     |     |     |     |     | CASE |     |     |     | manage |     |     |     |
| --- | --- | --- | --- | --- | ---- | --- | --- | --- | ------ | --- | --- | --- |
standards and/orby using restructuring tools, they can unnecessary cyclomatic
complexity.
The data from study supported previous research regarding the high between
|     |     |     | this |     |     |     |     |     |     |     | correlation |     |
| --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- | ----------- | --- |
cyclomatic complexity and NCSLOC. The authors extended the idea ofcyclomatic complex
ity to "cyclomatic density", which is the ratio ofthe module's cyclomatic complexity to its
NCSLOC.
length in The intent is to factor out the size component ofcomplexity. It has the
effect ofnormalizing the complexity of a module, and therefore its maintenance difficulty.
| The |     |     | was |     |     |     | and "shown |     | be  |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ---------- | --- | --- | --- | --- | --- |
density ratio tested in this research to a statistically significant single
| value | predictor |     | ofmaintenance |     | productivity." |     |     |     |     |     |     |     |
| ----- | --------- | --- | ------------- | --- | -------------- | --- | --- | --- | --- | --- | --- | --- |
A.12 Schneidewind
[SCHNEIDEWIND2],
Schneidewind performed a validation study the purpose being to deter
| mine |     |     |     |     |     | and |     |     |     | be used |     |     |
| ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------- | --- | --- |
whether cyclomatic complexity size metrics could to control factor reliabil-
|     | (represented |     |     |     |     |     |     | or  | combination. |     | A   | a   |
| --- | ------------ | --- | --- | --- | --- | --- | --- | --- | ------------ | --- | --- | --- |
ity as a factor error count), either singly in factor is quality
factor, "an attribute that contributes to quality, where software quality defined as the
|     |     |     |     |     |     | its |     |     |     |     | is  |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
degree to which software possesses a desired combination ofattributes." The data used in the
study was collected from actual software projects consisting of 1 12 total procedures, ofwhich
|     | were | known |     |     | and |     | no  | The |     |     | was |     |
| --- | ---- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
31 to have errors, 81 with errors. Pascal language used for the
| 1,600 | source | code | statements |     |      | were | included |     |        |     |     |     |
| ----- | ------ | ---- | ---------- | --- | ---- | ---- | -------- | --- | ------ | --- | --- | --- |
|       |        |      |            |     | that |      | in       | the | study. |     |     |     |
One ofthe statistical procedures used was a chi-square test, to determine whether cyclomatic
complexity could discriminate between those procedures with errors (as in low-quality soft-
The
ware) versus those without errors (a high-quality software). misclassifications that were
|         | were | divided |     | two  |         | Type |                      |     |     |          | procedures | with |
| ------- | ---- | ------- | --- | ---- | ------- | ---- | -------------------- | --- | --- | -------- | ---------- | ---- |
| studied |      |         |     | into | groups: |      | 1 misclassifications |     |     | included |            |      |
errors were classified not having The type 2 category wasjust the opposite:
|     | that |     |     | as  |     |     | errors. |     |     |     |     |     |
| --- | ---- | --- | --- | --- | --- | --- | ------- | --- | --- | --- | --- | --- |
those modules without errors were classified as having errors. The study found that as cyclo-
matic complexity increases. Type misclassifications increased because an increasing num-
1
many
ber ofhigh complexity procedures, of which had errors, were incorrectly classified as
| having | no  |         | However, |     |               |     | complexity |            |     | Type |                      |     |
| ------ | --- | ------- | -------- | --- | ------------- | --- | ---------- | ---------- | --- | ---- | -------------------- | --- |
|        |     | errors. |          |     | as cyclomatic |     |            | decreased. |     |      | 2 misclassifications |     |
increased, because an increasing number oflow complexity procedures, many having no
| errors, | were | incorrectly |     | classified |     | as having | errors. |     |     |     |     |     |
| ------- | ---- | ----------- | --- | ---------- | --- | --------- | ------- | --- | --- | --- | --- | --- |
100

The
most significant v(G) threshold for error prediction in this study was at v(G) <= 3, mean-
|     |     | would | be used |     |     |     |     |     |     |     |     |     |
| --- | --- | ----- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
ing that 3 as a critical value ofcyclomatic complexity to discriminate between
| components |     | containing | errors | and | those | do   | (This | value | was |           |     |          |
| ---------- | --- | ---------- | ------ | --- | ----- | ---- | ----- | ----- | --- | --------- | --- | -------- |
|            |     |            |        |     | that  | not. |       |       |     | supported | by  | plotting |
points, as well as by the chi-square Correctly classified were 75 ofthe 81 procedures
test.)
A
containing no errors, and 21 ofthe 31 procedures known to have errors. similar analysis
was
performed on source code size for these procedures, with an optimal value of 15 being
|     | The | authorconcludes |     |     | and |     |     |     |     |     |     |     |
| --- | --- | --------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
found. that size cyclomatic complexity are valid with respect to the
| "Discriminative |     |     | Power"     |     | and    | could | be used |     |             | between |     |            |
| --------------- | --- | --- | ---------- | --- | ------ | ----- | ------- | --- | ----------- | ------- | --- | ---------- |
|                 |     |     | criterion, |     | either |       |         | to  | distinguish |         |     | acceptable |
and unacceptable quality for the application studied and similar applications. Although the
author's focus was more on the validation technique than the specific validation study,
|     |     |     |     |     |     |     |     |     |     |     |     | it is |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- |
interesting that the thresholds for both complexity and size were found to be much less than
common
| those | in  |     | usage. |     |     |     |     |     |     |     |     |     |
| ----- | --- | --- | ------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
The author notes that quality control to allow software managers identify software
|     |     |     |     |     | "is |     |     |     |     | to  |     | that |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- |
has unacceptable quality sufficiently early in the development process to take corrective
action." Quality could be controlled throughout a component's life cycle, so that if v(G)
from
increased 3 to 8 due to a design change, it could indicate apossible degradation in qual-
ity.
| A.13 | Case | study | at Stratus | Computer |     |     |     |     |     |     |     |     |
| ---- | ---- | ----- | ---------- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
Cyclomatic and essential complexity were measured for a tape driver subsystem before and
|     |     |     |     | The | new | was |     |     |     | complex |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------- | --- | --- |
after a reengineering project. version significantly less than the origi-
|      | Twelve | months |       |          | follow-up |       | showed |     | fewer |      |              |     |
| ---- | ------ | ------ | ----- | -------- | --------- | ----- | ------ | --- | ----- | ---- | ------------ | --- |
| nal. |        |        | after | release, | a         | study |        |     | that  | than | five serious | or  |
critical errors had been discovered in the new software, a dramatic increase over
in reliability
the original system. Based on this result, complexity analysis was recommended as part ofthe
[GEORGE]
design process.
| A.14 | Case |       |            | Equipment |     |             |     |     |     |     |     |     |
| ---- | ---- | ----- | ---------- | --------- | --- | ----------- | --- | --- | --- | --- | --- | --- |
|      |      | study | at Digital |           |     | Corporation |     |     |     |     |     |     |
The relationship between defect corrections production software and both cyclomatic com-
in
plexity and the number oflines ofcode was studied. Defect corrections were used since they
map
defects to individual source modules in an objectively measurable way. Defect correc-
|     |     | more |     |     |     |     |     |     |     |     | number |     |
| --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- | ------ | --- |
tions were strongly correlated with cyclomatic complexity than with the oflines
ofcode.
The correlation between complexity and defect corrections was also investigated when mod-
ules with complexity greater than 12 and modules with complexity less than 12 were consid-
ered separately. In the high-complexity subset, complexity had a definite correlation with
| defect |              |     | However, |       | was    | no  |             |     |        | low-complexity |     |         |
| ------ | ------------ | --- | -------- | ----- | ------ | --- | ----------- | --- | ------ | -------------- | --- | ------- |
|        | corrections. |     |          | there | little | or  | correlation |     | in the |                |     | subset. |
101

The suggested explanation is that other factors outweigh complexity as asource oferror when
complexity is low, but that the impact ofcomplexity on defect occurrence is greater when
complexity is high. [HEIMANN]
A.15 Case study at U.S. Army Missile Command
Automated analysis ofcyclomatic complexity was used as part ofseveral Independent Valida-
tion and Verification projects, and found to be more accurate and comprehensive than the
manual methods for identifying overly complex software that had been previously used.
Automated complexity analysis also yielded a significant reduction in cost. Based on the suc-
cess ofthese projects, the same techniques were applied to other projects in various lan-
guages, including Ultra, Ada, C, C++, PL/M, and FORTRAN. [ROBERTS]
A.16 Coleman et al
A recent study was performed by Coleman, Ash, Lowther, and Oman [COLEMAN] to dem-
onstrate how automating the analysis ofsoftware maintainability can be used to guide soft-
ware-related decision making. The authors developed a four-metric polynomial, known as
HPMAS (HPMultidimensional AssessmentModel), in which cyclomatic complexity was one
ofthe four metrics used. The dataused to test and validate theirmodel utilized actual systems
provided by Hewlett-Packard and the Department ofDefense which encompassed eleven soft-
ware systems written in C for a Unix platform. They used their model to study three aspects
of system maintenance: To study pre/postanalysis ofmaintenance changes (over 1,200 lines
ofcode); to rank-order module maintainability (236,000 lines ofcode); and, to compare soft-
ware systems (one system consisted of 236,275 lines ofcode and the other 243,273 lines). In
each case, the model proved extremely useful.
The authors write that in each case,
theresults fromouranalysis corresponded tothe maintenance engineers' "intuition" aboutthe
maintainability ofthe (sub)system components. But, in every case, the automated analysis
provided additional datathat was useful in supporting orprovidingcredenceforthe experts'
opinions. Ouranalyses have assisted inbuy-versus-build decisions, targeting subcomponents
forperfective maintenance, controlling software quality andentropy overseveral versions of
the same software, identifyingchange-prone subcomponents, andassessing theeffects of
reengineeringefforts.
102

A.17 Case study at the AT&T Advanced Software Construction Center
Various aspects ofthe structured testing methodology have been integrated into the overall
development process, concentrating on code inspections and unit testing. The techniques
helped control complexity ofcode, select code for inspection, and measure basis path cover-
age during unit testing. The development team also used complexity analysis to re-design
overly complex modules, which reduced the unit testing effort. [BORGER]
A.18 Case study at Sterling SoftVt^are
The cyclomatic, design, and essential complexity metrics as well as test coverage were
applied to a successful large-scale prototyping effort. The project was part ofthe Air Force
Geographical Information Handling System (AFGIHS), a 3 year, $3.5 million effort to pro-
duce an advanced prototype for transition to a full scale development to support Air Force
requirements for geospatial display and analysis. Complexity analysis was used to monitor
software quality, reduce risk, and optimize testing resources. [BOYD]
A.19 Case Study at GTE Government Systems
Cyclomatic and design complexity were included in a large-scale software metrics collection
effort spanning many projects over an eight-year time period. Projects with similar cyclo-
matic and design complexity profiles were found to follow similar schedules, with respect to
the amount oftime spent on each development phase. Much ofthe development work
involves the reengineering oflegacy systems. Comparison ofthe cumulative complexity dis-
tribution of a legacy program with known programs in the metrics database is used to antici-
pate the development phases required to reengineer the legacy program. [SCHULTZ-JONES]
A.20 Case study at Elsag Bailey Process Automation
The cyclomatic and essential complexity metrics were used on a successful project that
involved the development ofapplication and communications interface software using a cli-
ent/server architecture to provide bi-directional communications to digital systems. Complex-
ity analysis helped identify potentially defective modules by pinpointing highly complex and
unstructured code, based on pre-defined company and industry standards. Acquisition ofthis
information early in the product release cycle helped minimize post-release maintenance
costs. These techniques allowed the product verification efforts to be quantified and moni-
[VENTRESS]
tored.
103

A.21 Koshgoftaar et al
Koshgoftaar, Allen, Kalaichelvan, andGoel [KOSHGOFTAAR] performedacase study using
a large telecommunications system that consisted of 1.3 million lines ofcode that was written
in a language similar to Pascal. The authors applied discriminant analysis to identify fault-
prone areas in a systempriorto testing. They developed amodel that incorporatedcyclomatic
complexity as one ofthe design product metrics. To evaluate the model's ability to predict
fault-prone modules, they compared the quality ofthe predictions based on test data to the
actual quality. The results were successful. The authors found that "design product metrics
basedoncall graphsandcontrol-flow graphscanbeuseful indicatorsoffault-pronemodules...
The study provided empirical evidence that in a software-maintenance context, a large sys-
tem's quality can be predicted from measurements ofearly development products and reuse
indicators."
104

Appendix B. Extended Example
This appendix illustrates the structured testing technique ofChapter 5 for a module ofsignifi-
cant complexity. The example is a C translation ofthe FORTRAN blackjack game program
used in [NBS99] for the same purpose. No attempt has been made to improve the structural
quality ofthe original version, and the error has been preserved. Section B.2 describes an
experimental framework forcomparison oftest coverage criteria. Although stmctured testing
does not guarantee detection ofthe error in the blackjack program, experimental results show
that it is much more effective than branch coverage.
B.1 Testing the blackjackprogram
Since there are many variants on the blackjack rules, the following specification describes the
rules being used for this example. The mechanics ofthe application of structured testing can
be understood without reference to the details ofthe specification, but the specification is
required to detect incorrect program behavior. The details ofthe "hand" module follow, as
does the description ofthe testing process.
B.1.1 The speciflcation
The program, as the dealer, deals two cards to itselfand two cards to the player. The player's
two cards are shown face up, while only one ofthe dealer's cards is shown. Both the dealer
and the player may draw additional cards, which is known as — being "hit." The player's goal is
to reach 21 or less, butbe closer to 21 than the dealer's hand in which case the player wins.
Ties go to the dealer. Ifthe player's or the dealer's hand totals greater than 21, the hand is
"busted" (a loss). The King, Queen, and Jack all count as 10 points. All other cards, except
the Ace, count according to their face values. The Ace counts as 1 1 unless this causes the
hand to be over 21, in which case it counts as 1.
Ifboth the dealer and the player get Blackjack, which i—s a two-card hand totaling 21, it is a
"push" (neither wins). Blackjack beats all other hands ifthe player has Blackjack, he wins
"automatically" before the dealer has a chance to take a hit. The player can also win automat-
ically by having five cards without being busted. The player may take any number ofhits, as
long as the hand is not busted. The dealer must take a hit while the hand is less than or equal
to 16, and must "stand" at 17.
105

|     |     |     |     |     | )   | ;; ; ;; | ;   |     | ;   | ;   |     | ;   |
| --- | --- | --- | --- | --- | --- | ------- | --- | --- | --- | --- | --- | --- |
The
| B.1.2 | module |     |     |     |     |     |     |     |     |     |     |     |
| ----- | ------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Figure B-1 shows thecode formodule "hand" fromtheblackjackprogram, which will beused
| to illustrate | structured | testing. |     |      |     |     |     |     |     |     |     |     |
| ------------- | ---------- | -------- | --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
|               | e          | AO       | int | hand |     |     |     |     |     |     |     |     |
retur(n
|     | 7   |               | {/* |              | win        | */           |           |        |           |        |     |      |
| --- | --- | ------------- | --- | ------------ | ---------- | ------------ | --------- | ------ | --------- | ------ | --- | ---- |
|     | 8   |               |     | int d        | = 0, pace, | dace;        |           |        |           |        |     |      |
|     | 9   |               |     | int fHit;    |            | /* 1         | for hit,  | zero   | for not   | hit    | */  |      |
|     | 10  | Al A2 A3 A4   | A5  | p = 0;       | d = 0;     | pace         | = 0; dace | =      | 0; win    | = 0;   |     |      |
|     | 11  |               | /*  | win will     | be         | if dealer    | wins,     |        | if player | wins,  | if  | push |
|     |     |               |     |              | 0          |              |           | 1      |           |        | 2 a |      |
|     | 12  | A6 A7 A8 A9   |     | hit(£ip,     | tpace)     | hit(&d,      | &dace)    |        |           |        |     |      |
|     | 1 3 | A l O All A12 | A13 | h i t ( Sep, | S ipace)   | ; hit(&d,    | Stdace)   | ;      |           |        |     |      |
|     |     |               |     | c o un t     |            | ;            |           | ;      |           |        |     |      |
|     | 1 4 | A1 4          |     |              | = 0;       |              |           |        |           |        |     |      |
|     | 1 5 | A 1 5 A16     |     | p r i n t f  | (" D E A L | E R S H O WS |           | %d\n", | cards     | i-1]); |     |      |
|     | 1 6 | A 1 7         |     | d s h o w    | c a r d    | s [ i- l ] ; |           |        |           | [      |     |      |
=
|     | 17  | A18 A19 |     | printf("PLAYER |        | = %d, | NO OF | ACES | - %d\n", | p, pace) |     |     |
| --- | --- | ------- | --- | -------------- | ------ | ----- | ----- | ---- | -------- | -------- | --- | --- |
|     | 18  | A20     |     | if (p          | == 21) |       |       |      |          |          |     |     |
{
|     | 19    | A 2 1 A22 |     | p r   | i nt f ("PLAYER |           | HAS BLACKJACKNn" |            | )       |          |       |     |
| --- | ----- | --------- | --- | ----- | --------------- | --------- | ---------------- | ---------- | ------- | -------- | ----- | --- |
|     | 2 0   | A 2 3     |     | w i   | n = 1           |           |                  |            |         |          |       |     |
|     | 21    |           |     | else  |                 |           |                  |            |         |          |       |     |
|     |       |           |     | )     | {               |           |                  |            |         |          |       |     |
|     | 22    | A24       |     | count | =               | 2         |                  |            |         |          |       |     |
|     | 23    |           | Lll |       |                 |           |                  |            |         |          |       |     |
|     | 2 4 . | A 2 5 A26 |     | c hec | k _ f o         | r hit (&f | Hit,             | p, count); |         |          |       |     |
|     | 2 5   | A 27      |     | if    | ( f H i t       | == 1)     |                  |            |         |          |       |     |
|     | 26    | A28 A29   |     |       | hit(&p,tpace)   |           | {                |            |         |          |       |     |
|     | 27    | A30       |     |       | count           | += 1;     |                  |            |         |          |       |     |
|     | 28    | A31 A32   |     |       | printf("PLAYER  |           | =                | %d, NO     | OF ACES | - %d\n". | pace) |     |
P-
|     | 29    | A33      |     |     | if  | (p > 21)  | {          |       |          |         |     |     |
| --- | ----- | -------- | --- | --- | --- | --------- | ---------- | ----- | -------- | ------- | --- | --- |
|     | 3 0   | A 34 A35 |     |     |     | p r i ntf | ( " PLAYER | BUSTS | - DEALER | WINS\n' |     |     |
|     |       |          |     |     |     | g ot o    |            |       |          |         | ) ; |     |
|     | ; 3 1 | A3 6     |     |     |     | L1        | 3 ;        |       |          |         |     |     |
32
|     | 33  | A37 A38   |     |          | goto )     | Lll;        |             |      |      |        |           |     |
| --- | --- | --------- | --- | -------- | ---------- | ----------- | ----------- | ---- | ---- | ------ | --------- | --- |
|     | 34  |           |     | }        |            |             |             |      |      |        |           |     |
|     | 35  | A39 A40   |     |          |            |             |             |      |      |        |           |     |
|     |     |           |     | Handle ) |            |             |             | case | when | dealer | blackjack |     |
|     | 36  |           | /*  |          | blackjac)c | situations, |             |      |      |        | has       |     |
|     | 3 7 | A 4 1     |     | if ( d   | = = 21 )   |             |             |      |      |        |           |     |
|     | 3 8 | A 4 2 A43 |     | p ri     | n tf       | "DE { ALER  | HAS BJ\n"); |      |      |        |           |     |
(
|     | 3 9 | A 4 4     |     | if           | ( w i n  | = = 1 )    | {             |                  |           |     |     |     |
| --- | --- | --------- | --- | ------------ | -------- | ---------- | ------------- | ---------------- | --------- | --- | --- | --- |
|     | 4 0 | A 4 5 A46 |     |              | p r i nt | f "        | PUSH\n"       |                  |           |     |     |     |
|     |     |           |     |              | w i n    | (          |               | )                | ;         |     |     |     |
|     | 4 1 | A 4 7     |     |              |          | = 2        |               |                  |           |     |     |     |
|     | 42  | A48       |     |              | goto     | L13;       |               |                  |           |     |     |     |
|     | 4 3 |           |     |              | els e    |            |               |                  |           |     |     |     |
|     |     |           |     | )            |          | {          |               |                  |           |     |     |     |
|     | 4 4 | A49 A50   |     |              | p rin    | tf("DEALER | AUTOMATICALLY |                  | WINSXn"); |     |     |     |
|     | 45  | A51       |     |              | goto     | L13;       |               |                  |           |     |     |     |
|     | 46  | A52       |     | )            |          |            |               |                  |           |     |     |     |
|     | 47  |           |     | else         |          |            |               |                  |           |     |     |     |
|     |     |           | /*  | case } where | { dealer | doesn't    |               | have blackjaclc: |           |     |     |     |
48
|     | 49    |             | *   | check for | player | blackjack  |           | or five         | card      | hand |     |     |
| --- | ----- | ----------- | --- | --------- | ------ | ---------- | --------- | --------------- | --------- | ---- | --- | --- |
|     | 50    |             | */  |           |        |            |           |                 |           |      |     |     |
|     |       |             |     |           | = =    | 2 1        |           |                 |           |      |     |     |
|     | ; 5 1 | A 53 A 5 4  |     | if        | ( p    | II         | c o u nt  | > = 5) TIC{ALLY |           |      |     |     |
|     | 5 2   | A 5 5 A 5 6 |     |           | p ri n | t f ("P LA | Y E R AUT | O MA            | WINS\n"); |      |     |     |
|     |       | A57         |     |           | win    |            |           |                 |           |      |     |     |
|     | 53 '  |             |     |           |        | = 1;       |           |                 |           |      |     |     |
|     | 54    | A58         |     |           | goto   | L13;       |           |                 |           |      |     |     |
55
)
|     | 56  | A59 A60 |     | }              |        |     |       |     |     |     |     |     |
| --- | --- | ------- | --- | -------------- | ------ | --- | ----- | --- | --- | --- | --- | --- |
|     | 57  | A61 A62 |     | printf("DEALER |        | HAS | %d\n" | d)  |     |     |     |     |
|     |     |         |     |                |        |     | ,     | ;   |     |     |     |     |
|     | 58  |         | L12 |                |        |     |       |     |     |     |     |     |
|     | 59  | A63     |     | if (d          | <= 16) |     |       |     |     |     |     |     |
|     | 60  | A64 A65 |     | hit(&d,Scdace) |        | {   |       |     |     |     |     |     |
;
|     | 61  | A66     |     | if  | (d >           | 21) { |       |     |        |           |     |     |
| --- | --- | ------- | --- | --- | -------------- | ----- | ----- | --- | ------ | --------- | --- | --- |
|     | 62  | A67 A68 |     |     | printf("DEALER |       | BUSTS | -   | PLAYER | WINSXn"); |     |     |
win
|     | 63  | A69 |     |     |      | = 1  |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | ---- | ---- | --- | --- | --- | --- | --- | --- |
|     | 64  | A70 |     |     | goto | L13; |     |     |     |     |     |     |
65
}
|     | 66  | A71 A72 |     | goto | L12; |     |     |     |     |     |     |     |
| --- | --- | ------- | --- | ---- | ---- | --- | --- | --- | --- | --- | --- | --- |
67
|     |     |             |     | }              |        |      | DEALER    |     |         |       |     |     |
| --- | --- | ----------- | --- | -------------- | ------ | ---- | --------- | --- | ------- | ----- | --- | --- |
|     | 68  | A73 A74 A75 |     | printf("       | PLAYER | = %d |           | =   | %d\n" , | p, d) |     |     |
|     | 69  | A76         |     | if (p          | > d)   |      |           |     |         |       |     |     |
|     | 70  | A77 A78     |     | printf("PLAYER |        | {    | WINSNn"); |     |         |       |     |     |
|     | 71  | A79         |     | win            | = 1    |      |           |     |         |       |     |     |
|     | 72  |             |     | else           |        |      |           |     |         |       |     |     |
}
|     | 73         | A80 A81 A82    |     | printf("DEALER  |      |     | WINSXn"); |     |     |     |     |     |
| --- | ---------- | -------------- | --- | --------------- | ---- | --- | --------- | --- | --- | --- | --- | --- |
|     | 74         |                | L13 |                 |      |     |           |     |     |     |     |     |
|     | 75         | A83            |     | return          | win; |     |           |     |     |     |     |     |
|     | 76         | A84            | }   |                 |      |     |           |     |     |     |     |     |
|     | FigureB-1. | Codeforexample |     | blackjackmodule |      |     | "hand."   |     |     |     |     |     |
106

| Figure    | B-2 shows  | the graph |      | module    | "hand,"    | which |            |            |           |              |
| --------- | ---------- | --------- | ---- | --------- | ---------- | ----- | ---------- | ---------- | --------- | ------------ |
|           |            |           | for  |           |            | has   | cyclomatic | complexity |           | 1 1 and      |
| essential | complexity | The       | high | essential | complexity | makes | the        |            |           |              |
|           |            | 9.        |      |           |            |       |            | control    | structure | difficult to |
follow. In such cases, the baseline method can be performed using the source as a
listing
guide, with paths represented by ordered lists ofdecision outcomes. Decisions are "flipped"
| exactly | as in the graphical |     | version | ofthe | method. |     |     |     |     |     |
| ------- | ------------------- | --- | ------- | ----- | ------- | --- | --- | --- | --- | --- |
X
|     |     |     |             |          | Bowai'apha   | TiMxi'fc>'Blackjack' |                  |        |     |     |
| --- | --- | --- | ----------- | -------- | ------------ | -------------------- | ---------------- | ------ | --- | --- |
|     |     |     | iPlot| Save | -Convert | |Backward    |                      |                  |        |     |     |
|     |     |     | i           | I        | I jForuiard| | | jEnlargej |        | Reduce | jClose| | [Help| |     |     |
|     |     |     | Page 1 of   | 3 2X     |              |                      |                  |        |     |     |
Blackjack
Ppogrsfli: bj.c
hand (A)
|     |     |     | Lansuage: | -inEtc |     |     |     |     |     |     |
| --- | --- | --- | --------- | ------ | --- | --- | --- | --- | --- | --- |
CyelomntHcGUraph
Cyclomat-ic
|     |     |     | tctential | 9   |     |     |     |     |     |     |
| --- | --- | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
Dec-ign10
FigureB-2.Graphformodule
''hand.
The original blackjack testing example [NBS99] demonstrated the manual application ofthe
we
baseline method in full detail, which will not be duplicated here. Instead, follow the mod-
| em  |     |     |     | which |     |     |     | on  |     |     |
| --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- |
tool-assisted testing process, in basis path coverage is built a foundation offunc-
We show unrealizable paths do not necessarily imply < v(G) or
| tional testing. |     |     | that |     | test |     |     |     | that | rc  |
| --------------- | --- | --- | ---- | --- | ---- | --- | --- | --- | ---- | --- |
that testing should cease, and we also demonstrate control dependency analysis as a case
test
| derivation | technique.    |     |        |     |     |     |     |     |     |     |
| ---------- | ------------- | --- | ------ | --- | --- | --- | --- | --- | --- | --- |
| B.1.3      | Tests through | the | module |     |     |     |     |     |     |     |
Replacing
the "hit" routine with a version thatallows userinput ofthe nextcardis sufficientto
allow individual paths be exercised. We now follow a typical structured process,
|     |     | to  |     |     |     |     |     |     | testing |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ------- | --- |
beginning with functional tests while using an automated tool to measure ac. Input data deri-
vation is simplified by first determining the meaning ofall program variables used in decision
"p"
expressions. The variable holds the total value ofthe player's hand, and "d" holds the
107

dealer's hand value. Those two variables are updated by the "hit" routine. The "fHit" and
When
"win" variables are commented with their usage. "fHit" is 1, the player or dealer has
|     |     |     |     | of0 | means | A   | of0 |     | means |     |     |
| --- | --- | --- | --- | --- | ----- | --- | --- | --- | ----- | --- | --- |
elected to hit, and a value stand. value for "win" the dealer wins, 1
| means |            |       | and | 2 means |       | was apush. | This |     | value returned | by  | mod- |
| ----- | ---------- | ----- | --- | ------- | ----- | ---------- | ---- | --- | -------------- | --- | ---- |
|       | the player | wins, |     |         | there |            |      | is  | the            | the |      |
Finally, the variable "count" stores the number ofcards the player's hand.
| ule. |     |     |     |     |     | total |     |     | in  |     |     |
| ---- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- |
The first functional test is a "push," which can be exercised by having the replacement "hit"
module first set p to 11 and pace to 1, then set d to 11 and dace to 1, then set p to 21 and leave
|     |     | d   |     | and | dace | We  |     |     | have | same | by  |
| --- | --- | --- | --- | --- | ---- | --- | --- | --- | ---- | ---- | --- |
pace at 1, then set to 21 leave at 1. could also exercised the path
having contents ofits argument unconditionally 21. However, best
|     | "hit" set | the |     |     | first |     |     |     | to  | it is | to  |
| --- | --------- | --- | --- | --- | ----- | --- | --- | --- | --- | ----- | --- |
make stub and driver modules conform to the specified behavior ofthe real modules that they
replace, and in fact behave as realistically as possible. Since the input data derivation is
we
straightforward, omit it for the rest ofthe paths. Execution ofthis test does in fact show a
|     |     |     |     | When |     |     |     |     | we  |     |     |
| --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- |
push, the correct behavior. discussing control flow paths, use the notation
| "18( | p==21 | ==> | TRUE" |     |             |          | on   |      | 18 node 20 | with decision |     |
| ---- | ----- | --- | ----- | --- | ----------- | -------- | ---- | ---- | ---------- | ------------- | --- |
|      | 20):  |     |       |     | to indicate | that the | test | line | at         |               |     |
predicate "p==21" takes on the value "TRUE." The path executed by the functional
|     |     |     |     |     |     |     |     |     | first |     | test |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | ---- |
is:
|     | 18  | 20)  | p==21  | ==> | TRUE |     |     |     |     |     |     |
| --- | --- | ---- | ------ | --- | ---- | --- | --- | --- | --- | --- | --- |
|     | (   | :    |        |     |      |     |     |     |     |     |     |
|     | 37  | 41): | d==21  | ==> | TRUE |     |     |     |     |     |     |
|     | (   |      |        | ==> |      |     |     |     |     |     |     |
|     | 39  | 44): | win==l |     | TRUE |     |     |     |     |     |     |
{
| The |     |     |     |     |     |     |     | which |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- |
second functional test is blackjack for the player, in the original deal leaves the
player with 21 andleaves the dealerwith an inferiorhand. Execution shows correctbehavior.
| The | associated | path |     |     |     |     |     |     |     |     |     |
| --- | ---------- | ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
is:
|     | 18  | 20)  | p==21 | ==> | TRUE  |     |     |     |     |     |     |
| --- | --- | ---- | ----- | --- | ----- | --- | --- | --- | --- | --- | --- |
|     | (   | :    |       |     |       |     |     |     |     |     |     |
|     | 37  | 41): | d==21 | ==> | FALSE |     |     |     |     |     |     |
(
|     | 51{ | 53): | p==21 | ==> | TRUE |     |       |     |     |     |     |
| --- | --- | ---- | ----- | --- | ---- | --- | ----- | --- | --- | --- | --- |
| The |     |      |       |     |      |     | which |     |     |     |     |
thirdfunctional test is blackjackforthe dealer, in the original deal leaves theplayer
|     |     |     |     | does |     | and |     | has | 21 Execution | shows |     |
| --- | --- | --- | --- | ---- | --- | --- | --- | --- | ------------ | ----- | --- |
with less then 21, the player not get hit, the dealer correct
.
| behavior. | The | associated |     | path |     |     |     |     |     |     |     |
| --------- | --- | ---------- | --- | ---- | --- | --- | --- | --- | --- | --- | --- |
is:
|     | 18  | 20) | p==21   | ==> | FALSE |     |     |     |     |     |     |
| --- | --- | --- | ------- | --- | ----- | --- | --- | --- | --- | --- | --- |
|     | (   | :   |         |     |       |     |     |     |     |     |     |
|     | 25( | 27) | fHit==l | ==> | FALSE |     |     |     |     |     |     |
:
|     | 37  | 41) | d==21  | ==> | TRUE  |     |     |     |     |     |     |
| --- | --- | --- | ------ | --- | ----- | --- | --- | --- | --- | --- | --- |
|     | (   | :   |        | ==> |       |     |     |     |     |     |     |
|     | 39  | 44) | win==l |     | FALSE |     |     |     |     |     |     |
|     | (   | :   |        |     |       |     |     |     |     |     |     |
108

> >>
The fourth functional a five-card win, which player accumulates
|     |     |     | test | is  | in the |     | five cards | with- |
| --- | --- | --- | ---- | --- | ------ | --- | ---------- | ----- |
out going over 21 and the dealer was not dealt blackjack. Execution shows correct behavior.
| The | associated | path | is:     |           |     |     |     |     |
| --- | ---------- | ---- | ------- | --------- | --- | --- | --- | --- |
|     | 18         | 20)  | p==21   | > FALSE   |     |     |     |     |
|     |            | {    |         | ==>       |     |     |     |     |
|     | 25{        | 27)  | fHit==1 | TRUE      |     |     |     |     |
|     |            |      | p>21    | ==> FALSE |     |     |     |     |
|     | 29{        | 33)  |         |           |     |     |     |     |
|     | 25(        | 27)  | fHit==1 | ==> TRUE  |     |     |     |     |
|     | 29         | 33)  | p>21    | == FALSE  |     |     |     |     |
(
|     | 25( | 27) | fHit==1 | ==> TRUE  |     |     |     |     |
| --- | --- | --- | ------- | --------- | --- | --- | --- | --- |
|     | 29  | 33) | p>21    | == FALSE  |     |     |     |     |
|     |     | (   | fHit==1 | ==> FALSE |     |     |     |     |
|     | 25( | 27) |         |           |     |     |     |     |
|     | 37  | 41) | d==21   | > FALSE   |     |     |     |     |
(
|     | 51( | 53) | p==21 | > FALSE     |     |     |     |     |
| --- | --- | --- | ----- | ----------- | --- | --- | --- | --- |
|     | 51( | 54) | count | =5 ==> TRUE |     |     |     |     |
The fifth functional test is a win for the player in which neither the player nor the dealer takes
|     | and |     |     |     | shows | The |     |     |
| --- | --- | --- | --- | --- | ----- | --- | --- | --- |
ahit, neither has blackjack. Execution correct behavior. associated path is:
|     |     |       | p==21   | => FALSE  |     |     |     |     |
| --- | --- | ----- | ------- | --------- | --- | --- | --- | --- |
|     | 18  | ( 20) |         |           |     |     |     |     |
|     | 25( | 27)   | fHit==1 | ==> FALSE |     |     |     |     |
|     | 37  | 41)   | d==21   | => FALSE  |     |     |     |     |
(
|     | 51( | 53) | p==21 | => FALSE |     |     |     |     |
| --- | --- | --- | ----- | -------- | --- | --- | --- | --- |
==>
|     | 51( | 54)   | count>  | 5 FALSE  |     |     |     |     |
| --- | --- | ----- | ------- | -------- | --- | --- | --- | --- |
|     |     |       | d<=16   | => FALSE |     |     |     |     |
|     | 59  | 63)   |         |          |     |     |     |     |
|     | 69( | ( 76) | p>d ==> | TRUE     |     |     |     |     |
The sixth functional awin forthe dealer in which neitherthe playernorthe dealertakes
|     |     |     | test is |     |     |     |     |     |
| --- | --- | --- | ------- | --- | --- | --- | --- | --- |
a hit, and neither has blackjack. Execution shows correct behavior. The associated path is:
|     | 18( | 20) | p==21   | ==> FALSE |     |     |     |     |
| --- | --- | --- | ------- | --------- | --- | --- | --- | --- |
|     | 25{ | 27) | fHit==1 | ==> FALSE |     |     |     |     |
|     |     |     | d==21   | ==> FALSE |     |     |     |     |
|     | 37  | 41) |         |           |     |     |     |     |
|     | 51{ | {   | p==21   | ==> FALSE |     |     |     |     |
53)
|     | 51{ | 54) | count>=5 | ==> FALSE |     |     |     |     |
| --- | --- | --- | -------- | --------- | --- | --- | --- | --- |
|     | 59{ | 63) | d<=16    | ==> FALSE |     |     |     |     |
|     | 69{ | 76) | p>d ==>  | FALSE     |     |     |     |     |
The seventh functional test is a win for the dealer in which the player is busted. Execution
| shows |         |           | The     |            |          |     |     |     |
| ----- | ------- | --------- | ------- | ---------- | -------- | --- | --- | --- |
|       | correct | behavior. |         | associated | path is: |     |     |     |
|       |         |           | p==21   | ==> FALSE  |          |     |     |     |
|       | 18      | ( 20):    |         |            |          |     |     |     |
|       | 25      | 27):      | fHit==l | ==> TRUE   |          |     |     |     |
(
|     | 29  | 33) | p>21 | ==> TRUE |     |     |     |     |
| --- | --- | --- | ---- | -------- | --- | --- | --- | --- |
|     |     | (   | :    |          |     |     |     |     |
The eighth functional test is a win forthe player in which the dealer is busted. Execution
| shows | correct | behavior. | The     | associated | path is: |     |     |     |
| ----- | ------- | --------- | ------- | ---------- | -------- | --- | --- | --- |
|       |         |           | p==21   | ==>        |          |     |     |     |
|       | 18      | 20):      |         | FALSE      |          |     |     |     |
|       |         | ( 27):    | fHit==l | ==> FALSE  |          |     |     |     |
25(
|     | 37  | 41): | d==21 | ==> FALSE |     |     |     |     |
| --- | --- | ---- | ----- | --------- | --- | --- | --- | --- |
(
|     | 51( | 53):  | p==21    | ==> FALSE |     |     |     |     |
| --- | --- | ----- | -------- | --------- | --- | --- | --- | --- |
|     | 51  | 54):  | count>=5 | ==> FALSE |     |     |     |     |
|     |     | {     |          | ==> TRUE  |     |     |     |     |
|     | 59  | 63)   | d<=16    |           |     |     |     |     |
|     |     | (     | : d>21   | ==> TRUE  |     |     |     |     |
|     | 61  | ( 66) | :        |           |     |     |     |     |
109

The ninth functional a win for the dealer which the player reach 21 and
|     |     |     | test | is  |     |     | in  |     | is hit | to  | the |
| --- | --- | --- | ---- | --- | --- | --- | --- | --- | ------ | --- | --- |
dealer has blackjack. Execution shows correct behavior. The associated path
is:
|     | 18  | 20) | p==21 | =>  | FALSE |     |     |     |     |     |     |
| --- | --- | --- | ----- | --- | ----- | --- | --- | --- | --- | --- | --- |
(
|     | 25( | 27) | fHit==1 |     | ==> TRUE  |     |     |     |     |     |     |
| --- | --- | --- | ------- | --- | --------- | --- | --- | --- | --- | --- | --- |
|     | 29  | 33) | p>21    | = > | FALSE     |     |     |     |     |     |     |
|     |     | (   | fHit==1 |     | ==> FALSE |     |     |     |     |     |     |
|     | 25( | 27) |         |     |           |     |     |     |     |     |     |
|     | 37  | 41) | d==21   | =>  | TRUE      |     |     |     |     |     |     |
(
|     | 39  | 44) | win==l | ==> | FALSE |     |     |     |     |     |     |
| --- | --- | --- | ------ | --- | ----- | --- | --- | --- | --- | --- | --- |
(
This concludes our initial set offunctional tests. No error has been detected yet, and each test
now
increased ac by 1, so ac is 9. The coverage analysis tool reports that one branch has not
|     |     |     |     |     | d>21 ==> | FALSE." |     |     |     |     |     |
| --- | --- | --- | --- | --- | -------- | ------- | --- | --- | --- | --- | --- |
yet been executed, "61( 66): This corresponds to the dealer taking a hit
| without | being |     | Since |     | branches |     |     |     |     | and |     |
| ------- | ----- | --- | ----- | --- | -------- | --- | --- | --- | --- | --- | --- |
busted. are usually easier to test than paths, testing a previ-
ously unexecuted branch must increase we construct a new for branch immedi-
|     |     |     |     |     |     | ac, |     | test |     | this |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | ---- | --- |
ately. The test makes the dealer win the hand by hitting once and then standing. Execution
| shows | correct | behavior. |          | The | associated | path | is: |     |     |     |     |
| ----- | ------- | --------- | -------- | --- | ---------- | ---- | --- | --- | --- | --- | --- |
|       | 18      | 20)       | p==21    |     | FALSE      |      |     |     |     |     |     |
|       |         | (         |          |     | ==>        |      |     |     |     |     |     |
|       | 25      | 27)       | fHit==1  |     | FALSE      |      |     |     |     |     |     |
|       |         | (         | d==21    | ==> | FALSE      |      |     |     |     |     |     |
|       | 37      | 41)       |          |     |            |      |     |     |     |     |     |
|       | 51(     | ( 53)     | p==21    |     | FALSE      |      |     |     |     |     |     |
|       | 51(     | 54)       | count>=5 |     | ==> FALSE  |      |     |     |     |     |     |
|       | 59      | 63)       | d<=16    | ==> | TRUE       |      |     |     |     |     |     |
(
|     | 61  | 66)   | d>21  | ==> | FALSE |     |     |     |     |     |     |
| --- | --- | ----- | ----- | --- | ----- | --- | --- | --- | --- | --- | --- |
|     |     | (     | d<=16 | ==> | FALSE |     |     |     |     |     |     |
|     | 59  | ( 63) |       |     |       |     |     |     |     |     |     |
|     | 69( | 76)   | p>d   | ==> | FALSE |     |     |     |     |     |     |
All branches have now been covered. No error has been detected yet, and ac now 10. The
is
coverage analysis tool reports that executing the following path would be sufficient to com-
| plete | basis | path coverage: |          |     |       |     |     |     |     |     |     |
| ----- | ----- | -------------- | -------- | --- | ----- | --- | --- | --- | --- | --- | --- |
|       | 18    | 20)            | p==21    |     | FALSE |     |     |     |     |     |     |
|       |       | (              | :        |     | FALSE |     |     |     |     |     |     |
|       | 25(   | 27)            | fHit==1  |     | =     |     |     |     |     |     |     |
|       | 37(   |                | :        |     | FALSE |     |     |     |     |     |     |
|       |       | 41)            | : d=:^21 |     |       |     |     |     |     |     |     |
|       | 51(   | 53)            | p==21    |     | TRUE  |     |     |     |     |     |     |
:
Unfortunately, this particular path unrealizable, since the value ofp not altered between
|     |     |     |     |     | is  |     |     |     | is  |           |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --------- | --- |
|     |     |     |     |     |     | ==> |     |     |     | ==> TRUE" |     |
the mutually exclusive "30( 13): p==21 FALSE" and "62( 44): p==21
we
decision outcomes. Ifthe basis completion path had been realizable, could havejust
For
derived the corresponding data, executed the test, and completed the testing process.
modules poorly "hand," however, unrealizable paths common, so
|     | as  |     | structured |     | as  |     |     |     | are | fairly | it  |
| --- | --- | --- | ---------- | --- | --- | --- | --- | --- | --- | ------ | --- |
important to be prepared for them. As discussed in section the existence ofunrealizable
| is  |     |     |     |     |     |     |     | 9,  |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
paths does not necessarily mean that rc < v(G). To help determine whether a realizable alter-
we
native path can complete basis path testing, use the dependency analysis technique. The
| dependency |     |     |     |     |     |     |     |     | number |     |     |
| ---------- | --- | --- | --- | --- | --- | --- | --- | --- | ------ | --- | --- |
analysis tool indicates that for every tested path, the total oftimes
branches "39( win== ==> TRUE" and "5 p==2 ==>TRUE" were executed
|     |     | 44): |     | 1   |     |     | 1( 53): | 1   |     |     | is  |
| --- | --- | ---- | --- | --- | --- | --- | ------- | --- | --- | --- | --- |
equal to the number oftimes branch "18( p==21 ==> TRUE" was executed. Note that
20):
for any single path, none ofthose three decision outcomes can be executed more than once
We may
and at most one ofthe first two can be executed. therefore rephrase the dependency
110

equation in terms ofthe module's functionality: The player has blackjack ifand only ifeither
the result is apush orthe player automatically wins with 21. Any test that does not satisfy this
dependency relationship will be independent ofthe current set oftests and increase ac, in this
case completing testing by making ac equal to v(G). On the other hand, if we can prove that
the dependency must hold for every feasible test, then we have shown that rc < v(G). Fortu-
nately, we can simplify the dependency even further, showing that rc = v(G) and giving a con-
cise characterization of all feasible basis completion paths. Note that ifthe player has
blackjack, the result must be either a push or an automatic win with 21 for the player. Also,
there is no way to reach a push result without the player having blackjack. Thus, a test breaks
the dependency relationship ifand only ifthe player gets an automatic win with 21 without
having blackjack. This is clearly possible for the module as written, for example by having
the — player reach exactly 21 after taking one hit. Execution ofthis test shows incorrect behav-
ior the module declares an automatic win for the player without giving the dealer a chance
to take hits and win by also reaching 21. The specification states that the player can only win
"automatically" with either Blackjack or a five-card hand. As expected, this test completes
the basis set. The associated path is:
18( 20) p==21 ==> FALSE
:
25( 27) fHit==l ==> TRUE
:
29 33) p>21 ==> FALSE
25( ( 27) : fHit:^=l ==> FALSE
:
37( 41) d==21 ==> FALSE
:
51( 53) p==21 ==> TRUE
:
Note that in addition to providing a test that detected the error, dependency analysis clarified
the nature ofthe error and gave a straightforward repair technique: replace the automatic win
test "51( 53): p==21" with "51( 53): win==l," since at that point win==l is precisely equiv-
alent to the player having blackjack. Ifthe error is repaired in this manner, there will be no
way to break the dependency with a feasible path, and rc will therefore be reduced to 10.
Note also that structured testing is not guaranteed to detect the error, as can be seen from
dependency analysis. Ifthe player reaches exactly 21 after taking at least three hits, the error
will not result in incorrect module output even though a dependency-breaking "incorrect"
control flow path is executed. The reason is that there is no difference in specified behavior
between an automatic win due to blackjack and an automatic win due to a five-card hand.
Hence, the five-card hand masks the error. This is the only situation in which structured test-
ing can fail to detect the error in the blackjack program, and as shown in section B-2 it is an
extremely rare situation during actual play ofthe game.
Ill

and
| B.2 | Experimental |     | comparison |     | ofstructured |     | testing | branch |     |     |
| --- | ------------ | --- | ---------- | --- | ------------ | --- | ------- | ------ | --- | --- |
coverage
| The | module |     |     |     |     |     |     |     | [WATSON4] |     |
| --- | ------ | --- | --- | --- | --- | --- | --- | --- | --------- | --- |
"hand" from section B-1 is one of several modules used in to com-
|     |     |     |     |     |     |     |     | branch |     | The |
| --- | --- | --- | --- | --- | --- | --- | --- | ------ | --- | --- |
pare the error detection effectiveness of structured testing with coverage. rest of
appendix discusses that work. Although neither testing technique guaranteed
| this |     |     |     |     |     |     |     |     | is  | to detect |
| ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --------- |
the error, structured testing performed dramatically better than branch coverage in the experi-
ment, which used random test data generation to simulate actual play.
| B.2.1 | Experimental | design |     |     |     |     |        |     |     |     |
| ----- | ------------ | ------ | --- | --- | --- | --- | ------ | --- | --- | --- |
| The   |              |        |     | was |     |     | module |     |     |     |
overall experimental design to package the test with a driver program that
|     | random | number | seed |     |     |     | random |     | from |     |
| --- | ------ | ------ | ---- | --- | --- | --- | ------ | --- | ---- | --- |
accepts a as input, generates test data a realistic distribu-
executes the module with that data, analyzes the module's behavior, and returns an
| tion, |     | test |     |     |     |     |     |     |     |     |
| ----- | --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
A
exit code indicating whether an error was detected. higher-level driver invokes the module
testdriver with a sequence ofseed values, uses an automatedtool to measure the testcoverage
level according to each criterion being compared, and tracks both the error detection and the
coverage
results.
For both structured testing and branch coverage, 100 experimental were performed, in
trials
each ofwhich random test cases were generated iteratively until the current testing criterion
was satisfied. Four kinds ofdata were collected during each trial for the two testing criteria:
• Tests, the total number oftests executed until the criterion was satisfied
number
• Testsinc, the oftests that increased coverage with respect to the criterion
| Detect, | whether | an  | error was | detected | during | the |       |     |     |     |
| ------- | ------- | --- | --------- | -------- | ------ | --- | ----- | --- | --- | --- |
| •       |         |     |           |          |        |     | trial |     |     |     |
• Detectinc, whether an error was detected by a test that increased coverage
There is an important distinction between considering all tests andjustconsidering the ones
that increased coverage. Considering tests essentially doingrandom testing while using
|     |     |     |     |     | all | is  |     |      |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- |
|     |     |     |     |     |     | may |     | when |     |     |
thecoverage criterion as astoppingrule. This be appropriate detecting incorrect
programbehaviorischeap, so thatprogrambehaviorcanbeexamined foreachtest. However,
|     | criteriacomparison |     |             |     | from such |     | experimenttends | tobe | by                |     |
| --- | ------------------ | --- | ----------- | --- | --------- | --- | --------------- | ---- | ----------------- | --- |
|     | the                |     | information |     |           | an  |                 |      | diluted theeffec- |     |
A
tivenessoftheunderlyingrandomtestdatadistribution. criterionthatrequiresmorerandom
todetectmore regardless ofthe value ofthe specific testcases thatcon-
|     | tests is likely |     |     | errors, |     |     |     |     |     |     |
| --- | --------------- | --- | --- | ------- | --- | --- | --- | --- | --- | --- |
we
tribute to satisfying thecriterion. Therefore, also considerjusttheteststhatincreasecover-
age. In thatcase, we factoroutmost ofthe influence ofthe underlying randomtestdata
|     |     |     |     |     | random | minimal |     |     |     |     |
| --- | --- | --- | --- | --- | ------ | ------- | --- | --- | --- | --- |
distribution by ineffectconsidering testdatasets that satisfy each criterion.
In addition to giving amore objective comparison, this more accurately models testeffective-
ness when detecting incorrectprogram behavioris expensive, sothatprogram behaviorcan
only be examined fortests thatcontribute to satisfaction ofthe testcoveragecriterion.
[WATS0N4]
112

1
Comparative
| B.2.2  |           |     | frequency         | oferror | detection |               |        |     |                 |     |            |
| ------ | --------- | --- | ----------------- | ------- | --------- | ------------- | ------ | --- | --------------- | --- | ---------- |
| Figure | B-3 shows |     |                   |         |           | "hand" module |        |     |                 |     |            |
|        |           |     | the datacollected |         | forthe    |               | during |     | the experiment. |     | Data about |
numberoftests averaged over the 100trials. Data about error detection added 100
|     |     | is  |     |     |     |     |     |     |     | is  | for the |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------- |
trials, giving aconvenient interpretation as apercentage oftrials in which errors were detected
by the criteria.
|       |                |     |                        |     | StructuredTesting |       | BranchCoverage |     |     |     |     |
| ----- | -------------- | --- | ---------------------- | --- | ----------------- | ----- | -------------- | --- | --- | --- | --- |
|       |                |     | Tests                  |     | 45                |       | 36             |     |     |     |     |
|       |                |     | Testsinc               |     | 1                 |       | 8              |     |     |     |     |
|       |                |     | Detect                 |     | 97                |       | 85             |     |     |     |     |
|       |                |     | Detectinc              |     | 96                |       | 53             |     |     |     |     |
|       |                |     | FigureB-3.Experimental |     |                   | data. |                |     |     |     |     |
| B.2.3 | Interpretation |     | ofexperimental         |     | data              |       |                |     |     |     |     |
Structured testing decisively outperformed branch coverage at detecting the error while
|     |     | 25% |     |     | 38% |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
requiring only more total tests and more tests that increase coverage. The most
notable feature ofthe data is the robustness ofstructured testing with respect to test set mini-
%
| mization. | Only |     | ofthe | detection |               |     | ofstructured |     |         | was | when |
| --------- | ---- | --- | ----- | --------- | ------------- | --- | ------------ | --- | ------- | --- | ---- |
|           |      | 1   | error |           | effectiveness |     |              |     | testing |     | lost |
considering only tests that increased coverage, whereas the number oftests required was
reduced by 75%. For branch coverage, 38% oferror detection effectiveness was lost, and the
number oftests required was reduced by 78%. This indicates that the effectiveness of struc-
number
tured testing is due to the criterion itselfrather thanjust the oftests required to satisfy
| For | complete |     | oftest | programs | used | [WATS0N4], |     |            |     |         | preserved |
| --- | -------- | --- | ------ | -------- | ---- | ---------- | --- | ---------- | --- | ------- | --------- |
| it. | the      |     | set    |          |      | in         |     | structured |     | testing |           |
94% ofits error detection effectiveness when restricted the 24% oftest cases that increased
to
coverage.
113

| ANNOUNCEMENT |     | OF NEW | PUBLICATIONS | ON  |     |
| ------------ | --- | ------ | ------------ | --- | --- |
COMPUTER
|                             |        | SYSTEMS | TECHNOLOGY |     |     |
| --------------------------- | ------ | ------- | ---------- | --- | --- |
| Superintendent of Documents |        |         |            |     |     |
| Government Printing         | Office |         |            |     |     |
| Washington, DC 20402        |        |         |            |     |     |
Dear
Sir:
Please add my name announcement of new publications be issued
|     | to the |     | list | to  | in  |
| --- | ------ | --- | ---- | --- | --- |
the series: National Institute of Standards and Technology Special Publication 500-.
Name
Company
Address
| City                     |     | State |     | Zip Code |     |
| ------------------------ | --- | ----- | --- | -------- | --- |
| (Notification key N-503) |     |       |     |          |     |

|     |     |     |     |     | Technical |     |     | Publications |     |     |     |     |
| --- | --- | --- | --- | --- | --------- | --- | --- | ------------ | --- | --- | --- | --- |
Periodical
—
Journal ofResearch ofthe National Institute of Standards and Technology Reports NIST research
| and | development |     |     |     |     |     | and |     |     |     | which |     |
| --- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- |
in those disciplines of the physical engineering sciences in the Institute is
active. These include physics, chemistry, engineering, mathematics, and computer sciences. Papers cover a
broad range of subjects, with major emphasis on measurement methodology and the basic technology
underlying standardization. Also included from time to time are survey articles on topics closely related to
| the |             | technical |     | and        |     | programs. | Issued | times | a     |     |     |     |
| --- | ----------- | --------- | --- | ---------- | --- | --------- | ------ | ----- | ----- | --- | --- | --- |
|     | Institute's |           |     | scientific |     |           |        | six   | year. |     |     |     |
Nonperiodicals
—
Monographs
Major contributions to the technical literature on various subjects related to the
| Institute's |     | scientific | and | technical | activities. |     |     |     |     |     |     |     |
| ----------- | --- | ---------- | --- | --------- | ----------- | --- | --- | --- | --- | --- | --- | --- |
—
Handbooks Recommended codes of engineering and (including codes)
|     |     |     |     |     |     |     |     | industrial | practice |     | safety | devel- |
| --- | --- | --- | --- | --- | --- | --- | --- | ---------- | -------- | --- | ------ | ------ |
oped
in cooperation with interested industries, professional organizations, and regulatory bodies.
—
Special Publications Include proceedings of conferences sponsored by NIST, NIST annual reports, and
other special publications appropriate grouping such wall pocket cards, and bibliographies.
|     |     |     |     |     |     | to this |     | as  | charts, |     |     |     |
| --- | --- | --- | --- | --- | --- | ------- | --- | --- | ------- | --- | --- | --- |
—
National Standard Reference Data Series Provides quantitative data on the physical and chemical
|     |     |     |     | compiled | from |     |     | and |     |     | Developed | under |
| --- | --- | --- | --- | -------- | ---- | --- | --- | --- | --- | --- | --------- | ----- |
properties of materials, the world's literature critically evaluated. a
NIST
worldwide program coordinated by under the authority of the National Standard Data Act (Public
Law
90-396). NOTE: The Journal of Physical and Chemical Reference Data (JPCRD) is published
bimonthly for NIST by the American Chemical Society (ACS) and the American Institute of Physics (AIP).
Subscriptions, reprints, and supplements are available from ACS, 1155 Sixteenth St., NW, Washington, DC
20056.
—
Building Science Series Disseminates technical information developed at the Institute on building
materials, components, systems, and whole structures. The series presents research results, test methods, and
performance criteria related to the structural and environmental functions and the durability and safety
|                 |     | of  | building | elements | and | systems. |     |     |     |     |     |     |
| --------------- | --- | --- | -------- | -------- | --- | -------- | --- | --- | --- | --- | --- | --- |
| characteristics |     |     | —        |          |     |          |     |     |     |     |     |     |
Technical Notes Studies or reports which are complete in themselves but restrictive in their treatment of
a subject. Analogous to monographs but not so comprehensive in scope or definitive in treatment of the
subject Often serve as a vehicle for reports of work performed NIST under the sponsorship of
|     | area. |     |     |     |     | final |     |     |     | at  |     |     |
| --- | ----- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- |
government
| other |     |     | agencies. |     |     |     |     |     |     |     |     |     |
| ----- | --- | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
—
Voluntary Product Standards Developed under procedures published by the Department of Commerce
Part Title of the Code of Federal Regulations. The standards establish nationally recognized
| in           | 10, |     | 15,       |     |         |           |           |      |       |        |               |     |
| ------------ | --- | --- | --------- | --- | ------- | --------- | --------- | ---- | ----- | ------ | ------------- | --- |
|              |     |     |           | and | provide | concerned |           | with | a     | common | understanding | of  |
| requirements |     | for | products, |     |         | all       | interests |      | basis | for    |               |     |
NIST
the characteristics of the products. administers this program in support of the efforts of private-sector
| standardizing |     | organizations. |     |     |     |     |     |     |     |     |     |     |
| ------------- | --- | -------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Order the following NISTpublications—FIPS andNISTlRs—from the National Technical Information
| Service, |     | Springfield, | VA  | 22161. |     |     |     |     |     |     |     |     |
| -------- | --- | ------------ | --- | ------ | --- | --- | --- | --- | --- | --- | --- | --- |
—
|     |     |     |     |     | Standards |     |     | (FIPS | PUB) |     |     |     |
| --- | --- | --- | --- | --- | --------- | --- | --- | ----- | ---- | --- | --- | --- |
Federal Information Processing Publications Publications in this series
The
collectively constitute the Federal Information Processing Standards Register. Register serves as the
official source of information in the Federal Government regarding standards issued by NIST pursuant to
the Federal Property and Administrative Services Act of 1949 as amended. Public Law 89-306 (79 Stat.
and implemented by Executive Order 11717 (38 FR 12315, dated May 1973) and Part 6 of
| 1127), |     | as  |     |     |     |     |     |     |     |     | 11, |     |
| ------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
CFR
| Title | 15  | (Code | ofFederal |     | Regulations). |     |     |     |     |     |     |     |
| ----- | --- | ----- | --------- | --- | ------------- | --- | --- | --- | --- | --- | --- | --- |
—
NIST Interagency Reports (NISTIR) A special series of interim or final reports on work performed by
NIST government and nongovernment). In general, distribution handled
|     | for | outside | sponsors | (bodi |     |     |     |     |     | initial |     | is  |
| --- | --- | ------- | -------- | ----- | --- | --- | --- | --- | --- | ------- | --- | --- |
VA 22161,
by the sponsor; public distribution is by the National Technical Information Service, Springfield,
| in  | paper | copy or | microfiche |     | form. |     |     |     |     |     |     |     |
| --- | ----- | ------- | ---------- | --- | ----- | --- | --- | --- | --- | --- | --- | --- |

^ 2
=O -1 r J (oV o p 3 — • IW—
g - . 3 => - sr* r © e
1 »< 1 3 . c3 oo Ss2a- "t
ft
c o o
2.
too GO O
8 0 s 0 o
1.1
8 - 3
re
<ni
n
