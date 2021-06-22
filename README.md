# Introduction
The program aims to collect user informations, including photos, screenshots, and recordings.

The user informations would be uploaded to S3 buckets, then trigger the [lambdas](https://github.com/nccuSimonLee/cloudproj-lambda) to perform the main logic of the system.

# Setup
First, you need to install the dependencies in a `python 3.8` environment using the following command.
```shell
pip install -r requirements.txt
```

Then modify the `config.yaml` to adapt your aws cognito settings because the program would request you log in with a cognito user to acquire S3 permissions.

# Usage
The program would take a photo and screenshot in a specified period in seconds. The period could be specified in `config.yaml` by modifying `SLEEP_TIME`.

If you want to record voices, the shortcut is ctrl.