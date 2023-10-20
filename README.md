# Economic diversity and labour specialization in the Latin-speaking Roman Empire

## About
[_In two to three sentences state the purpose of this repository, e.g., The purpose of this repository is to provide templates for all future PSN repositories in order to save precious time and maintain high standards and uniformity of our documentation._]

## Authors 

* Petra Hermankova [![](https://orcid.org/sites/default/files/images/orcid_16x16.png)](https://orcid.org/0000-0002-6349-0540), PSN, Aarhus University
* Matteo Mazzamurro [![](https://orcid.org/sites/default/files/images/orcid_16x16.png)](https://orcid.org/0009-0004-4454-1551), PSN, Aarhus University
* Tom Brughmans [![](https://orcid.org/sites/default/files/images/orcid_16x16.png)](https://orcid.org/0000-0002-1589-7768), PSN, Aarhus University
* Vojtech Kase [![](https://orcid.org/sites/default/files/images/orcid_16x16.png)](https://orcid.org/0000-0002-6601-1605), SDAM project, kase@kfi.zcu.cz
* Adela Sobotkova [![](https://orcid.org/sites/default/files/images/orcid_16x16.png)](https://orcid.org/0000-0002-4541-3963), SDAM project, adela@cas.au.dk
* [Name], [ORCID], [Institution]

## Funding
*The Past Social Networks Projects* is funded by The Carlsberg Foundation’s Young Researcher Fellowship (CF21-0382) in 2022-2026.

## License
CC-BY-SA 4.0, see attached [License.md](./License.md)

## Data
[_Describe the provenance of data used in the scripts contained and clarify how it is harvested and what other prerequisites are required to get the scripts working. In case of pure tool attribute any reused scripts to source, etc., license and specify any prerequisites or technical requirements. Provide information on data metadata and data used. Provide a link to a data repository or explanatory article._] 


1. The **Latin Inscriptions in Space and Time** (LIST) 
- aggregate of the Epigraphic Database Heidelberg (https://edh.ub.uni-heidelberg.de/); aggregated EDH on Zenodo and Epigraphic Database Clauss Slaby (http://www.manfredclauss.de/); aggregated EDCS on Zenodo epigraphic datasets created by the Social Dynamics in the Ancient Mediterranean Project (SDAM), 2019-2023, funded by the Aarhus University Forskningsfond Starting grant no. AUFF-E-2018-7-2. 
- consists of 525,870 inscriptions, enriched by 65 attributes. 77,091 inscriptions are overlapping between the two source datasets (i.e. EDH and EDCS); 3,316 inscriptions are exclusively from EDH; 445,463 inscriptions are exclusively from EDCS. 511,973 inscriptions have valid geospatial coordinates (the geometry attribute). This information is also used to determine the urban context of each inscription (i.e. whether it is in the neighbourhood (i.e. within a 5000m buffer) of a large city, medium city, or small city or rural (>5000m to any type of city; see the attributes urban_context, urban_context_city, and urban_context_pop). 206,570 inscriptions have a numerical date of origin expressed using an interval or singular year using the attributes not_before and not_after. The dataset also employs a machine learning model to classify the inscriptions covered exclusively by EDCS in terms of 22 categories employed by EDH, see Kaše, Heřmánková, Sobotkova 2021.
- Citation: `Vojtěch Kaše, Petra Heřmánková, & Adéla Sobotková. (2023). LIST (v1.0) [Data set]. Zenodo. https://doi.org/10.5281/zenodo.8431323`


## Scripts
[_Describe what individual scripts do, provide links to them, and order them in a sequence they should run. Point to any issues or specific settings people should be aware of._]

1. Scripts in the folder `data-generation` were originally published by `Kaše V, Heřmánková P, Sobotková A (2022) Division of labor, specialization and diversity in the ancient Roman cities: A quantitative approach to Latin epigraphy. PLoS ONE 17(6): e0269869. https://doi.org/10.1371/journal.pone.0269869` under a CC BY-SA 4.0 International License. https://github.com/sdam-au/social_diversity

2. Scripts in the folder `networks`:

- 1_OCCUPATIONAL-NETWORKS - published by `Kaše V, Heřmánková P, Sobotková A (2022) Division of labor, specialization and diversity in the ancient Roman cities: A quantitative approach to Latin epigraphy. PLoS ONE 17(6): e0269869. https://doi.org/10.1371/journal.pone.0269869` under a CC BY-SA 4.0 International License. https://github.com/sdam-au/social_diversity



## Screenshots
![Example screenshot](./img/screenshot.png)


## DOI
TBA

## How to cite us
TBA

---

<img src="./img/Main_banner.png" alt="Logo banner" >


