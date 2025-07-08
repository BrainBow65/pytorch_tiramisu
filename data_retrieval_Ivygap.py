from pathlib import Path
import requests

# Set up the base URL for the API
BASE_URL = "http://api.brain-map.org/api/v2/data/query.json"

SAVE_DIR = Path("Ivy_gap_dataset")
SAVE_DIR_HE = SAVE_DIR / "H&Es"
SAVE_DIR_ANNOTATED = SAVE_DIR / "Annotated"
SAVE_DIR_HE.mkdir(parents=True, exist_ok=True)
SAVE_DIR_ANNOTATED.mkdir(parents=True, exist_ok=True)


def fetch_specimen_ids():
    """Fetch all specimen IDs from the 'Anatomic Structures ISH Survey'."""
    url = f"{BASE_URL}?criteria=model::Specimen,rma::criteria,specimen_types[name$eq'Anatomic Structures ISH Survey'],rma::options[num_rows$eqall]"
    response = requests.get(url)
    data = response.json()
    return [specimen["external_specimen_name"] for specimen in data["msg"]]


def fetch_section_data_sets(specimen_id):
    """Fetch all ISH SectionDataSets for a given specimen."""
    url = f"{BASE_URL}?criteria=model::SectionDataSet,rma::criteria,specimen[external_specimen_name$eq'{specimen_id}'],treatments[name$eq'H%26E'],rma::include,sub_images"
    response = requests.get(url)
    data = response.json()
    return data["msg"]


def download_image(image_id, view_type, save_path):
    """Download a specific image."""
    if view_type is None:
        image_url = f"http://api.brain-map.org/api/v2/image_download/{image_id}"
    else:
        image_url = f"http://api.brain-map.org/api/v2/image_download/{image_id}?view={view_type}"

    response = requests.get(image_url)
    if response.status_code == 200:
        with open(save_path, "wb") as f:
            f.write(response.content)
        print(f"Downloaded {view_type} image to {save_path}")
    else:
        print(f"Failed to download {view_type} image for ID {image_id}")


def main():
    """Main function to orchestrate the download process."""
    specimen_ids = fetch_specimen_ids()
    for specimen_id in specimen_ids:
        section_data_sets = fetch_section_data_sets(specimen_id)
        for section in section_data_sets:
            for sub_image in section.get("sub_images", []):
                image_id = sub_image["id"]
                # Download H&E image
                download_image(
                    image_id,
                    None,
                    SAVE_DIR_HE / f"{specimen_id}_HE_{image_id}.jpg",
                )
                # Download TumorFeatureAnnotation image
                download_image(
                    image_id,
                    "tumor_feature_annotation",
                    SAVE_DIR_ANNOTATED / f"{specimen_id}_TFA_{image_id}.jpg",
                )


if __name__ == "__main__":
    main()
