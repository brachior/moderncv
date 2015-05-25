# ModernCV: TeX to HTML

Convert a ModernCV file written with LaTeX to a HTML file.

## Usage

```sh
python3 tex2html.py moderncv.tex > moderncv.html
```

To put your CV on your website, you need the *moderncv* directory (the *fonts*
directory and the *classic-xxx.min.css* file).

## Known issues

### Information missing

Information containing a brand icon (Github, LinkedIn, Twitter, ...) can be
masked be Adblock. To display this information, disable the *Fanboy's Social
Blocking List* option in Adblock preferences.

### Environment and arguments parsing

Currently, marcro's arguments and environments are not parsing yet.

## Contributing

### CSS

The CSS can be improve (for example the picture is not at the good position).  
The file *moderncv.json* can be opened at [IcoMoon](https://icomoon.io/app/).  
You can compress the CSS files using the *compress_css.py* script:

```sh
python3 compress_css.py moderncv/classic-blue.css
```

### Parser

It is a first draft :).  

The class *ModernCV* is divide in 3 parts:

  * *style (ModernCVStyle)*: the html header
  * *head (ModernCVHead)*: the CV information (name, phone, ...)
  * *content (ModernCVContent)*: document content

Each part contains its macro definitions. The *ModernCV* uses a *TeXFactory* to
register macros (*TeXMacro*) and environments (in the future ;)).
