import os
import certifi

# Fix macOS SSL Certificate errors
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
os.environ['SSL_CERT_FILE'] = certifi.where()

import sys
import json
import time
import requests
import cloudscraper
import subprocess
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
LEETCODE_SESSION = os.getenv("LEETCODE_SESSION")
LEETCODE_CSRF_TOKEN = os.getenv("LEETCODE_CSRF_TOKEN")
TARGET_REPO_DIR = os.getenv("TARGET_REPO_DIR", os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "LeetCode Solved")))

if not OPENROUTER_API_KEY:
    print("Error: OPENROUTER_API_KEY environment variable not set. Please run python setup.py")
    sys.exit(1)

# Initialize OpenRouter client via OpenAI SDK
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

# Initialize cloudscraper to bypass Cloudflare
scraper = cloudscraper.create_scraper(browser={
    'browser': 'chrome',
    'platform': 'windows',
    'desktop': True
})

# Top tier models for CP on OpenRouter (includes requested additions)
FALLBACK_MODELS = [
    "poolside/laguna-xs-2.1:free",
    "deepseek/deepseek-chat",
    "qwen/qwen3-coder",
    "qwen/qwen3-coder:free",
    "meta-llama/llama-3.3-70b-instruct:free",
    "nousresearch/hermes-3-llama-3.1-405b:free",
    "cohere/north-mini-code:free",
    "openrouter/free"
]

