pushd semantic
gulp build
popd

jekyll b
rsync -avh --delete output/ fanz@lion.cs.cornell.edu:/home/WIN/fanz/MyWeb/
