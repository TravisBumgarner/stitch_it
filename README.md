# Setup

1) Copy `.env.example` to `.env`
2) Generate `SECRET_KEY` for `.env` with `import os; os.urandom(24)`
3) Run `gcloud builds submit --tag gcr.io/stitch-it-311a5/stitchit`
4. Run `gcloud beta run deploy --image gcr.io/stitch-it-311a5/stitchit`

# To Do

- [x] Build flask server
- [x] Setup HTML Templates
- [x] Create form
- [x] Write a script to process photos
- [x] Integrate script into server
- [x] Pretty the UI
- [x] Fix UI bug with +- backwards
- [x] Resize incoming photos (Optional: Add checkbox options to UI instead of random values)
- [x] Add some friendly size notes
- [x] Form validation
- [x] Sort out all the awful CSS
- [x] Create copy to clipboard function
- [x] Prune dead code
- [x] Setup routing to save html pages to bucket
- [x] Create links you can share
- [x] Figure out how to handle settings between form and results pages
- [x] Protect against image attacks
- [x] Upload to GCP
- [x] Why are PNG photos blue
- [x] Improve quality / granularity of output css
- [x] Add some links on site (Created by ...)
- [x] Fix bug with 0 not being allowed in forms
- [ ] Productionalize
- [ ] Clean up repo
    - [ ] Figure out how to avoid hug of death
    - [x] Read Logan's articles
    - [x] Handle secret key
    - [x] Figure out CSRF
- [x] Fix bugs with uploading files from elsewhere
- [ ] ~~Add error page~~
- [ ] ~~Make it look like a stitching~~
- [x] ~~Handle grayscale photos~~ (Non issue?)
- [ ] ~~Fix stitch style buttons not working~~ (Non issue?)

# Research Resources

## Flask

https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms

## Fonts

https://fonts.google.com/?selection.family=Montserrat

## Flask File Uploads

https://www.javatpoint.com/flask-file-uploading
https://riptutorial.com/flask/example/19418/save-uploads-on-the-server

## Finding Interesting Colors

https://stackoverflow.com/questions/43111029/how-to-find-the-average-colour-of-an-image-in-python-with-opencv

## WTForms

https://flask-wtf.readthedocs.io/en/stable/quickstart.html
https://wtforms.readthedocs.io/

## Random Search Questions

Wrapping divs issue: https://stackoverflow.com/questions/14761119/how-to-stop-divs-from-wrapping
JavaScript and CSS Variables: https://css-tricks.com/updating-a-css-variable-with-javascript/
CSS Reset - https://meyerweb.com/eric/tools/css/reset/
Copying to clipboard - https://hackernoon.com/copying-text-to-clipboard-with-javascript-df4d4988697f
Validating Numbers - https://stackoverflow.com/questions/53048287/wtforms-not-validating-numberrange