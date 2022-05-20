from pyunsplash import PyUnsplash


if __name__ == "__main__":
    UNSPLASH_ACCESS_KEY = "WGbhFDWhRv2SIa_dKXGq2HZo4-WPztJzdtku1lxgZ4Y"
    pu = PyUnsplash(api_key=UNSPLASH_ACCESS_KEY)
    photos = pu.photos(type_='random', count=5, featured=True, query="splash")
    for photo in photos.entries:
        print(photo.id, photo.link_download)
