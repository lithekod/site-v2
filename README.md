# LiTHe kod's website

## Quickstart

```sh
git clone git@github.com:lithekod/site-v2.git
cd site-v2
make
```

This will clone the repo, `cd` into it, install dependencies in a virtual
environment and start a local server.

## Adding new pages

Add new markdown files to `website/pages/` representing a swedish and english
version of the page. Then add the endpoints to `website/__init__.py`.
