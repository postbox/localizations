import argparse
import os
import re

def loadini(strings, src, file):
  for match in re.finditer(r'^\s*(\S+?)\s*=.*', src, re.MULTILINE):
    strings[match.group(1)] = match.group()
  src = re.sub(r'^.*\S.*=.*', '', src, 0, re.MULTILINE)
  src = re.sub(r'^\s*#.*', '', src, 0, re.MULTILINE)
  src = re.sub(r'^\s*;.*', '', src, 0, re.MULTILINE) # Not a true ini comment...
  if re.match(r'\S', src):
    raise Exception("Unexpected characters %s in INI file %s" % (src, file))

def mergeini(strings, src):
  return re.sub(r'^\s*(\S+?)\s*=.*', lambda match: strings[match.group(1)], src, 0, re.MULTILINE)

def loaddtd(strings, src, file):
  for match in re.finditer(r'<!ENTITY\s+(\S*)\s+".*?">', src, re.DOTALL):
    strings[match.group(1)] = match.group()
  src = re.sub(r'<!ENTITY\s+(\S*)\s+".*?">', '', src, 0, re.DOTALL)
  src = re.sub(r'<!--.*?-->', '', src, 0, re.DOTALL)
  if re.match(r'\S', src):
    raise Exception("Unexpected characters %s in DTD file %s" % (src, file))

def mergedtd(strings, src):
  return re.sub(r'<!ENTITY\s+(\S*)\s+".*?">', lambda match: strings[match.group(1)], src, 0, re.DOTALL)

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--srcdir", required=True, help="Postbox merge result");
parser.add_argument("-t", "--tb52", required=True, help="Thunderbird 52 localisations");
parser.add_argument("-p", "--postbox", required=True, help="Previous Postbox localisations");
parser.add_argument("-o", "--output", required=True, help="Output directory for new localisations");
parser.add_argument("-l", "--locales", nargs="+", default="de fr it sv-SE ru nl pt-BR es-ES en-GB en-US".split(), help="Locales to merge")
args = parser.parse_args()
tb52 = args.tb52
postbox2 = args.postbox
postbox52 = args.srcdir
output = args.output
locales = args.locales
subdirs="dom editor/ui mail netwerk security/manager toolkit".split()
for dir in subdirs:
  base = os.path.join(postbox52, dir, "locales", "en-US")
  if not os.path.exists(base):
    base = os.path.join(postbox52, "mozilla", dir, "locales", "en-US")
    if not os.path.exists(base):
      raise Exception("Could not locate %s in source tree" % dir)
  for subdir, dummy, files in os.walk(base):
    for file in files:
      file = os.path.join(subdir, file)
      with open(file) as handle:
        src = handle.read()
      relpath = os.path.relpath(file, base)
      for locale in locales:
        if file.endswith((".css", ".txt", ".xml")):
          if os.path.exists(os.path.join(postbox2, locale, dir, relpath)):
            with open(os.path.join(postbox2, locale, dir, relpath)) as handle:
              data = handle.read()
          elif os.path.exists(os.path.join(tb52, locale, dir, relpath)):
            with open(os.path.join(tb52, locale, dir, relpath)) as handle:
              data = handle.read()
          else:
            data = src
        elif file.endswith((".js", ".inc")):
          data = src
        elif file.endswith((".properties", ".ini")):
          strings = {}
          loadini(strings, src, file)
          if os.path.exists(os.path.join(tb52, locale, dir, relpath)):
            with open(os.path.join(tb52, locale, dir, relpath)) as handle:
              loadini(strings, handle.read(), os.path.join(tb52, locale, dir, relpath))
          if os.path.exists(os.path.join(postbox52, locale, dir, relpath)):
            with open(os.path.join(postbox52, locale, dir, relpath)) as handle:
              loadini(strings, handle.read(), os.path.join(postbox52, locale, dir, relpath))
          data = mergeini(strings, src)
        elif file.endswith(".dtd"):
          strings = {}
          loaddtd(strings, src, file)
          if os.path.exists(os.path.join(tb52, locale, dir, relpath)):
            with open(os.path.join(tb52, locale, dir, relpath)) as handle:
              loaddtd(strings, handle.read(), os.path.join(tb52, locale, dir, relpath))
          if os.path.exists(os.path.join(postbox52, locale, dir, relpath)):
            with open(os.path.join(postbox52, locale, dir, relpath)) as handle:
              loaddtd(strings, handle.read(), os.path.join(postbox52, locale, dir, relpath))
          data = mergedtd(strings, src)
        else:
          raise Exception("Unmergable file type: %s" % os.path.join(dir, file))
        dest = os.path.join(output, locale, dir, relpath)
        if not os.path.exists(os.path.dirname(dest)):
          os.makedirs(os.path.dirname(dest))
        with open(dest, 'w') as handle:
          handle.write(data)
