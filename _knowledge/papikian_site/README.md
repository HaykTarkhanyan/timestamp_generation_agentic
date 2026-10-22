# Mihran Papikian's website: snapshot

Saved 2026-10-22 from https://sites.google.com/view/mpapikian (the user: "grab all the files and
useful info from mihrans site and store in the repo"). Professor of Mathematics, Pennsylvania State
University; lecturer of the umath channel's «Հանրահաշիվ և թվերի տեսություն» (Algebra and Number
Theory). Contact on his home page: papikian@psu.edu, 318C McAllister Building, Penn State.

## What is here

| Path | What | Size |
|---|---|---|
| `algebra_number_theory_2024/` | ASOF course, fall 2024: notes of 21 lectures, homework 1-5, midterm solutions, project, lecture 14 problems | 220 MB |
| `galois_theory_2025/` | ARCS-ai course, fall 2025: notes of 23 lectures (20 files), homework 1-8, final exam | 160 MB |
| `research/` | 46 of his papers and notes linked as Drive PDFs on the Research page | 22 MB |
| `pages/` | the visible text of all six pages (home, research, CV, meetings, both teaching pages) | |
| `manifest.json` | every link on the site with its label, kind (drive_file / recording / link), local file, size, SHA-256 and Drive file name | |

Recordings (PSU Kaltura, two Google Drive videos) are linked, not downloaded. All 104 PDFs
downloaded in 301 s, each checked to start with `%PDF`.

**The PDFs are not in git** (~400 MB; the user: "dont commit the pdfs"; `.gitignore` rule
`_knowledge/papikian_site/**/*.pdf`). A fresh clone has only this README, `manifest.json` and
`pages/`; get the PDFs back (and refresh the snapshot) with
`python scripts/non_essential/fetch_papikian_site.py --download` (~5 min).

## Algebra and Number Theory (ASOF Honors Course, fall 2024)

Page: https://sites.google.com/view/mpapikian/teaching/algebra-and-number-theory (text: `pages/teaching__algebra-and-number-theory.txt`).

