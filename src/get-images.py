from google_images_download import google_images_download

# conf_file = '../conf/get-images.json'

response = google_images_download.googleimagesdownload()

categories = [
    #"poodle",
    #"pizza",
    "plane"
    ]

similar = [
    #"https://s3.amazonaws.com/playbarkrun/wp-content/uploads/2018/05/28100132/best-poodle-clippers1.jpg",
    #"https://img.koket.se/media/pizza-med-rodlok-och-bacon.jpg",
    "http://www.slate.com/content/dam/slate/articles/health_and_science/explainer/2012/06/120614_EX_Airplane.jpg.CROP.rectangle3-large.jpg"
    ]

arguments={
    "limit":            100,
    "format":           "jpg",
    "size":             "medium",
    #"output_directory": "./images/training",
    "output_directory": "./images/validation",
}

if (arguments["limit"]>100):
    raise ValueError('the argument "limit" must not be greater than 100') 

for i in range(len(categories)):
    arguments["keywords"] = categories[i]
    arguments["similar_images"] = similar[i]

    response.download(arguments)
