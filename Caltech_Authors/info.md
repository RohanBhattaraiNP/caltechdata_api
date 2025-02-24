# **CaltechAuthors DOI Records Extraction & Its Query**

## **Overview**
The goal was to retrieve records from the CaltechAUTHORS API that contain related identifiers from **CaltechDATA**. These related identifiers are **DOIs** with the following prefixes: 
- `10.22002`
- `10.14291`
- `10.25989`

The extracted records were saved into a CSV file containing:
- **CaltechAUTHORS Identifier** (e.g., `6fqp8-y9536`)
- **Related DOIs** (e.g., `10.22002/aeffy-dcr62`, `10.22002/h88fq-dk449`, `10.22002/m4mpa-4mt17`)

## **Process**
1. **Understanding the API & Queries**  
   - I Studied the [CaltechAUTHORS API documentation](https://authors.library.caltech.edu/metadata_searching).  
   - and then Analyzed example code from [Caltech Library’s Ames harvester](https://github.com/caltechlibrary/ames/blob/main/ames/harvesters/caltechauthors.py). It helped me alot to understand the api calls. even the api documentation, i tried with different metadata queries but it always lookedup inside the metadata and not the field. Did alot of trial and error to get the right query. 

2. **Query**  
   - The search query used for each DOI prefix:  
     ```plaintext
     ?q=metadata.related_identifiers.identifier:["<DOI_PREFIX>/0" TO "<DOI_PREFIX>/z"]&size=1000
     ```
   - Example queries:
     ```
     https://authors.library.caltech.edu/api/records?q=metadata.related_identifiers.identifier:["10.22002/0" TO "10.22002/z"]&size=1000
     https://authors.library.caltech.edu/api/records?q=metadata.related_identifiers.identifier:["10.14291/0" TO "10.14291/z"]&size=1000
     https://authors.library.caltech.edu/api/records?q=metadata.related_identifiers.identifier:["10.25989/0" TO "10.25989/z"]&size=1000
     ```

3. **Data Extraction & Processing**  
   - Fetched records from the API for each DOI prefix.  
   - Extracted **CaltechAUTHORS identifiers** and **related DOIs**.  
   - Saved results into `data_citations.csv`.

## **Log Data**
```
Searching for records with DOI prefix: 10.22002
Trying search URL: https://authors.library.caltech.edu/api/records?q=metadata.related_identifiers.identifier:["10.22002/0" TO "10.22002/z"]&size=1000
Found 206 records
Found 206 records with 10.22002 DOIs

Searching for records with DOI prefix: 10.14291
Trying search URL: https://authors.library.caltech.edu/api/records?q=metadata.related_identifiers.identifier:["10.14291/0" TO "10.14291/z"]&size=1000
Found 5 records
Found 5 records with 10.14291 DOIs

Searching for records with DOI prefix: 10.25989
Trying search URL: https://authors.library.caltech.edu/api/records?q=metadata.related_identifiers.identifier:["10.25989/0" TO "10.25989/z"]&size=1000
Found 1 records
Found 1 records with 10.25989 DOIs

Results saved to data_citations.csv
Total records found: 212
```



