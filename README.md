# Characterizing DIA objects in Rubin alerts using the ALeRCE broker and LINCC Frameworks LSDB

[Open Tools, Open Sky: Doing LSST Science with Public Rubin Data & LINCC Frameworks, A LATAM Hack Days Workshop](https://plazasmalagon.com/lsst-science-public-rubin-data-products-hackathon-UdeA-2026/), Team 1 Repository

## Resources

### Software tools and libraries

We work with LSST alerts using primarily the [ALeRCE broker](https://science.alerce.online) and LINCC Frameworks' [LSDB](https://docs.lsdb.io/en/stable/) via python (version >=3.11). It's strongly recommended to use a virtual environment, see e.g. the installation hint at https://docs.lsdb.io/en/stable/getting-started.html.

#### Required libraries for this project

- numpy
- pandas
- matplotlib
- astropy
- [alerce client](https://alerce.readthedocs.io/en/latest/)
- [pyvo](https://pyvo.readthedocs.io/en/latest/) to run Astronomical Data Query Language ([ADQL](https://www.ivoa.net/documents/ADQL/)) queries using Table Access Protocol ([TAP](https://www.ivoa.net/documents/TAP/))
- [lsdb](https://docs.lsdb.io/en/stable/)

All of them can be installed using [pip](https://pypi.org/project/pip/).

#### Suggested additional software (recommended)

[Topcat](https://www.star.bris.ac.uk/~mbt/topcat/) and [Aladin](https://aladin.cds.unistra.fr/AladinDesktop/) for visualization/manipulation/querying of data tables and astronomical images. They provide installers in their websites but require java to run.

### Reading material and tutorials

#### Event website, resources section

- https://plazasmalagon.com/lsst-science-public-rubin-data-products-hackathon-UdeA-2026/#resources

#### Overview of Rubin

- https://rubinobservatory.org/about
- https://rubinobservatory.org/for-scientists/get-started
- https://rubinobservatory.org/explore/how-rubin-works/alerts
- https://rubinobservatory.org/for-scientists/data-products/alerts-and-brokers
- https://survey-strategy.lsst.io/baseline/ddf.html

#### ALeRCE

- https://science.alerce.online/alerce-lsst/
- https://github.com/alercebroker/usecases/blob/master/notebooks/LSST/ALeRCE_LSST_Tables.ipynb and https://github.com/alercebroker/usecases/blob/master/notebooks/LSST/ALeRCE_LSST_TAP_Queries.ipynb: jupyter notebooks as part of our ALeRCE LSST set. Note that these can run in [Google Colab](https://colab.research.google.com/) using the links included in each notebook introduction. To run them locally you must clone the repository as described in https://github.com/alercebroker/usecases.

#### LSDB

- https://docs.lsdb.io/en/latest/
- https://docs.lsdb.io/en/latest/getting-started.html
- https://docs.lsdb.io/en/latest/data-access/datalsdb.html
- https://docs.lsdb.io/en/latest/tutorials.html
