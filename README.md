# Economic complexity of the Roman Empire

## About
_Project exploring the economic complexity of the Roman Empire on the basis of mentions of occupations on Latin inscriptions._

## Authors 

* Matteo Mazzamurro [![](https://orcid.org/sites/default/files/images/orcid_16x16.png)](https://orcid.org/0009-0004-4454-1551), PSNP, Aarhus University
* Petra Hermankova [![](https://orcid.org/sites/default/files/images/orcid_16x16.png)](https://orcid.org/0000-0002-6349-0540), PSNP, Aarhus University
* Michele Coscia [![](https://orcid.org/sites/default/files/images/orcid_16x16.png)](https://orcid.org/0000-0001-5984-5137), IT University of Copenhagen
* Tom Brughmans [![](https://orcid.org/sites/default/files/images/orcid_16x16.png)](https://orcid.org/0000-0002-1589-7768), PSNP, Aarhus University

## Funding
*The Past Social Networks Projects* is funded by The Carlsberg Foundation’s Young Researcher Fellowship (CF21-0382) in 2022-2026.

## License
CC-BY-SA 4.0, see attached [License.md](./License.md)

## Data

1. The **Latin Inscriptions in Space and Time** (LIST) 
- aggregate of the Epigraphic Database Heidelberg (https://edh.ub.uni-heidelberg.de/); aggregated EDH on Zenodo and Epigraphic Database Clauss Slaby (http://www.manfredclauss.de/); aggregated EDCS on Zenodo epigraphic datasets created by the Social Dynamics in the Ancient Mediterranean Project (SDAM), 2019-2023, funded by the Aarhus University Forskningsfond Starting grant no. AUFF-E-2018-7-2. 
- consists of 525,870 inscriptions, enriched by 65 attributes. 77,091 inscriptions are overlapping between the two source datasets (i.e. EDH and EDCS); 3,316 inscriptions are exclusively from EDH; 445,463 inscriptions are exclusively from EDCS. 511,973 inscriptions have valid geospatial coordinates (the geometry attribute). 206,570 inscriptions have a numerical date of origin expressed using an interval or singular year using the attributes not_before and not_after. The dataset also employs a machine learning model to classify the inscriptions covered exclusively by EDCS in terms of 22 categories employed by EDH, see Kaše, Heřmánková, Sobotkova 2021.
- Citation: `Kaše, V., Heřmánková, P., & Sobotková, A. (2023). LIST (v1.0) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.8431323` and `Kaše, V., Heřmánková, P., & Sobotková, A. (2024). LIST (v1.2) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.10473706`

2. Geographic units data to compute economic complexity
- Modern countries: download from https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/world-administrative-boundaries/exports/shp
- Roman provinces: shapefile created by Adam Pažout on the basis of [TBD]
- Pleaides regions: https://raw.githubusercontent.com/pelagios/magis-pleiades-regions/main/pleiades-regions-magis-pelagios.geojson

3. Dataset of ancient cities
- `Hanson J. W., An urban geography of the Roman world, 100 BC to AD 300. Oxford: Archaeopress; 2016. http://oxrep.classics.ox.ac.uk/oxrep/docs/Hanson2016/Hanson2016_Cities_OxREP.csv`
- `Hanson J. W, Ortman S. G., A systematic method for estimating the populations of Greek and Roman settlements. J Roman Archaeol. 2017;30: 301–324.`

4. Dataset of occupations
Compiled by Petra Heřmánková in 2022, based on:
- `Waltzing JP. Étude historique sur les corporations professionnelles chez les Romains depuis les origines jusqu’à la chute de l’Empire d’Occident. Louvain: C. Peeters; 1895.`
- `Petrikovits H v. Die Spezialisierung des römischen Handwerks. Handw Vor- Frühgesch Zeit 1 Hist Rechtshistorische Beitr Untersuchungen Zur Frühgesch Gilde Ber Über Kolloquien Komm Für Altertumskunde Mittel- Nordeur Den Jahren 1977 Bis 1980. 1981; 63–132.`
- `Harris EM. Workshop, Marketplace and Household: The Nature of Technical Specialization in Classical Athens and its Influence on Economy and Society. In: Carledge P, Cohen EE, Foxhall L, editors. Money, Labour and Land: Approaches to the Economy of Ancient Greece. London—New York: Routledge; 2001. pp. 67–99.`
- `van Leeuwen MHD, Maas I, Miles A. HISCO: Historical International Standard Classification of Occupations. 2022 2002 [cited 27 Jan 2022]. Available: https://historyofwork.iisg.nl/`

5. Supplementary epigraphic dataset:  The **Greek Inscriptions in Space and Time** (GIST) 
- represents a comprehensive collection of ancient Greek inscriptions, enriched by temporal and spatial metadata. The dataset was created by the **Social Dynamics in the Ancient Mediterranean Project** (SDAM), 2019-2023, funded by the Aarhus University Forskningsfond Starting grant no. AUFF-E-2018-7-2. 
- mainly based on Greek inscriptions from the dataset of Searchable Greek Inscriptions [PHI](https://inscriptions.packhum.org/) and I.PHI dataset published by the Pythia Project `Sommerschield, T., Assael, Y., Shillingford, B., Bordbar, M., Pavlopoulos, J., Chatzipanagiotou, M., Androutsopoulos, I., Prag, J., & de Freitas, N. (2021). I.PHI dataset: Ancient Greek inscriptions. https://github.com/sommerschield/iphi.` The individual inscriptions have been cleaned, preprocessed and enriched with additional data, such as date in a numeric format and geolocation.
- The GIST dataset consists of 217,863 inscriptions, enriched by 36 attributes.
- Citation: `Kaše, V., Heřmánková, P., & Sobotková, A. (2023). GIST (v1.1) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.10139110`

6. Modern trade data [tba]

## Scripts

1. Python scripts in the folder `data-generation` were originally published by `Kaše V, Heřmánková P, Sobotková A (2022) Division of labor, specialization and diversity in the ancient Roman cities: A quantitative approach to Latin epigraphy. PLoS ONE 17(6): e0269869. https://doi.org/10.1371/journal.pone.0269869` under a CC BY-SA 4.0 International License. https://github.com/sdam-au/social_diversity and adjusted to the new data and purpose of the current project by Petra Heřmánková.

- Scripts are numbered in the order they should be run, starting from 1 to 4.
- Use version of the epigraphic dataset `LIST 1.0`.

2. Scripts in the folder `economic_complexity`: R scripts were generated by Matteo Mazzamurro to adjust the biases of epigraphic data and to compute economic complexity index on the basis of available epigraphic data.

3. Scripts in the folder `paper_figures`: Python scripts were generated by Michele Coscia to compute economic complexity index on the basis of available epigraphic data.

- Scripts are numbered in the strict order they should be run, starting from 1 to 8. The scripts `backboning.py` and `network_distance.py` contain custom libraries that are there for supporting the actual scripts and they should not be run on their own.  
- NOTE: The scripts don't generate the figures per se, but the data files that are necessary to render the figures. These files will be put in the same script folder and some scripts depend on the outputs of previous scripts to run properly.
- Use version of the epigraphic dataset `LIST 1.2` (contains the same number of inscriptions as `LIST 1.0`).
- Script `06_tab_1.py` uses 6.5GB of trade data accessible from other location, indicated in the script. The data needs to be manually downloaded for the script to run.





