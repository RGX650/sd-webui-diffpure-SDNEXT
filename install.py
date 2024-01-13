import os
import launch
import git

# Get the path to the requirements.txt file
req_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "requirements.txt")

# Open the requirements.txt file and process each line
with open(req_file) as file:
    for lib in file:
        lib = lib.strip()

        # Check if the package is from a GitHub repository
        if lib.startswith("git+"):
            # Install the GitHub repository package
            git_repo_url = lib[len("git+"):]
            repo_name = os.path.basename(git_repo_url.rstrip(".git"))
            install_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), repo_name)
            
            if not os.path.exists(install_path):
                git.Repo.clone_from(git_repo_url, install_path)

            launch.run_pip(f'install -e {install_path}', f"clear object requirement: {lib}")
        elif not launch.is_installed(lib):
            # Install other packages from PyPI if not already installed
            launch.run_pip(f'install {lib}', f"clear object requirement: {lib}")
