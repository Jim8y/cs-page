pushd semantic
gulp build
popd

python main.py
rsync -avh --delete output/ fanz@lion.cs.cornell.edu:/home/WIN/fanz/MyWeb/
