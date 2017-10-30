l10nmerge.py takes 5 parameters, of which 1 is optional:
--srcdir This is the Postbox srcdir, checkout out to tb-merge-result-3
--tb52 This is a directory containing the Thunderbird 52 locales, cloned from https://hg.mozilla.org/releases/l10n/mozilla-release/$locale (one for each locale)
--postbox This is the directory containing the Postbox 5 locales
--output This is where you want the files to go (don't use the --postbox directory because you won't know which files were deleted)
--locales If you only want to merge specific locale(s)

If you want to then push the resulting output, the easiest approach is as follows:

 * Clone Postbox's localisations from GitHub
 * Clone the localisations again locally. This becomes your --postbox
   argument
 * In the original clone, delete all of the localisations. This becomes
   your --output argument
