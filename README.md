PyProtector is a Python obfuscator. PyProtector allows you to protect your python codes !
Using PyProtector you can :
- [x] Invert the boolean values
- [x] Obfuscate numbers
- [x] Hide strings
- [x] Change the variable names
- [x] Change the importation names
- [x] Change function names
- [x] Put the script in bytecode
- [x] Protect the script from bytecode decoders. If you use this option, then you just have to give out the pyc file. The pyc file generated by PyProtector is protected from some of bytecode decoders (e.g. uncompyle2, uncompyle, easy python decompiler).

PyProtector use special **templates** to generate the obfuscated script.
To convert your python file to a template file, not a lot of work is needed !
To do it very quickly, you can use an IDE and use the refactoring to change the variables, function, importation names.
Example script:

`from sys import exit`<br />
`def foo(i):`<br />
- `x = 12`<br />
- `return (i+x)`<br />

`a=foo(3.2)`<br />
`if (__name__=="__main__")==True:`<br />
- `print("a : "+a)`<br />
- `exit(0)`<br />
  
Converted to template format :

`from sys import exit as IMP001`<br />
`def FUNC001(LOC001):`<br />
- `LOC002=[NBR]12[NBR]`<br />
- `return (LOC001+LOC002)`<br />

`VAR001=foo([NBR]3.2[NBR])`<br />
`if (__name__=="__main__")==True:`<br />
- `print("a : "+VAR001)`<br />
- `IMP001(0)**`<br />
  
