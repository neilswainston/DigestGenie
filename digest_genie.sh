pip install biopython
pip install pandas
pip install synbiochem-py

export PYTHONPATH=$PYTHONPATH:.

python \
	digest/digest_genie.py \
	https://ice.synbiochem.co.uk \
	ICE_USERNAME \
	ICE_PASSWORD \
	ice_ids.txt \
	1 \
	out \
	MlyI