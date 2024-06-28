python -m pydoc n0struct | perl -pE "s/<lambda> at 0x[0-9A-F]+>/<lambda>>/g" > n0struct.pydoc
