After an uplift to a new Thunderbird version, this script allows to
update the Postbox translation with the Thunderbird translations.

l10nmerge.py takes 5 parameters, of which 1 is optional:
* `--srcdir` This is the Postbox srcdir, checkout out to tb-merge-result-3
* `--tb52` This is a directory containing the Thunderbird 52 locales, cloned from https://hg.mozilla.org/releases/l10n/mozilla-release/$locale (one for each locale)
* `--postbox` This is the directory containing the Postbox 5 locales
* `--output` This is where you want the files to go (don't use the --postbox directory because you won't know which files were deleted)
* `--locales` If you only want to merge specific locale(s)

If you want to then push the resulting output, the easiest approach is as follows:
1. Clone Postbox's localisations from GitHub
2. Clone the localisations again locally. This becomes your
   `--postbox` argument
3. In the original clone, delete all of the localisations. This becomes your
   `--output` argument

Algorithm used by the script:
1. Iterate over all strings in Postbox 7. For each:
2. Iterate over all languages. For each:
3. If you find a corresponding string in Postbox 5 translations, use that.
4. Else, if you find a corresponding string in Thunderbird 52 translations, use that.
5. Else, use the Postbox 7 string in English.
