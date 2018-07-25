from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from google_images_download import google_images_download

# conf_file = '../conf/get-images.json'

_max_get = 100
_date_filter_months = 6
_image_base_dir = "./temp-images/"
_image_types = [
    "training",
    "validation",
    "test"
]
# _image_counts = [
#     1000,
#     300,
#     100
# ]
_image_counts = [
    10,
    10,
    10
]
_categories = [
    "flower",
    "sausage",
    "wolf"
    ]
_arguments={
    "format":           "jpg",
    "size":             "medium",
    "chromedriver":     "C:/Program Files/Chromedriver/chromedriver.exe"
    #"limit":            100,
    #"output_directory": "./images/...",
}

def get_images(
    categories,
    arguments=_arguments,
    image_types=_image_types,
    image_counts=_image_counts,
    image_base_dir=_image_base_dir):
    
    if (categories == None):
        raise ValueError("categories")
    if (arguments == None):
        raise ValueError("arguments")
    if (image_types == None):
        raise ValueError("image_types")
    if (image_counts == None):
        raise ValueError("image_counts")
    if (image_base_dir == None):
        raise ValueError("image_base_dir")
    if (len(image_types) != len(image_counts)):
        raise ValueError(f"len(image_types) must equal len(image_counts)")
    
    print(f"Starting to obtain images for {len(categories)} categories: {categories}...")
    downloader = google_images_download.googleimagesdownload()

    for i in range(len(image_types)):
        # assign image types
        im_type = image_types[i]
        im_count = image_counts[i]
        # reset date filter
        date_to = datetime.now()
        date_to = date_to - timedelta(days=date_to.day-1)
        date_from = date_to - relativedelta(months=_date_filter_months)

        print(f"Downloading {im_count} images for the {im_type}-set")
        arguments["limit"] = im_count
        arguments["output_directory"] = image_base_dir + im_type

        for i in range(len(categories)):
            arguments["keywords"] = categories[i]
            arguments["prefix"] = categories[i]
            #arguments["similar_images"] = similar[i]

            im_remaining = im_count
            while (im_remaining > 0):
                arguments["limit"] = min(im_remaining, _max_get)
                # arguments["time_range"] = get_date_range(date_from, date_to)
                downloader.download(arguments)

                # update image counter and date filter
                im_remaining = max(0, im_remaining-_max_get)
                date_to =   date_to - relativedelta(months=_date_filter_months)
                date_from = date_from - relativedelta(months=_date_filter_months)


def get_date_range_str(date_from: str, date_to: str):
    return f'{{"time_min": "{date_from}", "time_max": "{date_to}"}}'
        

def get_date_range(date_from: datetime, date_to: datetime):
    return get_date_range_str(date_from.strftime('%m/%d/%Y'), date_to.strftime('%m/%d/%Y'))


def remove_corrupt_images(categories, image_types=_image_types):
    print("Identifying and removing any corrupt images...")


get_images(_categories)
remove_corrupt_images(_categories)

