from google_images_download import google_images_download

# conf_file = '../conf/get-images.json'

response = google_images_download.googleimagesdownload()
image_base_dir = "./images/"

image_types = [
    "training",
    "validation",
    "test"
]
image_counts = [
    1000,
    300,
    100
]
categories = [
    "flower",
    "sausage",
    "wolf"
    ]
similar = [
    
    ]

arguments={
    "format":           "jpg",
    "size":             "medium",
    #"limit":            100,
    #"output_directory": "./images/...",
}

for i in range(3):
    im_type = image_types[i]
    im_count = image_counts[i]

    print("Downloading images")
    arguments["limit"] = im_count
    arguments["output_directory"] = image_base_dir + im_type

    for i in range(len(categories)):
        arguments["keywords"] = categories[i]
        #arguments["similar_images"] = similar[i]
        response.download(arguments)

