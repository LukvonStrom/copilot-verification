# copilot-verification


## ARM based Macs
For ARM based Macs, intel emulation via rosetta needs to be used, as microsoft provides only `z3-solver` binaries for macos arm, but not for linux arm via pip.
Building Z3 from source is quite expensive, therefore emulation can be used like this (given that you manage docker via colima https://github.com/abiosoft/colima and have rosetta installed already https://support.apple.com/en-gb/102527):
`colima start --profile amd64 -a x86_64 -c 4 -m 6`

## Changed Copilot System Prompt for shorter files

```
{"role": "user", "content": "I have the following code in the selection:\n```python\n# FILEPATH: /Users/lukasfruntke/Postman/test.py\n# BEGIN: ed8c6549bwf9\nimport os\nimport os\n\ncurrent_path = os.getcwd()\nprint(\"Current path:\", current_path)\n# END: ed8c6549bwf9\n```"}, 
```

```
Only change the code inside of the selection, delimited by markers '# BEGIN: ed8c6549bwf9' and '# END: ed8c6549bwf9'. The code block with the suggested changes should also contain the markers.
```