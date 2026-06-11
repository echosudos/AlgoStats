'''
Python module for verifying if someone completed a problem on:
- AtCoder
- Codeforces
- OnlineJudge

Available Functions:
- getProof_atcoder(user_id, problem_id)
- getProof_codeforces(username, contest_id, problem_index)
- getProof_onlinejudge(user_id, problem_id)
'''

import requests

# ------------------------------------------------------------------

def getProof_atcoder(user_id, problem_id):
    """
    Check if a user has completed a specific problem on AtCoder.
    
    Parameters:
        user_id (str): The user's AtCoder ID.
        problem_id (str): The problem ID to check (e.g., "arc037_C").
    
    Returns:
        bool: True if the problem is completed (result "AC"), False otherwise.
    """
    # API URL with parameters
    unix_second = 10368000  # Fixed value as per instructions
    api_url = f"https://kenkoooo.com/atcoder/atcoder-api/v3/user/submissions?user={user_id}&from_second={unix_second}"
    
    try:
        # Send a request to the API
        response = requests.get(api_url)
        response.raise_for_status()
        
        # Parse the JSON response
        submissions = response.json()
        
        # Iterate over submissions to find the problem with result "AC"
        for submission in submissions:
            if submission.get("problem_id") == problem_id and submission.get("result") == "AC":
                return True
        
        # If no matching problem_id with result "AC" is found, return False
        return False
    except requests.RequestException as e:
        print(f"Error accessing the API: {e}")
        return False

# ------------------------------------------------------------------

def getProof_codeforces(username, contest_id, problem_index):
    """
    Check if a user has completed a specific problem on Codeforces.

    Args:
        username (str): The Codeforces username.
        contest_id (str): The contest ID of the problem.
        problem_index (str): The index of the problem (e.g., "A", "B").

    Returns:
        bool: True if the user has completed the problem, False otherwise.
    """
    base_url = "https://codeforces.com/api/user.status"
    
    try:
        # Fetch the user's submission data
        response = requests.get(base_url, params={"handle": username})
        response.raise_for_status()
        data = response.json()

        # Check if API response status is OK
        if data["status"] != "OK":
            print("Error: Unable to fetch data from Codeforces API.")
            return False

        # Parse the submissions
        submissions = data["result"]
        for submission in submissions:
            # Check if the submission matches the problem ID and is correct
            problem = submission["problem"]
            submission_contest_id = str(problem.get("contestId", ""))
            submission_index = problem.get("index", "")

            if contest_id == submission_contest_id and problem_index == submission_index and submission["verdict"] == "OK":
                return True

        return False

    except requests.RequestException as e:
        print(f"Error: {e}")
        return False

# ------------------------------------------------------------------

def getProof_onlinejudge(user_id, problem_id):
    """
    Checks if the user has completed the specified problem on onlinejudge.org using the Uhunt API.

    Parameters:
        user_id (int): The user ID of the user (Uhunt ID).
        problem_id (int): The ID of the problem to check.

    Returns:
        bool: True if the user has completed the problem, False otherwise.
    """
    try:
        # Construct the URL to fetch the user's submission data
        url = f"https://uhunt.onlinejudge.org/api/subs-user/{user_id}"

        # Send a GET request to the API
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes

        # Parse the JSON response
        data = response.json()
        submissions = data.get("subs", [])

        # Check each submission for the target problem_id with verdict 90
        for submission in submissions:
            if submission[1] == problem_id:  # Check if problem_id matches
                if submission[2] == 90:  # Check if verdict is Accepted (90)
                    return True

        return False  # If no Accepted verdict is found for the problem_id

    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return False
    except KeyError:
        print("Unexpected response format.")
        return False