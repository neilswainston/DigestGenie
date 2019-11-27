c:\Python\Scripts\pip install biopython
c:\Python\Scripts\pip install pandas
c:\Python\Scripts\pip install synbiochem-py

set PYTHONPATH=%PYTHONPATH%;.

python digest/digest_genie.py https://ice.synbiochem.co.uk ICE_USERNAME ICE_PASSWORD ice_ids.txt 1 out MlyI

pause