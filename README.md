# EngineeringThings PySpice

A small series of tutorials and examples using pyspice, delivered in the youtube series on my [EnginneringThings channel](https://www.youtube.com/channel/UCrDM7plhff2fMSIIycZmw_Q).

## Structure

The raw script files used in earlier tutorial vidoes can be found in `scripts/`.

Better and more intuative notebooks can be found in the top level of the repository.

Finally, custom helper functions can be found in `utils/`.


## Enviroment

This repository is using Window for Subsytem Linux (WSL) on ubuntu, using conda.

The conda enviroment can be found and installed from `conda_env.yml`.

For this to work NGSpice is required.
This is installed by defualt on many versions of linux, but might require some manual instilation on windows.


## Misc

### Notebook Outputs

Notebook outputs are ommitted from this repository using thr `nbstripout` package.
To get the results, download and run yourself!

#### Preventing Commiting of Notebook Outputs

To prevent outputs from being included when files are added to be git commited, install `nbstripout` using
```
nbstripout --install
```


To stop this, just run:
```
nbstripout --uninstall
```