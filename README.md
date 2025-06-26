# Solidity Auditor Report Tool

This is a simple Python script that automates the generation of code metric reports for smart contracts using [solidity-code-metrics](https://github.com/ConsenSysDiligence/solidity-metrics) and outputs them in Org-mode format.

## Features

- Runs `solidity-code-metrics` on all `.sol` files in a directory 
- Cleans markdown output into readable Org-mode format

## Requirements

- Python 3.8 or higher
- Node.js (for `solidity-code-metrics`)

## Installation and Use

1. Install the required tools:

```bash
npm install -g solidity-code-metrics
```

2. Move audit.py and auditor_parser.py to the src dir 

3. Run in the src folder 

``` python
audit.py 
```

4. Output will be audit.org 
