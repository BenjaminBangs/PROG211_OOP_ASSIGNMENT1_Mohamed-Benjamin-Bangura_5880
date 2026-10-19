"""
Digital Exam & Results Management System (DERMS)
PROG211 - Object-Oriented Programming 1
Mohamed Benjamin Bangura_5880

A small open-source tool that records exam scores and produces grades
WITHOUT storing any personal data. Learners are identified only by an
anonymous, auto-generated candidate code (e.g. CAND-001).

Classes:
    Exam            - describes an exam (subject, total marks, pass mark)
    Candidate       - an anonymous learner (code + class level only)
    Result          - links one Candidate to one Exam with a score
    ResultsManager  - stores many Result objects in a LIST

Run:
    python exam_system.py          -> interactive menu
    python exam_system.py --demo   -> automatic demonstration
"""

import sys


# ---------------------------------------------------------------------------
# CLASS 1: Exam
# ---------------------------------------------------------------------------
class Exam:
    """An exam that candidates can sit."""

    exams_created = 0  # class attribute shared by all Exam objects

    def __init__(self, subject, total_marks=100, pass_mark=50):
        Exam.exams_created += 1
        self.exam_id = f"EXAM-{Exam.exams_created:03d}"
        self.subject = subject
        self.total_marks = total_marks
        self.pass_mark = pass_mark

    # Instance method: works on one specific exam object
    def display_info(self):
        return (f"{self.exam_id} | Subject: {self.subject} | "
                f"Total marks: {self.total_marks} | Pass mark: {self.pass_mark}")

    # Class method: works on the class, not one object
    @classmethod
    def total_exams(cls):
        return cls.exams_created


# ---------------------------------------------------------------------------
# CLASS 2: Candidate (anonymous - no names, ages, addresses or contacts)
# ---------------------------------------------------------------------------
class Candidate:
    """An anonymous learner identified only by a generated code."""

    candidates_created = 0

    def __init__(self, class_level):
        Candidate.candidates_created += 1
        self.candidate_code = f"CAND-{Candidate.candidates_created:03d}"
        self.class_level = class_level  # e.g. "SSS 1" (not personal data)

    # Instance method
    def display_info(self):
        return f"{self.candidate_code} | Class level: {self.class_level}"

    # Class method
    @classmethod
    def total_candidates(cls):
        return cls.candidates_created


# ---------------------------------------------------------------------------
# CLASS 3: Result (interaction between Candidate and Exam objects)
# ---------------------------------------------------------------------------
class Result:
    """The score a Candidate obtained in an Exam."""

    # Tuple of (minimum percentage, grade, remark) - read-only data
    GRADE_BANDS = (
        (75, "A", "Excellent"),
        (65, "B", "Very Good"),
        (55, "C", "Good"),
        (50, "D", "Pass"),
        (0, "F", "Fail"),
    )

    def __init__(self, candidate, exam, score):
        if not Result.is_valid_score(score, exam.total_marks):
            raise ValueError(
                f"Score must be a number from 0 to {exam.total_marks}.")
        self.candidate = candidate  # a Candidate object
        self.exam = exam            # an Exam object
        self.score = score

    # Static method: needs no object or class data
    @staticmethod
    def is_valid_score(score, total_marks):
        return isinstance(score, (int, float)) and 0 <= score <= total_marks

    # Instance methods
    def percentage(self):
        return round(self.score / self.exam.total_marks * 100, 1)

    def grade(self):
        pct = self.percentage()
        for minimum, letter, remark in Result.GRADE_BANDS:
            if pct >= minimum:
                return letter, remark

    def status(self):
        return "PASS" if self.score >= self.exam.pass_mark else "FAIL"

    def display_info(self):
        letter, remark = self.grade()
        return (f"{self.candidate.candidate_code} | {self.exam.subject} | "
                f"Score: {self.score}/{self.exam.total_marks} "
                f"({self.percentage()}%) | Grade: {letter} ({remark}) | "
                f"{self.status()}")


