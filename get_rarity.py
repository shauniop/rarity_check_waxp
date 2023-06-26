import requests

def get_rarest_attributes(collection_name, template_id):
    # collection_name = "your_collection_name"  # Replace with the actual collection name
    page = 1
    limit = 100
    attributes = {}

    while True:
        url = f"https://wax.api.atomicassets.io/atomicassets/v1/assets?collection_name={collection_name}&template_id={template_id}&page={page}&limit={limit}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()["data"]
            if not data:
                break

            for item in data:
                asset_data = item["immutable_data"]
                for key, value in asset_data.items():
                    if key in ["img", "name"]:
                        continue
                    if value in attributes:
                        attributes[value] += 1
                    else:
                        attributes[value] = 1

            page += 1
        else:
            print(f"Failed to retrieve assets. Status code: {response.status_code}")
            return []

    # Sort attribute counts in ascending order
    sorted_attributes = sorted(attributes.items(), key=lambda x: x[1])

    # Get the top 10 rarest attribute values
    rarest_attributes = sorted_attributes[:500]

    return rarest_attributes


# Specify the NFT template ID and collection name
template_id, collection_name = input("Enter template_id and collection_name seperated by a space:\n").split()

# madman example
# input --> 669571 tiltandshift
# template_id = "669571"
# collection_name = "tiltandshift"

# Retrieve the top 10 rarest attribute values
rarest_attributes = get_rarest_attributes(collection_name, template_id)

# Print the results
if rarest_attributes:
    print("\nTop 10 Rarest Attribute Values:")
    for attribute, count in rarest_attributes:
        print(attribute, "Count:", count)
else:
    print("No data found.")
