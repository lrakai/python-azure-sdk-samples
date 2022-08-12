#!/usr/bin/env bash
set -xe

BITBUCKET_USER=lrakai
VCF_BITBUCKET_CLONE_URL=https://$BITBUCKET_USER@bitbucket.org/cloudacademy/labs-vcf-boilerplates.git
VCF_BITBUCKET_PATH=..
VCF_BITBUCKET_DIR=$VCF_BITBUCKET_PATH/labs-vcf-boilerplates
CLOUD=azure # valid values=aws|azure|gcp
REQUIREMENTS=$VCF_BITBUCKET_DIR/deploy/lambdas/python3.8-$CLOUD/requirements.txt

if [ ! -d "$VCF_BITBUCKET_DIR" ] ; then
    git config credential.helper store # store bitbucket credential on disk
    git clone $VCF_BITBUCKET_CLONE_URL $VCF_BITBUCKET_DIR
else
    git -C $VCF_BITBUCKET_DIR pull origin master
fi

cp $REQUIREMENTS requirements.txt

rm -rf venv # clean start

python3 -m venv venv
source ./venv/bin/activate
pip install --upgrade pip
pip install pylint autopep8 # dev dependencies
pip install -r requirements.txt # prod dependencies

# Trim Azure mgmt packages included api versions
keep_api_versions=1
mgmt_client_dir=venv/lib/python*/site-packages/azure/mgmt
skip_clients=( "eventhub", "monitor", "keyvault") # skip clients requiring more than latest version of the API
for client_dir in $mgmt_client_dir/*; do
    if [[ " ${skip_clients[*]} " =~ " $(basename ${client_dir}) " ]]; then
        continue
    fi
    old_IFS=$IFS; IFS=$'\n'
    api_dirs=($(find $client_dir -maxdepth 1 -type d -regex "$client_dir/v[0-9][0-9][0-9][0-9].*" | sort))
    unset IFS; IFS=$old_IFS
    if [[ ${#api_dirs[@]} -le $keep_api_versions ]]; then
        continue
    fi
    for i in $(seq 0 1 $(( ${#api_dirs[@]} - $(( $keep_api_versions + 1 )) )) ); do
        rm -rf ${api_dirs[i]}
    done
done