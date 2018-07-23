from google_images_download import google_images_download

# conf_file = '../conf/get-images.json'

response = google_images_download.googleimagesdownload()
categories = ["poodle", "pizza"]
arguments={
    "limit": 100,
    "size":"medium",
    "output_directory": "./images"
}

if (arguments["limit"]>100):
    raise ValueError('the argument "limit" must not be greater than 100') 

for category in categories:
    arguments["keywords"] = category
    response.download(arguments)
