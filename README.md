# n0struct
list/OrderedDict extensions allow to 
* work with tree-like structures, generated for example by json.loads(..), using xpath approach 
* direct/wise compare lists/dictionaries/tree-like structures
* exclude from comparing subnodes
* transform on the fly values in attributes during comparing
* .to_json(): convert tree-like structure into string buffer for saving into JSON file
* .to_xml(): convert tree-like structure into string buffer for saving into XML file
* .to_xpath: convert tree-like structure into string buffer for saving into XPATH file
