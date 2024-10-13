# all plot combinations

python plot_xsecs_from_json.py --sqrt 13 --xmin 100 --xmax 3000
python plot_xsecs_from_json.py --sqrt 13 --gluino  --xmin 500 --xmax 3000
python plot_xsecs_from_json.py --sqrt 13 --squark  --xmin 100 --xmax 3000
python plot_xsecs_from_json.py --sqrt 13 --squark  --xmin 100 --xmax 3000 --debug
python plot_xsecs_from_json.py --sqrt 13 --slepton --xmin 1 --xmax 1500 
python plot_xsecs_from_json.py --sqrt 13 --stau    --xmin 1 --xmax 1000

python plot_xsecs_from_json.py --sqrt 13.6 --xmin 100 --xmax 3000
python plot_xsecs_from_json.py --sqrt 13.6 --gluino  --xmin 500 --xmax 3000
python plot_xsecs_from_json.py --sqrt 13.6 --squark  --xmin 100 --xmax 3000
python plot_xsecs_from_json.py --sqrt 13.6 --slepton --xmin 1 --xmax 1500
python plot_xsecs_from_json.py --sqrt 13.6 --slepton --xmin 1 --xmax 1500 --debug
python plot_xsecs_from_json.py --sqrt 13.6 --stau    --xmin 1 --xmax 1000

# plots for a given lumi
lumi=$(echo "36.71+28.09" | bc); 
lumi=${lumi%.*}
python plot_xsecs_from_json.py --sqrt 13 --lumi $lumi --xmin 100 --xmax 3000
python plot_xsecs_from_json.py --sqrt 13 --gluino --lumi $lumi --xmin 500 --xmax 3000
python plot_xsecs_from_json.py --sqrt 13 --squark --lumi $lumi --xmin 100 --xmax 3000
python plot_xsecs_from_json.py --sqrt 13 --squark --lumi $lumi --xmin 100 --xmax 3000 
python plot_xsecs_from_json.py --sqrt 13 --slepton --lumi $lumi --xmin 1 --xmax 1500
python plot_xsecs_from_json.py --sqrt 13 --stau --lumi $lumi --xmin 1 --xmax 1000

python plot_xsecs_from_json.py --sqrt 13.6 --lumi $lumi --xmin 100 --xmax 3000
python plot_xsecs_from_json.py --sqrt 13.6 --gluino --lumi $lumi --xmin 500 --xmax 3000
python plot_xsecs_from_json.py --sqrt 13.6 --squark --lumi $lumi --xmin 100 --xmax 3000
python plot_xsecs_from_json.py --sqrt 13.6 --squark --lumi $lumi --xmin 100 --xmax 3000 --limits
python plot_xsecs_from_json.py --sqrt 13.6 --slepton --lumi $lumi --xmin 1 --xmax 1500
python plot_xsecs_from_json.py --sqrt 13.6 --slepton --lumi $lumi --xmin 1 --xmax 1500 --limits
python plot_xsecs_from_json.py --sqrt 13.6 --stau --lumi $lumi --xmin 1 --xmax 1000