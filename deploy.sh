pushd semantic
gulp build
popd

jekyll build

pushd _site
aws s3 sync . s3://www.fanz.io
popd
