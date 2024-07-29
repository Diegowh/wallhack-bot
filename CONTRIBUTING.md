# CONTRIBUTING to Wallhack Bot
First of all, thank you for collaborate with me. 
To ensure a smooth collaboration process, please follow the guidelines and steps outlined below.

### Getting Started
> This project uses Python 3.12
1. Clone the repository
   ```bash
   git clone https://github.com/Diegowh/wallhack-bot.git
   ```
2. Create a Virtual Environment
   ```bash
   python -m venv .venv
   ```
3. Activate the Virtual Environment
   - Windows (cmd):
       ```
     .venv/Scripts/activate
     ```
   - Windows (Git Bash):
       ```
     source .venv/Scripts/activate
     ```
   - Linux and MacOS
       ```
     source .venv/bin/activate
     ```
4. Create a `.env` File
   
    Use the cloned `.env.example` to see whats required to put in the `.env.` file.

5. Install the required dependencies
   ```
   pip install -r requirements.txt
   ```
6. Run the Bot
    ```
   python main.py
   ```


### Contribution Guidelines

1. Create a new Branch
   - ```
     git checkout -b feature/your-feature-name
     ```
2. Implement your changes
    - Make your changes in the new branch. 
    - Ensure your code adheres to the project coding standards and includes appropriate documentation. 
    - Follow [PEP 8 - Style Guide for Python Code](https://peps.python.org/pep-0008/)
3.  Commit and push your changes
    - ```
      git add .
      ```
    - ```
      git commit -m "Add a description of your changes"
      ```
    - ```
      git push origin feature/your-feature-name
      ```
4. Create a Pull Request
   - Navigate to the [Wallhack Bot repository pull requests tab](https://github.com/Diegowh/wallhack-bot/pulls)
   - Click on `New pull request`
   - Select `main` branch and compare it with your branch `feature/your-feature-name`
   - Provide a detailed description of your changes in the PR description
   - Submit the pull request