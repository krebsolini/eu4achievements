# eu4achievements

### Disclaimer

- Won't work with private steam profile
- `--link` flag hardly ever works properly

### Help
```
usage: eu4achievements.py [-h] -u USER
                          [-f {completed,not-completed,very-easy,easy,medium,hard,very-hard,insane,uncategorizedc,nc,ve,e,m,h,vh,i,uc} [{...} ...]]
                          [-r] [-l] [-v] [--no-output]

options:
  -h, --help            show this help message and exit

  -u, --user USER       specify user to list achievements for (the id from the steamcommunity.com profile url)

  -f, --filter {completed,not-completed,very-easy,easy,medium,hard,very-hard,insane,uncategorized,c,nc,ve,e,m,h,vh,i,uc} [{...} ...]
                        filter achievements by specified criteria

  -r, --random          print only one random achievement

  -l, --link            print link to eu4.paradoxwikis.com for each achievement

  -v, --verbose         enable verbose logging

  --no-output           disable output
```

### Example 
```
$ eu4achievements.py -user "krebso" --filter not-completed easy medium hard --random
[H] Great Moravia:
|> Restore the Great Moravian borders as Nitra or Moravia.
```
