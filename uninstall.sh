echo "Enter the region you want to uninstall in: "
read region
echo "Enter the profile you want to use (Press enter if not needed):  "
read profile
if [ -n "${profile}" ]; then 
    sam delete --stack-name syso-auto-shutdown-instances-stack --region $region --profile $profile
else
    sam delete --stack-name syso-auto-shutdown-instances-stack --region $region 
fi