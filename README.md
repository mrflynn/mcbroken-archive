# mcbroken-archive
Archive for data from [mcbroken.com](https://mcbroken.com). Downloads and
commits data from the data storage space. Only data that has been changed
recently (within the last 31 minutes) is archived. It runs on the 7th and 37th
minute of every hour.

Heavily inspired by
[simonw/ca-fires-history](https://github.com/simonw/ca-fires-history).

## Import Data Into SQLite
For those who want to perform analysis over the entire corpus of data stored
in this repository (across many or all commits), this repository provides
a script that, when combined with the
[`git-history`](https://github.com/simonw/git-history) tool, can be used to
import everything into a SQLite database. The following command can be used
to import every entry from every commit into a database (this will take a
_very, very long time_, so if you only want to import a subset refer to the
usage info for `git-history`).

```bash
$ uvx --from 'git-history==0.7a0' git-history file \
    --import itertools \
    --import operator \
    --import re \
    --convert "$(cat ./scripts/git-history-transform.py)" \
    mcbroken.db mcbroken.json
```

Once this has finished, a useful query to get all of the relevant data from
each stored entry including fully timestamped updates (not just minute offsets)
can be found below.

```sql
select
    entries.is_broken,
    entries.is_active,
    entries.dot,
    datetime(
        commits.commit_at, format('-%d minutes', entries.last_checked_minutes)
    ) as last_updated,
    entries.street,
    entries.state,
    entries.country,
    entries.longitude,
    entries.latitude
from main.item entries
inner join main.commits commits on entries._commit = commits.id
;
```
