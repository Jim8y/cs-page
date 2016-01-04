pushd semantic
gulp build
popd

git add -u
git commit -m "Update at `date`"
git push 
