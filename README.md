# GitHunt

<p align="center">
 <img height=400px weight=400px src=".assets/GitHunt.png" >
</p>
GitHunt is a Python tool for detecting sensitive data exposure in GitHub repositories. Leveraging GitHub's powerful search functionality, it scans for private keys, credentials, authentication tokens, API keys, and more.  

  > [!NOTE]
> As of `March 11, 2024`, secret scanning and push protection will be enabled by default for all new user-owned public repositories that you create.

> [!WARNING]
> **⚠️ DISCLAIMER**
>
> THIS PROJECT IS ONLY FOR ***SECURITY RESEARCH*** AND REMINDS OTHERS TO PROTECT THEIR PROPERTY, DO NOT USE IT ILLEGALLY!!
>
> The project authors are not responsible for any consequences resulting from misuse.


## Installation 

Clone repo and install dependencies
```bash
git clone https://github.com/v4resk/GitHunt && cd GPTHunter
python3 -m virtualenv venv && source venv/bin/activate
pip3 install -r requirements.txt
```

## Usage

You must specify a Github access token in order to interact with the Github API, see [this page](https://docs.github.com/fr/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) to create one.

```bash

 python GitHunt.py -h

     ██████╗ ██╗████████╗██╗  ██╗██╗   ██╗███╗   ██╗████████╗
    ██╔════╝ ██║╚══██╔══╝██║  ██║██║   ██║████╗  ██║╚══██╔══╝
    ██║  ███╗██║   ██║   ███████║██║   ██║██╔██╗ ██║   ██║
    ██║   ██║██║   ██║   ██╔══██║██║   ██║██║╚██╗██║   ██║
    ╚██████╔╝██║   ██║   ██║  ██║╚██████╔╝██║ ╚████║   ██║
    ╚═════╝ ╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝
                                                 @v4resk

usage: GitHunt.py [-h] -m {gpt}

Hunt for sensitive data exposure on GitHub.

options:
  -h, --help          show this help message and exit
  -m, --module {gpt}  Hunting model to run
```


## References
GitHunt was largely inspired by [ChatGPT-API-Leakage](https://github.com/Junyi-99/ChatGPT-API-Leakage/tree/main) and projects [Github Dorks](https://github.com/techgaun/github-dorks).
