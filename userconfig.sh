#!/bin/bash

username=<YOUR IAM USERNAME>
output_file=credentials.txt
export AWS_DEFAULT_OUTPUT=json

echo "CREATING IAM USER"
aws iam create-user --user-name $username || { echo "Error creating IAM user"; exit 1; }
aws iam create-group --group-name my-group || { echo "Error creating IAM group"; exit 1; }
aws iam add-user-to-group --user-name $username --group-name my-group || { echo "Error adding user to group"; exit 1; }
aws iam attach-user-policy --user-name $username --policy-arn arn:aws:iam::aws:policy/AdministratorAccess || { echo "Error attaching policy"; exit 1; }
echo "IAM USER CREATED SUCCESSFULLY!"

echo "CREATING ACCESS KEYS"
output=$(aws iam create-access-key --user-name $username) || { echo "Error creating access keys"; exit 1; }

access_key_id=$(echo "$output" | grep -o '"AccessKeyId": "[^"]*' | cut -d'"' -f4) 
secret_access_key=$(echo "$output" | grep -o '"SecretAccessKey": "[^"]*' | cut -d'"' -f4)
echo "ACCESS KEYS GENERATED SUCCESSFULLY!"

echo "Setting Up IAM Profile"
aws configure set --profile $username aws_access_key_id $access_key_id || { echo "Error setting access key"; exit 1; }
aws configure set --profile $username aws_secret_access_key $secret_access_key || { echo "Error setting secret key"; exit 1; }
aws configure set --profile $username region us-east-1 || { echo "Error setting region"; exit 1; }
aws configure set --profile $username output json || { echo "Error setting output format"; exit 1; }
echo "Setup successful!"

echo "STORING THE CREDENTIALS"
echo "$access_key_id" >> $output_file
echo "$secret_access_key" >> $output_file
echo "us-east-1" >> $output_file

python3 <yourdbscript>.py