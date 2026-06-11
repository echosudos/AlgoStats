'''
Python module for extracting the difficulty of programming problems found on:
- AtCoder
- Codeforces
- OnlineJudge
- OpenKattis
- ProjectEuler

Available Functions:
- getDifficulty_atcoder(problem_id)
- getDifficulty_codeforces(contest_id, index)
- getDifficulty_onlinejudge(problem_id)
- getDifficulty_openkattis(problem_id)
- getDifficulty_projecteuler(problem_id)
'''

import requests
import json
from bs4 import BeautifulSoup

# ------------------------------------------------------------------

def getDifficulty_atcoder(problem_id):
    """
    Fetches the difficulty of a problem from the JSON file hosted online.

    Parameters:
        problem_id (str): The ID of the problem in the format "contestName_Letter" (e.g., "abc138_a").

    Returns:
        int or str: The difficulty of the problem, or a message if not found.
    """
    url = "https://kenkoooo.com/atcoder/resources/problem-models.json"

    try:
        # Fetch the latest JSON file
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP errors
        data = response.json()

        # Look for the problem ID in the JSON data
        if problem_id in data and "difficulty" in data[problem_id]:
            return data[problem_id]["difficulty"]
        else:
            return f"Problem ID '{problem_id}' not found or no difficulty data available."

    except requests.exceptions.RequestException as e:
        return f"Error fetching data: {e}"

# ------------------------------------------------------------------

def getDifficulty_codeforces(contest_id, index):
    url = "https://codeforces.com/api/problemset.problems"
    response = requests.get(url)
    data = response.json()
    
    if data["status"] == "OK":
        for problem in data["result"]["problems"]:
            if problem["contestId"] == contest_id and problem["index"] == index:
                return problem.get("rating", "No rating found")
    return "Problem not found"

# ------------------------------------------------------------------

def getDifficulty_onlinejudge(problem_id):
    """
    Fetches total submissions, users that tried, and users that solved
    a given problem from onlinejudge.org by parsing the HTML.
    
    Returns a tuple of (total_submissions, users_tried, users_solved).
    All of them will be strings
    """
    # Construct the URL for problem stats
    url = (
        "https://onlinejudge.org/index.php?"
        "option=com_onlinejudge&Itemid=8&page=problem_stats"
        f"&problemid={problem_id}&category=0"
    )

    # Fetch the page
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch stats page, status {response.status_code}")

    # Parse with BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Locate the <tr> that holds total submissions, users tried, users solved
    row = soup.find("tr", class_="sectiontableentry1")
    if not row:
        raise ValueError("Could not find the problem stats row in HTML.")

    # Extract the 3 <td> cells from that row
    tds = row.find_all("td", align="center")
    if len(tds) < 3:
        raise ValueError("Problem stats row does not have the expected 3 columns.")

    total_submissions = tds[0].get_text(strip=True)
    users_tried       = tds[1].get_text(strip=True)
    users_solved      = tds[2].get_text(strip=True)

    return total_submissions, users_tried, users_solved

# ------------------------------------------------------------------

def getDifficulty_openkattis(problem_id):
    """
    Scrape the Kattis Metadata tab for the given problem_id
    and return the numeric difficulty and label (e.g., 'Medium').
    """
    url = f"https://open.kattis.com/problems/{problem_id}?tab=metadata"
    
    # 1) Fetch the page.
    response = requests.get(url, timeout=10)
    response.raise_for_status()  # Raise for HTTP errors
    
    # 2) Parse with BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    
    # 3) Look for a div with class "metadata-difficulty-card"
    diff_card = soup.find("div", class_="metadata-difficulty-card")
    if not diff_card:
        print("No difficulty card found in HTML. Possibly loaded by JavaScript or not present.")
        return None
    
    # 4) Inside that card, look for the <span> with class "difficulty_number"
    difficulty_number_span = diff_card.find("span", class_="difficulty_number")
    if not difficulty_number_span:
        print("No difficulty_number span found. The HTML structure might have changed.")
        return None
    
    # 5) Extract the text, which might be something like '3.0'
    difficulty_str = difficulty_number_span.get_text(strip=True)
    try:
        numeric_difficulty = float(difficulty_str)
    except ValueError:
        numeric_difficulty = difficulty_str  # just store the raw string
    
    # 6) Also find the textual label (e.g., 'Medium')
    #    It's in the next <span> with class "text-lg font-bold text-blue-200"
    #    But let's look more specifically inside the same card:
    difficulty_label_span = diff_card.find("span", class_="text-lg font-bold text-blue-200")
    if difficulty_label_span:
        difficulty_label = difficulty_label_span.get_text(strip=True)
    else:
        difficulty_label = None
    
    return numeric_difficulty, difficulty_label

# ------------------------------------------------------------------

def getDifficulty_projecteuler(problem_id):
    """
    Fetches the difficulty of a problem from projecteuler.net based on the problem ID.

    Args:
        problem_id (int): The ID of the problem.

    Returns:
        str: The difficulty rating of the problem or an error message if not found.
    """
    url = f"https://projecteuler.net/problem={problem_id}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP issues

        soup = BeautifulSoup(response.text, 'html.parser')

        # Locate the tooltip text containing difficulty rating
        tooltip_span = soup.find('span', class_='tooltiptext_right')

        if tooltip_span:
            tooltip_text = tooltip_span.text
            # Extract the difficulty rating from the tooltip text
            for line in tooltip_text.split(';'):
                if "Difficulty rating" in line:
                    return line.split(':')[1].strip()
            return "Difficulty rating not found in the tooltip."
        else:
            return "Difficulty information not available for this problem."

    except requests.exceptions.RequestException as e:
        return f"Error fetching problem: {e}"