- Open to all students; basic abstract algebra with a view toward number theory; preparation for the
  CIMPA summer school he co-organized in 2025 (https://sites.google.com/view/ecasummerschool2025/home).
- Auditorium of the Institute of Mathematics of the Academy of Sciences (24/5 Marshal Baghramyan
  Avenue, Yerevan); 13 Sep - 13 Dec 2024; Tuesday and Friday 17:00-19:00: a 90-minute lecture over
  Zoom, then a 30-minute recitation in person by the TA.
- Lectures in Armenian, slides in English. Grades: weekly homework, one midterm, a final exam.

| Lecture | Files | Recording | Our video |
|---|---|---|---|
| 1 | [notes](algebra_number_theory_2024/lecture_01_notes.pdf) 3.3 MB | [recording](https://psu.mediaspace.kaltura.com/media/1_ap23sbel) | [Դաս 1](https://youtu.be/Y1pxBIXxn8c) |
| 2 | [notes](algebra_number_theory_2024/lecture_02_notes.pdf) 7.1 MB | [recording](https://psu.mediaspace.kaltura.com/media/Mihran+Papikian%27s+Personal+Meeting+Room/1_50rev83d) | [Դաս 2](https://youtu.be/O-XnSMczScA) |
| 3 | [notes](algebra_number_theory_2024/lecture_03_notes.pdf) 9.2 MB | [recording](https://psu.mediaspace.kaltura.com/media/Mihran+Papikian%27s+Personal+Meeting+Room/1_tae8j5pz) | [Դաս 3](https://youtu.be/0aP1DWmdv5o) |
| 4 | [notes](algebra_number_theory_2024/lecture_04_notes.pdf) 6.1 MB | [recording](https://psu.mediaspace.kaltura.com/media/Mihran+Papikian%27s+Personal+Meeting+Room/1_ljoni2xa) | [Դաս 4](https://youtu.be/15NgvpyWvmw) |
| 5 | [notes](algebra_number_theory_2024/lecture_05_notes.pdf) 6.8 MB | [recording](https://psu.mediaspace.kaltura.com/media/Mihran+Papikian%27s+Personal+Meeting+Room/1_tt99xumt) | [Դաս 5](https://youtu.be/oUPTRRN9P1k) |
| 6 | [notes](algebra_number_theory_2024/lecture_06_notes.pdf) 8.1 MB | [recording](https://psu.mediaspace.kaltura.com/media/Mihran+Papikian%27s+Personal+Meeting+Room/1_z0bss25p) | [Դաս 6](https://youtu.be/68EpTg9sgHs) |
| 7 | [notes](algebra_number_theory_2024/lecture_07_notes.pdf) 8.5 MB | [recording](https://psu.mediaspace.kaltura.com/media/Mihran+Papikian%27s+Personal+Meeting+Room/1_5k7k7ods) | [Դաս 7](https://youtu.be/QrO0RZEl0J8) |
| 8 | [notes](algebra_number_theory_2024/lecture_08_notes.pdf) 9.2 MB | [recording](https://psu.mediaspace.kaltura.com/media/Mihran+Papikian%27s+Personal+Meeting+Room/1_qjodpmp2) | [Դաս 8](https://youtu.be/lviyUT33OXc) |
| 9 | [notes](algebra_number_theory_2024/lecture_09_notes.pdf) 8.9 MB | [recording](https://psu.mediaspace.kaltura.com/media/Mihran+Papikian%27s+Personal+Meeting+Room/1_i33zqsx5) | [Դաս 9](https://youtu.be/f8zxS5MpP_E) |
| 10 | [notes](algebra_number_theory_2024/lecture_10_notes.pdf) 6.5 MB | [recording](https://psu.mediaspace.kaltura.com/media/Mihran+Papikian%27s+Personal+Meeting+Room/1_yuwoo90w) | [Դաս 10](https://youtu.be/4TAiDzy6R6w) |
| 12 | [notes](algebra_number_theory_2024/lecture_12_notes.pdf) 5.9 MB | [recording](https://psu.mediaspace.kaltura.com/media/Mihran+Papikian%27s+Personal+Meeting+Room/1_lw8veyep) | [Դաս 11-12](https://youtu.be/khvL7pQif3c) |
| 13 | [notes](algebra_number_theory_2024/lecture_13_notes.pdf) 13.3 MB | [recording](https://psu.mediaspace.kaltura.com/media/Mihran+Papikian%27s+Personal+Meeting+Room/1_l0j4si75) | [Դաս 13](https://youtu.be/Xws84WaDw04) |
| 14 | [notes](algebra_number_theory_2024/lecture_14_notes.pdf) 14.1 MB + [problems](algebra_number_theory_2024/lecture_14_problems.pdf) 0.1 MB | [recording](https://psu.mediaspace.kaltura.com/media/Mihran+Papikian%27s+Personal+Meeting+Room/1_250m94q5) | [Դաս 14](https://youtu.be/cHCKLOSxctg) |
| 15 | [notes](algebra_number_theory_2024/lecture_15_notes.pdf) 11.3 MB | [part 1](https://psu.mediaspace.kaltura.com/media/Mihran+Papikian%27s+Personal+Meeting+Room/1_i268j4ha), [part 2](https://psu.mediaspace.kaltura.com/media/Mihran+Papikian%27s+Personal+Meeting+Room/1_cp0kobo5) | [Դաս 15](https://youtu.be/hWpA9f5fmUg) |
| 16 | [notes](algebra_number_theory_2024/lecture_16_notes.pdf) 13.1 MB | [recording](https://psu.mediaspace.kaltura.com/media/Mihran+Papikians+Personal+Meeting+Room/1_ih9bifgs) | [Դաս 16](https://youtu.be/Xe6XRo8O8yk) |
| 17 | [notes](algebra_number_theory_2024/lecture_17_notes.pdf) 11.7 MB | [recording](https://psu.mediaspace.kaltura.com/media/Mihran+Papikians+Personal+Meeting+Room/1_fdulicbq) | [Դաս 17](https://youtu.be/6VxoPJLkCJA) |
| 19 | [notes](algebra_number_theory_2024/lecture_19_notes.pdf) 21.6 MB | [recording](https://psu.mediaspace.kaltura.com/media/Mihran+Papikians+Personal+Meeting+Room/1_grawxqvz) | [Դաս 18-19 (unlisted)](https://youtu.be/VyWS3Ppv2ao) |
| 20 | [notes](algebra_number_theory_2024/lecture_20_notes.pdf) 18.3 MB | [recording](https://psu.mediaspace.kaltura.com/media/Mihran+Papikians+Personal+Meeting+Room/1_ex8h566r) | [Դաս 20](https://youtu.be/VCK3I6CkJI8) |
| 21 | [notes](algebra_number_theory_2024/lecture_21_notes.pdf) 15.5 MB | [recording](https://psu.mediaspace.kaltura.com/media/Mihran+Papikians+Personal+Meeting+Room/1_dkan8rtp) | [Դաս 21](https://youtu.be/nzUWG6NFDCU) |
| 22 | [notes](algebra_number_theory_2024/lecture_22_notes.pdf) 9.9 MB | [recording](https://psu.mediaspace.kaltura.com/media/Mihran+Papikians+Personal+Meeting+Room/1_qkgnio64) | [Դաս 22](https://youtu.be/txvgnlhu78E) |
| 23 | [notes](algebra_number_theory_2024/lecture_23_notes.pdf) 10.8 MB | [recording](https://psu.mediaspace.kaltura.com/media/Mihran+Papikians+Personal+Meeting+Room/1_vd2t66t8) | [Դաս 23](https://youtu.be/5tm6tnp8_4A) |

Other files:

- [Homework 1 (due September 27)](algebra_number_theory_2024/homework_1.pdf) (0.1 MB) - source: https://drive.google.com/file/d/1Opo3KlF63nzEjy2VS3UmdS5A2hbGmcl0/view?usp=sharing
- [Homework 2 (due October 4)](algebra_number_theory_2024/homework_2.pdf) (0.1 MB) - source: https://drive.google.com/file/d/1D1ucEJU4kLAb542IHctwzwwIfMtdx0Nc/view?usp=sharing
- [Homework 3 (due October 11)](algebra_number_theory_2024/homework_3.pdf) (0.1 MB) - source: https://drive.google.com/file/d/1gKG6tAF23v4z3_a4Z4tBPLKdOXZVnyhD/view?usp=sharing
- [Midterm Solutions](algebra_number_theory_2024/midterm_solutions.pdf) (0.1 MB) - source: https://drive.google.com/file/d/1Zu6hly95sOmJ6A3M1VFgz5egwRCNwlVW/view?usp=sharing
- [Homework 4 (due October 12)](algebra_number_theory_2024/homework_4.pdf) (0.1 MB) - source: https://drive.google.com/file/d/1GY_gmd4l6LTli-ltxf_H0MG9ikx3sNC4/view?usp=sharing
- [Project](algebra_number_theory_2024/project.pdf) (0.2 MB) - source: https://drive.google.com/file/d/1WYj9pcjeAPmoYUHCYxrrUYTC5lwyE4RF/view?usp=sharing
- [Homework 5 (due December 3)](algebra_number_theory_2024/homework_5.pdf) (0.0 MB) - source: https://drive.google.com/file/d/1uKmNo0ZS8Wvz-s3tPHG16SQ9LuWmV6bA/view?usp=sharing

Notes on the page:
- No lecture 11 and no lecture 18 at all (no notes, no recording). Lecture 11's week (Oct 21-25)
  lists the midterm solutions; 18's slot would be Fri 22 Nov 2024. See DECISIONS #24.
- "Homework 4 (due October 12)" is listed in week 8 (Nov 4-8): the date looks like a typo.
- The lecture 3 link says "Recoding". Lecture 15 has two recordings (part 1, part 2).
- `lecture_19_notes.pdf` starts with a loose page that is not lecture 19's topic: group actions
  (N ⊲ G, G/N acting on Ω/N) and Γ(N) ⊲ SL₂(ℤ) acting on the upper half-plane, Y(N) = ℍ/Γ(N) → Y(1).
  The lecture 19 recording never mentions it; probably an answer to a question off the recording.

## Galois Theory (ARCS-ai Honors Course, fall 2025)

Page: https://sites.google.com/view/mpapikian/teaching (text: `pages/teaching.txt`). Not on the
umath channel (2026-10-22); a candidate for later, see `_knowledge/umath_todo.md`.

- Undergraduate course on Galois theory: solving equations by radicals, field extensions and minimal
  polynomials, automorphism groups, splitting fields and normal extensions, the fundamental theorem,
  applications (insolvability by radicals, trisecting an angle, doubling the cube, regular polygons).
- In the framework of ARCS-ai (Advanced Research in Computational Sciences and Artificial
  Intelligence - ԲԱԳԻՆ). Seminar room of the YSU Krisp AI lab; 12 weeks from 16 Sep 2025,
  Wednesday and Saturday 18:00-21:00: a 90-minute lecture over Zoom, a 60-minute recitation in
  person by the TA.
- Lectures in Armenian; notes and homework in English. Prerequisites: basic linear algebra,
  readiness for proofs. Assessment: weekly problem sets, a written midterm, an oral final.

| Lecture | Date (2025) | Files | Recording |
|---|---|---|---|
| 1 | September 17 | [notes](galois_theory_2025/lecture_01_notes.pdf) 5.0 MB | none |
| 2 | September 20 | [notes](galois_theory_2025/lecture_02_notes.pdf) 10.9 MB | [recording](https://psu.mediaspace.kaltura.com/media/Mihran%20Papikians%20Personal%20Meeting%20Room/1_umlogz22) |
| 3 | September 23 | [notes](galois_theory_2025/lecture_03_notes.pdf) 7.4 MB | [recording](https://psu.mediaspace.kaltura.com/media/Mihran%20Papikians%20Personal%20Meeting%20Room/1_0r7e48ry) |
| 4 | September 27 | [notes](galois_theory_2025/lecture_04_notes.pdf) 7.9 MB | [recording](https://psu.mediaspace.kaltura.com/media/Mihran%20Papikians%20Personal%20Meeting%20Room/1_vw2hnm2n) |
| 5 | October 1 | [notes](galois_theory_2025/lecture_05_notes.pdf) 14.8 MB | [recording](https://psu.mediaspace.kaltura.com/media/Mihran%20Papikians%20Personal%20Meeting%20Room/1_rn5x0zwn) |
| 6 | October 4 | [notes](galois_theory_2025/lecture_06_notes.pdf) 2.6 MB | [recording](https://psu.mediaspace.kaltura.com/media/Mihran%20Papikians%20Personal%20Meeting%20Room/1_zvlf45q7) |
| 7 | October 8 | [notes](galois_theory_2025/lecture_07_notes.pdf) 13.7 MB | [recording](https://psu.mediaspace.kaltura.com/media/Mihran%20Papikians%20Personal%20Meeting%20Room/1_q2430cz4) |
| 8 | October 11 | [notes](galois_theory_2025/lecture_08_notes.pdf) 6.3 MB | [recording](https://psu.mediaspace.kaltura.com/media/Mihran%20Papikians%20Personal%20Meeting%20Room/1_u1rutt96) |
| 9 | October 15 | [notes](galois_theory_2025/lecture_08_notes.pdf) (same file as Lecture 8 (October 11)) 6.3 MB | [recording](https://psu.mediaspace.kaltura.com/media/Mihran%20Papikians%20Personal%20Meeting%20Room/1_5yjzdogv) |
| 10 | October 18 | [notes](galois_theory_2025/lecture_10_notes.pdf) 18.2 MB | [recording](https://psu.mediaspace.kaltura.com/media/Mihran%20Papikians%20Personal%20Meeting%20Room/1_jpr02ehr) |
| 11 | October 22 | [notes](galois_theory_2025/lecture_10_notes.pdf) (same file as Lecture 10 (October 18)) 18.2 MB | [recording](https://psu.mediaspace.kaltura.com/media/Mihran%20Papikians%20Personal%20Meeting%20Room/1_jx85hpm6) |
| 12 | November 1 | [notes](galois_theory_2025/lecture_12_notes.pdf) 10.2 MB | [recording](https://psu.mediaspace.kaltura.com/media/Mihran%20Papikians%20Personal%20Meeting%20Room/1_xxl9cahz) |
| 13 | November 5 | [notes](galois_theory_2025/lecture_13_notes.pdf) 5.7 MB | [recording](https://psu.mediaspace.kaltura.com/media/Mihran%20Papikians%20Personal%20Meeting%20Room/1_r6j7xk45) |
| 14 | November 8 | [notes](galois_theory_2025/lecture_14_notes.pdf) 9.5 MB | [recording](https://psu.mediaspace.kaltura.com/media/Mihran%20Papikians%20Personal%20Meeting%20Room/1_oy6mi08c) |
| 15 | November 12 | [notes](galois_theory_2025/lecture_15_notes.pdf) 5.9 MB | [recording](https://drive.google.com/file/d/1x5m3tGyOSd5j-QsR-AvnzgYx_Jquwh5u/view) |
| 16 | November 15 | [notes](galois_theory_2025/lecture_15_notes.pdf) (same file as Lecture 15 (November 12)) 5.9 MB | [recording](https://drive.google.com/file/d/1-SyCTFA_9sDWejr5ARebaShEtYJbS-H0/view) |
| 17 | November 19 | [notes](galois_theory_2025/lecture_17_notes.pdf) 3.6 MB | [recording](https://psu.mediaspace.kaltura.com/media/Mihran%20Papikians%20Personal%20Meeting%20Room/1_8tzqfouu) |
| 18 | November 22 | [notes](galois_theory_2025/lecture_18_notes.pdf) 6.8 MB | [recording](https://psu.mediaspace.kaltura.com/media/Mihran%20Papikians%20Personal%20Meeting%20Room/1_50ywpmpe) |
| 19 | December 3 | [notes](galois_theory_2025/lecture_19_notes.pdf) 6.0 MB | [recording](https://psu.mediaspace.kaltura.com/media/Mihran%20Papikians%20Personal%20Meeting%20Room/1_c9t6qmkb) |
| 20 | December 6 | [notes](galois_theory_2025/lecture_20_notes.pdf) 4.7 MB | [recording](https://psu.mediaspace.kaltura.com/media/Mihran%20Papikians%20Personal%20Meeting%20Room/1_jsukzohv) |
| 21 | December 10 | [notes](galois_theory_2025/lecture_21_notes.pdf) 10.8 MB | [recording](https://psu.mediaspace.kaltura.com/media/Mihran%20Papikians%20Personal%20Meeting%20Room/1_vnxe7xpg) |
| 22 | December 13 | [notes](galois_theory_2025/lecture_22_notes.pdf) 3.0 MB | [recording](https://psu.mediaspace.kaltura.com/media/Mihran%20Papikians%20Personal%20Meeting%20Room/1_9b8gzrd6) |
| 23 | December 17 | [notes](galois_theory_2025/lecture_23_notes.pdf) 5.8 MB | [recording](https://psu.mediaspace.kaltura.com/media/Mihran%20Papikians%20Personal%20Meeting%20Room/1_2elfj9oi) |

Other files:

- [Homework 1](galois_theory_2025/homework_1.pdf) (0.1 MB) - source: https://drive.google.com/file/d/10h-2p22gYK-bDaV4OvC2m3GXNczfnT-K/view?usp=sharing
- [Homework 2](galois_theory_2025/homework_2.pdf) (0.1 MB) - source: https://drive.google.com/file/d/1j1xTnyH1YNe-vul-zmNQGPpSdqKV05aR/view?usp=sharing
- [Homework 3](galois_theory_2025/homework_3.pdf) (0.1 MB) - source: https://drive.google.com/file/d/1NzV7oEB2uqIsN2fsk33w209Gran_xFXB/view?usp=sharing
- [Homework 4](galois_theory_2025/homework_4.pdf) (0.1 MB) - source: https://drive.google.com/file/d/10QI1XzFOCcKEwkQNuWGei2PCMbCB7f-7/view?usp=sharing
- [Homework 5](galois_theory_2025/homework_5.pdf) (0.1 MB) - source: https://drive.google.com/file/d/1cfCMTdZoN-r6pREQ13Iu-8by2l0k2DKf/view?usp=sharing
- [Homework 6](galois_theory_2025/homework_6.pdf) (0.1 MB) - source: https://drive.google.com/file/d/1DWjn5QyN5SFEams1pgeePzwrxiKoJDIW/view?usp=sharing
- [Homework 7](galois_theory_2025/homework_7.pdf) (0.0 MB) - source: https://drive.google.com/file/d/167XM7VgW6g4WjX28YjZ1EQBxLZOb1282/view?usp=sharing
- [Homework 8](galois_theory_2025/homework_8.pdf) (0.1 MB) - source: https://drive.google.com/file/d/1URn4_Jlbam8ulMHDK8d2t5lo5UpWCRhe/view?usp=sharing
- [Final Exam](galois_theory_2025/final_exam.pdf) (0.3 MB) - source: https://drive.google.com/file/d/191GBu69hG2lOgHf7Vz2a3PuViIwzpLg9/view?usp=sharing

Notes on the page: lecture 1 has no recording; lectures 15 and 16 are Google Drive videos, the
rest PSU Kaltura; no midterm file (probably the gap 22 Oct - 1 Nov); lecture 24 (20 Dec) is the final.
Lectures 9, 11 and 16 link the same notes file as 8, 10 and 15 (Drive ids identical): either shared
notes or a copy-paste slip on the page that hides the real notes of 9, 11 and 16. Not checked.

## Research page

Papers with a Drive PDF are in `research/`; the others link to journals or arXiv. His book
*Drinfeld Modules* (Graduate Texts in Mathematics 296, 2023) is linked to Springer, not downloadable. The full list with every link is
in `pages/research.txt` and `manifest.json`.

- Simons Foundation: https://simonsfoundation.org/mathematics-physical-sciences
- Drinfeld Modules: https://link.springer.com/book/9783031197062
- On ideal class groups of totally degenerate number rings: [pdf](research/on_ideal_class_groups_of_totally_degenerate_number_rings.pdf)
- Ogg's conjectures over function fields: https://celebratio.org/Ogg_AP/article/1209/
- On Drinfeld modular curves for SL(2): [pdf](research/on_drinfeld_modular_curves_for_sl_2.pdf)
- Drinfeld discriminant function and Fourier expansion of harmonic cochains: [pdf](research/drinfeld_discriminant_function_and_fourier_expansion_of_harmonic_cochains.pdf)
- Isomorphism classes of Drinfeld modules over finite fields: [pdf](research/isomorphism_classes_of_drinfeld_modules_over_finite_fields.pdf)
- The growth of the discriminant of the endomorphism ring of the reduction of a rank 2 generic Drinfeld module: [pdf](research/the_growth_of_the_discriminant_of_the_endomorphism_ring_of_the_reduction_of_a_ra.pdf)
- Computing endomorphism rings and Frobenius matrices of Drinfeld modules: [pdf](research/computing_endomorphism_rings_and_frobenius_matrices_of_drinfeld_modules.pdf)
- Endomorphism rings of reductions of Drinfeld modules: [pdf](research/endomorphism_rings_of_reductions_of_drinfeld_modules.pdf)
- Galois extensions and a conjecture of Ogg: [pdf](research/galois_extensions_and_a_conjecture_of_ogg.pdf)
- On Ribet's isogeny for J0(65): [pdf](research/on_ribet_s_isogeny_for_j0_65.pdf)
- Drinfeld-Stuhler modules: [pdf](research/drinfeld_stuhler_modules.pdf)
- The rational torsion subgroups of Drinfeld modular Jacobians and Eisenstein pseudo-harmonic cochains: [pdf](research/the_rational_torsion_subgroups_of_drinfeld_modular_jacobians_and_eisenstein_pseu.pdf)
- Optimal quotients of Jacobians with toric reduction and component groups: [pdf](research/optimal_quotients_of_jacobians_with_toric_reduction_and_component_groups.pdf)
- Graph Laplacians, component groups and Drinfeld modular curves: [pdf](research/graph_laplacians_component_groups_and_drinfeld_modular_curves.pdf)
- On Garland's vanishing theorem for SL(n): [pdf](research/on_garland_s_vanishing_theorem_for_sl_n.pdf)
- On component groups of Jacobians of quaternionic modular curves: [pdf](research/on_component_groups_of_jacobians_of_quaternionic_modular_curves.pdf)
- On the Eisenstein ideal over function fields: [pdf](research/on_the_eisenstein_ideal_over_function_fields.pdf)
- Drinfeld modules, Frobenius endomorphisms, and CM-liftings: [pdf](research/drinfeld_modules_frobenius_endomorphisms_and_cm_liftings.pdf)
- The Eisenstein ideal and Jacquet-Langlands isogeny over function fields: [pdf](research/the_eisenstein_ideal_and_jacquet_langlands_isogeny_over_function_fields.pdf)
- Non-archimedean uniformization and monodromy pairing: [pdf](research/non_archimedean_uniformization_and_monodromy_pairing.pdf)
- D-elliptic sheaves and odd Jacobians: [pdf](research/d_elliptic_sheaves_and_odd_jacobians.pdf)
- Local diophantine properties of modular curves of D-elliptic sheaves: [pdf](research/local_diophantine_properties_of_modular_curves_of_d_elliptic_sheaves.pdf)
- On generators of arithmetic groups over function fields: [pdf](research/on_generators_of_arithmetic_groups_over_function_fields.pdf)
- On Jacquet-Langlands isogeny over function fields: [pdf](research/on_jacquet_langlands_isogeny_over_function_fields.pdf)
- On finite arithmetic simplicial complexes: [pdf](research/on_finite_arithmetic_simplicial_complexes.pdf)
- Endomorphisms of exceptional D-elliptic sheaves: [pdf](research/endomorphisms_of_exceptional_d_elliptic_sheaves.pdf)
- On hyperelliptic modular curves over function fields: [pdf](research/on_hyperelliptic_modular_curves_over_function_fields.pdf)
- Genus formula for modular curves of D-elliptic sheaves: [pdf](research/genus_formula_for_modular_curves_of_d_elliptic_sheaves.pdf)
- Modular varieties of D-elliptic sheaves and the Weil-Deligne bound: [pdf](research/modular_varieties_of_d_elliptic_sheaves_and_the_weil_deligne_bound.pdf)
- On eigenvalues of p-adic curvature: [pdf](research/on_eigenvalues_of_p_adic_curvature.pdf)
- Modular curves of D-elliptic sheaves are asymptotically optimal: [pdf](research/modular_curves_of_d_elliptic_sheaves_are_asymptotically_optimal.pdf)
- Analogue of the degree conjecture over function fields: [pdf](research/analogue_of_the_degree_conjecture_over_function_fields.pdf)
- Abelian subvarieties of Drinfeld Jacobians and congruences modulo the characteristic: [pdf](research/abelian_subvarieties_of_drinfeld_jacobians_and_congruences_modulo_the_characteri.pdf)
- The number of rational points on Drinfeld modular varieties over finite fields: [pdf](research/the_number_of_rational_points_on_drinfeld_modular_varieties_over_finite_fields.pdf)
- On the torsion of optimal elliptic curves over function fields: [pdf](research/on_the_torsion_of_optimal_elliptic_curves_over_function_fields.pdf)
- On the variation of Tate-Shafarevich groups of elliptic curves over hyperelliptic curves: [pdf](research/on_the_variation_of_tate_shafarevich_groups_of_elliptic_curves_over_hyperellipti.pdf)
- Rigid-analytic geometry and abelian varieties: [pdf](research/rigid_analytic_geometry_and_abelian_varieties.pdf)
- Pesenti-Szpiro inequality for optimal elliptic curves: [pdf](research/pesenti_szpiro_inequality_for_optimal_elliptic_curves.pdf)
- On component groups of Jacobians of Drinfeld modular curves: [pdf](research/on_component_groups_of_jacobians_of_drinfeld_modular_curves.pdf)
- On the degree of modular parametrizations over function fields: [pdf](research/on_the_degree_of_modular_parametrizations_over_function_fields.pdf)
- On coset coverings of solutions of homogeneous cubic equations over finite fields: [pdf](research/on_coset_coverings_of_solutions_of_homogeneous_cubic_equations_over_finite_field.pdf)
- D-elliptic sheaves and the Hasse principle: https://arxiv.org/abs/2409.19268
- Rank-metric codes from Drinfeld modules: http://arxiv.org/abs/2601.03653
- Stabilization of isogeny spaces between supersingular Drinfeld modules: https://arxiv.org/abs/2604.17080
- A general construction of codes from Drinfeld modules: https://arxiv.org/abs/2609.01484
- Non-Archimedean Poincaré series and geodesics on the Bruhat-Tits tree: https://arxiv.org/abs/2609.23964
- Independence of l of the characteristic polynomial: https://arxiv.org/abs/2512.12374
- Skew cyclic codes through Drinfeld modules: https://arxiv.org/abs/2609.32906
- An overview of the theory of Drinfeld modules: [pdf](research/an_overview_of_the_theory_of_drinfeld_modules.pdf)
- Honda-Tate theorem for elliptic curves: [pdf](research/honda_tate_theorem_for_elliptic_curves.pdf)
- Mass formula for central division algebras over function fields: [pdf](research/mass_formula_for_central_division_algebras_over_function_fields.pdf)
- Notes on "Heights and the special values of L-series" by B. Gross: [pdf](research/notes_on_heights_and_the_special_values_of_l_series_by_b_gross.pdf)
- Notes on "Kolyvagin's work on modular elliptic curves" by B. Gross: [pdf](research/notes_on_kolyvagin_s_work_on_modular_elliptic_curves_by_b_gross.pdf)
- Heegner point computations over function fields: [pdf](research/heegner_point_computations_over_function_fields.pdf)

## Other pages

`pages/home.txt` (address and email), `pages/curriculum-vitae.txt` (positions: Michigan, YSU, Penn
State, Stanford, NCTS, MPIM, TIMS, Saarland, IHES, ASOF; mentoring: postdocs, PhD and MA students),
`pages/meetings-organized.txt` (conferences and special sessions, incl. the 2025 CIMPA school).
