import requests
import csv
import json


def search_records(prefix):
    """
    Search for records with related identifiers containing specific DOI prefix
    Using range search syntax based on documentation
    """
    base_url = "https://authors.library.caltech.edu/api/records"

    # Try range-based search for DOI prefix
    # This will search for DOIs between prefix/0 and prefix/z to catch all possibilities
    query = f'?q=metadata.related_identifiers.identifier:["{prefix}/0" TO "{prefix}/z"]&size=1000'
    url = base_url + query

    print(f"Trying search URL: {url}")

    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error: Failed to fetch records. Status code: {response.status_code}")
        return None

    try:
        results = response.json()
        print(f"Found {results['hits']['total']} records")
        return results
    except json.JSONDecodeError:
        print("Error: Failed to parse JSON response")
        return None


def extract_data_citations(hits):
    """
    Extract CaltechAUTHORS ID and related DOIs from the search results
    """
    citations = []

    for hit in hits:
        record_id = hit["id"]
        related_dois = []

        if "metadata" in hit and "related_identifiers" in hit["metadata"]:
            for identifier in hit["metadata"]["related_identifiers"]:
                if "identifier" in identifier and "scheme" in identifier:
                    if identifier["scheme"] == "doi":
                        doi = identifier["identifier"]
                        if any(
                            doi.startswith(prefix)
                            for prefix in ["10.22002/", "10.14291/", "10.25989/"]
                        ):
                            related_dois.append(doi)

        if related_dois:
            citations.append({"record_id": record_id, "related_dois": related_dois})

    return citations


def main():
    # List of DOI prefixes to search for
    prefixes = ["10.22002", "10.14291", "10.25989"]
    all_citations = []

    # Search for each prefix
    for prefix in prefixes:
        print(f"\nSearching for records with DOI prefix: {prefix}")
        results = search_records(prefix)

        if results and "hits" in results:
            citations = extract_data_citations(results["hits"]["hits"])
            all_citations.extend(citations)
            print(f"Found {len(citations)} records with {prefix} DOIs")

    # Save results to CSV
    output_file = "data_citations.csv"
    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["CaltechAUTHORS_ID", "Related_DOIs"])

        for citation in all_citations:
            writer.writerow(
                [citation["record_id"], "; ".join(citation["related_dois"])]
            )

    print(f"\nResults saved to {output_file}")
    print(f"Total records found: {len(all_citations)}")


if __name__ == "__main__":
    main()
