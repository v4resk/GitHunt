# GHunter

<p align="center">
 <img height=400px weight=400px src=".assets/GHunter.png" >
</p>


GHunter is a small automation project designed to hunt for publicly exposed private keys, credentials, authentication tokens, API Keys, etc, using GitHub search. 

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
git clone https://github.com/v4resk/GHunter && cd GPTHunter
python3 -m virtualenv venv && source venv/bin/activate
pip3 install -r requirements.txt
```

## Usage

You must specify a Github access token in order to interact with the Github API, see [this page](https://docs.github.com/fr/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) to create one.
```bash

TO DO
```


## References
GHunter was largely inspired by [ChatGPT-API-Leakage](https://github.com/Junyi-99/ChatGPT-API-Leakage/tree/main) and projects [Github Dorks](https://github.com/techgaun/github-dorks).
