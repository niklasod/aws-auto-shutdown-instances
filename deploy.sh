
echo "Enter the region you want to install to: " ;read region
echo "Enter the profile you want to use: " ;read profile
sam build
sam package --resolve-s3 --region $region `if [ -n "${profile}" ]; then echo "--profile $profile"; fi` --save-params --output-template-file output.yml --template-file template.yml
sam deploy --stack-name syso-auto-shutdown-instances-stack --region $region --resolve-s3 `if [ -n "${profile}" ]; then echo "--profile $profile"; fi` --capabilities CAPABILITY_NAMED_IAM --template-file output.yml