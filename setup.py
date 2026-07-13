import os
import subprocess

def setup_env():
    print("=== LeetCode & GitHub Setup ===\n")
    print("To automate LeetCode submissions, you need to provide your session cookies.")
    print("1. Log in to LeetCode in your browser.")
    print("2. Open Developer Tools (F12) -> Application -> Cookies.")
    print("3. Copy the values for 'LEETCODE_SESSION' and 'csrftoken'.\n")

    leetcode_session = input("Enter LEETCODE_SESSION cookie: ").strip()
    csrf_token = input("Enter csrftoken cookie: ").strip()
    
    print("\nNext, OpenRouter API Key for the LLM.")
    openrouter_api_key = input("Enter OPENROUTER_API_KEY (leave blank to keep existing if any): ").strip()
    
    print("\nNext, specify the directory where solutions should be saved.")
    default_target = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "LeetCode Solved"))
    target_repo_dir = input(f"Enter Target Directory (leave blank for '{default_target}'): ").strip()
    if not target_repo_dir:
        target_repo_dir = default_target

    env_path = ".env"
    
    # Read existing env
    existing_env = {}
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    existing_env[k] = v

    if leetcode_session:
        existing_env["LEETCODE_SESSION"] = leetcode_session
    if csrf_token:
        existing_env["LEETCODE_CSRF_TOKEN"] = csrf_token
    if openrouter_api_key:
        existing_env["OPENROUTER_API_KEY"] = openrouter_api_key
    if target_repo_dir:
        existing_env["TARGET_REPO_DIR"] = target_repo_dir

    # Write back
    with open(env_path, "w") as f:
        for k, v in existing_env.items():
            f.write(f"{k}={v}\n")
            
    print("\n[+] .env file updated successfully.")
    return existing_env.get("TARGET_REPO_DIR", default_target)

def setup_github(target_dir):
    print("\n=== GitHub Setup ===")
    print(f"Provide your empty GitHub repository URL to push solutions automatically from: {target_dir}")
    repo_url = input("Enter Repo URL (e.g., https://github.com/user/repo.git) or press Enter to skip: ").strip()
    
    if repo_url:
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
            
        # Initialize git if not already a repo
        if not os.path.exists(os.path.join(target_dir, ".git")):
            subprocess.run(["git", "init"], cwd=target_dir, check=True)
            
        try:
            # Check if origin already exists
            res = subprocess.run(["git", "remote", "-v"], cwd=target_dir, capture_output=True, text=True)
            if "origin" in res.stdout:
                subprocess.run(["git", "remote", "set-url", "origin", repo_url], cwd=target_dir, check=True)
                print("[+] Updated existing remote 'origin'.")
            else:
                subprocess.run(["git", "remote", "add", "origin", repo_url], cwd=target_dir, check=True)
                print("[+] Added remote 'origin'.")
        except subprocess.CalledProcessError as e:
            print(f"[-] Error setting up Git remote: {e}")

if __name__ == "__main__":
    target_dir = setup_env()
    setup_github(target_dir)
    print("\n=== Setup Complete! ===")
    print("You can now run: python3 leetcode_solver.py or python leetcode_solver.py")
