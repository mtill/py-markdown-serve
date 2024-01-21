# py-markdown-serve

Tiny tool for serving a bunch of markdown files to a browser, parsing markdown files on-the-fly.

## requirements
- apt install python3-flask python3-markdown-it

## how to run
- gunicorn -w 2 -b localhost:5000 serve:app
- now, open http://localhost:5000/

## configuration
- by default, the current working directory is served. To change that behavior, one can set the MARKDOWN\_SERVE\_DIR environment variable before starting gunicorn.
- by default, dotfiles are hidden from file structure. Set environment variable MARKDOWN\_SERVE\_HIDE\_DOTFILES to 'False' to list them as well.

