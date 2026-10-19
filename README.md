# PROG211_OOP_ASSIGNMENT_1
# Digital Exam & Results Management System (DERMS)

**Module:** PROG211 – Object-Oriented Programming 1
**Domain:** Education – Digital Exam & Results Management System
Mohamed Benjamin Bangura_905005880

## Problem
Many schools record exam scores on paper or in spreadsheets that contain learners' names and other personal details. This is error-prone and a privacy risk. DERMS is a small, open-source tool that records scores, calculates percentages and grades, and summarises exam performance **without storing any personal data**. Learners are identified only by an anonymous code such as `CAND-001`.

## OOP Design

| Class | Purpose | Key attributes | Methods |
|---|---|---|---|
| `Exam` | An exam | `exam_id`, `subject`, `total_marks`, `pass_mark` | `display_info()` (instance), `total_exams()` (class) |
| `Candidate` | Anonymous learner | `candidate_code`, `class_level` | `display_info()` (instance), `total_candidates()` (class) |
| `Result` | Links a Candidate and an Exam | `candidate`, `exam`, `score` | `percentage()`, `grade()`, `status()`, `display_info()` (instance), `is_valid_score()` (static) |
| `ResultsManager` | Stores many results | `results` (list) | `add_record()`, `display_records()`, `class_summary()` |

**Object interaction:** a `Result` object holds a `Candidate` object and an `Exam` object, and uses the exam's total and pass mark to calculate the percentage and PASS/FAIL status.

**Data structure:** a **list** (`ResultsManager.results`) stores all `Result` objects. `add_record()` appends to it and `display_records()` loops through it. A **tuple** (`Result.GRADE_BANDS`) stores the read-only grade boundaries.

**Method types:**
- Instance methods: `percentage()`, `grade()`, `status()`, `display_info()`
- Class methods (`@classmethod`): `Exam.total_exams()`, `Candidate.total_candidates()`
- Static method (`@staticmethod`): `Result.is_valid_score()`

## How the System Meets Digital Public Goods (DPG) Standards

| DPG principle | How DERMS meets it |
|---|---|
| **Open-source** | Source code is published on GitHub for anyone to use, study, modify and share. Uses only the Python standard library, so there are no licence or cost barriers. |
| **Inclusive and accessible design** | Plain-text interface that works with screen readers; simple numbered menu and clear prompts; does not rely on colour or images; friendly error messages; runs on low-cost computers with no internet connection. |
| **Privacy-respecting** | No names, ages, addresses, phone numbers or other personal data are collected. Only an auto-generated code and a class level are stored. |
| **Modular and reusable** | Each class has one job and can be reused or extended separately (for example, adding a `Subject` or `Teacher` class, or saving to a file). Any school or subject can use it. |

## How to Run
```
python exam_system.py          # interactive menu
python exam_system.py --demo   # automatic demonstration
```

## Example Usage (Sample Input/Output)

**Input:** run `python exam_system.py --demo`

**Output:**
```
EXAM-001 | Subject: Mathematics | Total marks: 100 | Pass mark: 50
EXAM-002 | Subject: ICT | Total marks: 50 | Pass mark: 25

CAND-001 | Class level: SSS 1
CAND-002 | Class level: SSS 1
CAND-003 | Class level: SSS 2

Record added for CAND-001.
Record added for CAND-002.
Record added for CAND-003.

--- ALL RESULTS ---
1. CAND-001 | Mathematics | Score: 82/100 (82.0%) | Grade: A (Excellent) | PASS
2. CAND-002 | Mathematics | Score: 47/100 (47.0%) | Grade: F (Fail) | FAIL
3. CAND-003 | ICT | Score: 38/50 (76.0%) | Grade: A (Excellent) | PASS

--- SUMMARY ---
EXAM-001: 2 result(s), average score 64.5, passed 1 of 2
Exams created: 2 | Candidates created: 3

--- VALIDATION TEST ---
Error caught: Score must be a number from 0 to 100.
```

## Files
- `exam_system.py` – Python source code
- `README.md` – this documentation

## Licence
MIT Licence – free to use, modify and share.
 
