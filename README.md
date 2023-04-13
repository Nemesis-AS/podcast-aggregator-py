# TODO


- [x] Add a page to 'Add Podcasts'
- [x] Add custom fields to podcasts for 
    - Last fetched
    - Downloaded count(eps)
- [x] Add Image Caching
- [x] Fetch podcast episodes whenever a new one is added
- [ ] Add a scheduler to fetch podcast episodes periodically
- [x] Add a settings page

- [ ] Figure out a directory Structure
    - Podcast Name
        - EP {ep_num} - {ep_title}.mp3
        - Cover.jpg
- [x] Figure out a DB Structure
    - Podcast Fields
        1. id(unique)
        2. title
        3. link(url)
        4. Description
        5. author
        6. image/artwork
        7. last updated
        8. iTunes ID
        9. lang
        10. explicit
        11. ep_count
        12. categories
    - Episode Fields
        1. id(unique)
        2. title
        3. link
        4. description
        5. date_published
        6. duration
        7. explicit
        8. episode
        9. season
        10. image
        11. language?
        12. Downloaded
        13. File_path


# BUGS


# Features

- [ ] Auto downloader
- [ ] File Management tool
- [ ] Write metadata as ID3 tags on podcast mp3s