# ---------------------------------------------------------------------------
# CLASS 4: ResultsManager (uses a LIST to store many Result objects)
# ---------------------------------------------------------------------------
class ResultsManager:
    """Stores and reports on many Result objects."""

    def __init__(self):
        self.results = []  # the LIST data structure

    def add_record(self, result):
        """Add one Result object to the list."""
        self.results.append(result)
        print(f"Record added for {result.candidate.candidate_code}.")

    def display_records(self):
        """Loop through the list and print every record."""
        if not self.results:
            print("No records yet.")
            return
        print("\n--- ALL RESULTS ---")
        for number, result in enumerate(self.results, start=1):
            print(f"{number}. {result.display_info()}")

    def class_summary(self, exam_id):
        """Average score and pass rate for one exam."""
        scores = [r for r in self.results if r.exam.exam_id == exam_id]
        if not scores:
            return "No results for this exam."
        average = sum(r.score for r in scores) / len(scores)
        passed = sum(1 for r in scores if r.status() == "PASS")
        return (f"{exam_id}: {len(scores)} result(s), average score "
                f"{average:.1f}, passed {passed} of {len(scores)}")


# ---------------------------------------------------------------------------
# Demonstration and menu
# ---------------------------------------------------------------------------
def run_demo():
    print("=== DEMO: Digital Exam & Results Management System ===\n")
    math_exam = Exam("Mathematics", total_marks=100, pass_mark=50)
    ict_exam = Exam("ICT", total_marks=50, pass_mark=25)
    print(math_exam.display_info())
    print(ict_exam.display_info())

    c1, c2, c3 = Candidate("SSS 1"), Candidate("SSS 1"), Candidate("SSS 2")
    print()
    for c in (c1, c2, c3):
        print(c.display_info())

    manager = ResultsManager()
    print()
    manager.add_record(Result(c1, math_exam, 82))
    manager.add_record(Result(c2, math_exam, 47))
    manager.add_record(Result(c3, ict_exam, 38))
    manager.display_records()

    print("\n--- SUMMARY ---")
    print(manager.class_summary(math_exam.exam_id))
    print(f"Exams created: {Exam.total_exams()} | "
          f"Candidates created: {Candidate.total_candidates()}")

    print("\n--- VALIDATION TEST ---")
    try:
        Result(c1, math_exam, 150)
    except ValueError as error:
        print("Error caught:", error)


def read_number(prompt):
    try:
        return float(input(prompt))
    except ValueError:
        return None


def run_menu():
    manager = ResultsManager()
    exams, candidates = [], []
    print("Digital Exam & Results Management System")
    print("No personal data is stored. Learners get anonymous codes.")
    while True:
        print("\nMenu:\n 1 Create exam\n 2 Create candidate\n"
              " 3 Add result\n 4 Show all results\n 5 Exam summary\n 0 Exit")
        choice = input("Choose a number: ").strip()
        if choice == "1":
            subject = input("Subject name: ").strip()
            total = read_number("Total marks: ")
            pass_mark = read_number("Pass mark: ")
            if not subject or total is None or pass_mark is None:
                print("Please enter valid values.")
                continue
            exams.append(Exam(subject, total, pass_mark))
            print("Created:", exams[-1].display_info())
        elif choice == "2":
            candidates.append(Candidate(input("Class level (e.g. SSS 1): ").strip()))
            print("Created:", candidates[-1].display_info())
        elif choice == "3":
            if not exams or not candidates:
                print("Create at least one exam and one candidate first.")
                continue
            for e in exams:
                print(" ", e.display_info())
            exam = next((e for e in exams if e.exam_id == input("Exam ID: ").strip().upper()), None)
            for c in candidates:
                print(" ", c.display_info())
            cand = next((c for c in candidates if c.candidate_code == input("Candidate code: ").strip().upper()), None)
            score = read_number("Score: ")
            if exam is None or cand is None or score is None:
                print("Unknown ID/code or invalid score.")
                continue
            try:
                manager.add_record(Result(cand, exam, score))
            except ValueError as error:
                print("Error:", error)
        elif choice == "4":
            manager.display_records()
        elif choice == "5":
            print(manager.class_summary(input("Exam ID: ").strip().upper()))
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Please choose a number from the menu.")


if __name__ == "__main__":
    if "--demo" in sys.argv:
        run_demo()
    else:
        run_menu()
