# Hughes Clearing Co. website

Rebuild of hughesclearing.com from the Wayback Machine captures (Dec 2023 home page, original stylesheet).

## Structure
- `index.html` – home page
- `about-us/`, `contact-us/` – inner pages
- `css/site.css` – shared styles (colors, fonts and sizes from the original site)
- `images/` – photos and logos (original filenames are picked up automatically when added)
- `_build/pages.py` – regenerates inner pages from the home page's header and footer:
  `python3 _build/pages.py`

## Images still needed
logo.png, logo-icon.png, hero-bg-new.jpg, video.mp4, icon1.png, icon2.png, icon3.png, icon5.png,
carpentry-new.jpg, electrical.jpg, mask.jpg, serving-bg.jpg, pageheader.jpg, about-guarantee.jpg

## Contact form
Set `data-endpoint` on the form in `contact-us/` (via `_build/pages.py`) to a form service URL
such as Formspree. Without it, Submit opens the visitor's email app addressed to Info@HughesClearing.com.
