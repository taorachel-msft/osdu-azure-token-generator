# What is it?

This is a simple python tool that assists with generating access tokens for OSDU development on Azure
Based off documentation found here:
https://learn.microsoft.com/en-us/azure/energy-data-services/concepts-authentication

# How to Use

*on first run*

1. Clone the repository and navigate to the directory
2. [Optional] create and activate a virtual environment using `python -m venv venv`
3. Install necessary packages from `requirements.txt` using `pip install -r requirements.txt`
4. Update `environments.yml` with key vault information for commonly used environments

*on every run*

5. Log into Azure CLI using `az login [--use-device-code --tenant <tenant-id>]`
6. Run the script with `python run.py`

Once you have your token, all you need to do use use your token in authorization header or in the swagger ui

# Configuration

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| --tenant, -t | The tenant id of the environment you are generating the token for | AzureGlobal1 |
| --env, -e | Target OSDU environment ex. stg, glab | glab |
| --log-level, -l | Logging level of the application ex. INFO, DEBUG, ERROR | INFO |

## Environment yaml

This tool uses a yaml file to store environment key vault information so the tool knows which key vault to pull the required secret and client id data from.

# Tips and Tricks

## Aliasing the script

It could be beneficial to create an alias to run the script from anywhere.
To do so in linux, modify your `.bashrc` file to include:
`alias get-token="/path/to/venv/[bin | Script]/python /path/to/repo/run.py"`

*Note the path to your python executable will be different depending on your version of python*

If not using a virtual environment, you can remove the explicit path to the python executable.

Then, you should be able to use your script anywhere by running:
`get-token [-t] [-e] [-l]`

