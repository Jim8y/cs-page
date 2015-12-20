pushd semantic
gulp build
popd

jekyll build

pushd _site
aws s3 sync . s3://fanz.io --region us-west-2
popd
