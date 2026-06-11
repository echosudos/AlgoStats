# About

This repository contains two Python modules, `difficulty_scraper.py` and `submission_checker.py`, that can be used to check a programming problem's difficulty and to verify if someone completed a specific problem. 

The difficulty scraper supports:
- AtCoder
- OnlineJudge
- OpenKattis
- Codeforces
- ProjectEuler

The verification script supports:
- AtCoder
- Codeforces
- OnlineJudge

These Python modules were created around 2024.

# Setup

Clone the repository and run:
```bash
pip install -r requirements.txt
```

Then, import the modules into your script and call their functions:
```python
import difficulty_scraper
import submission_checker
```

# Difficulty Scales For Each Platform

**OpenKattis**
Problems are categorized as easy, medium, or hard. The platform also represents difficulty numerically (e.g., ~1.0 for the lowest difficulty and ~9.7 for the highest); however, there are times when numerical difficulty is presented as a range. 

**Codeforces**
Easy problems have a rating of around 800, and the most challenging ones are around 3500.

**OnlineJudge**
Difficulty is determined by the percentage of users who solved the problem. 

**AtCoder**
Difficulty is presented as an integer, where ~-848 represents the easiest problems and ~3800 represents the hardest ones.

**ProjectEuler**
Difficulty is displayed as a percentage, with ~5% usually representing the easiest problems and ~50% representing the hardest ones.