# Automatic EC2 instance shutdown

## Description
Automation that shuts down EC2 instances that are not tagged in a specific way. Could be used in dev/test/lab environments to save money by automatically shutting down instances that are not necessary or are forgotten

## Installation

### Prerequisites
* An AWS account is needed
* AWS CLI needs to be installed 
* SAM CLI needs to be installed
* Works on MAC/Linux since the install script uses bash (Haven't tested WSL but probably works there too)

### How to install
* Clone the repository
* Edit template.yml parameters to fit your needs.
    ** MaxAge Number of days before instance is shut down
    ** MainRegionParam: The primary region where you plan to use this. This is where the IAM roles/policies are installed. Once set, do not change as you will get an deployment error. If you want to change it, uninstall the solution and re-install with new region
    ** Tags: Comma separated list of tag keys that will be used to determine if an instance should stay up or be shutdown. 
* run 'bash deploy.sh'
* Enter the region you want to install to. If this is the first install you have to use the region you've set as main region in the template. If this has previously been installed to the main region, you can pick any region you want. 
* Enter the profile you want to use. This is an AWS profile


### Uninstall
* run 'bash uninstall.sh'
* Enter the region you want to uninstall from. If you are uninstalling from the main region, the IAM role will be removed
* Enter the profile you want to use. 


## Cost
This solution will create some minor cost. The parameters cost per parameter and the lambda in invocation time. The lambda can run at a maximum of once a day and invokation time will be dependent on how many instances you have. I estimate that the total cost per month will be a few cents up to a couple of dollars at most. To be sure, set a budget for max spend in your account and a notification at 80% so you don't spend more than you want to. 