def get_headers(title_slug=None):
    headers = {
        "Content-Type": "application/json",
        "Origin": "https://leetcode.com",
        "Referer": f"https://leetcode.com/problems/{title_slug}/" if title_slug else "https://leetcode.com/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    if LEETCODE_CSRF_TOKEN:
        headers["x-csrftoken"] = LEETCODE_CSRF_TOKEN
    return headers

def get_cookies():
    cookies = {}
    if LEETCODE_SESSION:
        cookies["LEETCODE_SESSION"] = LEETCODE_SESSION
    if LEETCODE_CSRF_TOKEN:
        cookies["csrftoken"] = LEETCODE_CSRF_TOKEN
    return cookies

def get_daily_problem():
    print("Fetching LeetCode problem of the day...")
    url = "https://leetcode.com/graphql"
    query = """
    query {
      activeDailyCodingChallengeQuestion {
        date
        link
        question {
          questionId
          title
          titleSlug
          difficulty
          topicTags {
            name
          }
          content
        }
      }
    }
    """
    
    response = scraper.post(
        url, 
        json={'query': query}, 
        headers=get_headers(),
        cookies=get_cookies()
    )
    
    if response.status_code == 200:
        data = response.json()
        if 'data' in data and data['data'].get('activeDailyCodingChallengeQuestion'):
            return data['data']['activeDailyCodingChallengeQuestion']
        else:
            print("Could not find the daily question in the response.")
            return None
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return None

def get_specific_problem(title_slug):
    print(f"Fetching LeetCode problem: {title_slug}...")
    url = "https://leetcode.com/graphql"
    query = f"""
    query {{
      question(titleSlug: "{title_slug}") {{
        questionId
        title
        titleSlug
        difficulty
        topicTags {{
          name
        }}
        content
      }}
    }}
    """
    
    response = scraper.post(
        url, 
        json={'query': query}, 
        headers=get_headers(title_slug),
        cookies=get_cookies()
    )
    
    if response.status_code == 200:
        data = response.json()
        if 'data' in data and data['data'].get('question'):
            # Wrap it in the same structure as the daily problem for compatibility
            return {
                'date': datetime.now().strftime("%Y-%m-%d"),
                'link': f"/problems/{title_slug}/",
                'question': data['data']['question']
            }
        else:
            print("Could not find the specified question.")
            return None
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return None

def solve_problem_with_llm(problem_data):
    print("Generating solution with OpenRouter...")
    question = problem_data['question']
    title = question['title']
    difficulty = question['difficulty']
    content = question['content']
    tags = ", ".join([tag['name'] for tag in question['topicTags']])
    
    prompt = f"""
You are an expert software engineer and competitive programmer.
I need you to solve the following LeetCode problem:
Title: {title}
Difficulty: {difficulty}
Tags: {tags}

Problem Description (HTML):
{content}

Please provide your output exactly in the following JSON format. Ensure the JSON is valid, nicely formatted, and properly escaped. Do not wrap in markdown blocks, just raw JSON.
{{
    "QA_analysis": "A comprehensive markdown-formatted discussion of the problem, optimal approach (time and space complexity), and the solution.",
    "soln": "class Solution:\\n    def method_name(self, args):\\n        pass"
}}
"""
    
    for model_name in FALLBACK_MODELS:
        print(f"Trying model: {model_name}...")
        try:
            response = client.chat.completions.create(
                model=model_name,
                response_format={ "type": "json_object" },
                messages=[
                    {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
                    {"role": "user", "content": prompt}
                ],
                timeout=60
            )
            
            result_text = response.choices[0].message.content
            result_json = json.loads(result_text)
            print(f"Success with {model_name}!")
            return result_json
            
        except Exception as e:
            print(f"Model {model_name} failed: {e}")
            continue
            
    raise Exception("All fallback models failed to generate a solution.")

def submit_to_leetcode(title_slug, question_id, code):
    if not LEETCODE_SESSION or not LEETCODE_CSRF_TOKEN:
        print("Skipping LeetCode submission (Cookies not provided).")
        return True # Pretend success to continue git push

    print("Submitting solution to LeetCode...")
    submit_url = f"https://leetcode.com/problems/{title_slug}/submit/"
    
    payload = {
        "lang": "python3",
        "question_id": int(question_id) if str(question_id).isdigit() else question_id,
        "typed_code": code
    }
    
    try:
        response = scraper.post(
            submit_url,
            json=payload,
            headers=get_headers(title_slug),
            cookies=get_cookies(),
            allow_redirects=False
        )
        
        if response.status_code != 200:
            print(f"Submission failed with status code {response.status_code}")
            print(response.text)
            return False
            
        submission_id = response.json().get('submission_id')
        if not submission_id:
            print("Failed to get submission ID. Response:", response.json())
            return False
            
        print(f"Submitted successfully (ID: {submission_id}). Waiting for results...")
        
        # Poll for results
        check_url = f"https://leetcode.com/submissions/detail/{submission_id}/check/"
        
        for _ in range(15):  # Try for 15*2 = 30 seconds
            time.sleep(2)
            check_resp = scraper.get(
                check_url,
                headers=get_headers(title_slug),
                cookies=get_cookies()
            )
            if check_resp.status_code == 200:
                result = check_resp.json()
                state = result.get('state')
                if state == 'SUCCESS':
                    status_msg = result.get('status_msg')
                    if status_msg == 'Accepted':
                        print(f"✅ Submission Accepted! Runtime: {result.get('status_runtime')}, Memory: {result.get('status_memory')}")
                        return True
                    else:
                        print(f"❌ Submission Failed. Status: {status_msg}")
                        return False
            
        print("Submission evaluation timed out.")
        return False
        
    except Exception as e:
        print(f"Error submitting to LeetCode: {e}")
        return False

def save_and_commit(problem_data, solution_data):
    date_str = problem_data['date']
    title_slug = problem_data['question']['titleSlug']
    title = problem_data['question']['title']
    
    folder_name = f"{date_str}_{title_slug}"
    
    # The full path to the new problem folder
    full_folder_path = os.path.join(TARGET_REPO_DIR, folder_name)
    
    # Create directory
    if not os.path.exists(full_folder_path):
        os.makedirs(full_folder_path)
        
    qa_path = os.path.join(full_folder_path, "QA_analysis.md")
    soln_path = os.path.join(full_folder_path, "soln.py")
    
    print(f"Saving files to {full_folder_path}...")
    with open(qa_path, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        f.write(f"**Difficulty:** {problem_data['question']['difficulty']}\n\n")
        f.write(f"**Link:** https://leetcode.com{problem_data['link']}\n\n")
        f.write("---\n\n")
        f.write(solution_data.get("QA_analysis", ""))
        
    with open(soln_path, "w", encoding="utf-8") as f:
        f.write(solution_data.get("soln", ""))
        
    # Git operations
    print("Committing to Git...")
    try:
        subprocess.run(["git", "add", folder_name], cwd=TARGET_REPO_DIR, check=True, capture_output=True)
        status = subprocess.run(["git", "status", "--porcelain"], cwd=TARGET_REPO_DIR, check=True, capture_output=True, text=True)
        
        if status.stdout.strip():
            commit_msg = f"Auto-solved: {title} ({date_str})"
            subprocess.run(["git", "commit", "-m", commit_msg], cwd=TARGET_REPO_DIR, check=True, capture_output=True)
            print(f"Committed: {commit_msg}")
            
            try:
                print("Attempting to push...")
                subprocess.run(["git", "push", "-u", "origin", "main"], cwd=TARGET_REPO_DIR, check=True, capture_output=True, text=True)
                print("Push successful!")
            except subprocess.CalledProcessError as e:
                print("Push failed. Error:", e.stderr)
        else:
            print("No changes to commit.")
            
    except subprocess.CalledProcessError as e:
        print(f"Git operation failed: {e.stderr if e.stderr else e.output}")

def main():
    if len(sys.argv) > 1:
        # User provided a specific problem slug (strip trailing slashes first)
        title_slug = sys.argv[1].strip('/').split('/')[-1]
        problem_data = get_specific_problem(title_slug)
    else:
        # Default to daily problem
        problem_data = get_daily_problem()

    if not problem_data:
        print("Could not retrieve problem data. Exiting.")
        sys.exit(1)
        
    print(f"Today's problem: {problem_data['question']['title']}")
    
    try:
        solution_data = solve_problem_with_llm(problem_data)
        
        code = solution_data.get("soln", "")
        question_id = problem_data['question']['questionId']
        title_slug = problem_data['question']['titleSlug']
        
        is_accepted = submit_to_leetcode(title_slug, question_id, code)
        
        if is_accepted:
            save_and_commit(problem_data, solution_data)
            print("Process completed successfully!")
        else:
            print("Solution was not accepted. Skipping save and commit.")
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
